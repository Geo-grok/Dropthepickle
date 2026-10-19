// Serves dist/ through env.ASSETS, stores email signups in D1 (binding DB),
// and handles /go/<slug> outbound redirects (counted in D1 table go_clicks).
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
export function goTarget(slug) {
  const entry = GO.links && Object.prototype.hasOwnProperty.call(GO.links, slug) ? GO.links[slug] : null;
  if (!entry || !/^https?:\/\//.test(entry.url)) return null;
  const tag = String(entry.affiliate_tag || "").replace(/^[?&]/, "");
  if (!tag) return entry.url;
  return entry.url + (entry.url.includes("?") ? "&" : "?") + tag;
}

async function handleGo(request, env, ctx, url) {
  const slug = decodeURIComponent(url.pathname.slice(4)).replace(/\/+$/, "").toLowerCase();
  const target = /^[a-z0-9-]{1,80}$/.test(slug) ? goTarget(slug) : null;
  if (!target) return Response.redirect(new URL("/deals", url).toString(), 302);
  if (env.DB) {
    let ref = null;
    try { ref = new URL(request.headers.get("referer") || "").pathname.slice(0, 200); } catch {}
    const write = env.DB.prepare(
      "INSERT INTO go_clicks (slug, referer_path, country, created_at) VALUES (?, ?, ?, ?)"
    ).bind(slug, ref, countryFrom(request), new Date().toISOString()).run().catch(() => {});
    if (ctx && ctx.waitUntil) ctx.waitUntil(write); else await write;
  }
  return new Response(null, {
    status: 302,
    headers: { location: target, "cache-control": "no-store", "x-robots-tag": "noindex", "referrer-policy": "strict-origin-when-cross-origin" },
  });
}
