# Claims in the shipped manuals that must stay true, checked against the built files.
#
# These manuals live outside the add-on repositories, so nothing in a product's own test
# suite can see them. That is exactly why they rot: a sentence written when it was true
# keeps being served after the code moves, and the person who changes the code never opens
# the web manual. Three of those were found on 2026-09-02 alone, all the same shape.
#
# Each assertion here pins a specific fact and says where the truth lives, so a future
# change to the add-on has a chance of failing here instead of misleading a buyer.
import pathlib

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
LANGS = ["", ".ko", ".ja", ".pt", ".es"]

def viewer_manuals():
    return [DOCS / ("zap-viewer%s.html" % s) for s in LANGS]

def test_all_five_viewer_manuals_exist():
    missing = [p.name for p in viewer_manuals() if not p.exists()]
    assert not missing, "missing built manuals: %s" % missing

def test_viewer_manuals_never_name_the_legacy_history_folder():
    # `zap_viewer_history` is prefs.LEGACY_FOLDER_NAME in the add-on -- the fallback used
    # only when it cannot read its own preferences. A normal install never creates that
    # folder, so printing the name sends a buyer looking for something that is not there.
    # The add-on repo fixed its own copies in a05aa30; these are the ones outside it.
    for p in viewer_manuals():
        assert "zap_viewer_history" not in p.read_text(encoding="utf-8"), (
            "%s names the legacy fallback folder; the real one is render_history" % p.name)

def test_viewer_manuals_name_the_real_history_folder():
    # The other half of the check: absence of the wrong name is not presence of the right
    # one. If the sentence is ever dropped entirely this fails rather than passing quietly.
    for p in viewer_manuals():
        assert "render_history" in p.read_text(encoding="utf-8"), (
            "%s no longer tells the reader where renders are stored" % p.name)

# --- the shared sidebar block -------------------------------------------------------
# add_manual_sidebar.py injects this into the hand-maintained manuals (doctor, output).
# The generated ones (board, viewer) never get injected directly: they are built from
# zap-doctor.html as a shell, so they inherit whatever sidebar it had at build time.
#
# That makes the order of the three commands load-bearing, and it is written down the
# other way round. Inject first, then generate -- otherwise the generated manuals carry
# the previous sidebar and nothing says so. All twenty agree today; this keeps it that way.
ALL_MANUALS = [DOCS / ("%s%s.html" % (prod, s))
               for prod in ("zap-doctor", "zap-output", "zap-board", "zap-viewer")
               for s in LANGS]

def _sidebar_block(text):
    import add_manual_sidebar as A
    a = text.find(A.START)
    if a < 0:
        return None
    b = text.find(A.END, a)
    return text[a:b + len(A.END)] if b >= 0 else None

def test_every_manual_carries_the_sidebar():
    missing = [p.name for p in ALL_MANUALS
               if _sidebar_block(p.read_text(encoding="utf-8")) is None]
    assert not missing, "no sidebar block in: %s" % missing

def test_every_manual_carries_the_same_sidebar():
    # A generated manual built before the injector last ran keeps the older block, and
    # both files look fine on their own -- the drift is only visible by comparing them.
    blocks = {}
    for p in ALL_MANUALS:
        blocks.setdefault(_sidebar_block(p.read_text(encoding="utf-8")), []).append(p.name)
    assert len(blocks) == 1, (
        "manuals carry %d different sidebar versions: %s"
        % (len(blocks), [names for names in blocks.values()]))

if __name__ == "__main__":
    test_every_manual_carries_the_sidebar()
    test_every_manual_carries_the_same_sidebar()
    test_all_five_viewer_manuals_exist()
    test_viewer_manuals_never_name_the_legacy_history_folder()
    test_viewer_manuals_name_the_real_history_folder()
    print("ok")
