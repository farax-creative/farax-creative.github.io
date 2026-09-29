# Zap Board Superhive 상세페이지 — 설계안 (2026-09-30 개정)

방향: **Prompt Motion 상세페이지와 같은 롱폼 디테일 페이지.** 카탈로그(작은 타일
그리드)가 아니라, 큰 미디어 + 짧은 산문이 리듬을 타고 위→아래로 읽히는 페이지.
전부 산세리프, 굵기 한 단계 올림(v005), 영상은 콘텐츠 폭을 꽉 채운다.

기준 파일: `zap-board/superhive.html` (승인되면 나머지 세 제품이 이 흐름을 복제).
참고 원본: `60_website/live/.claude/worktrees/pm-superhive/prompt-motion/superhive.html`.

## 왜 v006(카탈로그)이 반려됐나
아이콘+한 줄 카드 그리드 + 체크 표 + 가격 칩 = "상세페이지가 아니라 카탈로그"라는
평. → 그리드·표·칩을 버리고 PM식 섹션(라벨 + h2 + 산문 + 큰 미디어)로 다시 짰다.

## 구조 (위→아래) — 이게 표준 흐름
1. **릴리스 바** — 점 + 제품명·버전 + 에디션(Free & Pro) + changelog 링크(새 탭). 쿠폰 없음.
2. **히어로** — 킥커 + 제품명(Farax Display) + 한 줄 약속을 편 리드 + `hero.mp4`(콘텐츠 폭 꽉).
3. **문제 (01)** — 미디어 없이 2줄. "레퍼런스가 다른 창에 산다."
4. **해결 장면 (02)** — "끌어다 놓고, 정렬하고, 계속 작업." + 큰 영상(`solution.mp4`, 실제 드래그 데모).
5. **핵심 기능 4 (03–06)** — 각 = 라벨 + h2 + 1–2줄 + **큰 영상**:
   compare(`compare.mp4`) · colour Pro(`colour.mp4`) · adjust Pro(`adjust.mp4`) · send-to-3D Pro(`send3d.mp4`, 세운 앞뷰).
6. **Also in 2.0 (07)** — 한 섹션 안에 소제목+한 줄+미디어 서브블록을 쌓는다(그리드 아님):
   주석(`annotate.mp4`) · 보드 여러 개(`boards.mp4`) · URL 붙여넣기(`urlpaste.mp4`) ·
   그룹 프레임(`frames_two.png`) · 동영상 카드 Pro(`video_card.png`).
7. **Free / Pro (08)** — 표 없이 짧은 두 문단(패널 2개). 가격 자리표시자 $0 / $5 one-time.
8. **요구사항 (09)** 3줄 · **FAQ (10)** `<details>` 3개 · **CTA** · 푸터.

## 미디어 = 이 페이지의 핵심
- 기능마다 **큰 영상 하나**. 작은 타일 금지. `.media`는 콘텐츠 열(`.col` 640px) 폭을 꽉 채운다.
- 영상은 **before→after 진짜 스크린샷 2장을 이징 크로스페이드**한 루프(핑퐁이라 이음매 없이 반복).
  실제 상태만 캡처하고 그 사이 보간만 합성 — zap_board 데모 관습 그대로.
- 규격: 1280 wide, H.264 `yuv420p` `+faststart`, `<video autoplay muted loop playsinline>`,
  히어로만 `preload="auto"` 나머지 `preload="metadata"`. 스틸은 PNG.
- 스토어 리치텍스트가 `<video>`·`<script>`·`<style>`를 지우므로 **영상은 이 iframe 페이지 안에서만** 산다.
- mp4 원본 항상 보존. 갤러리용은 별도 2000×1000 WebP(시리즈 규칙).
- 캡처 하네스: `zbcap/capture_v2videos.py`(before/after 스틸) + `assemble_videos.py`(PIL 이징 + ffmpeg).
  실제 데모 컷은 `assets/store/demos/01–10.mp4`에서 다른 애드온 안 보이는 걸로 골라 1280 재인코딩.

## 폰트
- `--sans: -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`
- 큰 제목(h1·h2)만 브랜드 폰트 `@font-face 'Farax Display'`,
  `src: url('https://farax-creative.github.io/assets/fonts/farax-display.ttf')` (전체 URL, 단일 굵기 400).
- **굵기(v005 피드백)**: 본문 500 / 리드 600 / 소제목·라벨·강조 700 / 가격 800. 세리프 금지.
  `--mono`는 릴리스 바·킥커·라벨·푸터의 라벨성 텍스트에만.

## 색 토큰 (`:root`)
```
--bg #0B0D10  --panel #11161B  --bar #050506
--cream #F4EBDD  --body rgba(244,235,221,.86)  --dim rgba(244,235,221,.5)  --line rgba(244,235,221,.13)
--zap #FFC828   (브랜드 옐로 — 라벨 번호·Pro 배지·강조·링크에만)
```

## 섹션 해부 (복제 단위)
- `.wrap{max-width:900px}` 안에 `.col{max-width:640px}`. 섹션은 `.sec{padding:34px 0 50px}`.
- 라벨: `.label`(mono, `<b>01</b>` 옐로 번호 + 이름, Pro면 `<span class="pro">Pro</span>`), 위쪽 `--line` 구분선.
- 그 아래 h2(Farax Display) + 산문 `<p>`(있으면) + `.media`(영상/스틸, 라운드 10px + 그림자).
- 문제 섹션처럼 미디어 없는 텍스트 섹션을 사이사이 넣어 호흡을 준다.
- FAQ는 네이티브 `<details>/<summary>`(스토어가 `<script>`를 지워도 동작).

## 규칙(불변)
- 가로 스크롤 금지(390·1440 실측), 폰트 전체 URL, 허브에는 폴더째(영상 포함) 올리고 설명 한글.
- Gumroad·테스트 개수·"네트워크 없음" 단정 문구 금지(URL 붙여넣기 1건은 "요청할 때만 온라인"으로 표기).
- 가격은 확정 답 받은 값(현재 $0 / $5 자리표시자).
- 임베드: 스토어가 iframe 높이를 못 맞추므로 390·1440 실측 후
  `height: clamp(min, calc(A + B*vw), max)`로 고정, 라이브에서 한 번 확인.
