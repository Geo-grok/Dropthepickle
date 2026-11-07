# DropThePickle on-page SEO changelog

Date of this work: November 7, 2026.

This file is the review log for branch `cursor/seo-onpage-fixes-4c4f`. Nothing here is a merge or a publish. `wrangler.jsonc`, DNS, hosting settings, and the worker were not edited. A Cloudflare Workers Builds check does run against this branch; see "Deployment check" below. Local `python3 build.py` / `scripts/check_seo.py` are not CI.

Structured data below was parsed as JSON-LD and checked against the visible copy. Parsing is not a promise that Google will show a rich result.

## Follow-up on this same branch

A second pass the same day checked the club, the ticket page, and whether semifinal winners were final. This section is the shipped state where it conflicts with an earlier paragraph.

**Address.** The club's contact page, https://www.invitedclubs.com/clubs/brookhaven-country-club/contact-us/ (page title "Contact Us | Brookhaven Country Club"), read November 7, 2026, prints Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, TX 75234, phone 972-243-6151. United Pickleball's Nations Cup page, read the same day, prints 3334 Golfing Green Drive. Worlds, the Nations Cup page, both FAQs, and both Place schemas now use 3333 Golfing Green Dr and say that United Pickleball prints 3334.

**Tickets.** https://worlds.unitedpickleball.com/tickets , read November 7, 2026, still prints the same summary ranges and says they are Tixr data from October 11, 2026, fees included, and that prices vary. The table header is "October 11, 2026 Tixr figure." The intro says "Not a live checkout price." The SportsEvent AggregateOffer was removed so those figures are not a current offer in schema.

**Semifinal winners.** The PPA event page and United Pickleball's pro page, read November 7, 2026, showed a live semifinal board ("Live · auto-updating" on the PPA page). Neither presented a final winner list. No score was added. The page records that the November 7 reading had no final winner list.

**Build date.** The weekend heading follows the America/Chicago build date (`DTP_BUILD_DATE` overrides it). November 7: "Built November 7, 2026: semifinals, then Championship Sunday." November 8: "Built November 8, 2026: Championship Sunday." After November 8: "PPA Worlds weekend: the published schedule." A script moves that lead forward if the page is opened on a later day. The court board stays under "Court board snapshot, read November 7, 2026." The homepage card and the how-to-watch lead use the same split. `scripts/check_seo.py` was run after builds dated November 7, November 8, and November 9, then the tree was rebuilt for November 7.

**Event end.** Worlds `endDate` is `2026-11-08` with no clock. The description says the 4:00 p.m. CT PickleballTV window is a broadcast end, not an event-end time. Nations Cup `endDate` is `2026-11-01` with no clock. The old `15:30` matched the 3:30 p.m. coverage window, not a last ball.

**About meta description.** "DropThePickle, from Midland, Texas, copies paddle specs from maker pages, dates each maker price check, and pulls news and events from public feeds. Corrections: geolobo@mail.grokbot.com." The visible section leads with that sourcing. It does not invent a byline. There is no Person schema.

## Site-wide pass (same branch)

Inventory of the November 7 build: 309 HTML files, 306 sitemap URLs. Families covered: home, guides, three hand-written event guides plus PPA-feed event stubs, 43 paddle pages, the quiz, `vs-` pages, `best-` filters, per-brand discount-code pages, newsroom articles, creators, podcasts, deals, price index, price tracker, and root hubs. No missing H1. No unparseable JSON-LD. Noindex only on `/links/tiktok` and `/links/instagram`, both canonical to `/links`. The only shared title is those three link pages, on purpose. The one Person node is Ryan Morneau, named on his creator page.

Changes:

- Guides breadcrumb "Guides" now points at `/guides` instead of `/guides/how-to-choose-a-paddle`. Every `guides/*.html` page.
- `deals/*.html` gets a Deals crumb to `/deals` unless the page already passes crumbs. Black Friday already did.
- Product offers include availability only when `price_history.json` records true or false. Tempest Veyra and Bantam Jolt no longer claim InStock. Honeyfoam TKO-X stays OutOfStock. The other 40 recorded-available paddles stay InStock, including lists that embed those offers.
- https://dropthepickle.com/compare H1 is "Compare pickleball paddles". ItemList name is "All paddles".
- https://dropthepickle.com/tournaments title and H1 are "Upcoming pro pickleball tournaments".
- https://dropthepickle.com/pros title and H1 are "Pro pickleball players".
- https://dropthepickle.com/paddles title and H1 are "Pickleball paddle database".
- https://dropthepickle.com/reviews title and H1 are "Pickleball paddle review videos".
- https://dropthepickle.com/deals H1 is "Pickleball paddle deals". The title already said that.
- Each PPA-feed event page, other than the hand-written Worlds page, says it is copied from the official feed and to confirm on the official page. No new facts.

Left on purpose: robots, canonicals, sitemap membership, shop and community (short coming-soon pages, still indexable; noindex would be a coverage decision), the under-$100 filter and guide as two different pages, long unique titles, affiliate disclosures, prices, and `/go/` links. Not added: SearchAction, a named editor, ratings, or title shortening for pixel width. Search analytics are not in the repo, so titles that already match a query were not retuned.

## What was verified before editing

Public baseline (same day) plus a fresh read of the repo and of these sources on November 7, 2026:

- Volair product page https://volair.com/products/v-1f-xl-w-paddle lists **Average Weight: 8oz**. The site file already stored `8 oz`. The contradiction was the ounce parser, which only accepted decimals like `7.8` and then wrote "the maker doesn't publish a weight."
- United Pickleball pro page https://worlds.unitedpickleball.com/ppa-tour marks Monday Nov 2 through Friday Nov 6 completed, Saturday Nov 7 as semifinals, and Sunday Nov 8 as Championship Sunday. Its court board at that reading showed Championship Court first up at 11:00 AM CT and court SC1 first up at 8:45 AM CT, both semifinals. Broadcast windows still listed were PickleballTV 11 AM–7 PM CT (semifinals) and 10 AM–4 PM CT (Sunday).
- PPA event page https://www.ppatour.com/events/2026/pickleball-world-championships/ still lists Monday qualifying first serve at 11:00 AM, Saturday first serve at 11:00 AM, and Sunday first serve at 10:00 AM, and still says pro first serve is 11:00 AM Monday through Saturday. That disagreement is kept in the copy and in the event description.
- Maker prices in `data/price_history.json` (`updated` 2026-11-07). Five USD paddles are at or under $100. Eight more are over $100 and at or under $150. The filter page was sorting the whole mix A–Z, so the first cards were over $100.

Not changed, on purpose: robots rules (already allow `/`, disallow `/go/`, and point at the sitemap), canonical host and extensionless paths (already correct), the worker redirect from `/events/ppa-worlds-2026` (already 301), and any fact that was not re-read.

## Shared template effects

### 1. Paddle detail H1 includes the brand

`paddle_pages.py` hero. The document title already was `Brand Model · DropThePickle`. The H1 was the model only. It is now `Brand Model`. Titles were not rewritten. The visible "Updated" date on these pages follows the spec/price fingerprint, which did not change, so sitemap `lastmod` for these URLs did not move.

All 43 detail URLs:

- https://dropthepickle.com/paddle-crbn-crbn1-trufoam-barrage
- https://dropthepickle.com/paddle-crbn-crbn1-trufoam-genesis
- https://dropthepickle.com/paddle-crbn-crbn1-x-series
- https://dropthepickle.com/paddle-crbn-crbn3-trufoam-waves
- https://dropthepickle.com/paddle-engage-axiom-elongated-durable-grit
- https://dropthepickle.com/paddle-engage-pursuit-pro2-elongated-16mm
- https://dropthepickle.com/paddle-engage-x2-elongated
- https://dropthepickle.com/paddle-gearbox-gbx-power-elongated-gen-3
- https://dropthepickle.com/paddle-gearbox-gx2-power-hybrid
- https://dropthepickle.com/paddle-gearbox-pressure-x-8e
- https://dropthepickle.com/paddle-joola-hyperion-pro-v
- https://dropthepickle.com/paddle-joola-kosmos-pro-v
- https://dropthepickle.com/paddle-joola-perseus-3s-dual-16mm
- https://dropthepickle.com/paddle-joola-perseus-pro-v
- https://dropthepickle.com/paddle-joola-radius-pro-v
- https://dropthepickle.com/paddle-joola-scorpeus-pro-v
- https://dropthepickle.com/paddle-luzz-cannon-xpp-m1
- https://dropthepickle.com/paddle-luzz-glider-2026-hybrid
- https://dropthepickle.com/paddle-paddletek-bantam-jolt
- https://dropthepickle.com/paddle-paddletek-bantam-tko-c
- https://dropthepickle.com/paddle-paddletek-honeyfoam-tko-x
- https://dropthepickle.com/paddle-paddletek-tempest-veyra
- https://dropthepickle.com/paddle-paddletek-tempest-wave-pro-c
- https://dropthepickle.com/paddle-selkirk-labs-project-boomstik
- https://dropthepickle.com/paddle-selkirk-luxx-control-air-infinigrit
- https://dropthepickle.com/paddle-selkirk-omni
- https://dropthepickle.com/paddle-selkirk-slk-era-power
- https://dropthepickle.com/paddle-selkirk-slk-halo-power
- https://dropthepickle.com/paddle-six-zero-black-opal-14mm
- https://dropthepickle.com/paddle-six-zero-coral-16mm
- https://dropthepickle.com/paddle-six-zero-double-black-diamond-control
- https://dropthepickle.com/paddle-six-zero-ruby
- https://dropthepickle.com/paddle-volair-cmd-el-16mm
- https://dropthepickle.com/paddle-volair-cmd-hyb-16mm-dylan-frazier
- https://dropthepickle.com/paddle-volair-cmd-wb-16mm
- https://dropthepickle.com/paddle-volair-ctrl-1-forza
- https://dropthepickle.com/paddle-volair-ctrl-2-forza
- https://dropthepickle.com/paddle-volair-mach-1-forza
- https://dropthepickle.com/paddle-volair-mach-2
- https://dropthepickle.com/paddle-volair-mach-2-forza
- https://dropthepickle.com/paddle-volair-pro-1
- https://dropthepickle.com/paddle-volair-pro-2
- https://dropthepickle.com/paddle-volair-v-1f-xl-w-16mm

The same corrected cons text for the V.1F also appears on the one comparison that includes it: https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-v-1f-xl-w-16mm

### 2. Own-code disclosure no longer says the discount is "yours either way"

`own_codes.earn_line`. Before: "We earn {commission} when you use it, at no extra cost to you (the {discount} discount is yours either way)." After: "We earn {commission} when you use it, at no extra cost to you. The {discount} discount applies only if checkout accepts the code." For Blinded Wear, whose stored discount is "a checkout discount," the second sentence is "A checkout discount applies only if checkout accepts the code."

Affiliate disclosure stays. The V.1F callout still says Volair does not tag that paddle as included, so the code may not apply.

Rendered on these 41 URLs. The about page uses the same checkout sentence in its new section. The rest render `earn_line`:

- https://dropthepickle.com/about
- https://dropthepickle.com/deals
- https://dropthepickle.com/deals/black-friday-pickleball-deals-2026
- https://dropthepickle.com/discount-codes
- https://dropthepickle.com/discount-codes/blinded-wear
- https://dropthepickle.com/discount-codes/honolulu
- https://dropthepickle.com/discount-codes/solase
- https://dropthepickle.com/discount-codes/volair
- https://dropthepickle.com/guides/best-paddles-under-100
- https://dropthepickle.com/guides/best-volair-paddles
- https://dropthepickle.com/guides/pickleball-gift-guide-2026
- https://dropthepickle.com/guides/pickleball-grip-size
- https://dropthepickle.com/paddle-quiz
- https://dropthepickle.com/paddle-volair-cmd-el-16mm
- https://dropthepickle.com/paddle-volair-cmd-hyb-16mm-dylan-frazier
- https://dropthepickle.com/paddle-volair-cmd-wb-16mm
- https://dropthepickle.com/paddle-volair-ctrl-1-forza
- https://dropthepickle.com/paddle-volair-ctrl-2-forza
- https://dropthepickle.com/paddle-volair-mach-1-forza
- https://dropthepickle.com/paddle-volair-mach-2
- https://dropthepickle.com/paddle-volair-mach-2-forza
- https://dropthepickle.com/paddle-volair-pro-1
- https://dropthepickle.com/paddle-volair-pro-2
- https://dropthepickle.com/paddle-volair-v-1f-xl-w-16mm
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-cmd-hyb-16mm-dylan-frazier
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-cmd-wb-16mm
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-ctrl-1-forza
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-ctrl-2-forza
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-mach-1-forza
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-mach-2
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-mach-2-forza
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-pro-1
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-pro-2
- https://dropthepickle.com/vs-volair-cmd-el-16mm-vs-volair-v-1f-xl-w-16mm
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-cmd-wb-16mm
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-ctrl-1-forza
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-ctrl-2-forza
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-mach-1-forza
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-mach-2
- https://dropthepickle.com/vs-volair-cmd-hyb-16mm-dylan-frazier-vs-volair-mach-2-forza
- https://dropthepickle.com/vs-volair-mach-2-forza-vs-volair-pro-1

### 3. Best-of meta descriptions no longer say "from paddles.json"

Shared `lst()` description, except the under-$100 page which has its own description below. New text: "{title}: spec filter of paddles in our database, using published maker specs and the latest checked maker price. Not a playtest or a scored ranking."

Visible intros that named `paddles.json` now say "our database." Power and control intros no longer claim "we sort by the latest checked price" while the page also says the list is alphabetical. They are still alphabetical, and they still say so.

URLs:

- https://dropthepickle.com/best-16mm-paddles
- https://dropthepickle.com/best-crbn-paddles
- https://dropthepickle.com/best-elongated-paddles
- https://dropthepickle.com/best-engage-paddles
- https://dropthepickle.com/best-gearbox-paddles
- https://dropthepickle.com/best-joola-paddles
- https://dropthepickle.com/best-luzz-paddles
- https://dropthepickle.com/best-paddles-for-beginners
- https://dropthepickle.com/best-paddles-for-control
- https://dropthepickle.com/best-paddles-for-power
- https://dropthepickle.com/best-paddles-for-tennis-players
- https://dropthepickle.com/best-paddletek-paddles
- https://dropthepickle.com/best-selkirk-paddles
- https://dropthepickle.com/best-six-zero-paddles

Titles and H1s on these pages were left as they were. Order was left alphabetical, which is what the page already disclosed.

### 4. Link-in-bio H1

`links_page.py`. The wordmark stays a logo link. A real H1 was added: "Big Dill's pickleball links." The line under it is now "Discount codes, deals, buzz and the latest video."

- https://dropthepickle.com/links (in the sitemap)
- https://dropthepickle.com/links/tiktok (noindex, canonical to `/links`, not in the sitemap)
- https://dropthepickle.com/links/instagram (same)

## Page-by-page

### https://dropthepickle.com/

- H1 before: `ALL THINGS PICKLEBALL`. After: `Pickleball news, paddle prices and codes`. Title unchanged: `Pickleball news, paddle deals & prices · DropThePickle`.
- Worlds card, shown only Nov 3–8, 2026 CT. Before: "Main draw starts Tue Nov 3 at 11 AM CT" and a link to the how-to-watch guide. After: "Semifinals are Sat Nov 7 (PickleballTV 11 AM–7 PM CT). Championship Sunday is Nov 8 (first serve 10 AM CT, PickleballTV 10 AM–4 PM)." The first button now goes to `/events/opendoor-pickleball-world-championships#this-weekend`. Buzz link unchanged.
- `lastmod` was already 2026-11-07. The freshness hash changed.

### https://dropthepickle.com/best-paddles-under-100

- Title unchanged: `Best paddles under $100 · DropThePickle`.
- Description before: `Best paddles under $100. Spec filter only, from paddles.json. Not a scored ranking.` After: `5 paddles in our database at or under $100 (maker prices checked Nov 07, 2026), listed before $100 to $150 alternatives. Not a playtest ranking.` The date is the `price_history.json` updated date at build time, not a hardcoded day.
- Headings before: one H1, then product H3s, no group H2. After: H2 `At or under $100`, then H2 `Closest picks, $100 to $150`.
- Order before: one alphabetical mix, so the first cards were over $100 (CRBN¹ X Series $149.99, Engage Pursuit Pro2 $129.99, Luzz Glider $119, Paddletek Tempest Wave Pro-C $149.99, and so on). After, lowest price first inside each group:
  - At or under $100: Volair V.1F/ XL-W 16mm $49.99, Volair Mach 2 $69.99, Volair Pro 1 $69.99, Volair Pro 2 $69.99, Selkirk SLK HALO Power $70.00.
  - Then $100 to $150: Luzz Glider 2026 Hybrid $119.00, Volair Mach 1 Forza $119.99, Volair Mach 2 Forza $119.99, Engage Pursuit Pro2 Elongated 16mm $129.99, Volair CTRL 1 Forza $139.99, Volair CTRL 2 Forza $139.99, CRBN¹ X Series $149.99, Paddletek Tempest Wave Pro-C $149.99.
- Schema before: one ItemList of that alphabetical mix, including the over-$100 paddles. After: ItemList `At or under $100` (five products, each offer price ≤ 100) and ItemList `Closest picks, $100 to $150`. Positions restart at 1 in each list.
- The guide at https://dropthepickle.com/guides/best-paddles-under-100 already separated the two groups. Its tables were not reordered. It does pick up the new discount sentence from the shared disclosure.

### https://dropthepickle.com/paddle-volair-v-1f-xl-w-16mm

- H1 before: `V.1F/ XL-W 16mm`. After: `Volair V.1F/ XL-W 16mm`. Title unchanged.
- Specs and Product JSON-LD already said maker-listed weight `8 oz`, core 16mm, shape Widebody. Those stayed. They match Volair's published "Average Weight: 8oz" (re-read November 7, 2026). Price on the maker page at that read was regular $139.99, sale $49.99, which matches the tracked price.
- Cons before: "The maker doesn't publish a weight on its product page." After: the empty-cons fallback already in the template, "No obvious spec drawbacks. Watch the linked reviews for on-court impressions." No new con was invented.
- Code box still warns that Volair doesn't tag this paddle as included. The disclosure no longer says the discount is yours either way. See the shared disclosure above.
- Parser fix (`weights()`): integer ounces count, and a trailing `(16mm)` is not treated as 16 ounces. The weight guide's published range is unchanged: lowest 7.7 oz (Paddletek Bantam TKO-C), highest 8.5 oz (Six Zero Double Black Diamond Control).

### https://dropthepickle.com/events/opendoor-pickleball-world-championships

- Title unchanged: `Pickleball Worlds 2026 Schedule and How to Watch (TV, CT)`.
- Description before: led with Monday qualifying. After: `Pickleball Worlds 2026: semifinals Sat Nov 7 on PickleballTV 11 AM–7 PM CT, Championship Sunday Nov 8 at 10 AM CT. Qualifying was Mon Nov 2 (8 AM CT on record; PPA page still lists 11 AM).`
- New first section, `id="this-weekend"`: what's left on November 7, 2026. Semifinals Saturday, Championship Sunday November 8. United Pickleball's Nov 7 court-board times are quoted as a reading, not as a permanent order of play. The 4 PM Sunday time is labeled as the PickleballTV window.
- Qualifying stays on the page. The 8 AM CT figure remains the earlier United Pickleball / PPA Oct 28 X-post answer. The Nov 7 recheck of the PPA event page still showed 11 AM, and that conflict is repeated in the lead, the qualifying section, the day-by-day note, two FAQs, and the SportsEvent description. It was not deleted.
- SportsEvent `startDate` is `2026-11-02T08:00:00-06:00`. `endDate` is the date `2026-11-08` with no clock. See the follow-up section: the 4:00 p.m. figure is the broadcast window, and the October 11 ticket snapshot is not an AggregateOffer. No semifinal winners were added.
- FAQ "When is the 2026 Pickleball World Championships?" now leads with the Nov 7 status. "When does PPA Worlds qualifying start?" is past tense and keeps both clocks. "What time does Worlds start each day?" keeps the daily pattern and adds the Nov 7 court-board reading.
- `lastmod` 2026-11-02 → 2026-11-07.
- Ticket prices, parking, and prize money were not re-fetched and were not rewritten.

### https://dropthepickle.com/guides/how-to-watch-pro-pickleball

- The Worlds block now answers what is still ahead as of November 7, 2026 (Saturday semifinals, Sunday championship) and marks Monday–Friday as completed. The 8 AM / 11 AM qualifying note stays.
- Nations Cup block retitled to a result: Team USA beat Latin America 3-0. Semifinal winners match the results already published on the Nations Cup page (Latin America def. Asia Domestic 3-1; USA def. Europe East 3-1). Watch windows are described as what was scheduled, not as a live broadcast.
- "This week" intro no longer says the three events overlap as if the Nations Cup were still on. The week table itself was not rewritten.
- FAQ "What time is the MLP Nations Cup final?" is past tense and includes the USA result.
- `lastmod` 2026-11-01 → 2026-11-07.

### https://dropthepickle.com/events/mlp-nations-cup-2026

- Lead is past tense: the event was Oct 30–Nov 1, and Team USA won 3-0. The street address is 3333 Golfing Green Dr, from the club's contact page. The page also says United Pickleball prints 3334. `endDate` is `2026-11-01` with no clock.
- Standings copy no longer says the top two "advance" or that the final "is" Sunday.
- Format paragraph is past tense and points at the result already on the page.
- The Worlds handoff no longer says qualifying "starts" Monday. It points at `#this-weekend` and keeps the 8 AM / 11 AM note with the Nov 7 recheck.
- FAQs "When does Team USA play?" and "Who was in the Nations Cup semifinals?" no longer describe Sunday as upcoming.
- SportsEvent description says USA beat Latin America 3-0. `startDate` stays `2026-10-30T10:00:00-05:00`. `endDate` is `2026-11-01` (the last day, not the 3:30 p.m. coverage cutoff). `eventStatus` stays `EventScheduled` because schema.org has no "completed" status; the end date is in the past.
- `lastmod` 2026-11-01 → 2026-11-07.
- Scores were not newly researched. They were already on this page from the Nov 1 official-results read.

### https://dropthepickle.com/about

- New H2 `How the pages are checked`. States that no person is named as editor or reviewer, what is copied from maker pages, what the price script does, what comes from feeds, and that own-code discounts apply only if checkout accepts them. Corrections still go to geolobo@mail.grokbot.com. No Person/author schema was added.
- Description: `DropThePickle, from Midland, Texas, copies paddle specs from maker pages, dates each maker price check, and pulls news and events from public feeds. Corrections: geolobo@mail.grokbot.com.`
- `lastmod` was unset → 2026-11-07.

### https://dropthepickle.com/guides/pickleball-rules-for-beginners

- One sentence added under the existing rulebook line: no named reviewer; corrections go through the about page. Title, description, at-a-glance answers, and FAQs were not rewritten. No author schema.
- `lastmod` 2026-11-05 → 2026-11-07.

### https://dropthepickle.com/guides/pickleball-rules-cheat-sheet-2026

- Same reviewer sentence. Rules and FAQs unchanged. No author schema.
- `lastmod` was unset → 2026-11-07.

### https://dropthepickle.com/price-index

- Visible line and description no longer say `price_history.json`. They say the prices are the maker prices on record. The numbers, table, and CSV were not changed.
- `lastmod` was already 2026-11-07. The freshness hash changed.

## Crawl files

- `robots.txt` rules were not edited. Built file still allows `/`, disallows `/go/` for every listed agent, and declares `Sitemap: https://dropthepickle.com/sitemap.xml`.
- Sitemap is still one urlset of extensionless `https://dropthepickle.com/...` URLs. 306 URLs, each with a built HTML file. Excluded, as before: `404.html`, and the noindex copies `/links/tiktok` and `/links/instagram`. No `.html` URLs in the sitemap.
- `lastmod` moved to 2026-11-07 for pages whose freshness hash changed and whose previous date was older. Pages already stamped 2026-11-07 (including the homepage, the under-$100 filter, the price index, and the paddle quiz) kept that date. Detail-page `lastmod` values were not bumped just because the H1 gained the brand.
- Canonicals were already self-referencing and extensionless. They were not churned.
- Internal links in the built HTML, including `/go/` slugs against `src/go-links.json`, resolved. Live checks on November 7, 2026, without changing the host: an unknown path returns 404; `/about.html` returns 307 to `/about`; `/events/ppa-worlds-2026` returns 301 to the current Worlds URL.

## Files

- `paddle_pages.py` — weight parser, H1, under-$100 groups and schema, best-of descriptions, homepage H1, price-index wording
- `own_codes.py` — discount disclosure
- `worlds_card.py` — homepage weekend card
- `content_pages.py` — Worlds, how-to-watch, Nations Cup, rules reviewer line
- `build.py` — about section and description
- `links_page.py` — H1
- `data/page_dates.json` — freshness hashes and the `lastmod` dates above
- `scripts/check_seo.py` — new rendered-HTML check
- `reports/seo-changelog-2026-11-07.md` — this file

Not modified: `wrangler.jsonc`, `src/worker.js`, `config.json` prices or codes, `data/paddles.json`, `data/price_history.json`.

## Commands and results

```
python3 -m py_compile paddle_pages.py own_codes.py worlds_card.py build.py content_pages.py
python3 build.py
python3 scripts/check_seo.py
```

- `py_compile`: exit 0
- `build.py`: exit 0, `built 309 pages`
- `scripts/check_seo.py`: exit 0, `checked 309 HTML pages, 306 sitemap URLs`, `seo checks passed`

The check requires one title, one meta description, one H1, a `https://dropthepickle.com` canonical without `.html`, parseable JSON-LD, sitemap URLs that exist as built pages, and internal links that resolve. It also asserts the under-$100 ItemList prices, the V.1F weight wording, the Worlds start and date-only end, no ticket AggregateOffer, the club address 3333, the dated court-board snapshot, the build-date weekend heading, the about sourcing description, and that no page still says "yours either way" or puts `paddles.json` in a meta description.

The same check was run three times on November 7, 2026, each after `python3 build.py`:

- default build date (November 7, America/Chicago): exit 0
- `DTP_BUILD_DATE=2026-11-08`: exit 0
- `DTP_BUILD_DATE=2026-11-09`: exit 0, and the homepage event card was hidden

The committed pages are the November 7 build. Each run printed `checked 309 HTML pages, 306 sitemap URLs` and `seo checks passed`.

There is no project lint config and no unit-test suite. `python3 scripts/check_links.py` also calls every external URL; that full external crawl was not run. Internal links and `/go/` slugs were checked locally instead.

`pip install -r requirements.txt` was needed in this environment so BeautifulSoup was available for the check. That install is not a site change.

## Facts not established from a public official page

- Semifinal and championship match winners. On November 7, 2026 the PPA event page and United Pickleball's pro page showed a live board, not a final results list. Nothing on those pages named a semifinal winner. Scores were left off for that reason.
- A clock time for the last ball of Worlds or of the Nations Cup final. The published materials give the last calendar day and a broadcast window (Worlds PickleballTV until 4:00 p.m. CT Sunday; Nations Cup coverage until 3:30 p.m. CT). Schema uses the date only.
- A live Tixr cart price on November 7. The official ticket page itself still attributes its numbers to Tixr on October 11, 2026. The table repeats that snapshot and says so.
- A personal editor name. The site does not publish one, and none was added.

## Deployment check (not an SEO failure)

GitHub check "Workers Builds: dropthepickle" on commit `518a6878fe892c04849614fd9e1ff658bf8fb552` concluded failure. Check run: https://github.com/Geo-grok/Dropthepickle/runs/128471874373 . The GitHub output has no log text and no annotations. It only links to Cloudflare build `5fb8436a-cf26-46ba-b635-6cf31fdd4d84`: https://dash.cloudflare.com/f12f2564c774e2aff0eaf7aa86947e6e/workers/services/view/dropthepickle/production/builds/5fb8436a-cf26-46ba-b635-6cf31fdd4d84

A read-only look at that build, reported back for this pass: the build command was `pip install -r requirements.txt && python3 update.py --no-fetch`, it reported 309 pages, and the build command succeeded. The deploy command `npx wrangler preview` (Wrangler 4.158.0) failed because `wrangler.jsonc` has no `previews` block. The same failure happened on the earlier build `783ec64f-2334-49f1-b658-773f959efcd2` at commit `45094313`. `wrangler.jsonc` is the same on this branch and on the base: a D1 binding, no `previews`. Dashboard build settings, as reported, have `auto_build_enabled=true`, `previews_enabled=false`, and the production settings for this SEO branch call `npx wrangler preview`.

That is a deployment-configuration mismatch, not an SEO regression and not a failure of the static build. `wrangler.jsonc` was not edited. No deploy, preview, or check rerun was started from here. A preview-safe separate D1 binding or a validation-only workflow would need approval before anyone changes that configuration.

Risk left as-is: Workers Builds is on for this repo, so a push can start that production-targeted preview command even though the config cannot satisfy it. The failed command is `wrangler preview`, and this pass does not establish whether a later successful preview would publish. Production was still on the old pages at about 11:36 AM CT on November 7, 2026, after both failed checks.
