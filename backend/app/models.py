from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
  message: str = Field(..., min_length=1)
  session_id: Optional[str] = None


class SourceChunk(BaseModel):
  filename: str
  score: float
  snippet: str


class ChatResponse(BaseModel):
  answer: str
  sources: List[SourceChunk] = []