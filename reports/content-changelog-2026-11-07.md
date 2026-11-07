# DropThePickle content answers · November 7, 2026

Local branch `cursor/ai-content-answers-4c4f`. Base is `origin/main` at merge `3d1790b4e64ef97679985575fcab693196ab9b50` (PR 1, SEO head `37a716c`). This commit is not pushed, not merged, and not deployed. No Wrangler command was run. The unpushed preview draft (`wrangler.jsonc` empty `previews` block and `scripts/check_preview_config.mjs`) remains only in the other worktree on `cursor/seo-onpage-fixes-4c4f`.

URL inventory: `reports/content-changes-2026-11-07.csv` (309 HTML URLs).

These notes follow a Google AI Overview sample and a spelling inventory. They are not a ranking or citation guarantee.

## What changed

### Publisher spelling

Source wordmark was `DROPTHEPICKLE` inside `<b>`, and the logo font was Anton, which has no lowercase, so the rendered name was all capitals. The wordmark source is now `DropThePickle` (`DropThe` + `Pickle`), and `.logo b` uses Inter at 800 weight with `text-transform: none`, so the rendered header and footer show that spelling. The same change is on the three link-in-bio pages, whose wordmark had used Anton.

`og:image:alt` was `Drop the Pickle` on every standard page. It is `DropThePickle`. Link pages also get that alt and a `twitter:title` equal to their existing title, which already said DropThePickle.

Fifteen pages used `raw_title` and therefore had no publisher token in `<title>`, `og:title`, or `twitter:title`. Each of those three fields now ends with ` · DropThePickle`. The coupon wording in front is unchanged. Examples:

- Before: `Bodhi Pickleball Discount Codes: 15% Off (Nov 2026)`
- After: `Bodhi Pickleball Discount Codes: 15% Off (Nov 2026) · DropThePickle`
- Before: `Pickleball Worlds 2026 Schedule and How to Watch (TV, CT)`
- After: that title plus ` · DropThePickle`

The Worlds body was not edited. The suffix, the shared wordmark, and the shared image alt are the only Worlds differences.

Two Buzz summaries said "DTP" for the publisher. They now say DropThePickle. The coupon string `DROPTHEPICKLE` was not changed in config, go-links, or on-page code boxes.

### Homepage

The strip under the H1 now says: "DropThePickle tracks pickleball paddle prices, discount codes and pro events. Compare maker-sourced specs and dated price checks, then follow the original tournament and review sources. We do not claim to have playtested the paddles." The deal count and price-check date stay. The AvantLink confirm script on the homepage was not removed.

### Short event pages

Twelve PPA-feed event pages (every `events/*.html` except Worlds, Nations Cup, and USA Pickleball Nationals) replace the one-line date/place sentence with a table of dates, location, official page, and ticket link, using only fields already in `data/tournaments.json`. Missing fields say "Not in the feed record" or "No official page link" / "No ticket link". A second heading states that entry fees, the division list, and the registration deadline are not in the feed and are not invented. Example: https://dropthepickle.com/events/proton-daytona-beach-open

https://dropthepickle.com/tournaments now says the cards are the pro feed and amateur signups are only the directories below, and that fees are not added when the feed does not list them.

### Under $100

https://dropthepickle.com/best-paddles-under-100 keeps the five qualifying paddles first and the eight $100–$150 alternatives second, with the same two ItemLists. Each group now has a side-by-side table: paddle, latest maker price, price-checked date, weight, core, and shape, captioned "Side-by-side maker specs. Not a playtest." The intro says the database is a short major-brand list, the order is the checked price, and a code may change the checkout total.

### Paddle pages

All 43 detail pages: the spec table heading is "Maker-listed specs". The old "Pros & cons (from the specs)" heading is "Notes from those specs", with the line "These notes describe the published spec fields. DropThePickle has not playtested this paddle." The weight parser and the under-$100 price split were not reversed. https://dropthepickle.com/paddle-volair-v-1f-xl-w-16mm still shows the published 8 oz and does not claim a playtest.

## Checks

`python3 build.py` built 309 pages. `python3 scripts/check_seo.py` exited 0 (`seo checks passed`), including the earlier SEO assertions and the new ones for the wordmark, image alt, Worlds and Bodhi titles, the under-$100 table, the V.1F not-playtested line, the feed-event unknowns, the homepage sentence, the AvantLink script, and the unchanged `DROPTHEPICKLE` coupon on the Volair code page.

No Wrangler command. No push. No deploy. No merge.

## Follow-up after c3113a3

`c3113a3` is unchanged. This section is the next local commit.

### 16 titles versus 15

The spelling audit's title rows marked `brand_omitted_not_error` are 15 pages. Those are the ones named in the first commit. The 16th title page is https://dropthepickle.com/discount-codes/volair . Its title was `Volair Promo Code: 10% Off with DROPTHEPICKLE (2026)`. A case-insensitive search treats the coupon `DROPTHEPICKLE` as the publisher name, so that page was left off the audit's omitted-brand list. The publisher token `DropThePickle` is not in that coupon. The title rule is case-sensitive (`DropThePickle` must occur as that string), so the first commit already appended ` · DropThePickle` and left the coupon as `DROPTHEPICKLE`. Checked title, Open Graph title, and Twitter title:

`Volair Promo Code: 10% Off with DROPTHEPICKLE (2026) · DropThePickle`

That is one exact publisher suffix. No second suffix was added in this follow-up. Every other HTML title in the 309-page build also contains the exact string `DropThePickle`.

### Comparison pages

`/compare` did not meet the side-by-side requirement in `c3113a3`. It was a list of links and had no spec table. It now has the heading "Maker specs side by side" and one table of every paddle in the database: latest maker price, price-checked date, weight, core, shape, and maker spec page. The intro says that table is maker facts and that notes on a head-to-head page are a reading of those fields, not a playtest.

The 14 best-of hubs other than `/best-paddles-under-100` also had no table in `c3113a3` (cards only). Each now uses the same maker-facts table. `/best-paddles-under-100` keeps its two groups and now includes the maker-page column in those tables.

70 generated head-to-head pages gained two fact rows, "Price checked" and "Maker spec page". The sentence above the table says highlighted cells are the lower maker price or more listed core thicknesses, and that this is not a playtest. https://dropthepickle.com/vs-volair-mach-2-forza-vs-volair-pro-1 already stated the volair.com source links, the specs-read date, the prices-checked date, and "not a playtest". That page's body was not rewritten; only the shared title suffix from `c3113a3` applies.

### Event registration

Feed event tables now have a Registration row: "Not a separate field in this feed record." The ticket row stays labeled Tickets. The unknowns paragraph says a ticket link is only a ticket link. Fees, divisions, and the registration deadline remain unknown because they are not in the feed.

## Checks

`python3 build.py` built 309 pages. `python3 scripts/check_seo.py` exited 0 after this follow-up, including the compare table, the power best-of table, the Selkirk head-to-head price date and maker page, the Volair Mach 2 vs Pro 1 source dates, the Volair coupon-plus-exact-suffix title, and the registration wording.

No Wrangler command. No push. No deploy. No merge.

## Not verified here

- Live production after the `3d1790b` merge. That check is running separately.
- A preview URL. The empty `previews` block is not in this commit.
- Entry fees, division lists, and registration deadlines for feed events. They are absent from the feed record used to build the pages.
- Whether a search engine will cite the new sentences. The source sample was observational.
