# Zap Board Superhive 상세페이지 — 설계안 (2026-09-30 R3 개정)

방향: **Farax 메인 사이트와 같은 브랜드로 읽히되 더 현대적·정제된 하이엔드 제품
상세페이지.** 큰 미디어 + 짧은 산문이 위→아래로 리듬을 타는 롱폼(카탈로그 아님).
전부 산세리프, 여백 넉넉히, 타입 스케일은 타이트하게.

기준 파일: `zap-board/superhive.html` (승인되면 나머지 세 제품이 이 흐름을 복제).
브랜드 원본: 라이브 `farax-creative.github.io`의 `index.html` / `zap-board.html`.

## R3에서 바뀐 것 (v008 피드백)
1. **영상**: 새로 합성한 크로스페이드 4종(send3d·annotate·boards·urlpaste)이 "다 어색
   하다" → **전부 버림.** 새 블렌더 캡처 금지. **실존 진짜 푸티지만 사용.**
2. **스타일**: "아직 Farax 사이트 느낌과 멀다" → 사이트의 브랜드 언어를 실제로 반영
   (아래 "브랜드 언어" 참고). 큰 제목의 Farax Display 남용을 멈추고 사이트처럼
   **굵은 시스템 산세 + 타이트 트래킹**으로. 01–10 mono 번호 라벨 폐기.

## 브랜드 언어 (Farax 사이트에서 가져온 것)
- **점 그리드 배경**: `radial-gradient(circle at 1px 1px, rgba(244,235,221,.05) 1px,
  transparent 0)` 26px — 페이지 전체에 은은하게(시그니처).
- **큰 제목 = 시스템 산세 700 + `letter-spacing:-.03em`**(타이트). Farax Display는
  **히어로 제품명 한 곳에만**.
- **미디어 = 라운드 16px + 부드러운 그림자 + 아주 옅은 웜 글로우**(옐로 링/글로우 절제).
- **필 배지**(`border-radius:999px`) — 히어로의 "● Free & Pro · Blender 4.5+", CTA 필.
- **아이브로우는 절제**: mono 번호 대신 짧은 대문자 옐로 태그, 섹션 상단 헤어라인만.
- 색 토큰은 사이트 그대로: `--bg #0B0D10`, `--zap #FFC828`, `--cream #F4EBDD`,
  `--line rgba(244,235,221,.11)`. `--ease cubic-bezier(.16,.84,.28,1)`.

## 구조 (위→아래)
1. **릴리스 바** — 점 + 제품명·버전 + 에디션(Free & Pro) + changelog(새 탭). 쿠폰 없음.
2. **히어로** — 필 배지 + 제품명(Farax Display) + 한 줄 약속 + 큰 미디어(`import-folder.webp`).
3. **문제** — 미디어 없이 2줄.
4. **해결 장면** — "Drop it. Arrange it." + `solution.mp4`(실제 드래그 데모, 유일하게 남긴 영상).
5. **핵심 기능 4** — 각 = 아이브로우 + h2 + 1–2줄 + 큰 미디어(전부 실존 애니 WebP):
   Arrange(`arrange.webp`) · Move(`move.webp`) · Mark up(`draw.webp`) · Compare(`opacity.webp`).
6. **Also in 2.0** — 그룹 프레임(`frames_two.png`) · 동영상 카드 Pro(`video_card.png`) +
   **Pro 롤업 목록**(팔레트/조정/Send-to-3D/템플릿·내보내기 — 영상 없이 한 줄씩).
7. **Pricing** — 표 없이 짧은 두 패널. 자리표시자 $0 / $5 one-time.
8. **요구사항** 3줄 · **FAQ** `<details>` 3개 · **CTA**(필) · 푸터.

## 미디어 = 실존 진짜 푸티지만 (R3 규칙)
페이지가 참조하는 미디어를 전부 `zap-board/media/`에 두어 자체 완결(허브 폴더 업로드용).

| 파일 | 출처 | 규격 |
|---|---|---|
| `import-folder.webp` `arrange.webp` `move.webp` `draw.webp` `opacity.webp` | 라이브 사이트 `assets/img/zap-board/*.webp`(실제 데모 녹화) | 2000×1000 애니 WebP |
| `solution.mp4` | 기존 실제 01_Move 데모 재인코딩 | 1280×720 H.264 |
| `frames_two.png` `video_card.png` | 실제 UI 스크린샷 | 1280×756 PNG |

- **버린 것**: `hero/compare/colour/adjust/send3d/annotate/boards/urlpaste.mp4`(전부 합성).
- **실존 푸티지가 없는 Pro 기능**(팔레트/조정/Send-to-3D/템플릿·내보내기)은 영상 대신
  **한 줄 설명**으로만 다룬다(Also in 2.0 롤업). 억지 합성 금지.
- 작은 460×380 데모는 열 폭(660)에서 흐려져 제외 — 큰 2000×1000 WebP만 크게 쓴다.
- `<video>`에는 `width`/`height` 유지. WebP는 `<img>` + `width`/`height`(레이아웃 시프트 방지).
- 스토어 리치텍스트가 `<video>`·`<script>`·`<style>`를 지우므로 **영상은 iframe 안에서만** 산다.

## 폰트
- `--sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...`
- Farax Display는 히어로 h1 하나만. `@font-face`
  `src: url('https://farax-creative.github.io/assets/fonts/farax-display.ttf')`(전체 URL).
- 굵기: 본문 500 / 리드 600 / h2·소제목·강조 700 / 가격 800. 세리프 금지.

## 규칙(불변)
- 가로 스크롤 금지(390·726·1440 실측 — R3에서 overflow 없음 확인).
- 폰트 전체 URL. 허브에는 페이지로 렌더되게(임시 폴더에 `index.html`+`media/`+`changelog.html`).
- Gumroad·테스트 개수·"네트워크 없음" 단정 금지(URL 붙여넣기 1건은 "요청할 때만 온라인").
- 가격은 확정값 받기 전까지 $0 / $5 자리표시자.
- 임베드 높이: 스토어가 iframe을 못 맞추므로 실측으로 clamp 고정.
  R3 실측(콘텐츠 높이): 390열 6950 · 726열 7504 · 1440 8381.
  → 목 iframe `height: clamp(7060px, calc(6410px + 167vw), 7620px)`
  (콘텐츠보다 항상 ~110px 위 → 스크롤 없음, 여백 최소).
