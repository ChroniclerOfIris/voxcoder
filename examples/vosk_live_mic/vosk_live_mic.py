from vosk import Model, KaldiRecognizer
import pyaudio
import json

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import Config

def main() -> None:
    try:
        model = Model(str(Config.VOSK_MODEL_PATH))
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить модель Vosk: {e}")
    print(f"GEMINI_API_KEY = {Config.GEMINI_API_KEY[:10]}…")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    recognizer = KaldiRecognizer(model, 16000)
    print("Слушаю… (Ctrl+C — выйти)")
    try:
        while True:
            data = stream.read(8000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                if text := json.loads(recognizer.Result()).get("text"):
                    print("→", text)
            else:
                if partial := json.loads(recognizer.PartialResult()).get("partial"):
                    print(partial, end="\r", flush=True)
    except KeyboardInterrupt:
        print("\nОстанавливаю…")
        if text := json.loads(recognizer.FinalResult()).get("text"):
            print("→", text)
        print("Прощай…")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()