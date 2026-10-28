"""Extensionless public URLs for dropthepickle.com.

Files stay .html in dist/ (Cloudflare assets serve them), but every canonical, og:url, sitemap <loc>, JSON-LD url,
llms.txt entry and internal href uses the extensionless form Cloudflare serves: foo.html -> /foo, dir/index.html -> /dir/,
index.html -> /. Always https, never www. /go/ links are left alone.
"""
import re

def clean_path(path):
    if path == "index.html" or path.endswith("/index.html"): return path[:-len("index.html")]
    return path[:-5] if path.endswith(".html") else path

def base_url(base):
    return base.rstrip("/").replace("http://", "https://").replace("://www.", "://")

def canon(base, fn):
    return f"{base_url(base)}/{clean_path(fn)}"

_HREF = re.compile(r'''(\bhref=["'])((?:https?://(?:www\.)?dropthepickle\.com)?[^"'#?:]*?)((?:index)?\.html)([#?][^"']*)?(["'])''')

def clean_hrefs(base, doc):
    """Rewrite internal .html hrefs to extensionless URLs. External links and /go/ links are left alone."""
    def r(m):
        pre, path, suf, tail, q = m.groups()
        if "/go/" in path: return m.group(0)
        if path.startswith(("http://", "https://")):
            out = canon(base, re.sub(r"^https?://(?:www\.)?dropthepickle\.com/", "", path + suf))
        elif suf == "index.html" and path and not path.endswith("/"):
            out = path + "index"  # e.g. price-index.html -> price-index (not a directory index)
        elif suf == "index.html":
            out = path or "./"
        else:
            out = path
        return f"{pre}{out}{tail or ''}{q}"
    return _HREF.sub(r, doc)
