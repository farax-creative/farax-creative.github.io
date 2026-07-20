"""Regenerate the inlined Tailwind CSS in zap-board.html.

zap-board.html used to pull https://cdn.tailwindcss.com at runtime. That CDN was the
page's only styling source, so a slow or blocked request served the launch landing as
unstyled HTML - and Tailwind documents that build as not for production. The utilities
are now generated once and inlined, which also puts the page back in line with the rest
of the site (index.html, report/, docs/ are all self-contained).

The cost of that: adding a NEW Tailwind class to the markup does nothing until this is
re-run. Run it after any class change.

    python tools/build_zap_board_css.py

Pinned to tailwindcss@3 on purpose - the CDN this replaced served v3, and v4 renames
enough utilities that the page would shift. Needs npx on PATH; nothing is installed
into the repo.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAGE = REPO / "zap-board.html"

# Mirrors the tailwind.config that used to sit inline in the page. Keep in sync with the
# palette comment in zap-board.html: #FFC828 matches the shipped product icon.
CONFIG = """module.exports = {
  darkMode: 'class',
  content: [%s],
  theme: {
    extend: {
      colors: {
        ink: '#0b0b0d',
        panel: '#141417',
        line: '#26262b',
        accent: '#FFC828',
        accent2: '#ff5fa8'
      },
      fontFamily: {
        sans: ['-apple-system','BlinkMacSystemFont','Segoe UI','Inter','Roboto','sans-serif']
      }
    }
  }
}
"""

# The generated block is delimited by these, so re-running replaces it in place.
START = "<!-- Tailwind, generated instead of fetched."
END = "</style>"


def main():
    if shutil.which("npx") is None:
        sys.exit("npx not found on PATH - install Node, then re-run.")

    html = PAGE.read_text(encoding="utf-8")
    i = html.find(START)
    if i == -1:
        sys.exit(f"marker not found in {PAGE.name}: {START!r}\n"
                 "The generated block was renamed or removed; fix the marker before running.")
    j = html.index(END, i) + len(END)
    old_block = html[i:j]

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

    # Keep the explanatory comment and swap only the rules, so the reasoning recorded there
    # is never lost to a rebuild. Split on the comment terminator, NOT on the first "<style>":
    # the comment used to mention a style tag in prose, and splitting on that truncated the
    # comment mid-sentence, leaving it unclosed so it swallowed the real stylesheet and the
    # page rendered completely unstyled. Anchor on "-->" and require the tag right after it.
    head = old_block[:old_block.index("-->") + len("-->")] + "\n"
    rest = old_block[len(head):].lstrip()
    if not rest.startswith("<style>"):
        sys.exit("expected a style tag immediately after the generated block's comment; "
                 f"found {rest[:40]!r}. Refusing to write a malformed page.")
    PAGE.write_text(html[:i] + head + "<style>" + css + "</style>" + html[j:],
                    encoding="utf-8", newline="")

    old_css = len(old_block) - len(head)
    print(f"{PAGE.name}: {old_css:,} -> {len(css) + 15:,} bytes of inlined CSS")
    leftover = re.findall(r'(?:src|href)="(https?://[^"]+)"', PAGE.read_text(encoding="utf-8"))
    print("external requests:", leftover or "none")


if __name__ == "__main__":
    main()
