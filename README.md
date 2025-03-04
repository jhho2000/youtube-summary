# YouTube 영상 요약기

YouTube 영상의 자막을 추출하여 OpenAI GPT 모델을 통해 구조화된 요약을 제공하는 Flask 기반 웹 애플리케이션입니다. 영상의 핵심 내용을 빠르게 파악하고 주요 통찰을 얻을 수 있습니다.

## 📋 주요 기능

- **YouTube 자막 추출**: `youtube-transcript-api`를 사용하여 YouTube 영상의 자막을 자동으로 추출합니다.
- **다국어 지원**: 한국어(`ko`)와 영어(`en`) 자막을 우선적으로 시도하며, 다른 언어의 자막도 번역 가능한 경우 한국어로 번역합니다.
- **AI 기반 요약**: OpenAI API(GPT 모델)를 사용하여 자막 내용을 분석하고 구조화된 요약을 생성합니다.
- **구조화된 요약 결과**: 
  - 전체 내용 요약 (200-300자)
  - 주요 포인트 (7-8개의 불릿 포인트)
  - 주요 통찰 (7개의 깊이 있는 통찰)
- **반응형 웹 인터페이스**: 모바일 및 데스크톱 환경에 최적화된 사용자 친화적 UI를 제공합니다.
- **다양한 URL 형식 지원**: 표준 YouTube URL, 단축 URL(youtu.be), 영상 ID 직접 입력 등 다양한 형식을 지원합니다.

## 🛠️ 기술 스택

- **백엔드**: 
  - Python 3.8+
  - Flask 2.2.3 (웹 프레임워크)
  - OpenAI API (GPT 모델)
  - youtube-transcript-api 0.6.0 (자막 추출)
  - python-dotenv 1.0.0 (환경 변수 관리)

- **프론트엔드**:
  - HTML5, CSS3
  - JavaScript (ES6+)
  - Marked.js (마크다운 렌더링)

## 📦 설치 방법

1. 저장소 클론:
   ```bash
   git clone <repository-url>
   cd youtube-summary
   ```

2. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

3. OpenAI API 키 설정:
   - `.env` 파일 생성:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - 또는 `app.py` 파일에서 직접 설정:
     ```python
     openai.api_key = "YOUR-API-KEY"  # 직접 입력 방식 (노출 주의)
     ```

## 🚀 실행 방법

1. Flask 애플리케이션 실행:
   ```bash
   python app.py
   ```

2. 웹 브라우저에서 접속:
   ```
   http://localhost:11080
   ```

## 📝 사용 방법

1. 웹 인터페이스에서 YouTube 영상 URL 입력 (예: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. "요약하기" 버튼 클릭
3. 처리가 완료될 때까지 대기 (영상 길이에 따라 시간이 달라질 수 있음)
4. 구조화된 요약 결과 확인:
   - 전체 내용 요약
   - 주요 포인트 (이모지와 함께 표시)
   - 주요 통찰 (이모지와 함께 표시)

## 📁 프로젝트 구조

```
youtube-summary/
├── app.py                # 메인 애플리케이션 파일
├── requirements.txt      # 의존성 패키지 목록
├── .env                  # 환경 변수 파일 (API 키 등)
├── .gitignore            # Git 무시 파일 목록
└── templates/            # HTML 템플릿 디렉토리
    ├── index.html        # 기본 웹 인터페이스
    └── app.html          # 모바일 최적화 웹 인터페이스
```

## ⚙️ 커스터마이징

- **모델 변경**: `app.py` 파일에서 `summarize_text_with_chatgpt` 함수의 `model` 파라미터를 수정하여 다른 OpenAI 모델을 사용할 수 있습니다.
- **요약 프롬프트 수정**: 같은 함수 내의 `content` 필드를 수정하여 요약 방식을 변경할 수 있습니다.
- **UI 커스터마이징**: `templates` 디렉토리의 HTML 파일과 내장된 CSS를 수정하여 UI를 변경할 수 있습니다.

## ⚠️ 주의사항

- OpenAI API 사용에는 비용이 발생할 수 있습니다. API 사용량과 관련 비용을 모니터링하세요.
- 매우 긴 영상의 경우 토큰 제한으로 인해 요약이 불완전할 수 있습니다.
- 자막이 없는 영상은 요약할 수 없습니다.
