import re, pathlib
from build_landings import build_landing

SCRATCH = pathlib.Path(__file__).resolve().parent / "_scratch-board.html"

def test_board_generates_self_contained():
    html = build_landing("board", out_path=str(SCRATCH))
    # every slot filled
    assert "{{" not in html, "unfilled slot remains"
    # real content present
    for needle in ["Reference images that live inside your .blend", "Arrange", "FAQ", "Gumroad"]:
        assert needle in html, f"missing {needle!r}"
    # self-contained: only allowed external host is gumroad
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', html))
    assert hosts <= {"faraxdesigns.gumroad.com","farax-creative.github.io","gumroad.com"}, hosts
    assert "cdn.tailwindcss.com" not in html, "Tailwind CDN leaked back in"

def test_refuses_to_default_to_live_path():
    # Guard: calling without out_path must NOT silently write live/zap-board.html.
    try:
        build_landing("board")
    except ValueError:
        return
    raise AssertionError("build_landing without out_path should raise, not write the live page")

if __name__ == "__main__":
    test_board_generates_self_contained()
    test_refuses_to_default_to_live_path()
    print("ok")
