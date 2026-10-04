from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: List[ChatMessage] = []
    user_text: str
    customer_info: Dict[str, Optional[str]] = {}

class ChatResponse(BaseModel):
    reply: str
    emergency: bool
    audio_base64: Optional[str] = None