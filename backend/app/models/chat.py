from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    message: str
    audio_data: Optional[str] = None
    context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    ai_probability: float
