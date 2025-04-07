from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {"schema": "analytics"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String, nullable=False)
    conversation_id = Column(String, nullable=False)
    message_index = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    role = Column(String, nullable=False)
    text = Column(String)
    llm_time = Column(Integer, nullable=True)
    tokens = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)
    updated_by = Column(String)
