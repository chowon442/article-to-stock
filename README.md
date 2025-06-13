# Article-to-Stock 프로젝트

## 개요
이 프로젝트는 뉴스 기사에서 언급된 기업을 분석하고, 한국 주식시장 데이터를 활용해 주가 변동 정보를 제공합니다.

## 설치 방법
1. 프로젝트 디렉터리를 클론하거나 열어주세요.
2. 터미널에서 프로젝트 루트 디렉터리(`./article-to-stock`)로 이동하세요.
3. 의존성을 설치하세요: `pip install -r requirements.txt` 명령어를 실행하세요.

## 실행 방법 (Step-by-Step)
1. 터미널을 열고 프로젝트 루트 디렉터리(`./article-to-stock`)로 이동하세요.
2. `server.py` Python 스크립트를 실행하세요. (`python server.py`)
3. `localhost:3000`로 접속하세요. (`PORT` 설정에 따라 값이 다를 수 있음)
4. 분석을 원하는 뉴스 기사 url을 입력한 후, `분석 시작` 버튼을 누르세요. (LLM 실행 시간에 따라 긴 시간 소요될 수 있음)

## 환경 변수 설정 (.env 파일)
.env 파일을 프로젝트 루트 디렉터리에 생성한 후, 다음 변수를 추가하세요.

```
# openrouter api key
OPENROUTER_API_KEY=your_api_key_here

# port
PORT=3000
```

## 배포
`https://article-to-stock.onrender.com/`에서도 사용할 수 있습니다. (api limit에 따라 작동하지 않을 수 있음)

## 주요 파일 설명
- ac.py: 뉴스 기사에서 기업 이름과 관련 정보를 추출하는 함수를 포함합니다.
- b.py: 기사 URL을 분석하고 주가 변동 데이터를 처리하는 메인 스크립트입니다.
- server.py: 웹 서버를 실행하여 애플리케이션을 구동합니다.
- app.js: 프론트엔드 JavaScript 코드로 사용자 인터페이스와 상호작용을 처리합니다.
- index.html: 웹 페이지의 기본 HTML 구조를 정의합니다.
- requirements.txt: 프로젝트에 필요한 Python 패키지 목록입니다.
- stock.json: 주식 시장 데이터가 저장된 JSON 파일입니다. (패키지 로딩 시간 단축을 위해 임시로 사용)