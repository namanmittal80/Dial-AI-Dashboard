from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageItem(BaseModel):
    role: str  # 'user' or 'system'
    text: str
    message_index: int

class TranscriptPayload(BaseModel):
    session_id: str
    client_id: str
    client_name: str
    messages: List[MessageItem]
    start_time: datetime
    end_time: datetime

class ClientConfigPayload(BaseModel):
    client_id: str
    client_name: str
    client_config: dict
