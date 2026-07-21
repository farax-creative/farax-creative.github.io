import shutil, subprocess, sys, pathlib
from products import PRODUCTS

LIVE = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = LIVE / "assets" / "img" / "previews"

def build_preview(slug):
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not on PATH")
    p = PRODUCTS[slug]["preview"]
    src = LIVE / p["source"]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    # Name outputs by the product's public slug ("zap-board"), not the dict key ("board"),
    # so they match the slug-based references the landing shell writes into the page.
    name = PRODUCTS[slug]["slug"]
    poster = OUTDIR / f"{name}-poster.jpg"
    webp   = OUTDIR / f"{name}.webp"
    subprocess.run(["ffmpeg","-y","-i",str(src),"-frames:v","1","-vf","scale=480:-1",
                    "-q:v","7",str(poster)], check=True, capture_output=True)
    subprocess.run(["ffmpeg","-y","-t",str(p["seconds"]),"-i",str(src),"-vcodec","libwebp",
                    "-filter:v","fps=12,scale=480:-1","-quality","50","-compression_level","6",
                    "-loop","0","-an",str(webp)], check=True, capture_output=True)
    return str(poster), str(webp)

if __name__ == "__main__":
    for slug in [s for s in PRODUCTS if PRODUCTS[s]]:
        print(slug, *[f"{pathlib.Path(x).stat().st_size//1024}KB" for x in build_preview(slug)])
