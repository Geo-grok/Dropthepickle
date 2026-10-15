// Serves dist/ through env.ASSETS and stores email signups in D1 (binding DB).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/signup" && request.method === "POST") {
      return handleSignup(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

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
    await env.DB.prepare(
      "INSERT INTO subscribers (email, source, created_at, country) VALUES (?, ?, ?, ?) ON CONFLICT(email) DO NOTHING"
    ).bind(email, source, createdAt, country).run();
  } catch {
    return reply(request, false, "We couldn't save that just now. Please try again.", 500);
  }

  return reply(request, true, "Thanks! You're on the list.", 200);
}
