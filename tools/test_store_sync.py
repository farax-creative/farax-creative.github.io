# Guard against drift: store links in products.py must match those in index.html
import re, pathlib
from products import PRODUCTS

INDEX = pathlib.Path(__file__).resolve().parent.parent / "index.html"

# Every product the registry can build a landing for. Driven off PRODUCTS rather than a
# hand-written list: this test only covered "board" for its first three products, so the
# doctor and viewer store links went unguarded the whole time. A new product is now covered
# the moment it is added -- nobody has to remember to extend this file.
BUILDABLE = [slug for slug in PRODUCTS if PRODUCTS[slug]]

def store_urls_in_index(slug):
    html = INDEX.read_text(encoding="utf-8")
    # the DATA block lists ["Gumroad","https://...",...] / ["Superhive","https://...",...]
    return set(re.findall(r'"https://[^"]*' + re.escape(slug.replace("zap-","")) + r'[^"]*"', html))

def _assert_links_match(slug):
    p = PRODUCTS[slug]
    data_urls = {s["url"] for s in p["stores"]}
    if not data_urls:
        # A coming_soon product with no listing yet has nothing to keep in step, and must
        # not be required to appear in index.html's DATA before it is on sale.
        return
    index_urls = {u.strip('"').split("?")[0] for u in store_urls_in_index(p["slug"])}
    # every products.py store URL must appear in index.html (base path, ignoring UTM)
    for u in data_urls:
        assert u in index_urls, f"{slug} store {u} missing from index.html DATA"

def test_board_store_links_match():
    _assert_links_match("board")

def test_every_buildable_product_store_links_match():
    assert BUILDABLE, "no buildable products -- the registry is empty or all None"
    for slug in BUILDABLE:
        _assert_links_match(slug)

def test_a_listed_product_is_actually_listed():
    # The check above is one-directional by design (index.html carries products this
    # registry does not, e.g. Zap Output, whose landing is inline). What it must never do
    # is pass because it found nothing to compare: a live product with stores has to have
    # at least one of them reachable from index.html.
    for slug in BUILDABLE:
        p = PRODUCTS[slug]
        if p["status"] == "live" and p["stores"]:
            assert store_urls_in_index(p["slug"]), f"{slug} is live with stores but absent from index.html"

if __name__ == "__main__":
    test_board_store_links_match()
    test_every_buildable_product_store_links_match()
    test_a_listed_product_is_actually_listed()
    print("ok")
