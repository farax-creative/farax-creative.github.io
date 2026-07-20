# -*- coding: utf-8 -*-
"""Add the manuals sidebar (product switcher + in-page contents) to a manual.

The block is self-contained on purpose: markup, CSS and script all sit in one
piece injected before </body>, and the sidebar is position:fixed. Nothing in
the existing header/main/footer is touched, so this stays safe to apply to
twenty ~600KB files and just as easy to back out of.

The contents list is built at load time from the page's own <h2> elements
rather than baked in, so no anchors have to be written into any manual, and a
manual whose sections change needs no second pass here.

Two of the four manuals are generated (board, viewer). Their builders lift
everything from <footer> onward out of zap-doctor.html, so injecting into that
template is enough -- they pick the sidebar up on their next build. The other
ten files (doctor and output, five languages each) have no builder and are
edited directly by this script.

Usage:
    python tools/add_manual_sidebar.py            # all hand-maintained manuals
    python tools/add_manual_sidebar.py <file>...  # specific files
"""
import io
import os
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
DOCS = os.path.normpath(DOCS)

START = "<!-- zt-sidebar:start -->"
END = "<!-- zt-sidebar:end -->"

# zap-doctor.html is the template the board and viewer builders copy from, so
# it is listed here; its four translations and all five output manuals have no
# builder at all.
TARGETS = (
    ["zap-doctor.html"]
    + ["zap-doctor.%s.html" % s for s in ("ko", "ja", "pt", "es")]
    + ["zap-output.html"]
    + ["zap-output.%s.html" % s for s in ("ko", "ja", "pt", "es")]
)

BLOCK = u"""
<!-- zt-sidebar:start -->
<!-- ==========================================================
     Manuals sidebar. Self-contained: fixed position, own CSS,
     builds its contents list from the page's <h2> elements.
     Injected by tools/add_manual_sidebar.py -- re-running that
     script replaces everything between the start/end markers,
     so edit the script, never the generated block.
     ========================================================== -->
<style>
  #zt-side{
    position:fixed; top:0; left:0; bottom:0; width:236px;
    padding:26px 18px 40px; overflow-y:auto; z-index:40;
    background:var(--void2); border-right:1px solid var(--line);
    font-family:var(--label); font-size:13px; line-height:1.5;
    -webkit-overflow-scrolling:touch;
  }
  #zt-side h3{
    font-family:var(--display); font-size:11px; letter-spacing:.14em;
    text-transform:uppercase; color:var(--ink-3);
    margin:0 0 10px; font-weight:400;
  }
  #zt-side ul{list-style:none; margin:0 0 26px; padding:0}
  #zt-side li{margin:0}
  #zt-side a{
    display:block; padding:5px 8px; margin-left:-8px;
    color:var(--ink-2); text-decoration:none; border-radius:3px;
  }
  #zt-side a:hover{color:var(--ink); background:rgba(244,235,221,.05)}
  #zt-side .zt-here{color:var(--ink); background:rgba(244,235,221,.07)}
  /* The accent is reserved for Pro callouts elsewhere; here it marks only the
     one section you are actually reading, so it stays a signal. */
  #zt-side .zt-active{
    color:var(--zap); box-shadow:inset 2px 0 0 var(--zap);
    background:var(--zap-soft);
  }
  #zt-sep{border:0; border-top:1px solid var(--line); margin:0 0 22px}

  #zt-open{
    position:fixed; left:14px; bottom:14px; z-index:41;
    font-family:var(--display); font-size:12px; letter-spacing:.08em;
    text-transform:uppercase; color:var(--void); background:var(--zap);
    border:0; border-radius:2px; padding:11px 16px; cursor:pointer;
    display:none;
  }
  #zt-scrim{
    position:fixed; inset:0; z-index:39; background:rgba(11,13,16,.6);
    display:none;
  }

  /* The text column is a centred 900px block, so its left margin is only
     wide enough to hold the sidebar once the viewport passes ~1420px. Rather
     than wait for that, indent the whole page by the sidebar's width and let
     the column re-centre in what is left. */
  @media(min-width:1180px){
    #zt-side{display:block}
    body{padding-left:236px}
  }
  @media(max-width:1179px){
    #zt-side{display:none; box-shadow:0 0 40px rgba(0,0,0,.5)}
    #zt-side.zt-shown{display:block}
    #zt-open{display:block}
    #zt-scrim.zt-shown{display:block}
  }
  @media print{
    #zt-side,#zt-open,#zt-scrim{display:none !important}
  }
</style>

<button type="button" id="zt-open" aria-expanded="false"></button>
<div id="zt-scrim" hidden></div>
<aside id="zt-side" aria-label="Manuals"></aside>

<script>
(function(){
  var PRODUCTS = [
    ["zap-doctor", "Zap Doctor"],
    ["zap-board",  "Zap Board"],
    ["zap-viewer", "Zap Viewer"],
    ["zap-output", "Zap Output"]
  ];

  /* Product names stay in English -- they are the product names, not words to
     translate. Only the two headings and the toggle are localised. */
  var L = {
    en: {m:"Manuals", c:"Contents", o:"Contents"},
    ko: {m:"\\ub9e4\\ub274\\uc5bc", c:"\\ubaa9\\ucc28", o:"\\ubaa9\\ucc28"},
    ja: {m:"\\u30de\\u30cb\\u30e5\\u30a2\\u30eb", c:"\\u76ee\\u6b21", o:"\\u76ee\\u6b21"},
    pt: {m:"Manuais", c:"Conte\\u00fado", o:"Conte\\u00fado"},
    es: {m:"Manuales", c:"Contenido", o:"Contenido"}
  };

  /* Filenames carry the language: zap-board.html is English, zap-board.ko.html
     is Korean. Reading it back here is what keeps a product link from dropping
     the reader into a language they were not reading. */
  var file = (location.pathname.split("/").pop() || "zap-doctor.html");
  var parts = file.replace(/\\.html$/, "").split(".");
  var slug = parts[0];
  var lang = parts.length > 1 ? parts[1] : "en";
  var t = L[lang] || L.en;

  function hrefFor(p){
    return lang === "en" ? p + ".html" : p + "." + lang + ".html";
  }

  var side = document.getElementById("zt-side");
  var html = '<h3>' + t.m + '</h3><ul>';
  for (var i = 0; i < PRODUCTS.length; i++){
    var here = PRODUCTS[i][0] === slug;
    html += '<li><a href="' + hrefFor(PRODUCTS[i][0]) + '"'
         + (here ? ' class="zt-here" aria-current="page"' : '')
         + '>' + PRODUCTS[i][1] + '</a></li>';
  }
  html += '</ul>';

  var heads = document.querySelectorAll("main.wrap h2");
  var links = [];
  if (heads.length){
    html += '<hr id="zt-sep"><h3>' + t.c + '</h3><ul id="zt-toc">';
    for (var j = 0; j < heads.length; j++){
      /* Index-based ids rather than slugified headings: these run across five
         languages including CJK, and a stable id beats a pretty one. */
      if (!heads[j].id) { heads[j].id = "zt-s" + (j + 1); }
      html += '<li><a href="#' + heads[j].id + '">'
           + heads[j].textContent + '</a></li>';
    }
    html += '</ul>';
  }
  side.innerHTML = html;
  links = side.querySelectorAll("#zt-toc a");

  document.getElementById("zt-open").textContent = t.o;

  /* --- narrow screens: open as an overlay --------------------------------- */
  var openBtn = document.getElementById("zt-open");
  var scrim = document.getElementById("zt-scrim");

  function setOpen(on){
    side.classList.toggle("zt-shown", on);
    scrim.classList.toggle("zt-shown", on);
    scrim.hidden = !on;
    openBtn.setAttribute("aria-expanded", on ? "true" : "false");
  }
  openBtn.addEventListener("click", function(){
    setOpen(!side.classList.contains("zt-shown"));
  });
  scrim.addEventListener("click", function(){ setOpen(false); });
  document.addEventListener("keydown", function(e){
    if (e.key === "Escape") { setOpen(false); }
  });
  side.addEventListener("click", function(e){
    if (e.target.tagName === "A") { setOpen(false); }
  });

  /* --- highlight the section being read ----------------------------------- */
  if (links.length){
    var ticking = false;
    function mark(){
      ticking = false;
      var y = window.pageYOffset + 120, current = 0;
      for (var k = 0; k < heads.length; k++){
        if (heads[k].getBoundingClientRect().top + window.pageYOffset <= y){
          current = k;
        }
      }
      for (var n = 0; n < links.length; n++){
        links[n].classList.toggle("zt-active", n === current);
      }
    }
    window.addEventListener("scroll", function(){
      if (!ticking){ ticking = true; window.requestAnimationFrame(mark); }
    });
    mark();
  }
})();
</script>
<!-- zt-sidebar:end -->
"""


def inject(path):
    html = io.open(path, encoding="utf-8").read()

    # Replace rather than refuse: the block is generated, so a second run has
    # to be able to carry a fix into files that already have an older copy.
    a = html.find(START)
    if a >= 0:
        b = html.find(END, a)
        if b < 0:
            print("UNCLOSED BLOCK   %s" % os.path.basename(path))
            return False
        html = html[:a] + html[b + len(END):]
        verb = "replaced"
    else:
        verb = "injected"

    idx = html.rfind("</body>")
    if idx < 0:
        print("NO </body>       %s" % os.path.basename(path))
        return False
    out = html[:idx] + BLOCK + html[idx:]
    io.open(path, "w", encoding="utf-8").write(out)
    print("%-16s %-26s %8d bytes" % (verb, os.path.basename(path), len(out)))
    return True


def main(argv):
    names = argv[1:] or TARGETS
    done = 0
    for name in names:
        path = name if os.path.isabs(name) else os.path.join(DOCS, name)
        if not os.path.exists(path):
            print("missing          %s" % name)
            continue
        if inject(path):
            done += 1
    print("\n%d file(s) changed" % done)


if __name__ == "__main__":
    main(sys.argv)
