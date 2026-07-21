# Product data module — single source of truth for landing content

REQUIRED = ["name", "slug", "tagline", "blender_min", "price_label", "status", "flagship",
            "hero", "preview", "pillars", "why", "compat", "faq", "stores", "manual_url"]

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
    },
    "preview": {"source": "assets/img/zap-board/arrange.webp", "seconds": 2.5},
    "pillars": [
      {"title": "One key tidies the board",
       "blurb": "Ctrl+P packs everything with no overlaps. Select first and it only tidies the selection.",
       "clip": "assets/img/zap-board/v5_04_arrange.gif"},
      {"title": "Move them anywhere",
       "blurb": "Drag a box to select, then move the whole set at once. No modifier key needed to keep a selection together.",
       "clip": "assets/img/zap-board/v5_02_box_select.gif"},
      {"title": "Mark what's done",
       "blurb": "Pick a colour and draw straight on the board. Ticks, circles, arrows — whatever marks up a reference.",
       "clip": "assets/img/zap-board/v5_03_pen_zap.gif"},
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
       "a": "There is a Report a Bug button in the board sidebar and in Preferences → Add-ons → Zap Board. It opens the report form with your versions already filled in."},
    ],
    "stores": [
      {"name": "Gumroad", "url": "https://faraxdesigns.gumroad.com/l/zap-board", "primary": True},
    ],
    "manual_url": "https://farax-creative.github.io/docs/zap-board.html",
  },
  "output": None,
  "doctor": None,
  "viewer": None,
}

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
    missing = [k for k in REQUIRED if k not in p or _empty(p[k])]
    assert not missing, f"{slug}: empty required slots {missing}"
    assert sum(1 for s in p["stores"] if s.get("primary")) == 1, f"{slug}: need exactly one primary store"
