import html as H, pathlib
from products import PRODUCTS, validate

LIVE = pathlib.Path(__file__).resolve().parent.parent
SHELL = pathlib.Path(__file__).resolve().parent / "landing_shell.html"

def _pillars(p):
    # mirrors zap-board.html:99-128 — each card is a bordered clip, then h3 title, then blurb.
    return "".join(
        f'<div><div class="rounded-lg overflow-hidden border border-line">'
        f'<img src="{x["clip"]}" alt="{H.escape(x["title"])}" class="w-full block" loading="lazy" /></div>'
        f'<h3 class="mt-4 font-semibold text-lg">{H.escape(x["title"])}</h3>'
        f'<p class="mt-2 text-sm text-neutral-400">{H.escape(x["blurb"])}</p></div>'
        for x in p["pillars"])

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
    validate(slug)
    p = PRODUCTS[slug]
    s = SHELL.read_text(encoding="utf-8")
    repl = {
        "name": p["name"], "slug": p["slug"], "tagline": p["tagline"],
        "blender_min": p["blender_min"], "price_label": p["price_label"],
        "status_badge": _badge(p), "hero_headline": p["hero"]["headline"],
        "hero_sub": p["hero"]["sub"], "manual_url": p["manual_url"],
        "flagship_class": "flagship" if p["flagship"] else "",
        "pillars": _pillars(p), "why": _why(p),
        "compat_rows": _compat(p), "faq": _faq(p), "store_buttons": _stores(p),
    }
    for k, v in repl.items():
        s = s.replace("{{" + k + "}}", v)
    out = pathlib.Path(out_path) if out_path else (LIVE / f"zap-{slug}.html")
    out.write_text(s, encoding="utf-8", newline="")
    return out.read_text(encoding="utf-8")

if __name__ == "__main__":
    # Plan 1 writes only to scratch files — never the live zap-*.html. Plan 2 flips this
    # to the live path once the CSS-inline step is generalized and parity (Task 6) has passed.
    here = pathlib.Path(__file__).resolve().parent
    for slug in [s for s in PRODUCTS if PRODUCTS[s]]:
        build_landing(slug, out_path=str(here / f"_scratch-{slug}.html")); print("built", slug)
