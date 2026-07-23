import html as H, pathlib
from products import PRODUCTS, validate

SHELL = pathlib.Path(__file__).resolve().parent / "landing_shell.html"

# Cloudflare Web Analytics beacon token (a public, client-side value — not a secret).
# Empty string = emit NO tag, so an unconfigured build never ships a broken placeholder.
# From dash.cloudflare.com -> Web Analytics for farax-creative.github.io.
CF_ANALYTICS_TOKEN = "f8b03668620647fba75afc03db7c58fd"

def _analytics():
    if not CF_ANALYTICS_TOKEN:
        return ""
    # Matches the snippet Cloudflare issues (type="module").
    return ('<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
            f'data-cf-beacon=\'{{"token": "{CF_ANALYTICS_TOKEN}"}}\'></script>')

def _features(p):
    # Framed-demo panels (approved 2026-07-21): a dark-matted screen with soft shadow, then an
    # accent eyebrow, title, and one-line sub. Styled by the .feat-* CSS baked into the shell.
    return "".join(
        f'<div class="feat-card"><div class="feat-screen">'
        f'<img src="{x["clip"]}" alt="{H.escape(x["title"])}" loading="lazy" /></div>'
        f'<div class="feat-eyebrow">{H.escape(x["eyebrow"])}</div>'
        f'<h3 class="feat-title">{H.escape(x["title"])}</h3>'
        f'<p class="feat-sub">{H.escape(x["sub"])}</p></div>'
        for x in p["features"])

def _faq(p):
    # The question is escaped; the answer is authored HTML (it may carry an inline link such as
    # the report form), so it is emitted as-is. Keep FAQ answers free of raw '<'/'&' literals.
    return "".join(
        f'<details class="rounded-lg border border-line bg-panel p-5"><summary class="cursor-pointer '
        f'font-medium text-neutral-200">{H.escape(f["q"])}</summary>'
        f'<p class="mt-3 text-sm">{f["a"]}</p></details>'
        for f in p["faq"])

def _why(p):
    # mirrors zap-board.html:135-155 — titled blurbs, no image.
    return "".join(
        f'<div><h3 class="font-semibold text-lg">{H.escape(x["title"])}</h3>'
        f'<p class="mt-2 text-sm text-neutral-400 leading-relaxed">{H.escape(x["blurb"])}</p></div>'
        for x in p["why"])

def _compat(p):
    # mirrors zap-board.html:187-202 — four accent-labelled cards.
    return "".join(f'<div class="rounded-lg border border-line bg-ink p-5">'
                   f'<div class="text-accent font-semibold">{H.escape(k)}</div>'
                   f'<p class="mt-2 text-neutral-400">{H.escape(v)}</p></div>' for k, v in p["compat"])

def _utm_source(p):
    # zap-board -> zapboard. The landing is a measured conversion source, so its store links and
    # its footer link back to the map carry UTM (unlike the in-site DATA links, which stay clean).
    return p["slug"].replace("-", "")

def _landing_utm(p):
    src = _utm_source(p)
    return f"?utm_source={src}&utm_medium=landing&utm_campaign={src}-launch"

def _stores(p):
    utm = _landing_utm(p)
    out = []
    for s in p["stores"]:
        cls = "bg-accent text-ink font-semibold" if s["primary"] else "border border-line"
        out.append(f'<a href="{s["url"]}{utm}" class="rounded-full px-6 py-3 {cls}">{H.escape(s["name"])}</a>')
    if p["status"] == "coming_soon":
        out.append('<span class="rounded-full border border-line px-6 py-3 text-neutral-600" '
                   'aria-disabled="true">Coming soon</span>')
    return "".join(out)

_NUM = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
        7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}

def _what_sub(p):
    # "Nine things it does..." for the 9-panel board, "Four things..." for Doctor. Derived from
    # the feature count so the subhead can never disagree with the number of panels shown.
    n = len(p["features"])
    return f"{_NUM.get(n, str(n))} things it does, each shown in a few seconds."

def _cta_label(p):
    # A free product invites a download; a paid one just says "Get it" (price lives on the store).
    return "Download free" if p["price_label"] == "Free" else "Get it"

def _feat_grid_class(p):
    # 4 near-square beats read best as a 2x2; 9 stay on the default 3-wide grid. Leading space so
    # the board (empty) keeps class="feat-grid" byte-for-byte.
    return " cols-2" if len(p["features"]) == 4 else ""

def _badge(p):
    # A live product's own landing does not need a "Live" tag (it's implied); only a not-yet
    # released product shows a status pill.
    if p["status"] == "live":
        return ""
    return ('<div class="inline-flex items-center gap-2 rounded-full border border-line bg-panel '
            'px-3 py-1 text-xs text-neutral-400 mb-6"><span class="text-neutral-500">○</span> '
            'Coming soon</div>')

def build_landing(slug, out_path=None):
    # Plan 1 proves the engine against a scratch file and MUST NOT write live zap-*.html.
    # Refuse to default to the live path — a caller who wants a live page must say so
    # explicitly (Plan 2 will pass out_path deliberately). This closes the one failure
    # mode the plan is built around: an ad-hoc build_landing("board") clobbering the page.
    if out_path is None:
        raise ValueError(
            f"build_landing({slug!r}) needs an explicit out_path; refusing to overwrite "
            f"the live zap-{PRODUCTS[slug]['slug']}.html by default.")
    validate(slug)
    p = PRODUCTS[slug]
    s = SHELL.read_text(encoding="utf-8")
    # Price is optional. When price_label is "", emit nothing (and no dangling separator);
    # the store buttons carry the price. When set (e.g. "Free"), keep the "Free · " / "Free." form.
    pl = p["price_label"]
    repl = {
        "name": p["name"], "slug": p["slug"], "tagline": p["tagline"],
        "blender_min": p["blender_min"],
        "price_badge": f"{pl} · " if pl else "", "price_line": f"{pl}. " if pl else "",
        "status_badge": _badge(p), "hero_headline": p["hero"]["headline"],
        "hero_sub": p["hero"]["sub"], "hero_image": p["hero"]["image"],
        "manual_url": p["manual_url"],
        "flagship_class": "flagship" if p["flagship"] else "",
        "cta_label": _cta_label(p), "what_sub": _what_sub(p),
        "feat_grid_class": _feat_grid_class(p),
        "utm_source": _utm_source(p),
        "analytics": _analytics(),
        "features": _features(p), "why": _why(p),
        "compat_rows": _compat(p), "faq": _faq(p), "store_buttons": _stores(p),
    }
    for k, v in repl.items():
        s = s.replace("{{" + k + "}}", v)
    out = pathlib.Path(out_path)
    out.write_text(s, encoding="utf-8", newline="")
    return out.read_text(encoding="utf-8")

if __name__ == "__main__":
    # Plan 1 writes only to scratch files — never the live zap-*.html. Plan 2 flips this
    # to the live path once the CSS-inline step is generalized and parity (Task 6) has passed.
    here = pathlib.Path(__file__).resolve().parent
    for slug in [s for s in PRODUCTS if PRODUCTS[s]]:
        build_landing(slug, out_path=str(here / f"_scratch-{slug}.html")); print("built", slug)
