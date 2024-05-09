import os

from flask import Flask, render_template, request, send_file
import tempfile
from text2speech import text2speech
from speech2text import speech2text
from groq_service import groq_answer_question


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio_data = request.files['audio'].read()

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(audio_data)
        tmp.flush()

    text = speech2text(tmp.name)
    answer = groq_answer_question(text)
    generated_audio_file = text2speech(answer)

    os.remove(tmp.name)

    return send_file(generated_audio_file, mimetype='audio')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
