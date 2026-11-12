"""Read a sitemap urlset, or a sitemap index plus its children, and return page URLs."""
from pathlib import Path
from xml.etree import ElementTree as ET

SM_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
BASE = "https://dropthepickle.com"
# Child files the build writes. Checks require all of these to be present.
EXPECTED_CHILDREN = (
    "sitemap-guides.xml",
    "sitemap-codes.xml",
    "sitemap-buzz.xml",
    "sitemap-paddles.xml",
    "sitemap-vs.xml",
    "sitemap-pages.xml",
)

def local_tag(tag):
    return tag.split("}", 1)[-1] if isinstance(tag, str) and tag.startswith("{") else tag

def loc_texts(root, parent):
    return [(el.text or "").strip() for el in root.findall(f"sm:{parent}/sm:loc", SM_NS) if (el.text or "").strip()]

def page_locs_from_tree(root, resolve_child):
    """Return (page_locs, child_locs). resolve_child(loc) -> child urlset root."""
    kind = local_tag(root.tag)
    if kind == "sitemapindex":
        pages, children = [], []
        for loc in loc_texts(root, "sitemap"):
            children.append(loc)
            child_root = resolve_child(loc)
            if local_tag(child_root.tag) != "urlset":
                raise ValueError(f"child sitemap is not a urlset: {loc}")
            pages.extend(loc_texts(child_root, "url"))
        return pages, children
    if kind == "urlset":
        return loc_texts(root, "url"), []
    raise ValueError(f"unexpected sitemap root <{kind}>")

def child_filename(loc, base=BASE):
    prefix = base.rstrip("/") + "/"
    if not loc.startswith(prefix):
        raise ValueError(f"sitemap child off-host: {loc}")
    name = loc[len(prefix):]
    if "/" in name or not name.startswith("sitemap-") or not name.endswith(".xml"):
        raise ValueError(f"unexpected child sitemap loc: {loc}")
    return name

def page_locs_from_dist(dist, base=BASE):
    """Parse dist/sitemap.xml (index) and each child file. Raises ValueError on a bad index."""
    dist = Path(dist)
    root = ET.parse(dist / "sitemap.xml").getroot()
    def resolve(loc):
        name = child_filename(loc, base)
        path = dist / name
        if not path.is_file():
            raise ValueError(f"missing child sitemap: {name}")
        return ET.parse(path).getroot()
    return page_locs_from_tree(root, resolve)

def page_locs_from_xml_text(xml, resolve_child):
    return page_locs_from_tree(ET.fromstring(xml), resolve_child)
