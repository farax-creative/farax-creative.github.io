# Zap Board Superhive 상세페이지 — 설계안 (2026-09-29)

방향: Farax 사이트 컨셉, 전부 산세리프, 아이콘·이미지·캡처 영상 위주. 새 촬영은 최소.

## 구조 (위→아래)
1. 릴리스 바 — Prompt Motion과 동일 (버전 2.0 · 체인지로그)
2. 히어로 — 제품명 한 줄 + `media/hero.mp4`(흩어진 카드 → 정렬)
3. 기능 그리드 — 카드 1개 = 영상/스틸 1개 + 제목 한 줄 (설명문 없음)
   - 보드에 끌어다 놓기·정렬: `assets/store/demos/01_Move~10_ImportFolder.mp4` 중 다른 애드온이 안 보이는 컷
   - 비교(투명도·흑백): `media/compare.mp4`
   - 그룹 프레임: `media/frames_two.png`
   - 색 추출 (Pro): `media/colour.mp4`
   - 이미지 조정 (Pro): `media/adjust.mp4`
   - 동영상 카드 (Pro): `media/video_card.png`
   - 3D 뷰로 보내기 (Pro): `media/send3d.png` — 세워서 앞뷰로 재촬영 완료
   - 주석(화살표·박스·타원): `media/annotate.png` — 신규 촬영
   - 보드 여러 개: `media/boards_multi.png` — 신규 촬영(두 보드 나란히)
4. Free / Pro — 아이콘+체크 표 한 장 (가격은 답 받은 뒤)
5. 요구사항 3줄 · FAQ 3개 · CTA

## 규칙
- 폰트 전체 URL, 굵기 한 단계 올림(v005 피드백), 가로 스크롤 금지(390/1440)
- 허브에는 폴더째(영상 포함) 올리고 설명은 한글
- Gumroad·테스트 개수·"네트워크 없음" 문구 금지

## 새로 찍어야 하는 것 (재개 시)
send3d(세운 방향) · 주석 도형 · 보드 여러 개 — 셋만. 나머지는 기존 자산.
→ 2026-09-30 셋 다 촬영 완료(`media/send3d.png`·`annotate.png`·`boards_multi.png`).

---

# 재사용 스타일 스펙 (다른 세 제품이 그대로 복제)

Zap Board `superhive.html`이 승인 기준. 나머지 제품 상세페이지는 이 절만 보고
색·폰트·아이콘·섹션 구조를 그대로 가져오고, 카드 안 미디어와 문구만 제품에 맞춘다.

## 폰트
- `--sans: -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`
- 큰 제목(h1·h2)만 브랜드 폰트: `@font-face 'Farax Display'`,
  `src: url('https://farax-creative.github.io/assets/fonts/farax-display.ttf')` (전체 URL 필수, 단일 굵기 400).
- **굵기 한 단계 올린 값(v005 피드백)** — 본문 500 / 리드·표 항목 600 / 카드 제목·라벨 700 / 강조 700 / 가격 숫자 800.
  세리프 금지, `--mono`는 릴리스 바·킥커·푸터의 라벨성 텍스트에만.

## 색 토큰 (`:root`)
```
--bg #0B0D10  --panel #11161B  --bar #050506
--cream #F4EBDD  --body rgba(244,235,221,.86)  --dim rgba(244,235,221,.5)  --line rgba(244,235,221,.13)
--zap #FFC828   (브랜드 옐로 — 아이콘·체크·Pro 배지·강조에만)
```

## 아이콘
- **Lucide 스타일 인라인 SVG 한 벌**, 이모지 금지. `viewBox="0 0 24 24"`, `fill:none`,
  `stroke:currentColor`, `stroke-width:2`, `stroke-linecap/linejoin:round`.
- 기본 크기 `.ic { 19px }`, 표 안 체크 18px·기능 라벨 17px. 색은 `--zap`(강조) 또는 `--dim`(중립).

## 섹션 구조 (위→아래)
릴리스 바 → 히어로(제목 + hero 영상) → 기능 그리드 → Free/Pro(가격 칩 + 체크 표)
→ 요구사항 3줄 → FAQ 3개 → CTA → 푸터. 콘텐츠 폭 `.col{max-width:640px}`, 셸 `.wrap{max-width:940px}`.

## 카드 해부 (기능 그리드)
- 그리드 `repeat(2,1fr)`, 680px 이하 1열. 카드 = **미디어 1개 + 캡션 한 줄(설명문 없음)**.
- 캡션 = 인라인 SVG 아이콘 + `.t`(700/16px 제목 한 줄) + (Pro면 오른쪽 `.pro` 배지).
- 미디어: 카드 안에서는 테두리·라운드 제거하고 아래쪽 `--line` 구분선만.

## 미디어 규격
- 데모는 캡처 영상(mp4, H.264, ≤1280px), `<video autoplay muted loop playsinline>`,
  히어로만 `preload="auto"` 나머지 `preload="metadata"`. 스틸은 PNG.
- 스토어 리치텍스트가 `<video>`를 지우므로 **움직이는 데모는 이 iframe 페이지 안에서만** 재생된다.
- mp4 원본은 항상 보존(시리즈 규칙). 갤러리용은 별도로 2000×1000 WebP.

## 릴리스 바 / 임베드
- 릴리스 바: 점 + 제품명·버전 + 에디션 + `changelog.html` 링크(`target=_blank`).
- 스토어는 iframe 높이를 못 맞추므로 측정값으로 고정. 390/1440에서 재측정하고
  `height: clamp(min, calc(A - B*vw), max)`로 임베드. 링크는 새 탭.

## 규칙(불변)
- 가로 스크롤 금지(390·1440 실측), 폰트 전체 URL, 허브에는 폴더째 올리고 설명 한글.
- Gumroad·테스트 개수·"네트워크 없음" 문구 금지. 가격은 확정 답 받은 값(현재 $0 / $5 자리표시자).
