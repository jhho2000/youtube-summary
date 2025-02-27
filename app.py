import os
import openai
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

# 1) OpenAI API 키 설정
#    환경 변수 혹은 직접 문자열로 설정
#openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수 방식
openai.api_key = "OPENAI_API_KEY"      # 직접 입력 방식 (노출 주의)

def get_youtube_transcript(video_id, languages=['ko', 'en']):
    """
    주어진 video_id로 유튜브 자막을 가져오고, 여러 언어 중
    가용한 첫 번째 자막을 반환한다.
    """
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

def summarize_text_with_chatgpt(text, model="gpt-3.5-turbo"):
    """
    ChatGPT를 사용하여 텍스트를 한국어로 요약한다.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"""
                            아래에 제시된 유튜브 영상 스크립트를 확인하고, 영상의 핵심 주제, 중요 포인트, 그리고 결론을 중심으로 간결하고 명확하게 요약해 주세요.
                            또한 시청자가 얻을 수 있는 교훈이나 통찰이 있다면 함께 정리해 주시기 바랍니다.
                            : {text}
                        """
            }
        ]
    )

    # ChatCompletion 응답에서 토큰 사용량 출력
    print("Prompt tokens:", response["usage"]["prompt_tokens"])
    print("Completion tokens:", response["usage"]["completion_tokens"])
    print("Total tokens:", response["usage"]["total_tokens"])

    return response["choices"][0]["message"]["content"].strip()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    video_id = data.get("video_id", "").strip()

    if not video_id:
        return jsonify({"error": "No video_id provided"}), 400
    
    try:
        # 2) 자막 가져오기
        transcript_data = get_youtube_transcript(video_id, ['ko', 'en'])
        if not transcript_data:
            return jsonify({"error": "자막을 찾을 수 없습니다."}), 404

        # 3) 자막을 텍스트로 합치기
        transcript_text = extract_transcript_text(transcript_data)

        # 4) ChatGPT를 통해 요약
        summary = summarize_text_with_chatgpt(transcript_text, "gpt-4o")

        return jsonify({
            "transcript": transcript_text,
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 5) 서버 실행
    app.run(debug=True, host="0.0.0.0", port=5000)
