import os
import time
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
from gtts import gTTS

app = Flask(__name__)

# Папки для загрузки файлов и сохранения результатов
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

# Папка, где у вас установлена нейросеть (например, Wav2Lip или SadTalker)
AI_MODEL_DIR = 'Wav2Lip'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


def generate_lip_sync_video(image_path, audio_path, output_path):
    """
    Запуск нейросети через subprocess.
    Пример настроен под Wav2Lip (для SadTalker аргументы запуска будут иными).
    """
    abs_image_path = os.path.abspath(image_path)
    abs_audio_path = os.path.abspath(audio_path)
    abs_output_path = os.path.abspath(output_path)

    # Команда для запуска инференса Wav2Lip
    cmd = [
        "python", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
        "--face", abs_image_path,
        "--audio", abs_audio_path,
        "--outfile", abs_output_path,
        "--pads", "0", "10", "0", "0"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=AI_MODEL_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Лог нейросети:", result.stdout)

        # Проверяем, создался ли файл видео
        if not os.path.exists(output_path):
            raise Exception("Видеофайл не был сгенерирован нейросетью.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения нейросети: {e.stderr}")
        raise Exception(f"Ошибка ML-модели: {e.stderr}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Необходимо загрузить изображение и ввести текст'}), 400

    image_file = request.files['image']
    text_content = request.form['text']

    if image_file.filename == '' or not text_content.strip():
        return jsonify({'error': 'Пустой текст или файл не выбран'}), 400

    # 1. Сохранение загруженного изображения
    image_filename = f"input_{int(time.time())}.jpg"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_file.save(image_path)

    # 2. Генерация аудиофайла из текста с помощью gTTS (на русском языке)
    audio_filename = f"voice_{int(time.time())}.mp3"
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    tts = gTTS(text=text_content, lang='ru')
    tts.save(audio_path)

    # 3. Путь для итогового видео
    output_filename = f"result_{int(time.time())}.mp4"
    output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)

    try:
        # Запуск процесса оживления фото
        generate_lip_sync_video(image_path, audio_path, output_path)
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

    # Возвращаем ссылку на готовое видео
    return jsonify({
        'status': 'success',
        'video_url': f'/results/{output_filename}',
        'audio_url': f'/uploads/{audio_filename}'
    })


@app.route('/results/<filename>')
def get_result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)


@app.route('/uploads/<filename>')
def get_upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)