# Product data module — single source of truth for landing content

REQUIRED = ["name", "slug", "tagline", "blender_min", "price_label", "status", "flagship",
            "hero", "preview", "features", "why", "compat", "faq", "stores", "manual_url"]

PRODUCTS = {
  "board": {
    "name": "Zap Board",
    "slug": "zap-board",
    "tagline": "A free-form reference board inside Blender",
    "blender_min": "4.5",
    "price_label": "Free",
    "status": "live",
    "flagship": False,
    "hero": {
      "headline": "Reference images that live inside your .blend",
      "sub": "Turn any Image Editor into a free-form board. Arrange your references, "
             "move them, mark them up — and it saves with your file. "
             "No second app, nothing added to your 3D scene.",
      "image": "assets/img/zap-board/hero.png",
    },
    "preview": {"source": "assets/img/zap-board/arrange.webp", "seconds": 2.5},
    # Nine framed-demo panels (the "What it does" section). Each clip is the carousel slide
    # cropped to the centre Blender screen by tools/build_demos.py; the caption is HTML here.
    "features": [
      {"clip": "assets/img/zap-board/demos/02_Move.webp",
       "eyebrow": "SELECT", "title": "Move many at once", "sub": "Box-select a group and move them together."},
      {"clip": "assets/img/zap-board/demos/03_Align.webp",
       "eyebrow": "ARRANGE", "title": "One key tidies it", "sub": "Ctrl+P packs the board with no overlaps."},
      {"clip": "assets/img/zap-board/demos/04_Pen.webp",
       "eyebrow": "MARK UP", "title": "Draw on the board", "sub": "Notes anywhere, freehand over the top."},
      {"clip": "assets/img/zap-board/demos/05_Grid.webp",
       "eyebrow": "GRID", "title": "Snap to a grid", "sub": "Optional grid, adjustable size."},
      {"clip": "assets/img/zap-board/demos/06_Resize.webp",
       "eyebrow": "SIZE", "title": "Match every size", "sub": "Normalize by height, width, longest side or area."},
      {"clip": "assets/img/zap-board/demos/07_Solo.webp",
       "eyebrow": "FOCUS", "title": "Solo one image", "sub": "Hide everything else while you look."},
      {"clip": "assets/img/zap-board/demos/08_Opacity.webp",
       "eyebrow": "COMPARE", "title": "Fade to compare", "sub": "Drop a card's opacity over your render."},
      {"clip": "assets/img/zap-board/demos/09_Blackwhite.webp",
       "eyebrow": "VALUES", "title": "Check the values", "sub": "Black and white, without touching the file."},
      {"clip": "assets/img/zap-board/demos/10_Autoscale.webp",
       "eyebrow": "FIT", "title": "Auto-fit on import", "sub": "New images land sized to the board."},
    ],
    "why": [
      {"title": "It stays open",
       "blurb": "The board is a Blender editor, so it sits in your layout like any other. You stop alt-tabbing to look at a photo."},
      {"title": "It saves with the file",
       "blurb": "Layout, notes and pen marks live in the .blend. Close Blender, reopen the file, and the board is where you left it."},
      {"title": "It leaves your scene alone",
       "blurb": "Nothing in the outliner, nothing in the viewport, nothing in your render. Uninstall it and your file still opens fine."},
    ],
    "compat": [
      ["Blender 4.5 LTS+", "Tested on 4.5, 5.0, 5.1 and 5.2."],
      ["No dependencies", "One zip. Nothing to install alongside it."],
      ["No network access", "The add-on never talks to anything."],
      ["356 automated tests", "Run against real Blender, every version."],
    ],
    "faq": [
      {"q": "Does it touch my 3D scene?",
       "a": "No. The board lives in its own data, not in your scene. Nothing is added to the outliner, nothing appears in your render, and your viewport is untouched."},
      {"q": "If I send someone the .blend, do the images go with it?",
       "a": "Only if you pack them first. Blender stores images as paths, so a .blend on its own arrives with empty cards. Press Pack Images for Sharing in the sidebar before sending. That embeds the images and makes the file larger by roughly the size of the images."},
      {"q": "Does the person I send it to need this add-on?",
       "a": "No. The file opens normally without it — they simply see an ordinary Image Editor. If they edit and send it back, the board comes through intact."},
      {"q": "What happens if I remove the add-on?",
       "a": "Your .blend still opens and works exactly as before. The board data simply stops being displayed. Reinstall and it comes back."},
      {"q": "Will it slow Blender down?",
       "a": "No. The board draws only in the editor showing it, and the images are the same ones Blender already handles. A board of twenty large references adds no measurable cost to the viewport or to rendering."},
      {"q": "How many images can I put on a board?",
       "a": "There is no fixed limit. Memory is the practical one — the images are loaded the way any Blender image is."},
      {"q": "Can I have more than one board?",
       "a": "One board per .blend file. Board mode is per editor, so you can show it in one Image Editor while another stays an ordinary image viewer."},
      {"q": "Is it really free? Will it become paid later?",
       "a": "Everything you see here is free and stays that way. A Pro tier may follow later for heavier workflows, but it will add to this — never fence off something you already have."},
      {"q": "Where do I report a bug?",
       "a": 'There is a Report a Bug button in the board sidebar and in Preferences → Add-ons → Zap Board. It opens <a href="report/" class="text-accent underline underline-offset-4">the report form</a> with your versions already filled in.'},
    ],
    "stores": [
      {"name": "Gumroad", "url": "https://faraxdesigns.gumroad.com/l/zap-board", "primary": True},
    ],
    "manual_url": "https://farax-creative.github.io/docs/zap-board.html",
  },
  "output": None,
  "doctor": {
    "name": "Zap Doctor",
    "slug": "zap-doctor",
    "tagline": "Render preflight for Blender",
    "blender_min": "4.3",
    "price_label": "",   # paid — price shown on the store, not the landing (studio decision)
    "status": "live",
    "flagship": False,
    "hero": {
      "headline": "Catch render-ruining mistakes before you hit F12",
      "sub": "You queued an overnight render, went to bed, and woke up to a broken output "
             "folder, a missing texture, or a half-frame border render. Zap Doctor scans your "
             "scene for the classic mistakes that ruin final renders, lists them by severity, "
             "and fixes 14 of them with a single click.",
      "image": "assets/img/zap-doctor/hero.webp",
    },
    "preview": {"source": "assets/img/zap-doctor/demos/scan_gauge.webp", "seconds": 2.0},
    # The four canonical Zap Doctor beats, lifted verbatim from index.html's DATA.doctor.specs,
    # each paired with the matching product GIF (converted to WebP under demos/).
    "features": [
      {"clip": "assets/img/zap-doctor/demos/scan_gauge.webp",
       "eyebrow": "SCAN", "title": "One click, before F12",
       "sub": "Every check runs in about a tenth of a second, even on a 5,700-object scene."},
      {"clip": "assets/img/zap-doctor/demos/fix_all.webp",
       "eyebrow": "FIX", "title": "Most of it from the panel",
       "sub": "Reset to 100%, Clear Render Region, Switch to AgX, Use GPU, and more."},
      {"clip": "assets/img/zap-doctor/demos/fix_scn01.webp",
       "eyebrow": "JUDGEMENT", "title": "It won't guess for you",
       "sub": "A modifier off in the viewport and on for render is usually deliberate — that row hands you the real toggles."},
      {"clip": "assets/img/zap-doctor/demos/revert.webp",
       "eyebrow": "SAFE", "title": "Nothing runs on its own",
       "sub": "No auto-scan on file load, no network access, every fix logged with a revert."},
    ],
    "why": [
      {"title": "It catches what you can't see",
       "blurb": "A missing texture, a render region left on, Cycles stuck on CPU with a GPU configured — "
                "these are invisible until the frames come back wrong. Zap Doctor finds them before you hit F12."},
      {"title": "Farm-safe by design",
       "blurb": "It never scans on its own — not on file load, not on render, not in the background. "
                "The only thing that ever scans is you pressing the button. No network access, anywhere."},
      {"title": "It won't guess for you",
       "blurb": "Where a fix is unambiguous, one button does it. Where it isn't, Zap Doctor hands you the "
                "real toggles instead of a blind guess — and every fix it makes is logged with a Revert."},
    ],
    "compat": [
      ["Blender 4.3+", "Tested on 4.3, 4.4, 4.5, 5.1 and 5.2."],
      ["Cycles and EEVEE", "Works with both render engines."],
      ["Windows, macOS, Linux", "All three, no platform-specific setup."],
      ["No network access", "None. Anywhere. The add-on only opens a browser to report a bug."],
    ],
    # Assembled section: the answers are lifted from store-listing.md; the questions are the
    # natural buyer questions those answers address. Flagged for review (see wiki log).
    "faq": [
      {"q": "Will it slow my renders down or run in the background?",
       "a": "No. Zap Doctor never scans on its own — not on file load, not on render, not in the background. "
            "The only thing that ever scans is you pressing the button."},
      {"q": "What if a fix does the wrong thing?",
       "a": "Every fix is logged and revertable. Recently Fixed shows what changed in one line, with a Revert "
            "button where the change can be undone automatically."},
      {"q": "Does it need an internet connection?",
       "a": "No network access. None, anywhere. If something goes wrong, the Report a Bug link opens a browser "
            "with your versions pre-filled — the add-on itself sends nothing."},
      {"q": "How does it decide what's actually a problem?",
       "a": "Results come back grouped by severity: errors that will make the render wrong or fail, warnings "
            "that are very likely not what you meant, and suggestions that are worth knowing but never counted against you."},
      {"q": "Which Blender versions and platforms does it support?",
       "a": "Blender 4.3 or newer, on Windows, macOS and Linux, with both Cycles and EEVEE. "
            "Tested on 4.3, 4.4, 4.5, 5.1 and 5.2."},
    ],
    "stores": [
      {"name": "Gumroad", "url": "https://faraxdesigns.gumroad.com/l/zap-doctor", "primary": True},
      {"name": "Superhive", "url": "https://superhivemarket.com/products/zap-doctor", "primary": False},
    ],
    "manual_url": "https://farax-creative.github.io/docs/zap-doctor.html",
  },
  "viewer": None,
}

# Keys that must be present but may hold "" — an intentional empty value, not a gap.
# price_label = "" means "show no price on the landing; the store buttons carry it".
EMPTY_OK = {"price_label"}

def _empty(v):
    if v is None:
        return True
    if isinstance(v, bool):
        return False
    if hasattr(v, "__len__"):
        return len(v) == 0
    return False

def validate(slug):
    """Raise AssertionError if slug's data has any missing or empty required keys."""
    p = PRODUCTS.get(slug)
    assert p is not None, f"{slug}: no data yet"
    missing = [k for k in REQUIRED if k not in p or (k not in EMPTY_OK and _empty(p[k]))]
    assert not missing, f"{slug}: empty required slots {missing}"
    assert sum(1 for s in p["stores"] if s.get("primary")) == 1, f"{slug}: need exactly one primary store"
