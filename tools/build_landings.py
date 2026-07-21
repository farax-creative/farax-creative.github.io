import html as H, pathlib
from products import PRODUCTS, validate

SHELL = pathlib.Path(__file__).resolve().parent / "landing_shell.html"

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
    return "".join(
        f'<details class="rounded-lg border border-line bg-panel p-5"><summary class="cursor-pointer '
        f'font-medium text-neutral-200">{H.escape(f["q"])}</summary>'
        f'<p class="mt-3 text-sm">{H.escape(f["a"])}</p></details>'
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

def _stores(p):
    out = []
    for s in p["stores"]:
        cls = "bg-accent text-ink font-semibold" if s["primary"] else "border border-line"
        out.append(f'<a href="{s["url"]}" class="rounded-full px-6 py-3 {cls}">{H.escape(s["name"])}</a>')
    if p["status"] == "coming_soon":
        out.append('<span class="rounded-full border border-line px-6 py-3 text-neutral-600" '
                   'aria-disabled="true">Coming soon</span>')
    return "".join(out)

def _badge(p):
    return "Live" if p["status"] == "live" else "Coming soon"

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
    repl = {
        "name": p["name"], "slug": p["slug"], "tagline": p["tagline"],
        "blender_min": p["blender_min"], "price_label": p["price_label"],
        "status_badge": _badge(p), "hero_headline": p["hero"]["headline"],
        "hero_sub": p["hero"]["sub"], "hero_image": p["hero"]["image"],
        "manual_url": p["manual_url"],
        "flagship_class": "flagship" if p["flagship"] else "",
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
