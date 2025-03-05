import os
import openai
import logging
import pymysql
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# 로그 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 1) OpenAI API 키 설정
#    환경 변수 혹은 직접 문자열로 설정
#openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수 방식
#openai.api_key = "YOUR-API-KEY"      # 직접 입력 방식 (노출 주의)

load_dotenv()  # .env 파일 로드
openai.api_key = os.getenv("OPENAI_API_KEY")

# MySQL 연결 설정
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        db=os.getenv('DB_NAME', 'youtube_summary'),
        charset='utf8mb4'
    )

def get_youtube_transcript(video_id, languages=['ko', 'en']):
    """
    Generate a summary, highlight, and key insights in korean.
    """

    
    logger.info("Video ID : https://www.youtube.com/watch?v=" + video_id)


    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    # 여러 언어 중 우선 순위대로 자막을 시도
    for transcript in transcript_list:
        if transcript.language_code in languages or transcript.is_translatable:
            try:
                # 지정 언어가 아니더라도 번역 가능한 자막이면 번역
                if transcript.is_translatable and transcript.language_code not in languages:
                    translated = transcript.translate(languages[0])
                    return translated.fetch()
                else:
                    return transcript.fetch()
            except:
                pass
    return None

def extract_transcript_text(transcript_data):
    """
    자막 데이터를 받아 텍스트만 순서대로 합친다.
    """
    lines = [item['text'] for item in transcript_data]
    return " ".join(lines)

def load_prompt(filename):
    """프롬프트 파일을 로드하는 함수"""
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', filename)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"프롬프트 파일을 찾을 수 없습니다: {filename}")
        return None

def summarize_text_with_chatgpt(text, model="gpt-3.5-turbo"):
    """
    ChatGPT를 사용하여 텍스트를 한국어로 요약한다.
    """
    prompt = load_prompt('summary-0.2.0.txt')

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    # ChatCompletion 응답에서 토큰 사용량 출력
    model
    logger.info(f"Model : {model}")
    logger.info(f"Output :\n{response['choices'][0]['message']['content'].strip()}")
    logger.info(f"Prompt tokens: {response['usage']['prompt_tokens']}")
    logger.info(f"Completion tokens: {response['usage']['completion_tokens']}")
    logger.info(f"$ Total tokens: {response['usage']['total_tokens']}")

    return [response["choices"][0]["message"]["content"].strip(), response['usage']['total_tokens']]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/app", methods=["GET"])
def app_page():
    return render_template("app.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    video_id = data.get("video_id", "").strip()

    if not video_id:
        logger.warning("요약 요청 실패: video_id가 제공되지 않음")
        return jsonify({"error": "No video_id provided"}), 400
    
    try:
        # 2) 자막 가져오기
        transcript_data = get_youtube_transcript(video_id, ['ko', 'en'])
        if not transcript_data:
            logger.warning(f"자막을 찾을 수 없음: {video_id}")
            return jsonify({"error": "자막을 찾을 수 없습니다."}), 404

        # 3) 자막을 텍스트로 합치기
        transcript_text = extract_transcript_text(transcript_data)
                
        # 4) ChatGPT를 통해 요약
        #result = summarize_text_with_chatgpt(transcript_text, "o1-mini-2024-09-12")
        result = summarize_text_with_chatgpt(transcript_text, "gpt-4o-mini")
        
        return jsonify({
            "transcript": transcript_text,
            "summary": result[0],
            "totalTokens": result[1]
        })
    except Exception as e:
        logger.error(f"요약 요청 처리 중 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 5) 서버 실행
    app.run(debug=True, host="0.0.0.0", port=11080)
