// Serves dist/ through env.ASSETS, stores email signups in D1 (binding DB),
// and handles /go/<slug> outbound redirects (counted in D1 table go_clicks,
// with user_agent and an is_bot flag; HEAD requests are redirected but not logged).
import GO from "./go-links.json";
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/signup" && request.method === "POST") {
      return handleSignup(request, env);
    }
    if (url.pathname.startsWith("/go/")) {
      return handleGo(request, env, ctx, url);
    }
    if (url.pathname.startsWith("/media/")) {
      return handleMedia(request, env);
    }
    // /discount-codes/Volair etc.: brand pages are lowercase slugs, so send case variants to the real page instead of a 404.
    if (url.pathname.startsWith("/discount-codes/") && url.pathname !== url.pathname.toLowerCase()) {
      url.pathname = url.pathname.toLowerCase();
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};

// Public video files copied from media/ into dist/media by build.py. Served from static assets
// (content-type video/mp4, no redirect). If the asset layer answers a Range request with a full 200,
// slice it here so players can seek. Files stay under the 25 MiB asset limit, so buffering is fine.
async function handleMedia(request, env) {
  const res = await env.ASSETS.fetch(request);
  const range = request.headers.get("range");
  if (res.status !== 200 || !range || !["GET", "HEAD"].includes(request.method)) {
    if (res.status !== 200 || res.headers.has("accept-ranges")) return res;
    const out = new Response(res.body, res);
    out.headers.set("accept-ranges", "bytes");
    return out;
  }
  const buf = await res.arrayBuffer();
  const size = buf.byteLength;
  const m = /^bytes=(\d*)-(\d*)$/.exec(range.trim());
  let start, end;
  if (m && (m[1] || m[2])) {
    if (m[1]) { start = Number(m[1]); end = m[2] ? Math.min(Number(m[2]), size - 1) : size - 1; }
    else { start = Math.max(size - Number(m[2]), 0); end = size - 1; }
  }
  const headers = new Headers(res.headers);
  headers.set("accept-ranges", "bytes");
  if (start === undefined || start >= size || start > end) {
    headers.set("content-range", `bytes */${size}`);
    headers.delete("content-length");
    return new Response(null, { status: 416, headers });
  }
  headers.set("content-range", `bytes ${start}-${end}/${size}`);
  headers.set("content-length", String(end - start + 1));
  const body = request.method === "HEAD" ? null : buf.slice(start, end + 1);
  return new Response(body, { status: 206, headers });
}

function wantsJson(request) {
  const accept = request.headers.get("accept") || "";
  if (accept.includes("application/json")) return true;
  // fetch() sends Sec-Fetch-Dest: empty. A normal form navigation sends document.
  return (request.headers.get("sec-fetch-dest") || "") === "empty";
}

function reply(request, ok, message, status) {
  if (wantsJson(request)) {
    return Response.json(
      { ok, message },
      { status, headers: { "cache-control": "no-store" } }
    );
  }
  const title = ok ? "You're on the list" : "Signup";
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${escapeHtml(title)} — DropThePickle</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0b1426;color:#fff;font:16px/1.5 Inter,system-ui,sans-serif}main{max-width:32rem;margin:1.5rem;padding:1.6rem 1.4rem;background:#111d36;border-radius:18px}h1{font-family:Oswald,Impact,sans-serif;text-transform:uppercase;letter-spacing:.02em;margin:0 0 .6rem}a{color:#c6f432}</style></head>
<body><main><h1>${escapeHtml(title)}</h1><p>${escapeHtml(message)}</p><p><a href="/">Back to DropThePickle</a></p></main></body></html>`;
  return new Response(html, {
    status,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" },
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function validEmail(raw) {
  if (typeof raw !== "string") return "";
  const email = raw.trim().toLowerCase();
  if (email.length < 3 || email.length > 254) return "";
  if (!/^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$/.test(email)) return "";
  return email;
}

function cleanSource(raw) {
  const source = String(raw || "").trim().slice(0, 64);
  return source.replace(/[\u0000-\u001f\u007f]/g, "") || null;
}

function countryFrom(request) {
  const country = request.cf && request.cf.country;
  if (typeof country !== "string") return null;
  const code = country.trim().slice(0, 8);
  return code || null;
}

async function readFields(request) {
  const type = request.headers.get("content-type") || "";
  if (type.includes("application/json")) {
    const body = await request.json();
    return body && typeof body === "object" ? body : {};
  }
  const form = await request.formData();
  return {
    email: form.get("email"),
    source: form.get("source"),
    website: form.get("website"),
  };
}

async function handleSignup(request, env) {
  let fields;
  try {
    fields = await readFields(request);
  } catch {
    return reply(request, false, "That signup didn't come through. Please try again.", 400);
  }

  // Honeypot: humans never see this field. Pretend it worked and store nothing.
  if (String(fields.website || "").trim()) {
    return reply(request, true, "Thanks! You're on the list.", 200);
  }

  const email = validEmail(fields.email);
  if (!email) {
    return reply(request, false, "Please enter a valid email address.", 400);
  }

  const source = cleanSource(fields.source);
  const createdAt = new Date().toISOString();
  const country = countryFrom(request);

  try {
    // id is INTEGER PRIMARY KEY AUTOINCREMENT on subscribers. email is UNIQUE.
    await env.DB.prepare(
      "INSERT INTO subscribers (email, source, country, created_at) VALUES (?, ?, ?, ?) ON CONFLICT(email) DO NOTHING"
    ).bind(email, source, country, createdAt).run();
  } catch {
    return reply(request, false, "We couldn't save that just now. Please try again.", 500);
  }

  return reply(request, true, "Thanks! You're on the list.", 200);
}

// Builds the destination from src/go-links.json, appending affiliate_tag (a query string) when set.
// Network deep links (AvantLink, Awin, ShareASale) can't be a query string on the brand URL, so an affiliate_tag
// that is a full https:// URL containing {url} is used as a template, e.g.
// "https://www.awin1.com/cread.php?awinmid=124160&awinaffid=<ID>&ued={url}" -> {url} = encoded destination.
// Templates may only point at AFF_HOSTS (keep in sync with AFF_HOSTS in build.py); anything else falls back to
// the plain destination, so a bad or tampered go-links.json entry can't turn /go/ into a redirect to an arbitrary host.
export const AFF_HOSTS = ["awin1.com", "avantlink.com", "shareasale.com"];
const AFF_QS = /^[A-Za-z0-9_.~%+=&-]{1,200}$/;
function hostOk(host, list) {
  host = String(host || "").toLowerCase();
  return list.some((d) => host === d || host.endsWith("." + d));
}
function httpUrl(raw) {
  try {
    const u = new URL(raw);
    return u.protocol === "https:" || u.protocol === "http:" ? u : null;
  } catch { return null; }
}
export function goTarget(slug) {
  const entry = GO.links && Object.prototype.hasOwnProperty.call(GO.links, slug) ? GO.links[slug] : null;
  if (!entry || !/^https?:\/\//.test(entry.url) || !httpUrl(entry.url)) return null;
  const raw = String(entry.affiliate_tag || "").trim();
  if (/^https:\/\//i.test(raw)) {
    // Deep-link template: exactly one {url}, https, known affiliate network host.
    if (raw.split("{url}").length !== 2) return entry.url;
    const t = httpUrl(raw.replace("{url}", "x"));
    if (!t || t.protocol !== "https:" || !hostOk(t.hostname, AFF_HOSTS)) return entry.url;
    return raw.replace("{url}", encodeURIComponent(entry.url));
  }
  const tag = raw.replace(/^[?&]/, "");
  if (!tag || !AFF_QS.test(tag)) return entry.url;
  return entry.url + (entry.url.includes("?") ? "&" : "?") + tag;
}

// Likely non-human user agents: crawlers, link checkers, unfurl/preview fetchers, scripts, headless browsers.
// In-app browsers (Facebook FBAN, Instagram, LinkedInApp, Pinterest app) are real people and are NOT matched.
const BOT_UA = /bot\b|bot[\/;\-_ ]|crawl|spider|slurp|scrap|curl|wget|python|requests|aiohttp|httpx|go-http-client|okhttp|java\/|libwww|perl|ruby|php|node-fetch|axios|undici|got \(|postman|insomnia|headless|phantom|puppeteer|playwright|selenium|lighthouse|pagespeed|gtmetrix|pingdom|uptime|monitor|statuscake|preview|facebookexternalhit|facebookcatalog|meta-externalagent|facebot|slack-imgproxy|slackbot|twitterbot|discordbot|whatsapp|telegrambot|skypeuripreview|linkedinbot|pinterestbot|redditbot|embedly|quora link|vkshare|w3c_validator|validator|link ?check|linkcheck|checklink|xenu|screaming frog|ahrefs|semrush|mj12|dotbot|bingpreview|google-inspectiontool|feedfetcher|feed|rss|archive|wayback|httrack|scanner|nmap|masscan|zgrab|nikto|http-client|httpclient|fetch\b|^mozilla\/5\.0$/i;
// A real browser UA starts with Mozilla/5.0 (...) and names a rendering engine.
const BROWSER_UA = /^Mozilla\/5\.0 \(.+\) (AppleWebKit|Gecko|Chrome|Firefox|Safari)\b/i;

// Returns 1 for likely bots, 0 for likely browser clicks. HEAD requests are handled (not logged) by the caller.
export function isBot(request) {
  if (request.method === "HEAD") return 1;
  const ua = (request.headers.get("user-agent") || "").trim();
  if (!ua) return 1;
  if (BOT_UA.test(ua)) return 1;
  if (!request.headers.get("referer") && !BROWSER_UA.test(ua)) return 1;
  return 0;
}

async function handleGo(request, env, ctx, url) {
  let slug = "";
  try { slug = decodeURIComponent(url.pathname.slice(4)).replace(/\/+$/, "").toLowerCase(); } catch {}
  const target = /^[a-z0-9-]{1,80}$/.test(slug) ? goTarget(slug) : null;
  if (!target) return Response.redirect(new URL("/deals", url).toString(), 302);
  // HEAD (link checkers, unfurlers) still gets the redirect but is never logged.
  // Flagged GETs are logged with is_bot = 1 so nothing is lost; count real clicks with is_bot = 0.
  if (env.DB && request.method !== "HEAD") {
    let ref = null;
    try { ref = new URL(request.headers.get("referer") || "").pathname.slice(0, 200); } catch {}
    const ua = (request.headers.get("user-agent") || "").slice(0, 512) || null;
    const write = env.DB.prepare(
      "INSERT INTO go_clicks (slug, referer_path, country, created_at, user_agent, is_bot) VALUES (?, ?, ?, ?, ?, ?)"
    ).bind(slug, ref, countryFrom(request), new Date().toISOString(), ua, isBot(request)).run().catch(() => {});
    if (ctx && ctx.waitUntil) ctx.waitUntil(write); else await write;
  }
  return new Response(null, {
    status: 302,
    headers: { location: target, "cache-control": "no-store", "x-robots-tag": "noindex", "referrer-policy": "strict-origin-when-cross-origin" },
  });
}
