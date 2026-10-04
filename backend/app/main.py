# import base64
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import Response
# from .models import ChatRequest, ChatResponse
# from .agent import run_agent
# from .voice import transcribe, synthesize
# from .config import settings

# app = FastAPI(title="Car Service Voice Agent")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.post("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     try:
#         history = [m.dict() for m in req.history]
#         result = run_agent(history, req.user_text, req.customer_info)
#         audio_b64 = None
#         try:
#             audio_bytes = synthesize(result["reply"])
#             audio_b64 = base64.b64encode(audio_bytes).decode()
#         except Exception as e:
#             print("TTS failed:", e)
#         return ChatResponse(
#             reply=result["reply"],
#             emergency=result["emergency"],
#             audio_base64=audio_b64,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/stt")
# async def stt(file: UploadFile = File(...)):
#     data = await file.read()
#     try:
#         text = transcribe(data, file.filename or "audio.webm")
#         return {"text": text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/tts")
# def tts(text: str):
#     audio = synthesize(text)
#     return Response(content=audio, media_type="audio/mpeg")
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse
from .agent import run_agent
from .voice import transcribe
from .config import settings

app = FastAPI(title="Car Service Voice Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        history = [m.dict() for m in req.history]
        result = run_agent(history, req.user_text, req.customer_info)
        # audio_base64 is None — frontend uses browser TTS
        return ChatResponse(
            reply=result["reply"],
            emergency=result["emergency"],
            audio_base64=None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stt")
async def stt(file: UploadFile = File(...)):
    data = await file.read()
    try:
        text = transcribe(data, file.filename or "audio.webm")
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))