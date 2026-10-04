# from openai import OpenAI
# from .config import settings
# import io

# client = OpenAI(api_key=settings.OPENAI_API_KEY)


# def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
#     buf = io.BytesIO(audio_bytes)
#     buf.name = filename
#     result = client.audio.transcriptions.create(
#         model=settings.OPENAI_STT_MODEL,
#         file=buf,
#     )
#     return result.text


# def synthesize(text: str) -> bytes:
#     response = client.audio.speech.create(
#         model=settings.OPENAI_TTS_MODEL,
#         voice=settings.OPENAI_TTS_VOICE,
#         input=text,
#     )
#     return response.content
from groq import Groq
from .config import settings
import io

client = Groq(api_key=settings.GROQ_API_KEY)


def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """Transcribe audio using Groq Whisper (FREE)."""
    buf = io.BytesIO(audio_bytes)
    buf.name = filename
    result = client.audio.transcriptions.create(
        model=settings.GROQ_WHISPER_MODEL,
        file=buf,
    )
    return result.text


def synthesize(text: str) -> bytes:
    """
    Groq does not provide TTS.
    Return empty bytes -> frontend uses browser Web Speech API.
    """
    return b""