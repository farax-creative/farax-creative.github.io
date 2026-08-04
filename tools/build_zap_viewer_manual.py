# -*- coding: utf-8 -*-
"""Generate the five-language Zap Viewer user manual.

Reuses zap-doctor.html as the shell: the base64 font embeds, the CSS and the
language-switcher script are identical across every manual in this repo, and
duplicating ~600KB of font payload by hand is how they drift apart. Only the
<main> content, the <title>/<meta>, and the product-specific links differ.
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
    "en": "Zap Viewer — User Manual · Farax Creative",
    "ko": "Zap Viewer — 사용자 매뉴얼 · Farax Creative",
    "ja": "Zap Viewer — ユーザーマニュアル · Farax Creative",
    "pt": "Zap Viewer — Manual do Usuário · Farax Creative",
    "es": "Zap Viewer — Manual de Usuario · Farax Creative",
}

DESC = {
    "en": "User manual for Zap Viewer — a Picture-Viewer-style render history "
          "for Blender. Install, everyday use, screen reference, importing "
          "renders, and what is not in this release.",
    "ko": "Zap Viewer 사용자 매뉴얼 — 블렌더용 픽처 뷰어 스타일 렌더 히스토리. "
          "설치, 기본 사용법, 화면 설명, 렌더 불러오기, 이번 버전에서 빠진 것.",
    "ja": "Zap Viewer ユーザーマニュアル — Blender 用のピクチャービューア風レンダー"
          "履歴。インストール、基本操作、画面リファレンス、レンダーの読み込み。",
    "pt": "Manual do Zap Viewer — um histórico de renders no estilo Picture "
          "Viewer para o Blender. Instalação, uso diário e referência de tela.",
    "es": "Manual de Zap Viewer — un historial de renders al estilo Picture "
          "Viewer para Blender. Instalación, uso diario y referencia de pantalla.",
}

BACK = {
    "en": "Back to Zap Viewer", "ko": "Zap Viewer로 돌아가기",
    "ja": "Zap Viewer に戻る", "pt": "Voltar para Zap Viewer",
    "es": "Volver a Zap Viewer",
}

# The footer is lifted once from the ENGLISH doctor manual, so every localised
# string in it has to be substituted back per language -- this one was not, and
# the builder was quietly emitting "Report a Bug" in all five. The live pages
# carry the translations (they arrived by hand in 271695a), and doctor and
# output localise it too, so English everywhere is the odd one out.
#
# Note zap-board is still un-localised here; its builder has the same gap.
REPORT = {
    "en": "Report a Bug", "ko": "버그 제보",
    "ja": "バグを報告", "pt": "Relatar um erro",
    "es": "Reportar un error",
}

KICKER = {
    "en": "ZAP SERIES / USER MANUAL", "ko": "ZAP 시리즈 / 사용자 매뉴얼",
    "ja": "ZAP シリーズ / ユーザーマニュアル",
    "pt": "SÉRIE ZAP / MANUAL DO USUÁRIO",
    "es": "SERIE ZAP / MANUAL DE USUARIO",
}

FOOTNOTE = {
    "en": "FARAX CREATIVE &middot; Zap series &middot; Zap Viewer",
    "ko": "FARAX CREATIVE &middot; Zap 시리즈 &middot; Zap Viewer",
    "ja": "FARAX CREATIVE &middot; Zap シリーズ &middot; Zap Viewer",
    "pt": "FARAX CREATIVE &middot; Série Zap &middot; Zap Viewer",
    "es": "FARAX CREATIVE &middot; Serie Zap &middot; Zap Viewer",
}


def content(lang):
    """The <main> inner HTML for one language."""
    return CONTENT[lang]


# ---------------------------------------------------------------------------
# Body content. Written per language rather than machine-translated: these are
# the words a buyer reads before deciding the add-on is trustworthy.
# ---------------------------------------------------------------------------

CONTENT = {}

CONTENT["en"] = """
  <h1>Zap Viewer — User Manual</h1>
  <p class="lede">A Picture-Viewer-style render history for Blender. Every
  render you make — an F12 still or a whole animation — is saved to disk on its
  own and added to a history list you can label, replay and compare. A good
  test render is never silently overwritten.</p>

  <section>
    <h2>30-second version</h2>
    <ol>
      <li>Install it. There is nothing to configure.</li>
      <li>Render (F12). The <b>Zap Viewer</b> window opens by itself.</li>
      <li>The moment the render finishes it is <b>saved to disk and added to
      the history list</b>. No button to press.</li>
      <li>Click any entry to see it again. Pick two and <b>compare them A/B</b>.</li>
      <li>Close Blender, reopen the file — the history is still there.</li>
    </ol>
  </section>

  <section>
    <h2>Requirements</h2>
    <p>Blender <b>5.0 or newer</b>. Verified on 5.0.1, 5.1.2 and 5.2.</p>
  </section>

  <section>
    <h2>Installing</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions &rsaquo; the drop-down
      in the corner &rsaquo; <b>Install from Disk…</b></li>
      <li>Pick <code>zap_viewer-2.9.0.zip</code>.</li>
      <li>That is all. The Viewer opens on your next render.</li>
    </ol>
  </section>

  <section>
    <h2>Everyday use</h2>
    <h3>Just render</h3>
    <p>Press F12, or render an animation. The Viewer window opens and shows the
    live Render Result while Blender works, then swaps to the finished entry.
    A still becomes one <b>Still</b> entry; an animation becomes one
    <b>Sequence</b> entry — a dated folder of frames, not one entry per frame.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/history.webp" alt="" loading="lazy" /></figure>
    <h3>Look at an older render</h3>
    <p>Click it in the history list. A Still opens full size; a Sequence is
    ready to scrub and play.</p>

    <h3>Label it</h3>
    <p>Type into the entry's name field — "v3 key light warmer", whatever you
    will recognise tomorrow. Labels are saved with the .blend.</p>

    <h3>Compare two versions</h3>
    <p>Select one and press <b>Set A</b>, select another and press <b>Set B</b>,
    then <b>Compare</b>. The Viewer splits between them with a wipe you can
    drag. Zap Viewer refuses to compare two different resolutions rather than
    stretching one to fit — that would falsify what you are looking at.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/compare.webp" alt="" loading="lazy" /></figure>
    <h2>Screen reference</h2>
    <h3>The Viewer window</h3>
    <p>Zap Viewer lives in its own window, like C4D's Picture Viewer, rather than
    buried in a Properties tab. One window per session: the next render reuses
    it. The big view fills the window and the history list is docked in the
    sidebar (press <b>N</b> if it is hidden).</p>

    <h3>Transport bar</h3>
    <p>Along the bottom: jump to start, step back, play/pause, step forward,
    jump to end, loop, and playback settings. The frame field shows where you
    are; the Start/End fields narrow playback to a range.</p>
    <p><b>Playback is separate from your scene.</b> Playing a render here does
    not move the scene's playhead, so your 3D viewport does not animate along
    with it. Arrow keys scrub the viewer, Shift+arrows jump to the ends of the
    play range, and Space plays — but only inside the Viewer window.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/playback.webp" alt="" loading="lazy" /></figure>
    <h3>Tabs</h3>
    <ul>
      <li><b>History</b> — the list, with thumbnails, labels and times.</li>
      <li><b>Info</b> — resolution, render time and, for a Sequence, how long
      each frame took (see below).</li>
      <li><b>Layer</b> — what layers the shown image has, and a note about
      multilayer EXR (see "Not in this release").</li>
    </ul>

    <h3>Navigator</h3>
    <p>A small overview of the whole image in the top-left corner, with a
    rectangle showing where your current zoom sits inside it.</p>

    <h3>Refresh / Import / Remove / Clear</h3>
    <ul>
      <li><b>Refresh</b> — rescan the history folder for renders not yet listed.</li>
      <li><b>Import</b> — add renders from any other folder (see below).</li>
      <li><b>Remove</b> — take the selected entry out of the list.</li>
      <li><b>Clear</b> — empty the list.</li>
    </ul>
    <p><b>Remove and Clear do not delete your files.</b> They only stop tracking
    them. Even Remove's "Also delete files" option refuses to touch anything
    outside your history folder — an imported folder is never deleted.</p>
  </section>

  <section>
    <h2>Importing renders from a folder</h2>
    <p>Press <b>Import</b> and pick a folder to bring in renders Zap Viewer did
    not make: an older project, a render farm's output, a folder a colleague
    sent over.</p>
    <ul>
      <li><b>Nothing is copied or moved.</b> The entries point at the files
      where they already are.</li>
      <li>A flat run of numbered frames — <code>frame_0001.png</code> …
      <code>frame_0250.png</code> — comes in as <b>one Sequence</b>, not as 250
      separate stills.</li>
      <li>Importing the same folder twice adds nothing the second time.</li>
    </ul>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/import.webp" alt="" loading="lazy" /></figure>
    <h2>Per-frame render times</h2>
    <p>Select a Sequence and open the <b>Info</b> tab. Zap Viewer records how
    long each frame took while it rendered:</p>
    <pre><code>Average per frame: 6s (48 frames)

Per-frame render time
  Frame 12        41s
  Frame 7         18s
  ...
  slowest 12 of 48 frames</code></pre>
    <p>The <b>slowest</b> frames are listed first, because "which frame cost me"
    is the question this answers. It updates live as each frame lands, so you
    can watch it during a render.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/frametimes.webp" alt="" loading="lazy" /></figure>
    <h2>Where files go, and staying put</h2>
    <p>Zap Viewer keeps its files in a folder it calls the history store.
    Out of the box that is a <code>render_history</code> folder next to your
    .blend, and you can move it in Preferences &gt; Add-ons &gt; Zap Viewer:
    beside the project, one folder away from your projects with a subfolder per
    project, or anywhere you pick. You can rename the folder there too. A
    History Folder set on the scene itself still wins over all of it.</p>
    <p>Names are timestamps — <code>20260717_143022.png</code> for a still,
    <code>20260717_143530/</code> for a sequence folder.</p>
    <h3>Animation frames: copy, or point at them</h3>
    <p>Blender has already written your animation to your output path, so Zap
    Viewer does not have to write it again. <b>Keep a Copy</b> — the default —
    saves a second copy into the history store, and nothing you render later can
    change what that entry shows. <b>Use Output Files</b> leaves the frames where
    Blender put them and simply points at them: no duplicate, but rendering over
    those frames again changes what the entry shows, and the row is marked
    <b>Changed</b> when it does. An F12 still is always saved either way, because
    Blender writes no file for one.</p>
    <h3>Packing into the .blend</h3>
    <p>Set the store to <b>Pack into the .blend</b> and stills are embedded in
    the project file itself, so it travels as one file with nothing beside it.
    The .blend grows by the full size of every still and every save rewrites all
    of it, so this is for carrying a project, not for saving space. Animation
    frames cannot be packed and stay at your render output path. Packed renders
    arrive locked, because there is no file on disk to fall back on.</p>
    <p>Because every entry is a real file — or a real record of one — quitting
    Blender loses nothing. Reopen the .blend and the list is rebuilt,
    thumbnails included.</p>
    <p>Zap Viewer does not touch your render settings, Blender's own render slots
    or the sequence editor, and it never opens a window in a headless render —
    so it is safe on a farm.</p>
  </section>

  <section>
    <h2>Keeping the folder from filling up</h2>
    <p>Test renders pile up. <b>Delete After</b>, in the panel's Storage
    Settings, removes entries past a number of days you choose. It ships off, and
    0 means never.</p>
    <p>It is deliberately narrow about what it will delete. Only files Zap Viewer
    wrote into its own store are removed; your own renders — anything referenced,
    imported, or simply sitting in the folder — are dropped from the list and
    left on disk. It never touches a locked entry or the one you have selected,
    and it never runs during a background render, so a farm node opening your
    file cannot clean your history.</p>
    <p>Click the padlock on any row to keep it, or use the lock and unlock
    buttons beside the list to do the whole list at once. <b>Delete Unlocked</b>
    does the same job immediately, ignoring the age setting, and
    <b>Remove Packed</b> takes Zap Viewer's embedded renders back out of the
    .blend — only its own, unlike Blender's Purge, which cannot see them at all.
    Every one of these tells you the exact count and size first, because none of
    them can be undone.</p>
  </section>

  <section style="border-bottom:none">
    <h2>Not in this release</h2>
    <h3>Multilayer EXR history — coming soon</h3>
    <p>Renders save and replay normally, but a saved <b>still</b> is flattened
    to its combined result, so its passes are not kept in the history copy.
    Blender writes no file at all for an interactive F12 still, so Zap Viewer has
    to produce one from the Render Result, and every route available for that
    discards the layers. If you need the history copy to carry passes, render to
    single-layer EXR for now. The Layer tab says the same thing in the interface
    rather than letting you find out later.</p>

  </section>
"""

CONTENT["ko"] = """
  <h1>Zap Viewer — 사용자 매뉴얼</h1>
  <p class="lede">블렌더용 픽처 뷰어 스타일 렌더 히스토리입니다. F12 스틸이든
  애니메이션이든, 렌더가 끝나면 알아서 디스크에 저장되고 이름표를 달거나 다시
  재생하고 비교할 수 있는 목록에 추가됩니다. 잘 나온 테스트 렌더가 조용히
  덮어써지는 일이 없습니다.</p>

  <section>
    <h2>30초 요약</h2>
    <ol>
      <li>설치하면 끝입니다. 설정할 것이 없습니다.</li>
      <li>렌더(F12)하면 <b>Zap Viewer</b> 창이 저절로 열립니다.</li>
      <li>렌더가 끝나는 순간 <b>디스크에 저장되고 히스토리 목록에 추가</b>됩니다.
      버튼을 누를 필요가 없습니다.</li>
      <li>목록에서 아무거나 클릭하면 다시 볼 수 있고, 두 개를 골라
      <b>A/B 비교</b>도 됩니다.</li>
      <li>블렌더를 껐다 다시 열어도 히스토리는 그대로입니다.</li>
    </ol>
  </section>

  <section>
    <h2>요구 사항</h2>
    <p>블렌더 <b>5.0 이상</b>. 5.0.1 · 5.1.2 · 5.2에서 검증했습니다.</p>
  </section>

  <section>
    <h2>설치</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions &rsaquo; 우측 상단
      드롭다운 &rsaquo; <b>Install from Disk…</b></li>
      <li><code>zap_viewer-2.9.0.zip</code>을 선택합니다.</li>
      <li>끝입니다. 다음 렌더부터 Viewer가 열립니다.</li>
    </ol>
  </section>

  <section>
    <h2>기본 사용법</h2>
    <h3>그냥 렌더하면 됩니다</h3>
    <p>F12를 누르거나 애니메이션을 렌더하세요. Viewer 창이 열리면서 렌더가
    도는 동안 실시간 결과를 보여주고, 끝나면 저장된 항목으로 바뀝니다. 스틸은
    <b>Still</b> 항목 하나, 애니메이션은 <b>Sequence</b> 항목 하나(날짜별 프레임
    폴더)로 들어갑니다 — 프레임마다 항목이 생기지 않습니다.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/history.webp" alt="" loading="lazy" /></figure>
    <h3>예전 렌더 다시 보기</h3>
    <p>목록에서 클릭하면 됩니다. Still은 원본 크기로, Sequence는 바로 스크럽·
    재생할 수 있는 상태로 열립니다.</p>

    <h3>이름표 달기</h3>
    <p>항목의 이름 칸에 입력하세요 — "v3 키라이트 따뜻하게" 처럼 내일의 내가
    알아볼 말이면 됩니다. .blend와 함께 저장됩니다.</p>

    <h3>두 버전 비교하기</h3>
    <p>하나 고르고 <b>Set A</b>, 다른 것 고르고 <b>Set B</b>, 그리고
    <b>Compare</b>. 드래그할 수 있는 경계선으로 화면이 나뉩니다. 해상도가 다르면
    Zap Viewer는 늘려 맞추지 않고 비교를 거부합니다 — 그렇게 하면 보고 있는 것이
    거짓이 되기 때문입니다.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/compare.webp" alt="" loading="lazy" /></figure>
    <h2>화면 설명</h2>
    <h3>Viewer 창</h3>
    <p>프로퍼티 탭 구석이 아니라, C4D 픽처 뷰어처럼 <b>전용 창</b>을 씁니다.
    세션당 하나이고 다음 렌더가 같은 창을 재사용합니다. 큰 미리보기가 창을
    채우고 히스토리 목록은 사이드바에 있습니다(안 보이면 <b>N</b>).</p>

    <h3>재생 바</h3>
    <p>아래쪽에 처음으로 · 뒤로 · 재생/정지 · 앞으로 · 끝으로 · 반복 · 재생 설정이
    있습니다. 프레임 칸은 현재 위치를, Start/End 칸은 재생 구간을 정합니다.</p>
    <p><b>재생은 씬과 분리돼 있습니다.</b> 여기서 렌더를 재생해도 씬의 플레이헤드가
    움직이지 않으므로 3D 뷰포트가 같이 움직이지 않습니다. 화살표 키로 스크럽,
    Shift+화살표로 구간 처음·끝 이동, Space로 재생 — 모두 Viewer 창 안에서만
    동작합니다.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/playback.webp" alt="" loading="lazy" /></figure>
    <h3>탭</h3>
    <ul>
      <li><b>History</b> — 썸네일·이름표·시각이 있는 목록.</li>
      <li><b>Info</b> — 해상도, 렌더 시간, 그리고 Sequence면 프레임별 소요 시간
      (아래 참고).</li>
      <li><b>Layer</b> — 지금 이미지의 레이어 상태와 멀티레이어 EXR 안내
      ("이번 버전에서 빠진 것" 참고).</li>
    </ul>

    <h3>Navigator</h3>
    <p>좌측 상단에 전체 이미지 축소판이 뜨고, 지금 확대해서 보는 영역이 사각형으로
    표시됩니다.</p>

    <h3>Refresh / Import / Remove / Clear</h3>
    <ul>
      <li><b>Refresh</b> — 히스토리 폴더를 다시 훑어 목록에 없는 렌더를 찾습니다.</li>
      <li><b>Import</b> — 다른 폴더의 렌더를 불러옵니다(아래 참고).</li>
      <li><b>Remove</b> — 선택한 항목을 목록에서 뺍니다.</li>
      <li><b>Clear</b> — 목록을 비웁니다.</li>
    </ul>
    <p><b>Remove와 Clear는 파일을 지우지 않습니다.</b> 목록에서만 빠집니다.
    Remove의 "Also delete files" 옵션도 <b>히스토리 폴더 밖은 절대 건드리지
    않습니다</b> — 불러온 폴더는 삭제되지 않습니다.</p>
  </section>

  <section>
    <h2>다른 폴더에서 렌더 불러오기</h2>
    <p><b>Import</b>를 누르고 폴더를 고르면 Zap Viewer가 만들지 않은 렌더도
    목록에 들어옵니다 — 예전 프로젝트, 렌더팜 출력, 동료가 보내준 폴더 등.</p>
    <ul>
      <li><b>파일을 복사하거나 옮기지 않습니다.</b> 항목은 원래 자리의 파일을
      가리킵니다.</li>
      <li><code>frame_0001.png</code> … <code>frame_0250.png</code> 처럼 번호가
      이어지는 묶음은 <b>Sequence 한 개</b>로 들어옵니다. 스틸 250개로 쪼개지지
      않습니다.</li>
      <li>같은 폴더를 두 번 불러와도 중복으로 쌓이지 않습니다.</li>
    </ul>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/import.webp" alt="" loading="lazy" /></figure>
    <h2>프레임별 렌더 시간</h2>
    <p>Sequence를 고르고 <b>Info</b> 탭을 여세요. 렌더 중에 각 프레임이 몇 초
    걸렸는지 기록됩니다:</p>
    <pre><code>Average per frame: 6s (48 frames)

Per-frame render time
  Frame 12        41s
  Frame 7         18s
  ...
  slowest 12 of 48 frames</code></pre>
    <p><b>가장 오래 걸린 프레임부터</b> 보여줍니다 — "어느 프레임이 비쌌나"가
    이 목록이 답하는 질문이기 때문입니다. 렌더가 도는 중에도 프레임이 하나씩
    끝날 때마다 실시간으로 갱신됩니다.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/frametimes.webp" alt="" loading="lazy" /></figure>
    <h2>저장 위치와 지속성</h2>
    <p>Zap Viewer는 자기 파일을 히스토리 저장소라고 부르는 폴더에 둡니다.
    기본값은 .blend 옆의 <code>render_history</code> 폴더이고, 환경설정 &gt;
    애드온 &gt; Zap Viewer에서 옮길 수 있습니다 — 프로젝트 옆, 프로젝트와 떨어진
    한 폴더(프로젝트별 하위 폴더), 또는 원하는 아무 곳. 폴더 이름도 거기서
    바꿉니다. 씬에 직접 지정한 History Folder는 이 모든 것보다 우선합니다.</p>
    <p>이름은 타임스탬프입니다 — 스틸은 <code>20260717_143022.png</code>,
    시퀀스 폴더는 <code>20260717_143530/</code>.</p>
    <h3>애니메이션 프레임: 복사할까, 가리킬까</h3>
    <p>애니메이션은 이미 블렌더가 출력 경로에 써놨으니 Zap Viewer가 다시 쓸
    필요가 없습니다. <b>Keep a Copy</b>(기본값)는 저장소에 사본을 한 벌 더
    만들고, 그러면 나중에 무엇을 렌더하든 그 항목이 보여주는 그림은 안 바뀝니다.
    <b>Use Output Files</b>는 블렌더가 쓴 자리에 그대로 두고 가리키기만 합니다 —
    중복이 없는 대신, 같은 프레임 위에 다시 렌더하면 그 항목이 보여주는 그림도
    바뀌고 목록에 <b>Changed</b>로 표시됩니다. F12 스틸은 어느 쪽이든 항상
    저장됩니다. 블렌더가 스틸에는 파일을 안 만들기 때문입니다.</p>
    <h3>.blend 안에 넣기(패킹)</h3>
    <p>저장소를 <b>Pack into the .blend</b>로 두면 스틸이 프로젝트 파일 안에
    들어가서, 옆에 아무것도 없이 한 파일로 다닐 수 있습니다. 대신 .blend가
    스틸 크기만큼 커지고 저장할 때마다 그 전체가 다시 쓰이므로, 용량을 아끼는
    기능이 아니라 프로젝트를 들고 다니는 기능입니다. 애니메이션 프레임은 패킹할
    수 없어 출력 경로에 남습니다. 패킹된 렌더는 처음부터 잠긴 상태로 생깁니다 —
    디스크에 되돌아갈 파일이 없기 때문입니다.</p>
    <p>모든 항목이 실제 파일이거나 그 파일의 실제 기록이므로, 블렌더를 꺼도
    잃는 게 없습니다. .blend를 다시 열면 썸네일까지 포함해 목록이 복원됩니다.</p>
    <p>Zap Viewer는 렌더 설정, 블렌더 자체 렌더 슬롯, 시퀀스 에디터를 건드리지
    않고, 헤드리스 렌더에서는 창을 열지 않습니다 — 렌더팜에서 안전합니다.</p>
  </section>

  <section>
    <h2>폴더가 가득 차지 않게 하기</h2>
    <p>테스트 렌더는 쌓입니다. 패널의 Storage Settings에 있는 <b>Delete
    After</b>는 정한 일수가 지난 항목을 지웁니다. 기본은 꺼져 있고 0은 "안 함"
    입니다.</p>
    <p>무엇을 지울지에 대해서는 일부러 좁게 잡았습니다. Zap Viewer가 자기
    저장소에 쓴 파일만 지웁니다. 사용자의 렌더 — 참조한 것, 불러온 것, 그냥 그
    폴더에 있던 것 — 는 목록에서만 빠지고 디스크에는 그대로 남습니다. 잠긴
    항목과 지금 선택한 항목은 절대 건드리지 않고, 백그라운드 렌더 중에는 아예
    돌지 않으므로 렌더팜 노드가 파일을 열어도 히스토리가 청소되지 않습니다.</p>
    <p>남길 항목은 행의 자물쇠를 누르거나, 목록 옆 잠금·해제 버튼으로 한꺼번에
    처리합니다. <b>Delete Unlocked</b>는 기간과 무관하게 잠기지 않은 것을 지금
    지우고, <b>Remove Packed</b>는 .blend에 넣어둔 렌더만 다시 빼냅니다 —
    블렌더의 Purge는 이것들을 아예 보지 못하는 반면 이 버튼은 Zap Viewer 것만
    골라냅니다. 셋 다 되돌릴 수 없으므로 실행 전에 정확한 개수와 용량을
    알려줍니다.</p>
  </section>

  <section style="border-bottom:none">
    <h2>이번 버전에서 빠진 것</h2>
    <h3>멀티레이어 EXR 히스토리 — 준비 중</h3>
    <p>렌더 저장과 재생은 정상이지만, 저장된 <b>스틸</b>은 합쳐진 결과로 저장되어
    패스가 히스토리 사본에 보존되지 않습니다. 블렌더가 F12 스틸에 대해서는 파일을
    아예 쓰지 않기 때문에 Zap Viewer가 렌더 결과에서 직접 만들어야 하는데, 그
    경로들이 모두 레이어를 버립니다. 히스토리 사본에 패스가 필요하시면 당분간
    <b>단일 레이어 EXR</b>로 렌더해 주세요. Layer 탭에도 같은 안내가 표시되므로
    나중에 알게 되는 일은 없습니다.</p>

  </section>
"""

CONTENT["ja"] = """
  <h1>Zap Viewer — ユーザーマニュアル</h1>
  <p class="lede">Blender 用のピクチャービューア風レンダー履歴です。F12 の静止画
  でもアニメーションでも、レンダーが終わると自動的にディスクへ保存され、ラベル付け・
  再生・比較ができる履歴リストに追加されます。うまくいったテストレンダーが黙って
  上書きされることはありません。</p>

  <section>
    <h2>30秒でわかる</h2>
    <ol>
      <li>インストールするだけ。設定は不要です。</li>
      <li>レンダー（F12）すると <b>Zap Viewer</b> ウィンドウが自動で開きます。</li>
      <li>レンダー完了と同時に<b>ディスクへ保存され履歴に追加</b>されます。
      ボタンを押す必要はありません。</li>
      <li>履歴の項目をクリックすれば再表示。2つ選んで <b>A/B 比較</b> も可能です。</li>
      <li>Blender を終了して開き直しても履歴は残っています。</li>
    </ol>
  </section>

  <section>
    <h2>動作環境</h2>
    <p>Blender <b>5.0 以降</b>。5.0.1・5.1.2・5.2 で検証済みです。</p>
  </section>

  <section>
    <h2>インストール</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions &rsaquo; 右上の
      ドロップダウン &rsaquo; <b>Install from Disk…</b></li>
      <li><code>zap_viewer-2.9.0.zip</code> を選択します。</li>
      <li>以上です。次のレンダーから Viewer が開きます。</li>
    </ol>
  </section>

  <section>
    <h2>基本的な使い方</h2>
    <h3>レンダーするだけ</h3>
    <p>F12 を押すか、アニメーションをレンダーします。Viewer ウィンドウが開き、
    レンダー中はライブの Render Result を表示し、完了すると保存済みの項目に
    切り替わります。静止画は <b>Still</b> 項目 1つ、アニメーションは
    <b>Sequence</b> 項目 1つ（日付フォルダ）になります。フレームごとに項目が
    増えることはありません。</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/history.webp" alt="" loading="lazy" /></figure>
    <h3>過去のレンダーを見る</h3>
    <p>履歴リストでクリックします。Still は原寸で、Sequence はスクラブ・再生
    できる状態で開きます。</p>

    <h3>ラベルを付ける</h3>
    <p>項目の名前欄に入力します。「v3 キーライト暖かめ」など、明日の自分が
    わかる言葉で十分です。.blend と一緒に保存されます。</p>

    <h3>2つを比較する</h3>
    <p>1つ選んで <b>Set A</b>、別のものを選んで <b>Set B</b>、そして
    <b>Compare</b>。ドラッグできる境界線で画面が分割されます。解像度が違う場合、
    Zap Viewer は引き伸ばして合わせず比較を拒否します — それでは見ているものが
    偽りになるからです。</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/compare.webp" alt="" loading="lazy" /></figure>
    <h2>画面リファレンス</h2>
    <h3>Viewer ウィンドウ</h3>
    <p>プロパティタブの奥ではなく、C4D のピクチャービューアのように<b>専用
    ウィンドウ</b>を使います。セッションにつき 1つで、次のレンダーも同じ
    ウィンドウを再利用します。大きなプレビューがウィンドウを占め、履歴リストは
    サイドバーにあります（表示されていなければ <b>N</b>）。</p>

    <h3>再生バー</h3>
    <p>下部に、先頭へ・戻る・再生/停止・進む・末尾へ・ループ・再生設定が並びます。
    フレーム欄は現在位置、Start/End 欄は再生範囲を指定します。</p>
    <p><b>再生はシーンから独立しています。</b>ここでレンダーを再生しても
    シーンのプレイヘッドは動かないので、3D ビューポートが一緒に動くことは
    ありません。矢印キーでスクラブ、Shift+矢印で範囲の先頭・末尾へ、Space で
    再生 — いずれも Viewer ウィンドウ内でのみ動作します。</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/playback.webp" alt="" loading="lazy" /></figure>
    <h3>タブ</h3>
    <ul>
      <li><b>History</b> — サムネイル・ラベル・時刻付きのリスト。</li>
      <li><b>Info</b> — 解像度、レンダー時間、Sequence ならフレームごとの
      所要時間（下記）。</li>
      <li><b>Layer</b> — 表示中の画像のレイヤー状態と、マルチレイヤー EXR に
      関する注記（「今回のリリースに含まれないもの」参照）。</li>
    </ul>

    <h3>Navigator</h3>
    <p>左上に画像全体の縮小表示が出て、現在ズームしている範囲が矩形で示されます。</p>

    <h3>Refresh / Import / Remove / Clear</h3>
    <ul>
      <li><b>Refresh</b> — 履歴フォルダを再スキャンして未登録のレンダーを探します。</li>
      <li><b>Import</b> — 他のフォルダのレンダーを取り込みます（下記）。</li>
      <li><b>Remove</b> — 選択した項目をリストから外します。</li>
      <li><b>Clear</b> — リストを空にします。</li>
    </ul>
    <p><b>Remove と Clear はファイルを削除しません。</b>リストから外れるだけです。
    Remove の「Also delete files」オプションも<b>履歴フォルダの外には一切
    触れません</b> — 取り込んだフォルダが削除されることはありません。</p>
  </section>

  <section>
    <h2>フォルダからレンダーを取り込む</h2>
    <p><b>Import</b> を押してフォルダを選ぶと、Zap Viewer が作ったものでない
    レンダーも履歴に入ります — 昔のプロジェクト、レンダーファームの出力、
    同僚から届いたフォルダなど。</p>
    <ul>
      <li><b>コピーも移動もしません。</b>項目は元の場所のファイルを指します。</li>
      <li><code>frame_0001.png</code> … <code>frame_0250.png</code> のような
      連番のまとまりは <b>1つの Sequence</b> として入ります。250個の静止画に
      分割されることはありません。</li>
      <li>同じフォルダを 2回取り込んでも重複しません。</li>
    </ul>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/import.webp" alt="" loading="lazy" /></figure>
    <h2>フレームごとのレンダー時間</h2>
    <p>Sequence を選んで <b>Info</b> タブを開きます。レンダー中に各フレームが
    何秒かかったかが記録されています:</p>
    <pre><code>Average per frame: 6s (48 frames)

Per-frame render time
  Frame 12        41s
  Frame 7         18s
  ...
  slowest 12 of 48 frames</code></pre>
    <p><b>最も時間がかかったフレームから</b>表示されます — 「どのフレームが
    重かったか」がこのリストの答えるべき問いだからです。レンダー中も、
    フレームが終わるたびにリアルタイムで更新されます。</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/frametimes.webp" alt="" loading="lazy" /></figure>
    <h2>保存先と永続性</h2>
    <p>Zap Viewer は自分のファイルを「履歴ストア」と呼ぶフォルダーに保存します。
    初期状態では .blend の隣の <code>render_history</code> フォルダーで、
    プリファレンス &gt; アドオン &gt; Zap Viewer から移動できます —
    プロジェクトの隣、プロジェクトから離れた 1 つのフォルダー(プロジェクトごとの
    サブフォルダー)、または任意の場所。フォルダー名もそこで変更します。シーンに
    直接指定した History Folder はこれらすべてに優先します。</p>
    <p>名前はタイムスタンプです — 静止画は <code>20260717_143022.png</code>、
    シーケンスフォルダーは <code>20260717_143530/</code>。</p>
    <h3>アニメーションのフレーム: コピーするか、参照するか</h3>
    <p>アニメーションは Blender がすでに出力パスへ書き出しているので、Zap Viewer
    が書き直す必要はありません。<b>Keep a Copy</b>(初期値)はストアにもう 1 部
    コピーを保存し、あとで何をレンダーしてもその項目が示す画は変わりません。
    <b>Use Output Files</b> は Blender が置いた場所にそのまま残して参照するだけ
    です — 重複はありませんが、同じフレームに上書きレンダーするとその項目が示す
    画も変わり、行に <b>Changed</b> と表示されます。F12 の静止画はどちらでも必ず
    保存されます。Blender が静止画にはファイルを書かないためです。</p>
    <h3>.blend への埋め込み(パック)</h3>
    <p>ストアを <b>Pack into the .blend</b> にすると静止画がプロジェクトファイル
    自体に埋め込まれ、隣に何もない 1 ファイルとして持ち運べます。その分 .blend は
    静止画のサイズだけ大きくなり、保存のたびに全体が書き直されるため、容量を
    節約する機能ではなくプロジェクトを持ち運ぶための機能です。アニメーションの
    フレームはパックできず、出力パスに残ります。パックされたレンダーは最初から
    ロックされた状態で作成されます — ディスクに戻れるファイルがないからです。</p>
    <p>すべての項目が実際のファイル、またはその実際の記録なので、Blender を
    終了しても失われるものはありません。.blend を開き直せばサムネイルを含めて
    リストが再構築されます。</p>
    <p>Zap Viewer はレンダー設定、Blender 自身のレンダースロット、シーケンス
    エディターに触れず、ヘッドレスレンダーではウィンドウを開きません —
    レンダーファームでも安全です。</p>
  </section>

  <section>
    <h2>フォルダーをいっぱいにしないために</h2>
    <p>テストレンダーは溜まります。パネルの Storage Settings にある
    <b>Delete After</b> は、指定した日数を過ぎた項目を削除します。初期状態は
    オフで、0 は「しない」です。</p>
    <p>何を削除するかは意図的に狭くしてあります。Zap Viewer が自分のストアに
    書いたファイルだけを削除します。ユーザーのレンダー — 参照したもの、
    読み込んだもの、単にそのフォルダーにあったもの — はリストから外れるだけで
    ディスクには残ります。ロックされた項目と現在選択中の項目には決して触れず、
    バックグラウンドレンダー中は動作しないため、レンダーファームのノードが
    ファイルを開いても履歴が掃除されることはありません。</p>
    <p>残したい項目は行の鍵アイコンを押すか、リスト横のロック・解除ボタンで
    まとめて処理します。<b>Delete Unlocked</b> は期間に関係なくロックされて
    いないものを今すぐ削除し、<b>Remove Packed</b> は .blend に埋め込んだ
    レンダーだけを取り出します — Blender の Purge はこれらを認識できませんが、
    このボタンは Zap Viewer のものだけを選び出します。いずれも取り消せないため、
    実行前に正確な個数とサイズを表示します。</p>
  </section>

  <section style="border-bottom:none">
    <h2>今回のリリースに含まれないもの</h2>
    <h3>マルチレイヤー EXR の履歴 — 近日対応</h3>
    <p>レンダーの保存と再生は正常ですが、保存された<b>静止画</b>は合成結果に
    統合されるため、パスが履歴のコピーに残りません。Blender は対話的な F12
    静止画に対してファイルを一切書き出さないため、Zap Viewer が Render Result
    から生成する必要があり、そのために使えるどの経路もレイヤーを破棄します。
    履歴のコピーにパスが必要な場合は、当面<b>シングルレイヤー EXR</b> で
    レンダーしてください。Layer タブにも同じ案内を表示しています。</p>

  </section>
"""

CONTENT["pt"] = """
  <h1>Zap Viewer — Manual do Usuário</h1>
  <p class="lede">Um histórico de renders no estilo Picture Viewer para o
  Blender. Todo render que você faz — um still com F12 ou uma animação inteira —
  é salvo em disco sozinho e adicionado a uma lista que você pode rotular,
  reproduzir e comparar. Um bom render de teste nunca é sobrescrito em
  silêncio.</p>

  <section>
    <h2>Versão de 30 segundos</h2>
    <ol>
      <li>Instale. Não há nada para configurar.</li>
      <li>Renderize (F12). A janela <b>Zap Viewer</b> abre sozinha.</li>
      <li>Assim que o render termina, ele é <b>salvo em disco e adicionado ao
      histórico</b>. Nenhum botão para apertar.</li>
      <li>Clique em qualquer entrada para vê-la de novo. Escolha duas e
      <b>compare A/B</b>.</li>
      <li>Feche o Blender e reabra o arquivo — o histórico continua lá.</li>
    </ol>
  </section>

  <section>
    <h2>Requisitos</h2>
    <p>Blender <b>5.0 ou mais recente</b>. Verificado em 5.0.1, 5.1.2 e 5.2.</p>
  </section>

  <section>
    <h2>Instalação</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions &rsaquo; menu no
      canto &rsaquo; <b>Install from Disk…</b></li>
      <li>Escolha <code>zap_viewer-2.9.0.zip</code>.</li>
      <li>Pronto. O Viewer abre no seu próximo render.</li>
    </ol>
  </section>

  <section>
    <h2>Uso no dia a dia</h2>
    <h3>É só renderizar</h3>
    <p>Aperte F12 ou renderize uma animação. A janela do Viewer abre e mostra o
    Render Result ao vivo enquanto o Blender trabalha, depois troca para a
    entrada finalizada. Um still vira uma entrada <b>Still</b>; uma animação
    vira uma entrada <b>Sequence</b> — uma pasta de frames com data, não uma
    entrada por frame.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/history.webp" alt="" loading="lazy" /></figure>
    <h3>Ver um render antigo</h3>
    <p>Clique nele na lista. Um Still abre em tamanho real; uma Sequence já vem
    pronta para percorrer e reproduzir.</p>

    <h3>Rotular</h3>
    <p>Digite no campo de nome da entrada — "v3 key light mais quente", o que
    você vai reconhecer amanhã. Os rótulos são salvos com o .blend.</p>

    <h3>Comparar duas versões</h3>
    <p>Selecione uma e aperte <b>Set A</b>, selecione outra e aperte
    <b>Set B</b>, depois <b>Compare</b>. O Viewer se divide entre as duas com
    uma linha que você arrasta. O Zap Viewer se recusa a comparar resoluções
    diferentes em vez de esticar uma delas — isso falsificaria o que você está
    vendo.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/compare.webp" alt="" loading="lazy" /></figure>
    <h2>Referência de tela</h2>
    <h3>A janela do Viewer</h3>
    <p>O Zap Viewer vive em sua própria janela, como o Picture Viewer do C4D, em
    vez de ficar enterrado numa aba de Properties. Uma janela por sessão: o
    próximo render reaproveita a mesma. A visualização grande ocupa a janela e a
    lista fica na barra lateral (aperte <b>N</b> se estiver escondida).</p>

    <h3>Barra de reprodução</h3>
    <p>Embaixo: ir ao início, voltar um frame, play/pause, avançar um frame, ir
    ao fim, loop e ajustes de reprodução. O campo de frame mostra onde você está;
    os campos Start/End limitam a reprodução a um intervalo.</p>
    <p><b>A reprodução é separada da sua cena.</b> Reproduzir um render aqui não
    move o playhead da cena, então sua viewport 3D não anima junto. As setas
    percorrem os frames, Shift+setas pulam para as pontas do intervalo e Space
    reproduz — mas só dentro da janela do Viewer.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/playback.webp" alt="" loading="lazy" /></figure>
    <h3>Abas</h3>
    <ul>
      <li><b>History</b> — a lista, com miniaturas, rótulos e horários.</li>
      <li><b>Info</b> — resolução, tempo de render e, para uma Sequence, quanto
      cada frame levou (veja abaixo).</li>
      <li><b>Layer</b> — quais camadas a imagem tem, e uma nota sobre EXR
      multilayer (veja "Fora desta versão").</li>
    </ul>

    <h3>Navigator</h3>
    <p>Uma miniatura da imagem inteira no canto superior esquerdo, com um
    retângulo mostrando onde seu zoom atual está dentro dela.</p>

    <h3>Refresh / Import / Remove / Clear</h3>
    <ul>
      <li><b>Refresh</b> — revarre a pasta do histórico atrás de renders ainda
      não listados.</li>
      <li><b>Import</b> — adiciona renders de qualquer outra pasta (veja abaixo).</li>
      <li><b>Remove</b> — tira a entrada selecionada da lista.</li>
      <li><b>Clear</b> — esvazia a lista.</li>
    </ul>
    <p><b>Remove e Clear não apagam seus arquivos.</b> Eles só param de
    rastreá-los. Até a opção "Also delete files" do Remove se recusa a tocar em
    qualquer coisa fora da sua pasta de histórico — uma pasta importada nunca é
    apagada.</p>
  </section>

  <section>
    <h2>Importar renders de uma pasta</h2>
    <p>Aperte <b>Import</b> e escolha uma pasta para trazer renders que o Zap
    Slots não fez: um projeto antigo, a saída de uma render farm, uma pasta que
    um colega mandou.</p>
    <ul>
      <li><b>Nada é copiado ou movido.</b> As entradas apontam para os arquivos
      onde eles já estão.</li>
      <li>Uma sequência numerada — <code>frame_0001.png</code> …
      <code>frame_0250.png</code> — entra como <b>uma Sequence</b>, não como 250
      stills separados.</li>
      <li>Importar a mesma pasta duas vezes não adiciona nada na segunda.</li>
    </ul>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/import.webp" alt="" loading="lazy" /></figure>
    <h2>Tempo de render por frame</h2>
    <p>Selecione uma Sequence e abra a aba <b>Info</b>. O Zap Viewer registra
    quanto cada frame levou enquanto renderizava:</p>
    <pre><code>Average per frame: 6s (48 frames)

Per-frame render time
  Frame 12        41s
  Frame 7         18s
  ...
  slowest 12 of 48 frames</code></pre>
    <p>Os frames <b>mais lentos</b> vêm primeiro, porque "qual frame me custou
    caro" é a pergunta que isso responde. Atualiza ao vivo conforme cada frame
    fica pronto, então dá para acompanhar durante o render.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/frametimes.webp" alt="" loading="lazy" /></figure>
    <h2>Onde os arquivos ficam, e permanência</h2>
    <p>O Zap Viewer guarda seus arquivos numa pasta que ele chama de repositório
    de histórico. De início é uma pasta <code>render_history</code> ao lado do
    seu .blend, e você pode movê-la em Preferências &gt; Add-ons &gt; Zap Viewer:
    ao lado do projeto, numa pasta longe dos seus projetos com uma subpasta por
    projeto, ou onde você quiser. O nome da pasta também se muda ali. Um History
    Folder definido na própria cena continua tendo prioridade sobre tudo
    isso.</p>
    <p>Os nomes são timestamps — <code>20260717_143022.png</code> para um still,
    <code>20260717_143530/</code> para uma pasta de sequência.</p>
    <h3>Frames de animação: copiar ou apontar</h3>
    <p>O Blender já escreveu sua animação no caminho de saída, então o Zap Viewer
    não precisa escrevê-la de novo. <b>Keep a Copy</b> — o padrão — salva uma
    segunda cópia no repositório, e nada que você renderize depois muda o que
    aquela entrada mostra. <b>Use Output Files</b> deixa os frames onde o Blender
    os colocou e apenas aponta para eles: sem duplicata, mas renderizar por cima
    daqueles frames muda o que a entrada mostra, e a linha é marcada como
    <b>Changed</b> quando isso acontece. Um still de F12 é sempre salvo de
    qualquer forma, porque o Blender não escreve arquivo nenhum para um.</p>
    <h3>Empacotar no .blend</h3>
    <p>Defina o repositório como <b>Pack into the .blend</b> e os stills passam a
    ficar embutidos no próprio arquivo do projeto, que viaja como um arquivo só,
    sem nada ao lado. O .blend cresce o tamanho inteiro de cada still e cada
    salvamento reescreve tudo, então isso serve para carregar um projeto, não
    para economizar espaço. Frames de animação não podem ser empacotados e ficam
    no seu caminho de saída. Renders empacotados já chegam bloqueados, porque não
    há arquivo em disco para onde voltar.</p>
    <p>Como toda entrada é um arquivo real — ou um registro real de um —, sair do
    Blender não perde nada. Reabra o .blend e a lista é reconstruída, miniaturas
    incluídas.</p>
    <p>O Zap Viewer não mexe nas suas configurações de render, nos render slots
    do próprio Blender nem no sequence editor, e nunca abre uma janela num render
    headless — então é seguro numa farm.</p>
  </section>

  <section>
    <h2>Evitando que a pasta encha</h2>
    <p>Renders de teste se acumulam. O <b>Delete After</b>, em Storage Settings
    no painel, remove entradas passados os dias que você escolher. Vem desligado,
    e 0 significa nunca.</p>
    <p>Ele é deliberadamente restrito sobre o que apaga. Só remove arquivos que o
    Zap Viewer escreveu no próprio repositório; os seus renders — qualquer coisa
    referenciada, importada, ou simplesmente presente na pasta — saem da lista e
    ficam no disco. Nunca toca numa entrada bloqueada nem na que você tem
    selecionada, e nunca roda durante um render em segundo plano, então um nó de
    farm abrindo seu arquivo não limpa seu histórico.</p>
    <p>Clique no cadeado de qualquer linha para mantê-la, ou use os botões de
    bloquear e desbloquear ao lado da lista para fazer tudo de uma vez.
    <b>Delete Unlocked</b> faz o mesmo imediatamente, ignorando o prazo, e
    <b>Remove Packed</b> tira do .blend os renders embutidos pelo Zap Viewer —
    só os dele, ao contrário do Purge do Blender, que não os enxerga. Todos
    informam a contagem e o tamanho exatos antes, porque nenhum pode ser
    desfeito.</p>
  </section>

  <section style="border-bottom:none">
    <h2>Fora desta versão</h2>
    <h3>Histórico de EXR multilayer — em breve</h3>
    <p>Os renders salvam e reproduzem normalmente, mas um <b>still</b> salvo é
    achatado no resultado combinado, então seus passes não ficam na cópia do
    histórico. O Blender não escreve arquivo nenhum para um still F12
    interativo, então o Zap Viewer precisa produzir um a partir do Render Result,
    e todo caminho disponível para isso descarta as camadas. Se você precisa que
    a cópia do histórico carregue os passes, renderize em EXR de camada única
    por enquanto. A aba Layer diz o mesmo na interface, em vez de deixar você
    descobrir depois.</p>

  </section>
"""

CONTENT["es"] = """
  <h1>Zap Viewer — Manual de Usuario</h1>
  <p class="lede">Un historial de renders al estilo Picture Viewer para Blender.
  Cada render que haces — un still con F12 o una animación entera — se guarda en
  disco por su cuenta y se añade a una lista que puedes etiquetar, reproducir y
  comparar. Un buen render de prueba nunca se sobrescribe en silencio.</p>

  <section>
    <h2>Versión de 30 segundos</h2>
    <ol>
      <li>Instálalo. No hay nada que configurar.</li>
      <li>Renderiza (F12). La ventana <b>Zap Viewer</b> se abre sola.</li>
      <li>En cuanto el render termina, queda <b>guardado en disco y añadido al
      historial</b>. Ningún botón que pulsar.</li>
      <li>Haz clic en cualquier entrada para volver a verla. Elige dos y
      <b>compáralas A/B</b>.</li>
      <li>Cierra Blender y reabre el archivo — el historial sigue ahí.</li>
    </ol>
  </section>

  <section>
    <h2>Requisitos</h2>
    <p>Blender <b>5.0 o superior</b>. Verificado en 5.0.1, 5.1.2 y 5.2.</p>
  </section>

  <section>
    <h2>Instalación</h2>
    <ol>
      <li>Edit &rsaquo; Preferences &rsaquo; Get Extensions &rsaquo; el menú de
      la esquina &rsaquo; <b>Install from Disk…</b></li>
      <li>Elige <code>zap_viewer-2.9.0.zip</code>.</li>
      <li>Ya está. El Viewer se abre en tu siguiente render.</li>
    </ol>
  </section>

  <section>
    <h2>Uso diario</h2>
    <h3>Solo renderiza</h3>
    <p>Pulsa F12 o renderiza una animación. La ventana del Viewer se abre y
    muestra el Render Result en vivo mientras Blender trabaja, y luego cambia a
    la entrada terminada. Un still se convierte en una entrada <b>Still</b>; una
    animación en una entrada <b>Sequence</b> — una carpeta de frames con fecha,
    no una entrada por frame.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/history.webp" alt="" loading="lazy" /></figure>
    <h3>Ver un render antiguo</h3>
    <p>Haz clic en él en la lista. Un Still se abre a tamaño completo; una
    Sequence llega lista para recorrer y reproducir.</p>

    <h3>Etiquetar</h3>
    <p>Escribe en el campo de nombre de la entrada — "v3 key light más cálida",
    lo que vayas a reconocer mañana. Las etiquetas se guardan con el .blend.</p>

    <h3>Comparar dos versiones</h3>
    <p>Selecciona una y pulsa <b>Set A</b>, selecciona otra y pulsa <b>Set B</b>,
    y luego <b>Compare</b>. El Viewer se divide entre ambas con una línea que
    puedes arrastrar. Zap Viewer se niega a comparar resoluciones distintas en
    lugar de estirar una — eso falsearía lo que estás viendo.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/compare.webp" alt="" loading="lazy" /></figure>
    <h2>Referencia de pantalla</h2>
    <h3>La ventana del Viewer</h3>
    <p>Zap Viewer vive en su propia ventana, como el Picture Viewer de C4D, en
    lugar de estar enterrado en una pestaña de Properties. Una ventana por
    sesión: el siguiente render reutiliza la misma. La vista grande ocupa la
    ventana y la lista queda en la barra lateral (pulsa <b>N</b> si está
    oculta).</p>

    <h3>Barra de reproducción</h3>
    <p>Abajo: ir al inicio, retroceder un frame, play/pausa, avanzar un frame,
    ir al final, bucle y ajustes de reproducción. El campo de frame indica dónde
    estás; los campos Start/End limitan la reproducción a un rango.</p>
    <p><b>La reproducción está separada de tu escena.</b> Reproducir un render
    aquí no mueve el playhead de la escena, así que tu viewport 3D no se anima
    con él. Las flechas recorren los frames, Shift+flechas saltan a los extremos
    del rango y Space reproduce — pero solo dentro de la ventana del Viewer.</p>

    <figure class="demo"><img src="../assets/img/zap-viewer/demos/playback.webp" alt="" loading="lazy" /></figure>
    <h3>Pestañas</h3>
    <ul>
      <li><b>History</b> — la lista, con miniaturas, etiquetas y horas.</li>
      <li><b>Info</b> — resolución, tiempo de render y, para una Sequence,
      cuánto tardó cada frame (ver abajo).</li>
      <li><b>Layer</b> — qué capas tiene la imagen mostrada, y una nota sobre
      EXR multicapa (ver "Fuera de esta versión").</li>
    </ul>

    <h3>Navigator</h3>
    <p>Una vista reducida de la imagen completa en la esquina superior
    izquierda, con un rectángulo que muestra dónde está tu zoom actual.</p>

    <h3>Refresh / Import / Remove / Clear</h3>
    <ul>
      <li><b>Refresh</b> — vuelve a escanear la carpeta del historial buscando
      renders que aún no están en la lista.</li>
      <li><b>Import</b> — añade renders desde cualquier otra carpeta (ver abajo).</li>
      <li><b>Remove</b> — saca la entrada seleccionada de la lista.</li>
      <li><b>Clear</b> — vacía la lista.</li>
    </ul>
    <p><b>Remove y Clear no borran tus archivos.</b> Solo dejan de seguirlos.
    Incluso la opción "Also delete files" de Remove se niega a tocar nada fuera
    de tu carpeta de historial — una carpeta importada nunca se borra.</p>
  </section>

  <section>
    <h2>Importar renders desde una carpeta</h2>
    <p>Pulsa <b>Import</b> y elige una carpeta para traer renders que Zap Viewer
    no hizo: un proyecto antiguo, la salida de una render farm, una carpeta que
    te mandó un compañero.</p>
    <ul>
      <li><b>No se copia ni se mueve nada.</b> Las entradas apuntan a los
      archivos donde ya están.</li>
      <li>Una serie numerada — <code>frame_0001.png</code> …
      <code>frame_0250.png</code> — entra como <b>una Sequence</b>, no como 250
      stills sueltos.</li>
      <li>Importar la misma carpeta dos veces no añade nada la segunda vez.</li>
    </ul>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/import.webp" alt="" loading="lazy" /></figure>
    <h2>Tiempo de render por frame</h2>
    <p>Selecciona una Sequence y abre la pestaña <b>Info</b>. Zap Viewer registra
    cuánto tardó cada frame mientras se renderizaba:</p>
    <pre><code>Average per frame: 6s (48 frames)

Per-frame render time
  Frame 12        41s
  Frame 7         18s
  ...
  slowest 12 of 48 frames</code></pre>
    <p>Los frames <b>más lentos</b> aparecen primero, porque "qué frame me
    costó caro" es la pregunta que esto responde. Se actualiza en vivo según
    cada frame termina, así que puedes seguirlo durante el render.</p>
  </section>

  <section>
    <figure class="demo"><img src="../assets/img/zap-viewer/demos/frametimes.webp" alt="" loading="lazy" /></figure>
    <h2>Dónde van los archivos, y permanencia</h2>
    <p>Zap Viewer guarda sus archivos en una carpeta que llama el almacén de
    historial. De entrada es una carpeta <code>render_history</code> junto a tu
    .blend, y puedes moverla en Preferencias &gt; Add-ons &gt; Zap Viewer: junto
    al proyecto, en una carpeta lejos de tus proyectos con una subcarpeta por
    proyecto, o donde tú elijas. El nombre de la carpeta también se cambia ahí.
    Un History Folder definido en la propia escena sigue teniendo prioridad sobre
    todo esto.</p>
    <p>Los nombres son marcas de tiempo — <code>20260717_143022.png</code> para
    un still, <code>20260717_143530/</code> para una carpeta de secuencia.</p>
    <h3>Frames de animación: copiar o apuntar</h3>
    <p>Blender ya ha escrito tu animación en tu ruta de salida, así que Zap
    Viewer no tiene que escribirla otra vez. <b>Keep a Copy</b> — la opción por
    defecto — guarda una segunda copia en el almacén, y nada que renderices
    después cambia lo que muestra esa entrada. <b>Use Output Files</b> deja los
    frames donde Blender los puso y simplemente apunta a ellos: sin duplicado,
    pero volver a renderizar sobre esos frames cambia lo que muestra la entrada,
    y la fila se marca como <b>Changed</b> cuando ocurre. Un still de F12 se
    guarda siempre en cualquier caso, porque Blender no escribe ningún archivo
    para uno.</p>
    <h3>Empaquetar en el .blend</h3>
    <p>Pon el almacén en <b>Pack into the .blend</b> y los stills quedan
    incrustados en el propio archivo del proyecto, que viaja como un solo archivo
    sin nada al lado. El .blend crece el tamaño completo de cada still y cada
    guardado reescribe todo, así que esto sirve para llevarte un proyecto, no
    para ahorrar espacio. Los frames de animación no se pueden empaquetar y se
    quedan en tu ruta de salida. Los renders empaquetados llegan bloqueados,
    porque no hay archivo en disco al que volver.</p>
    <p>Como cada entrada es un archivo real — o un registro real de uno —, salir
    de Blender no pierde nada. Reabre el .blend y la lista se reconstruye,
    miniaturas incluidas.</p>
    <p>Zap Viewer no toca tus ajustes de render, los render slots del propio
    Blender ni el sequence editor, y nunca abre una ventana en un render headless
    — así que es seguro en una farm.</p>
  </section>

  <section>
    <h2>Evitar que la carpeta se llene</h2>
    <p>Los renders de prueba se acumulan. <b>Delete After</b>, en Storage
    Settings del panel, elimina entradas pasados los días que elijas. Viene
    desactivado, y 0 significa nunca.</p>
    <p>Es deliberadamente estricto con lo que borra. Solo elimina archivos que
    Zap Viewer escribió en su propio almacén; tus renders — cualquier cosa
    referenciada, importada o que simplemente estuviera en la carpeta — salen de
    la lista y se quedan en el disco. Nunca toca una entrada bloqueada ni la que
    tienes seleccionada, y nunca se ejecuta durante un render en segundo plano,
    así que un nodo de farm abriendo tu archivo no limpia tu historial.</p>
    <p>Pulsa el candado de cualquier fila para conservarla, o usa los botones de
    bloquear y desbloquear junto a la lista para hacerlo con toda la lista.
    <b>Delete Unlocked</b> hace lo mismo al momento, ignorando el plazo, y
    <b>Remove Packed</b> saca del .blend los renders incrustados por Zap
    Viewer — solo los suyos, a diferencia del Purge de Blender, que no llega a
    verlos. Los tres te dicen antes la cantidad y el tamaño exactos, porque
    ninguno se puede deshacer.</p>
  </section>

  <section style="border-bottom:none">
    <h2>Fuera de esta versión</h2>
    <h3>Historial de EXR multicapa — próximamente</h3>
    <p>Los renders se guardan y reproducen con normalidad, pero un <b>still</b>
    guardado se aplana a su resultado combinado, así que sus passes no quedan en
    la copia del historial. Blender no escribe ningún archivo para un still F12
    interactivo, así que Zap Viewer tiene que producir uno a partir del Render
    Result, y todas las rutas disponibles para eso descartan las capas. Si
    necesitas que la copia del historial lleve los passes, renderiza a EXR de
    una sola capa por ahora. La pestaña Layer dice lo mismo en la interfaz, en
    vez de dejar que lo descubras después.</p>

  </section>
"""


def build():
    shell = io.open(TEMPLATE, encoding="utf-8").read()

    head_end = shell.find("<main class=\"wrap\">")
    foot_start = shell.find("<footer>")
    assert head_end > 0 and foot_start > head_end, "template shape changed"
    head = shell[:head_end]
    foot = shell[foot_start:]

    # The doctor manual carries a Collapse/Expand script for its 30-check list.
    # Zap Viewer has no such list, so drop that script but keep the language
    # switcher (the one that references .lang-switch).
    foot = re.sub(r"<script>\s*/\* Collapse All.*?</script>", "", foot,
                  flags=re.S)

    for suffix, code, _label in LANGS:
        out_name = "zap-viewer.html" if not suffix else "zap-viewer.%s.html" % suffix
        h = head
        h = h.replace('<html lang="en">', '<html lang="%s">' % code)
        h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE[code], h,
                   flags=re.S)
        h = re.sub(r'(<meta name="description" content=")[^"]*(")',
                   lambda m: m.group(1) + DESC[code] + m.group(2), h)
        h = h.replace("#zap-doctor", "#zap-viewer")
        h = h.replace("Back to Zap Doctor", BACK[code])
        h = h.replace("ZAP SERIES / USER MANUAL", KICKER[code])
        # language switcher: point at zap-viewer files and mark the current one
        h = h.replace("zap-doctor.html", "zap-viewer.html")
        for s2, c2, _l2 in LANGS:
            if s2:
                h = h.replace("zap-doctor.%s.html" % s2, "zap-viewer.%s.html" % s2)
        cur_label = dict((c, l) for _s, c, l in LANGS)[code]
        h = re.sub(r'(<button type="button" class="lang-current"[^>]*>)[^<]*',
                   lambda m: m.group(1) + cur_label, h)
        h = re.sub(r'aria-selected="true"', 'aria-selected="false"', h)
        h = h.replace('><a href="%s">%s</a>' % (out_name, cur_label),
                      ' aria-selected="true"><a href="%s">%s</a>'
                      % (out_name, cur_label))

        f = foot
        f = f.replace("#zap-doctor", "#zap-viewer")
        f = f.replace("Back to Zap Doctor", BACK[code])
        # The report page fills its form from this parameter. The template is
        # the doctor manual, so the name arrives wrong and nothing complains --
        # a mismatched product lands in the form as a blank field, not an error.
        f = f.replace("report/?product=Zap%20Doctor",
                      "report/?product=Zap%20Viewer")
        # ...and the link's visible text, which the English footer carries.
        f = re.sub(r'(report/\?product=Zap%20Viewer">)[^<]*',
                   lambda m: m.group(1) + REPORT[code], f)
        f = re.sub(r"FARAX CREATIVE &middot; Zap series &middot; [^\n<]*",
                   FOOTNOTE[code], f)

        html = h + '<main class="wrap">\n' + CONTENT[code] + "\n</main>\n\n" + f
        path = os.path.join(REPO, out_name)
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote %-24s %8d bytes" % (out_name, len(html)))


if __name__ == "__main__":
    build()
