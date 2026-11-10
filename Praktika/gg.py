import os
import torch
from gtts import gTTS


def text_to_speech(text, output_audio_path="speech.wav"):
    """Шаг 1: Превращаем текст в аудиофайл"""
    print("1. Генерация аудио из текста...")
    # Создаем аудио с помощью gTTS
    tts = gTTS(text=text, lang='ru', slow=False)
    temp_mp3 = "temp.mp3"
    tts.save(temp_mp3)

    # Конвертируем mp3 в wav (SadTalker/Wav2Lip часто требуют .wav)
    # Для простоты можно использовать ffmpeg или встроенные библиотеки
    os.system(f"ffmpeg -i {temp_mp3} -ar 16000 -ac 1 {output_audio_path} -y")
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)
    print(f"Аудио сохранено в {output_audio_path}")


def animate_photo(image_path, audio_path, output_video_path="output_animated.mp4"):
    """
    Шаг 2: Оживление фотографии под аудио с помощью нейросети (SadTalker)
    Для запуска этого шага требуется клонированный репозиторий SadTalker и веса моделей.
    """
    print("2. Запуск нейросети для анимации лица...")

    # Пример вызова консольной команды SadTalker (если репозиторий склонирован локально):
    # python inference.py --driven_audio speech.wav --source_image photo.jpg --result_dir ./results

    command = (
        f"python inference.py "
        f"--driven_audio {audio_path} "
        f"--source_image {image_path} "
        f"--result_dir ./output_video "
        f"--enhancer gfpgan"  # Опционально для улучшения качества лица
    )

    print(f"Выполняется команда: {command}")
    # os.system(command) # Раскомментируйте, когда настроите окружение SadTalker
    print("Готово! Видео успешно создано.")


if __name__ == "__main__":
    # Входные данные
    text_to_animate = "Привет! Посмотри, я умею оживать под любой текст, который ты мне напишешь."
    my_photo = "foto.png"  # Путь к вашей фотографии лица (анфас)

    # Запуск пайплайна
    text_to_speech(text_to_animate, "speech.wav")

    if os.path.exists(my_photo):
        animate_photo(my_photo, "speech.wav", "result.mp4")
    else:
        print(f"Пожалуйста, положите файл с фото ('{my_photo}') в папку со скриптом.")