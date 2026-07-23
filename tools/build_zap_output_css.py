"""Inline the Tailwind CSS in zap-output.html (replacing the runtime CDN).

zap-output.html is the product's own bespoke landing (lifted from
zap_output/assets/store/landing.html), not an engine-generated page. It shipped
against https://cdn.tailwindcss.com, which is a single point of failure once
published: if that CDN is slow or blocked, the page is the *only* styling source
and renders unstyled. This generates the utilities once and inlines them, putting
the page in line with the rest of the site (index.html, zap-board.html, docs/ are
all self-contained).

Re-run after any Tailwind class change in zap-output.html:

    python tools/build_zap_output_css.py

Pinned to tailwindcss@3 (the CDN served v3; v4 renames enough utilities to shift the
page). Needs npx on PATH; nothing is installed into the repo. Mirrors
build_zap_board_css.py, but this page still carries the raw CDN <script> the first
time, so the replaced span is the CDN script + the inline tailwind.config, not an
already-generated block.
"""

import re
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAGE = REPO / "zap-output.html"

# Mirrors the tailwind.config that sat inline in the page head. Output keeps its own
# flagship palette: accent #ffcc33 (gold) + accent2 #ff5fa8 (pink).
CONFIG = """module.exports = {
  darkMode: 'class',
  content: [%s],
  theme: {
    extend: {
      colors: {
        ink: '#0b0b0d',
        panel: '#141417',
        line: '#26262b',
        accent: '#ffcc33',
        accent2: '#ff5fa8'
      },
      fontFamily: {
        sans: ['-apple-system','BlinkMacSystemFont','Segoe UI','Inter','Roboto','sans-serif']
      }
    }
  }
}
"""

GENERATED_COMMENT = (
    "<!-- Tailwind, generated instead of fetched. This page shipped with a runtime\n"
    "     Tailwind browser-CDN <script>; published as a real page that CDN was the only\n"
    "     styling source, so a blocked request served the landing unstyled (Tailwind also\n"
    "     documents that build as not for production). The rules below are the same\n"
    "     utilities, built once from the classes this file uses (tailwindcss@3).\n"
    "     (Host not named as a URL here so an external-host audit doesn't match this comment.)\n"
    "     Re-run tools/build_zap_output_css.py after adding a new Tailwind class. -->")


def main():
    if shutil.which("npx") is None:
        sys.exit("npx not found on PATH - install Node, then re-run.")

    html = PAGE.read_text(encoding="utf-8")

    # Span to replace: the CDN <script> through the close of the inline tailwind.config.
    cdn = html.find('<script src="https://cdn.tailwindcss.com"></script>')
    if cdn == -1:
        # Already inlined? Fall back to replacing the generated block in place.
        start = html.find(GENERATED_COMMENT[:40])
        if start == -1:
            sys.exit("neither the CDN script nor a generated block was found in zap-output.html")
        end = html.index("</style>", start) + len("</style>")
        i, j = start, end
    else:
        cfg = html.index("tailwind.config", cdn)
        i = cdn
        j = html.index("</script>", cfg) + len("</script>")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "tailwind.config.js").write_text(
            CONFIG % repr(str(PAGE)).replace("'", '"'), encoding="utf-8")
        (tmp / "in.css").write_text(
            "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n", encoding="utf-8")
        out = tmp / "out.css"
        r = subprocess.run(
            ["npx", "-y", "tailwindcss@3", "-c", str(tmp / "tailwind.config.js"),
             "-i", str(tmp / "in.css"), "-o", str(out), "--minify"],
            capture_output=True, text=True, shell=(sys.platform == "win32"))
        if r.returncode != 0 or not out.exists():
            sys.exit(f"tailwind build failed:\n{r.stderr[-2000:]}")
        css = out.read_text(encoding="utf-8").strip()

    block = GENERATED_COMMENT + "\n<style>" + css + "</style>"
    PAGE.write_text(html[:i] + block + html[j:], encoding="utf-8", newline="")

    print(f"{PAGE.name}: inlined {len(css) + 15:,} bytes of CSS")
    leftover = re.findall(r'(?:src|href)="(https?://[^"]+)"', PAGE.read_text(encoding="utf-8"))
    print("external requests:", leftover or "none")


if __name__ == "__main__":
    main()
