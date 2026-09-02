# The coming_soon path had never been exercised: every product in the registry is live, so
# nothing built a page for a product with no store listing and no manual yet. Farax Motion
# will be the first, and a probe found it emitted three Manual links to a page that does not
# exist -- the report/index.html __FORM_URL__ failure again, where the page renders but the
# link 404s. These tests pin the behaviour before that product is added.
import pathlib
import copy

import products
from build_landings import build_landing

SCRATCH = pathlib.Path(__file__).resolve().parent / "_scratch-coming-soon.html"

# A minimal not-yet-released product. Deliberately not a real one: the registry must be able
# to describe a product whose name and slug are still undecided.
UNRELEASED = {
    "name": "Unreleased Product", "slug": "unreleased-product",
    "tagline": "Not out yet", "blender_min": "4.5",
    "price_label": "", "status": "coming_soon", "flagship": True,
    "hero": {"headline": "Headline", "sub": "Sub", "image": "assets/img/x/hero.png"},
    "preview": {"source": "assets/img/x/p.webp", "seconds": 2.0},
    "features": [{"clip": "a.webp", "eyebrow": "E", "title": "T", "sub": "S"}] * 4,
    "why": [{"title": "T", "blurb": "B"}],
    "compat": [["Needs an NVIDIA GPU", "The model runs on CUDA."]],
    "faq": [{"q": "Q", "a": "A"}],
    "stores": [],
    "manual_url": "",
}

def _register(**overrides):
    products.PRODUCTS["_test_unreleased"] = {**copy.deepcopy(UNRELEASED), **overrides}
    return products.PRODUCTS["_test_unreleased"]

def _build(**overrides):
    _register(**overrides)
    try:
        return build_landing("_test_unreleased", out_path=str(SCRATCH))
    finally:
        products.PRODUCTS.pop("_test_unreleased", None)

def test_no_manual_means_no_manual_link():
    html = _build()
    assert "{{" not in html, "unfilled slot remains"
    assert ">Manual<" not in html, "nav/footer link to a manual that does not exist"
    assert "user manual" not in html, "compat block links a manual that does not exist"
    # The licence still has to be stated; only the manual sentence goes.
    assert "GPL-3.0-or-later." in html

def test_manual_link_comes_back_when_the_manual_exists():
    html = _build(manual_url="https://farax-creative.github.io/docs/unreleased-product.html")
    assert html.count("docs/unreleased-product.html") == 3   # nav, compat block, footer
    assert "user manual" in html
    assert "(English, 한국어, 日本語, Português, Español)." in html

def test_series_is_not_hardcoded_to_zap():
    # The footer credit read "Zap series" for every product. Not every product is one.
    html = _build(series="Farax Creative")
    assert "FARAX CREATIVE · Farax Creative · Unreleased Product" in html
    assert "Zap series" not in html

def test_zap_products_keep_the_series_credit_by_default():
    # Omitting "series" must leave the existing pages exactly as they were.
    html = _build()
    assert "FARAX CREATIVE · Zap series · Unreleased Product" in html

def test_coming_soon_shows_no_buy_button():
    html = _build()
    assert "Coming soon" in html
    assert "gumroad.com" not in html and "superhivemarket.com" not in html

def test_a_live_product_may_not_omit_its_manual():
    # Only a not-yet-released product is allowed to have no manual. A live one without one
    # is a mistake, not a state.
    _register(status="live", stores=[{"name": "Gumroad", "url": "https://x", "primary": True}])
    try:
        products.validate("_test_unreleased")
    except AssertionError as e:
        assert "only coming_soon may ship without a manual" in str(e)
    else:
        raise AssertionError("a live product with no manual_url should be rejected")
    finally:
        products.PRODUCTS.pop("_test_unreleased", None)

if __name__ == "__main__":
    test_no_manual_means_no_manual_link()
    test_manual_link_comes_back_when_the_manual_exists()
    test_series_is_not_hardcoded_to_zap()
    test_zap_products_keep_the_series_credit_by_default()
    test_coming_soon_shows_no_buy_button()
    test_a_live_product_may_not_omit_its_manual()
    print("ok")
