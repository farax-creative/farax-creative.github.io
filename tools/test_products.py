from products import PRODUCTS, validate

def test_board_is_complete():
    assert "board" in PRODUCTS
    validate("board")                      # raises if any required slot is empty
    b = PRODUCTS["board"]
    assert b["flagship"] is False          # only output is flagship
    assert b["status"] == "live"
    assert any(s["primary"] for s in b["stores"])   # exactly one primary store
    assert b["stores"][0]["url"].startswith("https://faraxdesigns.gumroad.com/l/zap-board")

if __name__ == "__main__":
    test_board_is_complete()
    print("ok")
