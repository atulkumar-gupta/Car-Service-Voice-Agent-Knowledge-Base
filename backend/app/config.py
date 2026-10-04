# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
#     OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#     OPENAI_TTS_MODEL: str = os.getenv("OPENAI_TTS_MODEL", "tts-1")
#     OPENAI_TTS_VOICE: str = os.getenv("OPENAI_TTS_VOICE", "alloy")
#     OPENAI_STT_MODEL: str = os.getenv("OPENAI_STT_MODEL", "whisper-1")
#     ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
#     KB_PATH: str = os.path.join(os.path.dirname(__file__), "knowledge_base.md")

# settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_WHISPER_MODEL: str = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3")
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:5173"
    ).split(",")
    KB_PATH: str = os.path.join(os.path.dirname(__file__), "knowledge_base.md")


settings = Settings()