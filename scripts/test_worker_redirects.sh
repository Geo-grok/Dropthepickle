#!/usr/bin/env bash
# Local test of the Worker's URL handling against the built dist/ (run python3 build.py first).
# Starts `wrangler dev --local`, checks status + Location for each case, then stops it. Exit 1 on any mismatch.
set -uo pipefail
cd "$(dirname "$0")/.."
PORT=${PORT:-8799}; B="http://127.0.0.1:$PORT"
npx --yes wrangler dev --local --port "$PORT" --ip 127.0.0.1 >/tmp/dtp-wrangler-dev.log 2>&1 &
PID=$!; trap 'kill $PID 2>/dev/null' EXIT
for i in $(seq 1 60); do curl -s -o /dev/null "$B/robots.txt" && break; sleep 1; done
fail=0
t() { # path expected_status expected_location(or -) [host]
  local h=${4:-}; local out
  if [ -n "$h" ]; then out=$(curl -s -o /dev/null -H "Host: $h" -w '%{http_code} %{redirect_url}' "$B$1"); else out=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$B$1"); fi
  local want="$2 $([ "$3" = - ] && echo "" || echo "$3")"
  if [ "${out% }" = "${want% }" ]; then echo "ok   $1 -> $out"; else echo "FAIL $1 -> '$out' (want '$want')"; fail=1; fi
}
t /buzz.html 301 "$B/buzz"
t "/buzz.html?utm_source=x&b=2" 301 "$B/buzz?utm_source=x&b=2"
t /buzz/ 301 "$B/buzz"
t /buzz 200 -
t /index.html 301 "$B/"
t / 200 -
t /guides/ 301 "$B/guides"
t /discount-codes.html 301 "$B/discount-codes"
t /discount-codes/volair.html 301 "$B/discount-codes/volair"
t /discount-codes/volair/ 301 "$B/discount-codes/volair"
t /discount-codes/Volair 301 "$B/discount-codes/volair"
t /discount-codes/Volair.html 301 "$B/discount-codes/volair"
t "/discount-codes/Volair.html?x=1" 301 "$B/discount-codes/volair?x=1"
t /discount-codes/Volair/ 301 "$B/discount-codes/volair"
t /buzz/ 301 "https://dropthepickle.com/buzz" www.dropthepickle.com
t /vs-selkirk-omni-vs-selkirk-slk-era-power.html 301 "$B/vs-selkirk-omni-vs-selkirk-slk-era-power"
t /events/ppa-worlds-2026.html 301 "$B/events/opendoor-pickleball-world-championships"
t /best-paddles-under-100 301 "$B/guides/best-paddles-under-100"
t /best-paddles-under-100.html 301 "$B/guides/best-paddles-under-100"
t /best-paddles-under-100/ 301 "$B/guides/best-paddles-under-100"
t "/best-paddles-under-100.html?utm=1" 301 "$B/guides/best-paddles-under-100?utm=1"
t /best-paddles-under-100.html 301 "https://dropthepickle.com/guides/best-paddles-under-100" www.dropthepickle.com
t /guides/best-paddles-under-100 200 -
t /nonexistent.html 404 -
t /nonexistent/ 404 -
t /nonexistent 404 -
t /buzz/2001-01-01-no-such-story 301 "$B/buzz"
t /events/mojo-energy-pouches-virginia-beach-open 301 "$B/articles/virginia-beach-open-2026-first-time-champions"
t /events/mojo-energy-pouches-virginia-beach-open.html 301 "$B/articles/virginia-beach-open-2026-first-time-champions"
t /events/mojo-energy-pouches-virginia-beach-open/ 301 "$B/articles/virginia-beach-open-2026-first-time-champions"
t "/events/mojo-energy-pouches-virginia-beach-open?utm=1" 301 "$B/articles/virginia-beach-open-2026-first-time-champions?utm=1"
t /events/mojo-energy-pouches-virginia-beach-open 301 "https://dropthepickle.com/articles/virginia-beach-open-2026-first-time-champions" www.dropthepickle.com
t /vs-selkirk-labs-project-boomstik-vs-six-zero-coral-16mm 301 "$B/paddle-selkirk-labs-project-boomstik"
t /vs-selkirk-labs-project-boomstik-vs-six-zero-coral-16mm.html 301 "$B/paddle-selkirk-labs-project-boomstik"
t /vs-gearbox-gbx-power-elongated-gen-3-vs-six-zero-coral-16mm 301 "$B/paddle-gearbox-gbx-power-elongated-gen-3"
t /vs-joola-hyperion-pro-v-vs-six-zero-coral-16mm 301 "$B/paddle-joola-hyperion-pro-v"
t /vs-gearbox-gbx-power-elongated-gen-3-vs-joola-hyperion-pro-v 301 "$B/paddle-gearbox-gbx-power-elongated-gen-3"
t /vs-gearbox-gbx-power-elongated-gen-3-vs-joola-hyperion-pro-v.html 301 "$B/paddle-gearbox-gbx-power-elongated-gen-3"
t /articles/virginia-beach-open-2026-first-time-champions 200 -
t /paddle-selkirk-labs-project-boomstik 200 -
t /sitemap.xml 200 -
t /sitemap-guides.xml 200 -
t /sitemap-codes.xml 200 -
t /sitemap-buzz.xml 200 -
t /sitemap-paddles.xml 200 -
t /sitemap-vs.xml 200 -
t /sitemap-pages.xml 200 -
t /robots.txt 200 -
t /llms.txt 200 -
t /style.css 200 -
t /media/physics-topspin.jpg 200 -
t /buzz.html 301 "https://dropthepickle.com/buzz" www.dropthepickle.com
FIRST=$(ls dist/buzz | head -1); t "/buzz/${FIRST%.html}" 200 -
t "/buzz/$FIRST" 301 "$B/buzz/${FIRST%.html}"
exit $fail
