# -*- coding: utf-8 -*-
"""Generate the five-language Zap Board user manual.

Reuses zap-doctor.html as the shell, exactly as build_zap_viewer_manual.py
does: the base64 font embeds, the CSS and the language-switcher script are
identical across every manual in this repo, and duplicating ~600KB of font
payload by hand is how they drift apart. Only the <main> content, the
<title>/<meta>, and the product-specific links differ.

Chapter 8 of the design ("UX problem notes") is deliberately NOT shipped -
writing a manual is itself a UX review, and those notes are for us.
"""
import io
import os
import re

REPO = r"C:\Users\calar\Documents\Claude\Farax_Creative\60_website\live\docs"
TEMPLATE = os.path.join(REPO, "zap-doctor.html")

LANGS = [
    ("", "en", "EN — English"),
    ("ko", "ko", "KO — 한국어"),
    ("ja", "ja", "JA — 日本語"),
    ("pt", "pt", "PT — Português"),
    ("es", "es", "ES — Español"),
]

TITLE = {
    "en": "Zap Board — User Manual · Farax Creative",
    "ko": "Zap Board — 사용자 매뉴얼 · Farax Creative",
    "ja": "Zap Board — ユーザーマニュアル · Farax Creative",
    "pt": "Zap Board — Manual do Usuário · Farax Creative",
    "es": "Zap Board — Manual de Usuario · Farax Creative",
}

DESC = {
    "en": "User manual for Zap Board — a reference board that lives inside "
          "your .blend. Install, getting images in, arranging, notes and "
          "drawing, working with cards, and sending a board to someone else.",
    "ko": "Zap Board 사용자 매뉴얼 — .blend 안에 사는 레퍼런스 보드. 설치, "
          "이미지 가져오기, 정렬, 노트와 펜, 카드 다루기, 보드 전달하기.",
    "ja": "Zap Board ユーザーマニュアル — .blend の中に住むリファレンスボード。"
          "インストール、画像の取り込み、整列、ノートとペン、カードの操作、受け渡し。",
    "pt": "Manual do Zap Board — um quadro de referências que vive dentro do "
          "seu .blend. Instalação, importação, organização, notas e caneta.",
    "es": "Manual de Zap Board — un tablero de referencias que vive dentro de "
          "tu .blend. Instalación, importación, organización, notas y lápiz.",
}

BACK = {
    "en": "Back to Zap Board", "ko": "Zap Board로 돌아가기",
    "ja": "Zap Board に戻る", "pt": "Voltar para Zap Board",
    "es": "Volver a Zap Board",
}

KICKER = {
    "en": "ZAP SERIES / USER MANUAL", "ko": "ZAP 시리즈 / 사용자 매뉴얼",
    "ja": "ZAP シリーズ / ユーザーマニュアル",
    "pt": "SÉRIE ZAP / MANUAL DO USUÁRIO",
    "es": "SERIE ZAP / MANUAL DE USUARIO",
}

FOOTNOTE = {
    "en": "FARAX CREATIVE &middot; Zap series &middot; Zap Board",
    "ko": "FARAX CREATIVE &middot; Zap 시리즈 &middot; Zap Board",
    "ja": "FARAX CREATIVE &middot; Zap シリーズ &middot; Zap Board",
    "pt": "FARAX CREATIVE &middot; Série Zap &middot; Zap Board",
    "es": "FARAX CREATIVE &middot; Serie Zap &middot; Zap Board",
}


def content(lang):
    """The <main> inner HTML for one language."""
    return CONTENT[lang]


# ---------------------------------------------------------------------------
# Body content. Written per language rather than machine-translated: these are
# the words a user reads before deciding the add-on is trustworthy.
#
# Chapter 7 (Sharing) carries the one fact that bites people: images are
# referenced by path, so an unpacked .blend arrives with empty cards and the
# SENDER never sees it, because their copy of the files is still on disk.
# ---------------------------------------------------------------------------

CONTENT = {}

CONTENT["en"] = """
  <h1>Zap Board — User Manual</h1>
  <p class="lede">A reference board that lives inside your .blend. Turn any
  Image Editor into a free-form 2D canvas, put your references on it, arrange
  them, mark them up — and it saves with your file. Nothing is added to your
  3D scene, and nothing shows up in your render.</p>

  <section>
    <h2>30-second version</h2>
    <ol>
      <li>Install it, then open an <b>Image Editor</b>.</li>
      <li>Click the <b>Zap Board</b> toggle in that editor's header.</li>
      <li>Drag image files onto it from your file browser, or press
      <code>Ctrl+Shift+I</code> to pick them from a dialog.</li>
      <li>Move them around. Press <code>Ctrl+P</code> to tidy the whole board
      with no overlaps.</li>
      <li>Save. Reopen the file — the board is exactly as you left it.</li>
    </ol>
  </section>

  <section>
    <h2>1. What it is</h2>
    <p>Zap Board turns one Image Editor into a board you can drop reference
    images onto. It is <b>per editor</b>, so you can have a board in one area
    while another Image Editor stays an ordinary image viewer.</p>
    <p><b>It does not touch your 3D scene.</b> Nothing is added to the
    outliner, nothing appears in your viewport, and nothing reaches your
    render. The board is its own data, saved inside the <code>.blend</code>
    alongside everything else.</p>
    <p>One board per file in this release.</p>
    <h3>Requirements</h3>
    <p>Blender <b>4.5 LTS or newer</b>. Verified on 4.5, 5.0 and 5.2.</p>
  </section>

  <section>
    <h2>2. Installing</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions / Add-ons &rsaquo;
      the drop-down in the corner &rsaquo; <b>Install from Disk…</b></li>
      <li>Pick <code>zap_board-1.0.0.zip</code>.</li>
      <li>Enable <b>Zap Board</b> in the list.</li>
      <li>Open an Image Editor and click the <b>Zap Board</b> toggle in its
      header. There is also a board button in the 3D Viewport header that
      converts the current area in one click.</li>
    </ol>
    <p>Press <code>N</code> inside the board to open the sidebar, where every
    command also has a button.</p>
  </section>

  <section>
    <h2>3. Getting images in</h2>
    <p>Four ways, all of which land the image as a card on the board:</p>
    <ul>
      <li><b>Drag and drop</b> image files straight from your file browser
      onto the board.</li>
      <li><b>Import Images…</b> (<code>Ctrl+Shift+I</code>) to pick files from
      a dialog.</li>
      <li><b>Load Folder</b> to add every image in a folder at once.</li>
      <li><b>Paste</b> (<code>Ctrl+V</code>) to drop in an image you just
      copied from anywhere.</li>
    </ul>
    <p class="note"><b>Pasted images are embedded immediately.</b> A pasted
    image has no file on disk to point at, so Zap Board packs it into the
    <code>.blend</code> the moment you paste. You do not need to do anything,
    and the card survives a reload.</p>
  
    <p class="note"><b>Paste and Reveal File are Windows only.</b> Both hand
    off to a Windows tool - PowerShell for the clipboard, Explorer for
    Reveal File. On macOS and Linux they do nothing and say so. Use
    <b>Import Images&hellip;</b> or drag and drop instead of pasting.</p>
  </section>

  <section>
    <h2>4. Arranging</h2>
    <h3>Moving and selecting</h3>
    <ul>
      <li>Click a card to select it, drag it to move it.</li>
      <li><code>Shift</code>+click to add to the selection.</li>
      <li>Drag on empty space to <b>box-select</b>.</li>
      <li><code>A</code> selects everything.</li>
      <li>With several cards selected, dragging any one of them moves the
      whole set.</li>
      <li>Middle-mouse to pan, wheel to zoom, <code>Home</code> to fit the
      whole board on screen.</li>
    </ul>
    <h3>Laying the board out</h3>
    <ul>
      <li><code>Ctrl+P</code> — <b>Best Fit</b>: packs everything with no
      overlaps. If anything is selected, only the selection is packed.</li>
      <li><code>Ctrl+Alt+N</code> / <code>A</code> / <code>D</code> /
      <code>R</code> — sort by name, added order, file path, or at random.</li>
      <li><code>Ctrl+Shift+</code>arrow — align the selection to its top,
      bottom, left or right edge.</li>
      <li><b>Distribute</b> in the sidebar — even spacing.</li>
      <li><code>Ctrl+Alt+</code>arrow — make the selection one size (by
      height, width, or longest edge).</li>
    </ul>
    <h3>Grid and snapping</h3>
    <p><code>G</code> shows the grid, <code>Shift+G</code> snaps to it. Grid
    size is in Preferences.</p>
  </section>

  <section>
    <h2>5. Notes and drawing</h2>
    <h3>Notes</h3>
    <p><code>Shift+N</code> adds a text card. Double-click it to edit, or edit
    it line by line in the sidebar — which is also where you set the font
    size, card colour and text alignment. <b>Fit to Text</b> resizes the card
    to whatever it now contains.</p>
    <p>Notes are backed by a Blender text datablock, so they hold multiple
    lines and accept any language your system can type.</p>
    <h3>Drawing</h3>
    <p><code>D</code> toggles draw mode. Pick a colour and thickness in the
    sidebar and draw straight on the board — ticks, circles, arrows, whatever
    marks up a reference. <b>Undo Line</b> removes the last stroke,
    <b>Clear</b> removes them all. Strokes can also be selected, moved and
    deleted like any other item.</p>
  </section>

  <section>
    <h2>6. Working with cards</h2>
    <ul>
      <li><b>Opacity</b> — drag the slider on the card, use the sidebar
      buttons, or <code>Ctrl+Shift+Numpad&nbsp;+</code> /
      <code>Numpad&nbsp;−</code>.</li>
      <li><b>Flip and rotate</b> — horizontal, vertical, and 90° presets.</li>
      <li><b>Crop</b> — turn on crop mode and drag a card's handles. It is
      <b>non-destructive</b>: the source file is untouched and
      <b>Reset</b> restores the full image.</li>
      <li><b>Lock</b> a card so it cannot be dragged or resized by accident.
      <b>Group</b> cards so clicking one moves the whole set.</li>
      <li><b>Bring to Front / Send to Back</b>
      (<code>Ctrl+Shift+A</code> / <code>B</code>) for overlapping cards.</li>
      <li><b>Solo</b> hides everything except the selection.
      <code>F</code> focuses a card; the bracket keys step to the next and
      previous one.</li>
      <li><b>Greyscale</b> — <code>Alt+G</code> for the selection,
      <code>Ctrl+Alt+G</code> for the whole board, to judge values.</li>
      <li><b>Export as Image</b> writes the whole board out as one file.</li>
    </ul>
    <p class="note">The four greyscale and grid shortcuts all sit on
    <code>G</code> (<code>G</code>, <code>Shift+G</code>, <code>Alt+G</code>,
    <code>Ctrl+Alt+G</code>). If the board suddenly looks wrong, one of these
    is the first thing to check.</p>
  </section>

  <section>
    <h2>7. Sending a board to someone else</h2>
    <p>The layout is stored in your <code>.blend</code>, but images are stored
    the way Blender stores any image: as a <b>path to a file on disk</b>. Send
    the <code>.blend</code> on its own and the person opening it gets your
    layout with <b>empty cards</b>, because the image files never left your
    machine.</p>
    <p class="note"><b>You will not notice this yourself.</b> Your copy of the
    files is still there, so your board looks fine no matter what. This is the
    one thing worth remembering from this manual.</p>
    <p>Before sending, press <b>Pack Images for Sharing</b> in the sidebar. It
    embeds the images inside the <code>.blend</code> so the board arrives
    complete. The trade is size: packing a large reference set makes the
    <code>.blend</code> about as large as the references themselves. If the
    file never leaves your machine, you do not need to pack anything.</p>
    <h3>They do not need this add-on</h3>
    <p>The file opens normally without Zap Board installed — no errors, no
    warnings. They simply see an ordinary Image Editor. If they edit and send
    it back, the board comes through intact: cards, notes, packed images and
    which editor was a board all survive a round trip through a Blender that
    has never had this add-on installed.</p>
  </section>

  <section>
    <h2>If something goes wrong</h2>
    <p>There is a <b>Report a Bug</b> button in the board sidebar and in
    Edit &rsaquo; Preferences &rsaquo; Add-ons &rsaquo; Zap Board. It opens a
    form in your browser with your add-on version, Blender version and OS
    already filled in. Nothing is sent from Blender itself.</p>
  </section>
"""


CONTENT["ko"] = """
  <h1>Zap Board — 사용자 매뉴얼</h1>
  <p class="lede">.blend 안에 사는 레퍼런스 보드입니다. 아무 이미지 에디터나
  자유 배치 2D 캔버스로 바꿔서 레퍼런스를 올리고, 정리하고, 펜으로 표시하면
  파일과 함께 저장됩니다. 3D 씬에는 아무것도 추가되지 않고, 렌더에도 나오지
  않습니다.</p>

  <section>
    <h2>30초 요약</h2>
    <ol>
      <li>설치한 뒤 <b>이미지 에디터</b>를 엽니다.</li>
      <li>그 에디터 헤더의 <b>Zap Board</b> 토글을 켭니다.</li>
      <li>탐색기에서 이미지 파일을 끌어다 놓거나,
      <code>Ctrl+Shift+I</code>로 파일을 고릅니다.</li>
      <li>마음대로 옮깁니다. <code>Ctrl+P</code>를 누르면 겹침 없이 한 번에
      정리됩니다.</li>
      <li>저장하고 파일을 다시 열면 보드가 그대로 있습니다.</li>
    </ol>
  </section>

  <section>
    <h2>1. 이게 무엇인가</h2>
    <p>Zap Board는 이미지 에디터 하나를 레퍼런스를 올려놓는 보드로 바꿉니다.
    <b>에디터 단위</b>로 동작하므로, 한쪽은 보드로 쓰면서 다른 이미지 에디터는
    평범한 이미지 뷰어로 그대로 둘 수 있습니다.</p>
    <p><b>3D 씬은 건드리지 않습니다.</b> 아웃라이너에 아무것도 추가되지 않고,
    뷰포트에도 나타나지 않으며, 렌더에도 들어가지 않습니다. 보드는 자기만의
    데이터이고 <code>.blend</code> 안에 함께 저장됩니다.</p>
    <p>이번 버전은 <b>파일당 보드 하나</b>입니다.</p>
    <h3>요구 사항</h3>
    <p>Blender <b>4.5 LTS 이상</b>. 4.5 · 5.0 · 5.2에서 검증했습니다.</p>
  </section>

  <section>
    <h2>2. 설치</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions / Add-ons &rsaquo;
      모서리 드롭다운 &rsaquo; <b>Install from Disk…</b></li>
      <li><code>zap_board-1.0.0.zip</code>을 고릅니다.</li>
      <li>목록에서 <b>Zap Board</b>를 켭니다.</li>
      <li>이미지 에디터를 열고 헤더의 <b>Zap Board</b> 토글을 누릅니다. 3D
      뷰포트 헤더에도 현재 영역을 한 번에 보드로 바꾸는 버튼이 있습니다.</li>
    </ol>
    <p>보드 안에서 <code>N</code>을 누르면 사이드바가 열립니다. 모든 명령에
    버튼이 하나씩 있습니다.</p>
  </section>

  <section>
    <h2>3. 이미지 가져오기</h2>
    <p>네 가지 방법이 있고, 어느 쪽이든 이미지가 카드로 올라옵니다.</p>
    <ul>
      <li>탐색기에서 이미지 파일을 <b>끌어다 놓기</b>.</li>
      <li><b>Import Images…</b>(<code>Ctrl+Shift+I</code>)로 파일 선택.</li>
      <li><b>Load Folder</b>로 폴더 안 이미지를 통째로 추가.</li>
      <li><b>붙여넣기</b>(<code>Ctrl+V</code>)로 방금 복사한 이미지를 올리기.</li>
    </ul>
    <p class="note"><b>붙여넣은 이미지는 즉시 파일에 포함됩니다.</b> 붙여넣은
    이미지는 디스크에 가리킬 파일이 없기 때문에, Zap Board가 붙여넣는 순간
    <code>.blend</code> 안에 넣습니다. 따로 할 일은 없고 다시 열어도 카드가
    남아 있습니다.</p>
  
    <p class="note"><b>붙여넣기와 Reveal File은 윈도우 전용입니다.</b> 둘 다
    윈도우 도구에 넘기기 때문입니다 — 클립보드는 PowerShell, Reveal File은
    탐색기. macOS와 리눅스에서는 아무 일도 하지 않고 그렇다고 알려줍니다.
    붙여넣기 대신 <b>Import Images&hellip;</b>나 끌어다 놓기를 쓰세요.</p>
  </section>

  <section>
    <h2>4. 정렬하기</h2>
    <h3>이동과 선택</h3>
    <ul>
      <li>카드를 클릭하면 선택되고, 끌면 이동합니다.</li>
      <li><code>Shift</code>+클릭으로 선택에 추가합니다.</li>
      <li>빈 곳을 드래그하면 <b>박스 선택</b>입니다.</li>
      <li><code>A</code>는 전체 선택입니다.</li>
      <li>여러 장을 선택한 상태에서는 그중 아무거나 끌면 <b>전부 함께</b>
      움직입니다.</li>
      <li>휠 클릭으로 이동, 휠로 확대·축소, <code>Home</code>으로 보드 전체
      보기.</li>
    </ul>
    <h3>보드 배치</h3>
    <ul>
      <li><code>Ctrl+P</code> — <b>Best Fit</b>: 겹치지 않게 채웁니다. 선택된
      것이 있으면 선택된 것만 정리합니다.</li>
      <li><code>Ctrl+Alt+N</code> / <code>A</code> / <code>D</code> /
      <code>R</code> — 이름 · 추가순 · 경로 · 무작위 정렬.</li>
      <li><code>Ctrl+Shift+</code>화살표 — 선택을 위 · 아래 · 왼쪽 · 오른쪽
      가장자리로 정렬.</li>
      <li>사이드바의 <b>Distribute</b> — 간격을 균등하게.</li>
      <li><code>Ctrl+Alt+</code>화살표 — 선택의 크기를 하나로 통일(높이 ·
      너비 · 긴 변 기준).</li>
    </ul>
    <h3>그리드와 스냅</h3>
    <p><code>G</code>는 그리드 표시, <code>Shift+G</code>는 그리드에 붙이기.
    그리드 크기는 환경 설정에 있습니다.</p>
  </section>

  <section>
    <h2>5. 노트와 펜</h2>
    <h3>노트</h3>
    <p><code>Shift+N</code>으로 텍스트 카드를 추가합니다. 더블클릭해서
    편집하거나 사이드바에서 줄 단위로 고칠 수 있고, 글자 크기 · 카드 색 ·
    정렬도 거기서 정합니다. <b>Fit to Text</b>는 내용에 맞춰 카드 크기를
    맞춥니다.</p>
    <p>노트는 Blender 텍스트 데이터블록을 쓰기 때문에 여러 줄이 들어가고,
    시스템에서 입력 가능한 언어면 무엇이든 들어갑니다(한글 포함).</p>
    <h3>펜</h3>
    <p><code>D</code>로 그리기 모드를 켭니다. 사이드바에서 색과 굵기를 고르고
    보드 위에 바로 그리면 됩니다 — 체크, 동그라미, 화살표 등 레퍼런스에 표시할
    것이면 무엇이든. <b>Undo Line</b>은 마지막 획을, <b>Clear</b>는 전부
    지웁니다. 그린 획도 다른 항목처럼 선택 · 이동 · 삭제할 수 있습니다.</p>
  </section>

  <section>
    <h2>6. 카드 다루기</h2>
    <ul>
      <li><b>불투명도</b> — 카드의 슬라이더를 끌거나, 사이드바 버튼, 또는
      <code>Ctrl+Shift+Numpad&nbsp;+</code> / <code>Numpad&nbsp;−</code>.</li>
      <li><b>뒤집기와 회전</b> — 수평 · 수직 뒤집기와 90° 프리셋.</li>
      <li><b>크롭</b> — 크롭 모드를 켜고 카드 핸들을 끕니다.
      <b>비파괴적</b>이라 원본 파일은 그대로이고 <b>Reset</b>으로 언제든
      전체 이미지로 되돌립니다.</li>
      <li><b>Lock</b>으로 실수로 끌리거나 크기가 바뀌지 않게 잠급니다.
      <b>Group</b>으로 묶으면 하나만 클릭해도 묶음 전체가 움직입니다.</li>
      <li>겹친 카드는 <b>Bring to Front / Send to Back</b>
      (<code>Ctrl+Shift+A</code> / <code>B</code>)으로 순서를 바꿉니다.</li>
      <li><b>Solo</b>는 선택한 것만 남기고 숨깁니다. <code>F</code>는 카드에
      초점을 맞추고, 대괄호 키로 다음 · 이전으로 넘어갑니다.</li>
      <li><b>흑백</b> — 선택만 <code>Alt+G</code>, 보드 전체
      <code>Ctrl+Alt+G</code>. 명암을 볼 때 씁니다.</li>
      <li><b>Export as Image</b>는 보드 전체를 이미지 파일 하나로 내보냅니다.</li>
    </ul>
    <p class="note">흑백과 그리드 단축키 네 개가 전부 <code>G</code>에 몰려
    있습니다(<code>G</code>, <code>Shift+G</code>, <code>Alt+G</code>,
    <code>Ctrl+Alt+G</code>). 보드가 갑자기 이상해 보이면 여기부터
    확인하세요.</p>
  </section>

  <section>
    <h2>7. 보드를 다른 사람에게 보내기</h2>
    <p>배치는 <code>.blend</code> 안에 저장되지만, 이미지는 Blender가 원래
    이미지를 다루는 방식대로 <b>디스크상의 파일 경로</b>로 저장됩니다.
    <code>.blend</code>만 보내면 받는 사람은 배치는 그대로인데 <b>카드가 텅 빈</b>
    보드를 보게 됩니다. 이미지 파일은 보낸 사람 컴퓨터를 떠나지 않았으니까요.</p>
    <p class="note"><b>보내는 쪽에서는 이걸 절대 눈치챌 수 없습니다.</b> 내
    컴퓨터에는 파일이 그대로 있어서 보드가 멀쩡해 보이거든요. 이 매뉴얼에서
    딱 하나만 기억한다면 이겁니다.</p>
    <p>보내기 전에 사이드바의 <b>Pack Images for Sharing</b>을 누르세요.
    이미지를 <code>.blend</code> 안에 넣어서 보드가 온전히 도착합니다. 대가는
    용량입니다 — 큰 레퍼런스 묶음을 넣으면 <code>.blend</code>가 레퍼런스
    전체만큼 커집니다. 파일이 내 컴퓨터를 떠나지 않는다면 넣을 필요가
    없습니다.</p>
    <h3>받는 사람은 이 애드온이 필요 없습니다</h3>
    <p>Zap Board가 없어도 파일은 정상적으로 열립니다 — 오류도 경고도 없고,
    그냥 평범한 이미지 에디터로 보일 뿐입니다. 그쪽에서 편집해 되돌려줘도 보드는
    그대로입니다. 카드 · 노트 · 포함된 이미지 · 어느 에디터가 보드였는지까지,
    이 애드온을 한 번도 설치한 적 없는 Blender를 거쳐 와도 전부 살아남습니다.</p>
  </section>

  <section>
    <h2>문제가 생기면</h2>
    <p>보드 사이드바와 Edit &rsaquo; Preferences &rsaquo; Add-ons &rsaquo;
    Zap Board에 <b>Report a Bug</b> 버튼이 있습니다. 애드온 버전 · Blender 버전
    · 운영체제가 미리 채워진 상태로 브라우저에 양식이 열립니다. Blender에서
    직접 전송되는 것은 아무것도 없습니다.</p>
  </section>
"""


CONTENT["ja"] = """
  <h1>Zap Board — ユーザーマニュアル</h1>
  <p class="lede">.blend の中に住むリファレンスボードです。任意の Image Editor を
  自由配置の 2D キャンバスに変え、参考画像を並べ、整理し、書き込む — そしてその
  まま .blend と一緒に保存されます。3D シーンには何も追加されず、レンダーにも
  一切写りません。</p>

  <section>
    <h2>30秒でわかる</h2>
    <ol>
      <li>インストールして <b>Image Editor</b> を開きます。</li>
      <li>そのエディタのヘッダーで <b>Zap Board</b> トグルをクリックします。</li>
      <li>ファイルブラウザから画像をドラッグ＆ドロップするか、
      <code>Ctrl+Shift+I</code> でダイアログから選びます。</li>
      <li>好きな位置へ動かします。<code>Ctrl+P</code> を押せばボード全体が
      重なりなく整列します。</li>
      <li>保存します。ファイルを開き直すと、ボードは閉じたときのままです。</li>
    </ol>
  </section>

  <section>
    <h2>1. これは何か</h2>
    <p>Zap Board は Image Editor をひとつ、参考画像を置けるボードに変えます。
    <b>エディタ単位</b>で切り替わるので、片方のエリアをボードにしつつ、別の
    Image Editor は通常の画像ビューアのまま使えます。</p>
    <p><b>3D シーンには一切触れません。</b>アウトライナーに何も増えず、
    ビューポートにも現れず、レンダーにも届きません。ボードは独立したデータで、
    他のデータと同じように <code>.blend</code> の中に保存されます。</p>
    <p>このリリースでは 1ファイルにつきボードは 1つです。</p>
    <h3>動作環境</h3>
    <p>Blender <b>4.5 LTS 以降</b>。4.5・5.0・5.2 で検証済みです。</p>
  </section>

  <section>
    <h2>2. インストール</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions / Add-ons &rsaquo;
      右上のドロップダウン &rsaquo; <b>Install from Disk…</b></li>
      <li><code>zap_board-1.0.0.zip</code> を選択します。</li>
      <li>リストで <b>Zap Board</b> を有効にします。</li>
      <li>Image Editor を開き、ヘッダーの <b>Zap Board</b> トグルをクリックします。
      3D Viewport のヘッダーにもボタンがあり、現在のエリアをワンクリックで
      ボードに変換できます。</li>
    </ol>
    <p>ボード上で <code>N</code> を押すとサイドバーが開きます。すべてのコマンドは
    そこにボタンとしても用意されています。</p>
  </section>

  <section>
    <h2>3. 画像を取り込む</h2>
    <p>方法は 4つ。どれも画像はカードとしてボードに載ります:</p>
    <ul>
      <li><b>ドラッグ＆ドロップ</b> — ファイルブラウザから画像ファイルを直接
      ボードへ。</li>
      <li><b>Import Images…</b>（<code>Ctrl+Shift+I</code>）— ダイアログから
      ファイルを選ぶ。</li>
      <li><b>Load Folder</b> — フォルダ内の画像をまとめて追加する。</li>
      <li><b>ペースト</b>（<code>Ctrl+V</code>）— どこかでコピーしてきた画像を
      そのまま貼り付ける。</li>
    </ul>
    <p class="note"><b>ペーストした画像はその場で埋め込まれます。</b>貼り付けた
    画像にはディスク上の参照先ファイルが存在しないため、Zap Board はペースト
    した瞬間に <code>.blend</code> へパックします。特別な操作は必要なく、
    読み込み直してもカードは残ります。</p>
  
    <p class="note"><b>ペーストと Reveal File は Windows 専用です。</b>どちらも
    Windows のツールに処理を渡すためです — クリップボードは PowerShell、
    Reveal File はエクスプローラー。macOS と Linux では何も実行せず、その旨を
    表示します。ペーストの代わりに <b>Import Images&hellip;</b> か
    ドラッグ＆ドロップを使ってください。</p>
  </section>

  <section>
    <h2>4. 整列する</h2>
    <h3>移動と選択</h3>
    <ul>
      <li>カードをクリックで選択、ドラッグで移動。</li>
      <li><code>Shift</code>+クリックで選択に追加。</li>
      <li>何もない場所をドラッグすると<b>ボックス選択</b>。</li>
      <li><code>A</code> で全選択。</li>
      <li>複数選択した状態でどれか1枚をドラッグすると、まとめて動きます。</li>
      <li>中ボタンでパン、ホイールでズーム、<code>Home</code> でボード全体を
      画面に収めます。</li>
    </ul>
    <h3>ボードのレイアウト</h3>
    <ul>
      <li><code>Ctrl+P</code> — <b>Best Fit</b>: 重なりなく敷き詰めます。
      何か選択されていれば、その選択分だけが対象になります。</li>
      <li><code>Ctrl+Alt+N</code> / <code>A</code> / <code>D</code> /
      <code>R</code> — 名前順・追加順・ファイルパス順・ランダムで並べ替え。</li>
      <li><code>Ctrl+Shift+</code>矢印 — 選択を上・下・左・右の端で整列。</li>
      <li>サイドバーの <b>Distribute</b> — 等間隔に配置。</li>
      <li><code>Ctrl+Alt+</code>矢印 — 選択のサイズを揃える（高さ・幅・長辺の
      いずれか基準）。</li>
    </ul>
    <h3>グリッドとスナップ</h3>
    <p><code>G</code> でグリッド表示、<code>Shift+G</code> でスナップ。
    グリッド間隔は Preferences で設定します。</p>
  </section>

  <section>
    <h2>5. ノートと描き込み</h2>
    <h3>ノート</h3>
    <p><code>Shift+N</code> でテキストカードを追加します。ダブルクリックで編集
    するか、サイドバーで 1行ずつ編集します。フォントサイズ・カード色・文字
    揃えもサイドバーで指定できます。<b>Fit to Text</b> は現在の内容に合わせて
    カードの大きさを調整します。</p>
    <p>ノートの実体は Blender のテキストデータブロックなので、複数行を保持でき、
    システムで入力できる言語ならそのまま扱えます。</p>
    <h3>描き込み</h3>
    <p><code>D</code> でドローモードを切り替えます。サイドバーで色と太さを選び、
    ボードに直接描けます — チェック、丸囲み、矢印など、リファレンスへの
    書き込みに使うものはひと通り。<b>Undo Line</b> で直前のストロークを取り消し、
    <b>Clear</b> で全消去。ストロークも他のアイテムと同じように選択・移動・
    削除できます。</p>
  </section>

  <section>
    <h2>6. カードを扱う</h2>
    <ul>
      <li><b>不透明度</b> — カード上のスライダーをドラッグ、サイドバーの
      ボタン、または <code>Ctrl+Shift+Numpad&nbsp;+</code> /
      <code>Numpad&nbsp;−</code>。</li>
      <li><b>反転と回転</b> — 水平・垂直反転と 90° 単位のプリセット。</li>
      <li><b>クロップ</b> — クロップモードにしてカードのハンドルをドラッグ。
      <b>非破壊</b>です: 元のファイルには手を加えず、<b>Reset</b> で元の画像
      全体に戻ります。</li>
      <li><b>Lock</b> でカードを固定し、うっかり動かしたりサイズを変えたり
      するのを防ぎます。<b>Group</b> でまとめれば、1枚をクリックするだけで
      グループ全体が動きます。</li>
      <li><b>Bring to Front / Send to Back</b>
      （<code>Ctrl+Shift+A</code> / <code>B</code>）— 重なり順の入れ替え。</li>
      <li><b>Solo</b> は選択以外をすべて隠します。<code>F</code> でカードに
      フォーカス、ブラケットキーで次・前のカードへ移動します。</li>
      <li><b>グレースケール</b> — 選択は <code>Alt+G</code>、ボード全体は
      <code>Ctrl+Alt+G</code>。明度のバランスを見るために使います。</li>
      <li><b>Export as Image</b> はボード全体を 1枚の画像として書き出します。</li>
    </ul>
    <p class="note">グレースケールとグリッドの 4つのショートカットはすべて
    <code>G</code> に集まっています（<code>G</code>・<code>Shift+G</code>・
    <code>Alt+G</code>・<code>Ctrl+Alt+G</code>）。ボードの見た目が急に
    おかしくなったら、まずこのどれかを疑ってください。</p>
  </section>

  <section>
    <h2>7. ボードを人に渡す</h2>
    <p>レイアウトは <code>.blend</code> に保存されますが、画像は Blender が
    画像を扱うときと同じ方式 — <b>ディスク上のファイルへのパス</b>として
    保存されます。<code>.blend</code> だけを送ると、開いた相手にはレイアウト
    だけが届き、<b>カードは空</b>になります。画像ファイルはあなたのマシンから
    出ていないからです。</p>
    <p class="note"><b>この状態は送った本人には見えません。</b>あなたの手元には
    ファイルが残っているので、ボードは何をしても正常に見えます。このマニュアル
    で覚えて帰る価値があるのは、この 1点です。</p>
    <p>送る前に、サイドバーの <b>Pack Images for Sharing</b> を押してください。
    画像を <code>.blend</code> の中に埋め込むので、ボードは完全な状態で相手に
    届きます。代償はサイズです: 大量のリファレンスをパックすると、
    <code>.blend</code> はリファレンス自体とほぼ同じ大きさになります。ファイルを
    自分のマシンから出さないなら、パックする必要はありません。</p>
    <h3>相手にこのアドオンは不要です</h3>
    <p>Zap Board がインストールされていなくてもファイルは普通に開きます —
    エラーも警告も出ません。相手にはただの Image Editor に見えるだけです。
    相手が編集して送り返しても、ボードはそのまま戻ってきます: カード・ノート・
    パックされた画像・どのエディタがボードだったか、すべてがこのアドオンを
    一度も入れたことのない Blender を往復しても保たれます。</p>
  </section>

  <section>
    <h2>うまくいかないとき</h2>
    <p>ボードのサイドバーと、Edit &rsaquo; Preferences &rsaquo; Add-ons
    &rsaquo; Zap Board に <b>Report a Bug</b> ボタンがあります。押すとブラウザ
    でフォームが開き、アドオンのバージョン・Blender のバージョン・OS が入力済み
    の状態になっています。Blender 自体からは何も送信されません。</p>
  </section>
"""

CONTENT["pt"] = """
  <h1>Zap Board — Manual do Usuário</h1>
  <p class="lede">Um quadro de referências que vive dentro do seu .blend.
  Transforme qualquer Image Editor numa tela 2D livre, coloque suas referências
  nela, organize, anote — e tudo é salvo junto com o arquivo. Nada é adicionado
  à sua cena 3D, e nada aparece no seu render.</p>

  <section>
    <h2>Versão de 30 segundos</h2>
    <ol>
      <li>Instale e abra um <b>Image Editor</b>.</li>
      <li>Clique no botão <b>Zap Board</b> no cabeçalho desse editor.</li>
      <li>Arraste arquivos de imagem do seu gerenciador de arquivos para lá, ou
      aperte <code>Ctrl+Shift+I</code> para escolhê-los numa janela.</li>
      <li>Mova as imagens à vontade. Aperte <code>Ctrl+P</code> para arrumar o
      quadro inteiro sem sobreposições.</li>
      <li>Salve. Reabra o arquivo — o quadro está exatamente como você
      deixou.</li>
    </ol>
  </section>

  <section>
    <h2>1. O que é</h2>
    <p>O Zap Board transforma um Image Editor num quadro onde você solta
    imagens de referência. Ele é <b>por editor</b>, então dá para ter um quadro
    numa área enquanto outro Image Editor continua sendo um visualizador de
    imagens comum.</p>
    <p><b>Ele não mexe na sua cena 3D.</b> Nada é adicionado ao outliner, nada
    aparece na sua viewport e nada chega ao seu render. O quadro são dados
    próprios, salvos dentro do <code>.blend</code> junto com todo o resto.</p>
    <p>Um quadro por arquivo nesta versão.</p>
    <h3>Requisitos</h3>
    <p>Blender <b>4.5 LTS ou mais recente</b>. Verificado em 4.5, 5.0 e 5.2.</p>
  </section>

  <section>
    <h2>2. Instalação</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions / Add-ons &rsaquo;
      menu no canto &rsaquo; <b>Install from Disk…</b></li>
      <li>Escolha <code>zap_board-1.0.0.zip</code>.</li>
      <li>Ative <b>Zap Board</b> na lista.</li>
      <li>Abra um Image Editor e clique no botão <b>Zap Board</b> no cabeçalho
      dele. Há também um botão de quadro no cabeçalho da 3D Viewport que
      converte a área atual com um clique.</li>
    </ol>
    <p>Aperte <code>N</code> dentro do quadro para abrir a barra lateral, onde
    todo comando também tem um botão.</p>
  </section>

  <section>
    <h2>3. Trazendo imagens</h2>
    <p>Quatro caminhos, e todos colocam a imagem como um card no quadro:</p>
    <ul>
      <li><b>Arraste e solte</b> arquivos de imagem direto do seu gerenciador
      de arquivos sobre o quadro.</li>
      <li><b>Import Images…</b> (<code>Ctrl+Shift+I</code>) para escolher
      arquivos numa janela.</li>
      <li><b>Load Folder</b> para adicionar todas as imagens de uma pasta de
      uma vez.</li>
      <li><b>Colar</b> (<code>Ctrl+V</code>) para jogar no quadro uma imagem
      que você acabou de copiar de qualquer lugar.</li>
    </ul>
    <p class="note"><b>Imagens coladas são embutidas na hora.</b> Uma imagem
    colada não tem arquivo em disco para apontar, então o Zap Board a empacota
    dentro do <code>.blend</code> no momento em que você cola. Você não precisa
    fazer nada, e o card sobrevive a um recarregamento.</p>
  
    <p class="note"><b>Colar e Reveal File s&atilde;o s&oacute; para Windows.</b>
    Os dois passam a tarefa para uma ferramenta do Windows - PowerShell para
    a &aacute;rea de transfer&ecirc;ncia, Explorer para o Reveal File. No macOS
    e no Linux eles n&atilde;o fazem nada e avisam. Use
    <b>Import Images&hellip;</b> ou arraste e solte em vez de colar.</p>
  </section>

  <section>
    <h2>4. Organizando</h2>
    <h3>Mover e selecionar</h3>
    <ul>
      <li>Clique num card para selecioná-lo, arraste para movê-lo.</li>
      <li><code>Shift</code>+clique para somar à seleção.</li>
      <li>Arraste no espaço vazio para <b>selecionar por caixa</b>.</li>
      <li><code>A</code> seleciona tudo.</li>
      <li>Com vários cards selecionados, arrastar qualquer um deles move o
      conjunto inteiro.</li>
      <li>Botão do meio para deslocar a vista, roda para o zoom,
      <code>Home</code> para caber o quadro inteiro na tela.</li>
    </ul>
    <h3>Dando forma ao quadro</h3>
    <ul>
      <li><code>Ctrl+P</code> — <b>Best Fit</b>: junta tudo sem sobreposições.
      Se houver algo selecionado, só a seleção é arrumada.</li>
      <li><code>Ctrl+Alt+N</code> / <code>A</code> / <code>D</code> /
      <code>R</code> — ordenar por nome, ordem de entrada, caminho do arquivo
      ou aleatoriamente.</li>
      <li><code>Ctrl+Shift+</code>seta — alinhar a seleção pela borda de cima,
      de baixo, esquerda ou direita.</li>
      <li><b>Distribute</b> na barra lateral — espaçamento uniforme.</li>
      <li><code>Ctrl+Alt+</code>seta — deixar a seleção do mesmo tamanho (por
      altura, largura ou maior lado).</li>
    </ul>
    <h3>Grade e encaixe</h3>
    <p><code>G</code> mostra a grade, <code>Shift+G</code> encaixa nela. O
    tamanho da grade fica em Preferences.</p>
  </section>

  <section>
    <h2>5. Notas e desenho</h2>
    <h3>Notas</h3>
    <p><code>Shift+N</code> adiciona um card de texto. Dê um duplo clique para
    editar, ou edite linha por linha na barra lateral — que é também onde você
    define o tamanho da fonte, a cor do card e o alinhamento do texto.
    <b>Fit to Text</b> redimensiona o card para o que ele contém agora.</p>
    <p>As notas são apoiadas num datablock de texto do Blender, então aceitam
    várias linhas e qualquer idioma que seu sistema consiga digitar.</p>
    <h3>Desenho</h3>
    <p><code>D</code> alterna o modo de desenho. Escolha cor e espessura na
    barra lateral e desenhe direto sobre o quadro — marcações, círculos, setas,
    o que sirva para anotar uma referência. <b>Undo Line</b> remove o último
    traço, <b>Clear</b> remove todos. Os traços também podem ser selecionados,
    movidos e apagados como qualquer outro item.</p>
  </section>

  <section>
    <h2>6. Trabalhando com os cards</h2>
    <ul>
      <li><b>Opacidade</b> — arraste o controle no card, use os botões da barra
      lateral, ou <code>Ctrl+Shift+Numpad&nbsp;+</code> /
      <code>Numpad&nbsp;−</code>.</li>
      <li><b>Espelhar e girar</b> — horizontal, vertical e presets de 90°.</li>
      <li><b>Recortar</b> — ligue o modo de recorte e arraste as alças do card.
      É <b>não destrutivo</b>: o arquivo de origem fica intacto e <b>Reset</b>
      devolve a imagem inteira.</li>
      <li><b>Lock</b> num card para que ele não seja arrastado ou
      redimensionado sem querer. <b>Group</b> em cards para que clicar em um
      mova o conjunto todo.</li>
      <li><b>Bring to Front / Send to Back</b>
      (<code>Ctrl+Shift+A</code> / <code>B</code>) para cards sobrepostos.</li>
      <li><b>Solo</b> esconde tudo menos a seleção. <code>F</code> foca um
      card; as teclas de colchete pulam para o próximo e o anterior.</li>
      <li><b>Escala de cinza</b> — <code>Alt+G</code> para a seleção,
      <code>Ctrl+Alt+G</code> para o quadro inteiro, para avaliar valores.</li>
      <li><b>Export as Image</b> escreve o quadro inteiro como um arquivo
      só.</li>
    </ul>
    <p class="note">Os quatro atalhos de escala de cinza e de grade ficam todos
    no <code>G</code> (<code>G</code>, <code>Shift+G</code>,
    <code>Alt+G</code>, <code>Ctrl+Alt+G</code>). Se o quadro de repente parecer
    errado, é a primeira coisa a conferir.</p>
  </section>

  <section>
    <h2>7. Enviando um quadro para outra pessoa</h2>
    <p>O layout fica guardado no seu <code>.blend</code>, mas as imagens são
    guardadas do jeito que o Blender guarda qualquer imagem: como um
    <b>caminho para um arquivo em disco</b>. Mande o <code>.blend</code>
    sozinho e quem abrir recebe o seu layout com os <b>cards vazios</b>, porque
    os arquivos de imagem nunca saíram da sua máquina.</p>
    <p class="note"><b>Você mesmo não vai perceber isso.</b> A sua cópia dos
    arquivos continua aí, então o seu quadro parece perfeito de qualquer jeito.
    Esta é a única coisa que vale a pena guardar deste manual.</p>
    <p>Antes de enviar, aperte <b>Pack Images for Sharing</b> na barra lateral.
    Isso embute as imagens dentro do <code>.blend</code>, e aí o quadro chega
    completo. O preço é o tamanho: empacotar um conjunto grande de referências
    deixa o <code>.blend</code> mais ou menos do tamanho das próprias
    referências. Se o arquivo nunca sai da sua máquina, você não precisa
    empacotar nada.</p>
    <h3>A outra pessoa não precisa deste add-on</h3>
    <p>O arquivo abre normalmente sem o Zap Board instalado — sem erros, sem
    avisos. A pessoa simplesmente vê um Image Editor comum. Se ela editar e
    devolver, o quadro volta intacto: cards, notas, imagens empacotadas e qual
    editor era um quadro sobrevivem à ida e volta por um Blender que nunca teve
    este add-on instalado.</p>
  </section>

  <section>
    <h2>Se algo der errado</h2>
    <p>Há um botão <b>Report a Bug</b> na barra lateral do quadro e em
    Edit &rsaquo; Preferences &rsaquo; Add-ons &rsaquo; Zap Board. Ele abre um
    formulário no seu navegador já preenchido com a versão do add-on, a versão
    do Blender e o sistema operacional. Nada é enviado pelo Blender em si.</p>
  </section>
"""

CONTENT["es"] = """
  <h1>Zap Board — Manual de Usuario</h1>
  <p class="lede">Un tablero de referencias que vive dentro de tu .blend.
  Convierte cualquier Image Editor en un lienzo 2D libre, pon ahí tus
  referencias, ordénalas, anótalas — y se guarda con tu archivo. No se añade
  nada a tu escena 3D, y nada aparece en tu render.</p>

  <section>
    <h2>Versión de 30 segundos</h2>
    <ol>
      <li>Instálalo y abre un <b>Image Editor</b>.</li>
      <li>Pulsa el interruptor <b>Zap Board</b> en la cabecera de ese editor.</li>
      <li>Arrastra archivos de imagen sobre él desde tu explorador de archivos,
      o pulsa <code>Ctrl+Shift+I</code> para elegirlos desde un diálogo.</li>
      <li>Muévelas a tu gusto. Pulsa <code>Ctrl+P</code> para ordenar el tablero
      entero sin solapes.</li>
      <li>Guarda. Vuelve a abrir el archivo — el tablero está tal como lo
      dejaste.</li>
    </ol>
  </section>

  <section>
    <h2>1. Qué es</h2>
    <p>Zap Board convierte un Image Editor en un tablero sobre el que puedes
    soltar imágenes de referencia. Funciona <b>por editor</b>, así que puedes
    tener un tablero en un área mientras otro Image Editor sigue siendo un
    visor de imágenes normal.</p>
    <p><b>No toca tu escena 3D.</b> No se añade nada al outliner, no aparece
    nada en tu viewport y nada llega a tu render. El tablero son sus propios
    datos, guardados dentro del <code>.blend</code> junto con todo lo
    demás.</p>
    <p>Un tablero por archivo en esta versión.</p>
    <h3>Requisitos</h3>
    <p>Blender <b>4.5 LTS o superior</b>. Verificado en 4.5, 5.0 y 5.2.</p>
  </section>

  <section>
    <h2>2. Instalación</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions / Add-ons &rsaquo;
      el menú de la esquina &rsaquo; <b>Install from Disk…</b></li>
      <li>Elige <code>zap_board-1.0.0.zip</code>.</li>
      <li>Activa <b>Zap Board</b> en la lista.</li>
      <li>Abre un Image Editor y pulsa el interruptor <b>Zap Board</b> en su
      cabecera. También hay un botón de tablero en la cabecera del 3D Viewport
      que convierte el área actual con un solo clic.</li>
    </ol>
    <p>Pulsa <code>N</code> dentro del tablero para abrir la barra lateral,
    donde cada comando tiene además su botón.</p>
  </section>

  <section>
    <h2>3. Meter imágenes</h2>
    <p>Cuatro maneras, y todas dejan la imagen como una tarjeta en el
    tablero:</p>
    <ul>
      <li><b>Arrastrar y soltar</b> archivos de imagen directamente desde tu
      explorador de archivos al tablero.</li>
      <li><b>Import Images…</b> (<code>Ctrl+Shift+I</code>) para elegir
      archivos desde un diálogo.</li>
      <li><b>Load Folder</b> para añadir de golpe todas las imágenes de una
      carpeta.</li>
      <li><b>Pegar</b> (<code>Ctrl+V</code>) para soltar una imagen que acabas
      de copiar desde cualquier sitio.</li>
    </ul>
    <p class="note"><b>Las imágenes pegadas se incrustan al instante.</b> Una
    imagen pegada no tiene ningún archivo en disco al que apuntar, así que Zap
    Board la empaqueta dentro del <code>.blend</code> en el momento de pegarla.
    No tienes que hacer nada, y la tarjeta sobrevive a una recarga.</p>
  
    <p class="note"><b>Pegar y Reveal File son solo para Windows.</b> Ambos
    delegan en una herramienta de Windows - PowerShell para el portapapeles,
    Explorer para Reveal File. En macOS y Linux no hacen nada y lo indican.
    Usa <b>Import Images&hellip;</b> o arrastrar y soltar en lugar de pegar.</p>
  </section>

  <section>
    <h2>4. Organizar</h2>
    <h3>Mover y seleccionar</h3>
    <ul>
      <li>Haz clic en una tarjeta para seleccionarla, arrástrala para
      moverla.</li>
      <li><code>Shift</code>+clic para añadir a la selección.</li>
      <li>Arrastra sobre espacio vacío para <b>seleccionar por caja</b>.</li>
      <li><code>A</code> selecciona todo.</li>
      <li>Con varias tarjetas seleccionadas, arrastrar cualquiera de ellas
      mueve el conjunto entero.</li>
      <li>Botón central para desplazar la vista, rueda para hacer zoom,
      <code>Home</code> para encajar el tablero entero en pantalla.</li>
    </ul>
    <h3>Distribuir el tablero</h3>
    <ul>
      <li><code>Ctrl+P</code> — <b>Best Fit</b>: lo empaqueta todo sin solapes.
      Si hay algo seleccionado, solo se empaqueta la selección.</li>
      <li><code>Ctrl+Alt+N</code> / <code>A</code> / <code>D</code> /
      <code>R</code> — ordenar por nombre, orden de entrada, ruta del archivo,
      o al azar.</li>
      <li><code>Ctrl+Shift+</code>flecha — alinear la selección por su borde
      superior, inferior, izquierdo o derecho.</li>
      <li><b>Distribute</b> en la barra lateral — espaciado uniforme.</li>
      <li><code>Ctrl+Alt+</code>flecha — igualar el tamaño de la selección (por
      altura, anchura, o lado más largo).</li>
    </ul>
    <h3>Rejilla y ajuste</h3>
    <p><code>G</code> muestra la rejilla, <code>Shift+G</code> ajusta a ella.
    El tamaño de la rejilla está en Preferences.</p>
  </section>

  <section>
    <h2>5. Notas y dibujo</h2>
    <h3>Notas</h3>
    <p><code>Shift+N</code> añade una tarjeta de texto. Haz doble clic para
    editarla, o edítala línea a línea en la barra lateral — que es también
    donde ajustas el tamaño de fuente, el color de la tarjeta y la alineación
    del texto. <b>Fit to Text</b> redimensiona la tarjeta a lo que contenga en
    ese momento.</p>
    <p>Las notas se apoyan en un datablock de texto de Blender, así que admiten
    varias líneas y aceptan cualquier idioma que tu sistema pueda escribir.</p>
    <h3>Dibujo</h3>
    <p><code>D</code> activa y desactiva el modo dibujo. Elige color y grosor
    en la barra lateral y dibuja directamente sobre el tablero — marcas,
    círculos, flechas, lo que sirva para anotar una referencia. <b>Undo Line</b>
    quita el último trazo, <b>Clear</b> los quita todos. Los trazos también se
    pueden seleccionar, mover y borrar como cualquier otro elemento.</p>
  </section>

  <section>
    <h2>6. Trabajar con tarjetas</h2>
    <ul>
      <li><b>Opacidad</b> — arrastra el deslizador de la tarjeta, usa los
      botones de la barra lateral, o
      <code>Ctrl+Shift+Numpad&nbsp;+</code> /
      <code>Numpad&nbsp;−</code>.</li>
      <li><b>Voltear y rotar</b> — horizontal, vertical, y presets de 90°.</li>
      <li><b>Recortar</b> — activa el modo de recorte y arrastra los tiradores
      de una tarjeta. Es <b>no destructivo</b>: el archivo original queda
      intacto y <b>Reset</b> devuelve la imagen completa.</li>
      <li><b>Lock</b> bloquea una tarjeta para que no se pueda arrastrar ni
      redimensionar por accidente. <b>Group</b> agrupa tarjetas para que al
      hacer clic en una se mueva todo el conjunto.</li>
      <li><b>Bring to Front / Send to Back</b>
      (<code>Ctrl+Shift+A</code> / <code>B</code>) para tarjetas
      solapadas.</li>
      <li><b>Solo</b> oculta todo salvo la selección.
      <code>F</code> enfoca una tarjeta; las teclas de corchetes saltan a la
      siguiente y a la anterior.</li>
      <li><b>Escala de grises</b> — <code>Alt+G</code> para la selección,
      <code>Ctrl+Alt+G</code> para el tablero entero, para juzgar valores.</li>
      <li><b>Export as Image</b> escribe el tablero entero como un solo
      archivo.</li>
    </ul>
    <p class="note">Los cuatro atajos de escala de grises y rejilla están todos
    sobre <code>G</code> (<code>G</code>, <code>Shift+G</code>,
    <code>Alt+G</code>, <code>Ctrl+Alt+G</code>). Si de pronto el tablero se ve
    raro, esto es lo primero que conviene comprobar.</p>
  </section>

  <section>
    <h2>7. Enviar un tablero a otra persona</h2>
    <p>La disposición se guarda en tu <code>.blend</code>, pero las imágenes se
    guardan como Blender guarda cualquier imagen: como una <b>ruta a un archivo
    en disco</b>. Envía el <code>.blend</code> a secas y quien lo abra recibirá
    tu disposición con <b>las tarjetas vacías</b>, porque los archivos de imagen
    nunca salieron de tu equipo.</p>
    <p class="note"><b>Tú no vas a notarlo.</b> Tu copia de los archivos sigue
    ahí, así que tu tablero se ve bien pase lo que pase. Esto es lo único que
    de verdad conviene recordar de este manual.</p>
    <p>Antes de enviarlo, pulsa <b>Pack Images for Sharing</b> en la barra
    lateral. Incrusta las imágenes dentro del <code>.blend</code> para que el
    tablero llegue completo. Lo que se paga es tamaño: empaquetar un conjunto
    grande de referencias deja el <code>.blend</code> más o menos tan grande
    como las propias referencias. Si el archivo nunca sale de tu equipo, no
    necesitas empaquetar nada.</p>
    <h3>No necesitan este add-on</h3>
    <p>El archivo se abre con normalidad sin Zap Board instalado — sin errores
    y sin avisos. Simplemente ven un Image Editor corriente. Si lo editan y te
    lo devuelven, el tablero vuelve intacto: las tarjetas, las notas, las
    imágenes empaquetadas y qué editor era un tablero sobreviven todos a la ida
    y vuelta por un Blender que nunca tuvo este add-on instalado.</p>
  </section>

  <section>
    <h2>Si algo va mal</h2>
    <p>Hay un botón <b>Report a Bug</b> en la barra lateral del tablero y en
    Edit &rsaquo; Preferences &rsaquo; Add-ons &rsaquo; Zap Board. Abre un
    formulario en tu navegador con la versión del add-on, la versión de Blender
    y tu sistema operativo ya rellenados. No se envía nada desde el propio
    Blender.</p>
  </section>
"""

def build():
    shell = io.open(TEMPLATE, encoding="utf-8").read()

    head_end = shell.find('<main class="wrap">')
    foot_start = shell.find("<footer>")
    assert head_end > 0 and foot_start > head_end, "template shape changed"
    head = shell[:head_end]
    foot = shell[foot_start:]

    # The doctor manual carries a Collapse/Expand script for its 30-check list.
    # Zap Board has no such list, so drop that script but keep the language
    # switcher (the one that references .lang-switch).
    foot = re.sub(r"<script>\s*/\* Collapse All.*?</script>", "", foot,
                  flags=re.S)

    for suffix, code, _label in LANGS:
        if code not in CONTENT:
            print("skipped %-24s (no content yet)" % code)
            continue
        out_name = "zap-board.html" if not suffix else "zap-board.%s.html" % suffix
        h = head
        h = h.replace('<html lang="en">', '<html lang="%s">' % code)
        h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE[code], h,
                   flags=re.S)
        h = re.sub(r'(<meta name="description" content=")[^"]*(")',
                   lambda m: m.group(1) + DESC[code] + m.group(2), h)
        h = h.replace("#zap-doctor", "#zap-board")
        h = h.replace("Back to Zap Doctor", BACK[code])
        h = h.replace("ZAP SERIES / USER MANUAL", KICKER[code])
        h = h.replace("zap-doctor.html", "zap-board.html")
        for s2, _c2, _l2 in LANGS:
            if s2:
                h = h.replace("zap-doctor.%s.html" % s2, "zap-board.%s.html" % s2)
        cur_label = dict((c, l) for _s, c, l in LANGS)[code]
        h = re.sub(r'(<button type="button" class="lang-current"[^>]*>)[^<]*',
                   lambda m: m.group(1) + cur_label, h)
        h = re.sub(r'aria-selected="true"', 'aria-selected="false"', h)
        h = h.replace('><a href="%s">%s</a>' % (out_name, cur_label),
                      ' aria-selected="true"><a href="%s">%s</a>'
                      % (out_name, cur_label))

        f = foot
        f = f.replace("#zap-doctor", "#zap-board")
        f = f.replace("Back to Zap Doctor", BACK[code])
        f = re.sub(r"FARAX CREATIVE &middot; Zap series &middot; [^\n<]*",
                   FOOTNOTE[code], f)

        html = h + '<main class="wrap">\n' + CONTENT[code] + "\n</main>\n\n" + f
        path = os.path.join(REPO, out_name)
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote %-24s %8d bytes" % (out_name, len(html)))


if __name__ == "__main__":
    build()
