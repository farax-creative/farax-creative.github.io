import copy

from products import PRODUCTS, validate

def test_board_is_complete():
    assert "board" in PRODUCTS
    validate("board")                      # raises if any required slot is empty
    b = PRODUCTS["board"]
    assert b["flagship"] is False          # only output is flagship
    assert b["status"] == "live"
    assert any(s["primary"] for s in b["stores"])   # exactly one primary store
    assert b["stores"][0]["url"].startswith("https://faraxdesigns.gumroad.com/l/zap-board")

def test_board_pillars_shape():
    b = PRODUCTS["board"]
    assert len(b["pillars"]) == 3
    for pillar in b["pillars"]:
        assert pillar["title"]
        assert pillar["blurb"]
        assert pillar["clip"]

def test_board_why_shape():
    b = PRODUCTS["board"]
    assert len(b["why"]) == 3
    for item in b["why"]:
        assert item["title"]
        assert item["blurb"]

def test_board_compat_shape():
    b = PRODUCTS["board"]
    assert len(b["compat"]) == 4
    for row in b["compat"]:
        assert len(row) == 2

def test_validate_rejects_empty_slots():
    broken = copy.deepcopy(PRODUCTS)
    broken["board"]["tagline"] = ""
    import products
    original = products.PRODUCTS
    products.PRODUCTS = broken
    try:
        raised = False
        try:
            validate("board")
        except AssertionError:
            raised = True
        assert raised, "validate() should reject an empty tagline"
    finally:
        products.PRODUCTS = original

if __name__ == "__main__":
    test_board_is_complete()
    test_board_pillars_shape()
    test_board_why_shape()
    test_board_compat_shape()
    test_validate_rejects_empty_slots()
    print("ok")
