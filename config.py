from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(override=True)

MODEL_DIR = Path(__file__).parent.resolve() / "model"

class Config:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    VOSK_MODEL_PATH: Path = Path(os.getenv("VOSK_MODEL_PATH", MODEL_DIR / "vosk-model-small-ru-0.22")).expanduser().resolve()

    @classmethod
    def validate(cls) -> None:
        missing = []
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY is missing or empty")
        if not cls.VOSK_MODEL_PATH.exists():
            missing.append(f"Vosk model not found at: {cls.VOSK_MODEL_PATH}")
        if missing:
            raise ValueError("\n  " + "\n  ".join(missing))

Config.validate()