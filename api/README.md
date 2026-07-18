# api/

애드온이 실행 중에 읽어가는 정적 JSON. 서버 로직은 없다 — GitHub Pages가 그대로 내려준다.

## 왜 여기인가

원래 `zap-output-version.json`은 개인 계정(`calars-dev`)의 Gist에 있었다. 브랜드 자산이
개인 계정에 묶여 있어 계정 분리 규칙에 어긋났고, Gist는 계정 간 이전이 아예 안 된다.
이 저장소는 이미 브랜드 소유이고 Public이라 옮길 곳으로 맞다.

## 파일

- `zap-output-version.json` — [[Zap Output]]의 Check for Updates가 조회한다.
  `zap_output/updates.py`의 `VERSION_URL`이 이 주소를 가리킨다.

## ⚠️ 새 버전을 배포할 때

**`latest` 값을 손으로 올려야 한다.** 자동화돼 있지 않다. 여기를 안 올리면 고객의
"Check for Updates"가 계속 옛 버전을 최신이라고 답한다.

`url`은 구매/다운로드 페이지다. 판매 채널을 바꾸면 여기도 바꾼다.
