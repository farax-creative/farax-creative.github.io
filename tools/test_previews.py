import pathlib, subprocess
from build_previews import build_preview

def test_board_preview_built():
    poster, webp = build_preview("board")
    assert pathlib.Path(poster).exists() and pathlib.Path(webp).exists()
    assert pathlib.Path(webp).stat().st_size < 260_000, "preview webp over budget"
    # webp must be animated (more than 1 frame)
    n = subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v:0",
                        "-show_entries","stream=nb_read_frames","-of","csv=p=0", webp],
                       capture_output=True, text=True).stdout.strip()
    assert int(n) > 1, "preview is a still, not animated"

if __name__ == "__main__":
    test_board_preview_built(); print("ok")
