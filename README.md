# youtube-summary
Flask 기반 웹 애플리케이션으로, 사용자가 입력한 YouTube URL에서 자막을 가져온 뒤 OpenAI GPT 모델을 통해 요약 결과를 제공하는 프로젝트입니다.


## 주요 기능
- **YouTube 자막 추출**: `youtube-transcript-api`를 사용하여 주어진 YouTube 영상의 자막을 가져옵니다.  
- **다국어 지원**: 한국어(`ko`)와 영어(`en`) 자막을 우선 시도하며, 다른 언어 자막도 번역 가능할 경우 번역을 시도합니다.  
- **GPT 요약**: OpenAI API를 사용하여 추출된 자막을 간결하게 요약하고, 시청자가 얻을 수 있는 통찰이나 교훈을 정리해 줍니다.  
- **간단한 UI**: Flask 템플릿(`index.html`)로 구성된 웹 페이지에서 손쉽게 영상 URL을 입력하고 요약 결과를 확인할 수 있습니다.

## 기술 스택
- **프레임워크**: Flask (Python)
- **AI 모델**: OpenAI API (GPT 계열 모델)
- **자막 처리**: `youtube-transcript-api`
- **프론트엔드**: HTML, CSS, JavaScript

## 요구 사항
- Python 3.8 이상
- OpenAI API 키 (유효한 API 키를 환경 변수 혹은 소스코드에 직접 설정 필요)

