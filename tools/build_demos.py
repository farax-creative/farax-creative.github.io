"""Generate the Board landing's demo panels from the Instagram carousel clips.

Each carousel slide is a 1080x1350 composite (top logo band, a title, the Blender demo, a
bottom Free/Blender band). The landing shows only the centre Blender screen with its own HTML
caption, so this crops the demo out of each slide and writes a short WebP. GIF is never used.

Source clips live in the zap_board add-on repo (not this website repo); path hardcoded per the
same convention as the manual builders. Outputs are build artifacts (gitignored) written to
assets/img/zap-board/demos/. Re-run after changing the crop or the clip set.

    python tools/build_demos.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

LIVE = Path(__file__).resolve().parent.parent
CAROUSEL = Path(
    r"C:\Users\calar\Documents\Claude\Farax_Creative\50_addons\zap_series\zap_board"
    r"\assets\store\social\instagram\carousel"
)
OUTDIR = LIVE / "assets" / "img" / "zap-board" / "demos"

# Centre Blender screen inside the 1080x1350 slide (measured from a frame): x=69, y=378,
# w=942, h=778. Drops the top logo band, the title, and the bottom Free/Blender band.
CROP = "crop=942:778:69:378,fps=12,scale=460:-1"
SECONDS = "2.5"

# The nine features shown on the landing, in order. ImportFolder is deliberately excluded
# (the user cut "Load a whole folder" to keep a clean 3x3). Names are the carousel filenames.
CLIPS = ["02_Move", "03_Align", "04_Pen", "05_Grid", "06_Resize",
         "07_Solo", "08_Opacity", "09_Blackwhite", "10_Autoscale"]


def build_demo(name):
    src = CAROUSEL / f"{name}.mp4"
    if not src.exists():
        sys.exit(f"source clip missing: {src}")
    out = OUTDIR / f"{name}.webp"
    subprocess.run(
        ["ffmpeg", "-y", "-t", SECONDS, "-i", str(src), "-filter:v", CROP,
         "-vcodec", "libwebp", "-quality", "52", "-compression_level", "6",
         "-loop", "0", "-an", str(out)],
        check=True, capture_output=True)
    return out


def main():
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not on PATH")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for name in CLIPS:
        out = build_demo(name)
        print(f"{name:16} {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
