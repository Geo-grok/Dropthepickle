#!/usr/bin/env node
// Unit check for the five Phase 0 retired-URL 301s. Does not start wrangler.
// Mirrors src/worker.js retiredRedirect / cleanPath / RETIRED_301, and asserts
// the Worker source actually wires that map in.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const data = JSON.parse(readFileSync(join(root, "src/page-redirects.json"), "utf8"));
const RETIRED_301 = data.redirects;
const worker = readFileSync(join(root, "src/worker.js"), "utf8");

const EXPECTED = {
  "/events/mojo-energy-pouches-virginia-beach-open": "/articles/virginia-beach-open-2026-first-time-champions",
  "/vs-selkirk-labs-project-boomstik-vs-six-zero-coral-16mm": "/paddle-selkirk-labs-project-boomstik",
  "/vs-gearbox-gbx-power-elongated-gen-3-vs-six-zero-coral-16mm": "/paddle-gearbox-gbx-power-elongated-gen-3",
  "/vs-joola-hyperion-pro-v-vs-six-zero-coral-16mm": "/paddle-joola-hyperion-pro-v",
  "/vs-gearbox-gbx-power-elongated-gen-3-vs-joola-hyperion-pro-v": "/paddle-gearbox-gbx-power-elongated-gen-3",
};

function cleanPath(path) {
  let p = path;
  if (p.endsWith("/index.html")) p = p.slice(0, -"index.html".length);
  else if (p.endsWith(".html")) p = p.slice(0, -".html".length);
  if (p.length > 1 && p.endsWith("/")) p = p.slice(0, -1);
  return p || "/";
}

function retiredRedirect(href) {
  const url = new URL(href);
  if (url.pathname.startsWith("/go/")) return null;
  const dest = RETIRED_301[cleanPath(url.pathname)];
  if (!dest) return null;
  if (url.hostname.startsWith("www.")) {
    url.hostname = url.hostname.slice(4);
    url.protocol = "https:";
  }
  url.pathname = dest;
  return { status: 301, location: url.toString() };
}

const bad = [];
function fail(msg) { bad.push(msg); console.log("FAIL " + msg); }
function ok(msg) { console.log("ok   " + msg); }

if (JSON.stringify(RETIRED_301) !== JSON.stringify(EXPECTED)) {
  fail("src/page-redirects.json redirects do not match the five retired URLs");
}
if (!worker.includes('import PAGE_REDIRECTS from "./page-redirects.json"')) {
  fail("worker.js does not import src/page-redirects.json");
}
if (!worker.includes("RETIRED_301[cleanPath(url.pathname)]")) {
  fail("worker.js does not look up retired 301s with cleanPath");
}
if (!/if\s*\(\s*url\.pathname\.startsWith\("\/go\/"\)\s*\)/.test(worker)) {
  fail("worker.js no longer handles /go/ before page 301s");
}
// /go/ must stay ahead of the retired lookup in source order.
const goAt = worker.indexOf('url.pathname.startsWith("/go/")');
const retiredAt = worker.indexOf("RETIRED_301[cleanPath(url.pathname)]");
if (goAt < 0 || retiredAt < 0 || goAt > retiredAt) {
  fail("retired 301s must not run before /go/ handling");
}
for (const path of Object.keys(RETIRED_301)) {
  if (path.startsWith("/go/")) fail(`redirect map must not include /go/ path ${path}`);
}

const origin = "https://dropthepickle.com";
for (const [from, to] of Object.entries(EXPECTED)) {
  const cases = [
    [`${origin}${from}`, `${origin}${to}`],
    [`${origin}${from}.html`, `${origin}${to}`],
    [`${origin}${from}/`, `${origin}${to}`],
    [`${origin}${from}.html?utm=1`, `${origin}${to}?utm=1`],
    [`https://www.dropthepickle.com${from}`, `${origin}${to}`],
    [`https://www.dropthepickle.com${from}.html?x=1`, `${origin}${to}?x=1`],
  ];
  for (const [href, want] of cases) {
    const got = retiredRedirect(href);
    if (!got || got.status !== 301 || got.location !== want) {
      fail(`${href} -> ${JSON.stringify(got)} (want 301 ${want})`);
    } else {
      ok(`${href} -> 301 ${got.location}`);
    }
  }
}

const skipped = [
  `${origin}/go/udrippin-home`,
  `${origin}/buzz`,
  `${origin}/vs-selkirk-omni-vs-selkirk-slk-era-power`,
  `${origin}/paddle-selkirk-labs-project-boomstik`,
];
for (const href of skipped) {
  const got = retiredRedirect(href);
  if (got !== null) fail(`${href} should not be a retired 301, got ${JSON.stringify(got)}`);
  else ok(`${href} not rewritten`);
}

if (bad.length) {
  console.log(`${bad.length} problems`);
  process.exit(1);
}
console.log("retired redirect checks passed");
