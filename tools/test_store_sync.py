# Guard against drift: store links in products.py must match those in index.html
import re, pathlib
from products import PRODUCTS

INDEX = pathlib.Path(__file__).resolve().parent.parent / "index.html"

def store_urls_in_index(slug):
    html = INDEX.read_text(encoding="utf-8")
    # the DATA block lists ["Gumroad","https://...",...] / ["Superhive","https://...",...]
    return set(re.findall(r'"https://[^"]*' + re.escape(slug.replace("zap-","")) + r'[^"]*"', html))

def test_board_store_links_match():
    data_urls = {s["url"] for s in PRODUCTS["board"]["stores"]}
    index_urls = {u.strip('"').split("?")[0] for u in store_urls_in_index("zap-board")}
    # every products.py store URL must appear in index.html (base path, ignoring UTM)
    for u in data_urls:
        assert u in index_urls, f"board store {u} missing from index.html DATA"

if __name__ == "__main__":
    test_board_store_links_match()
    print("ok")
