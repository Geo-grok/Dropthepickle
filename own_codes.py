"""DropThePickle's own affiliate discount codes (config.json OWN_CODES).

These are codes a brand issued to DropThePickle itself (approved affiliate programs that pay only when the code is
used). They live in config.json, not data/discount-codes.json, because scripts/refresh-codes rewrites that file from
creator source pages every day and would drop a code no third-party page publishes.

Templates call own_code(C, brand) and callout(...) so every surface (deals, paddle pages, codes pages, quiz) shows the
same code, wording and disclosure.
"""
import datetime

def own_codes(C):
    """Active own codes keyed by brand. An entry is active unless "active" is false or "ends" (YYYY-MM-DD) has passed."""
    today = datetime.date.today().isoformat()
    out = {}
    for oc in C.get("OWN_CODES") or []:
        if not (oc.get("brand") and oc.get("code") and oc.get("discount")): continue
        if oc.get("active") is False or (oc.get("ends") and oc["ends"] < today): continue
        out[oc["brand"]] = oc
    return out

def own_code(C, brand): return own_codes(C).get(brand)

def earn_line(oc):
    """FTC disclosure for an own code. Must stay accurate: we earn only when the code is used."""
    pay = oc.get("commission") or "a commission"
    return (f'This is DropThePickle\'s own {oc["brand"]} code. We earn {pay} when you use it, at no extra cost to you '
            f'(the {oc["discount"]} discount is yours either way).')

# Minimal copy-to-clipboard handler for pages that don't already have one (deals, paddle pages). Guarded so it binds once.
COPY_JS = ("<script>if(!window.__dtpOwnCopy){window.__dtpOwnCopy=1;document.addEventListener('click',ev=>{const b=ev.target.closest('.owncode [data-code]');"
           "if(!b)return;const c=b.dataset.code,k=b.parentNode.querySelector('.ccopy'),done=()=>{if(k){k.textContent='Copied!';k.classList.add('ok');"
           "setTimeout(()=>{k.textContent='Copy';k.classList.remove('ok')},1800)}};if(navigator.clipboard)navigator.clipboard.writeText(c).then(done,done);else done()})}</script>")

CSS = (".owncode{background:#f4ffd6;border:3px solid var(--navy);border-left:10px solid var(--neon);border-radius:16px;padding:14px 16px;margin:12px 0;display:flex;flex-direction:column;gap:.5rem;color:var(--navy)}"
       ".owncode .owntag{display:inline-block;align-self:flex-start;background:var(--navy);color:var(--neon);font-weight:900;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;padding:3px 10px;border-radius:999px;margin:0}"
       ".owncode .ownhead{font-size:1.25rem;font-weight:800;margin:0;line-height:1.25}.owncode .cshop{font-weight:800;color:var(--navy)}"
       ".owncode .ownhow{font-size:1.05rem;margin:0}.owncode .owndet{align-self:stretch;text-align:center;min-height:48px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;line-height:1.25;padding:.7rem 1rem}.owncode .ccode{white-space:nowrap;font-size:clamp(1rem,5.2vw,1.5rem);padding-left:.6rem;padding-right:.6rem}.owncode .ownnote{font-size:1.05rem;margin:0;background:#fff3c4;border-radius:10px;padding:8px 10px}"
       ".owncode .owndisc{font-size:.92rem;color:#3d4a63;margin:0}.owncode .owndisc a{color:inherit}")

def callout(e, oc, disclosure_href="disclosure.html", shop=True, js=False, note="", details=False):
    """details=True adds a big link to oc["page"] (the brand's promo-code page), if set."""
    """oc["how"] (optional): checkout instructions, shown as their own line. note (optional): per-product warning HTML-escaped."""
    cd = e(oc["code"])
    head = f'Use code <b>{cd}</b> for {e(oc["discount"])} at {e(oc["brand"])}'
    cond = f' <span class="meta">({e(oc["conditions"])})</span>' if oc.get("conditions") and not oc.get("how") else ""
    how = f'<p class="ownhow">{e(oc["how"])}</p>' if oc.get("how") else ""
    det = (f'<a class="btn owndet" href="{e(oc["page"])}">{e(oc["brand"])} promo code details: how to use it →</a>' if details and oc.get("page") else "")
    warn = f'<p class="ownnote"><b>Heads up:</b> {e(note)}</p>' if note else ""
    shop_a = (f'<a class="cshop" href="{e(oc["shop_url"])}" target="_blank" rel="sponsored nofollow noopener">Shop {e(oc["brand"])} with code {cd} →</a>'
              if shop and oc.get("shop_url") else "")
    return (f'<div class="owncode" data-owncode="{cd}"><p class="owntag">★ Our own code</p><p class="ownhead">{head}{cond}</p>'
            f'<div class="crow"><button class="ccode" data-code="{cd}" aria-label="Copy code {cd}">{cd}</button><button class="btn ccopy" data-code="{cd}">Copy</button></div>'
            f'{how}{warn}{det}{shop_a}<p class="owndisc"><b>Disclosure:</b> {e(earn_line(oc))} <a href="{e(disclosure_href)}">Details</a>.</p></div>'
            + (COPY_JS if js else ""))
