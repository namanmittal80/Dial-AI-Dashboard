from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class ConversationInsights(Base):
    __tablename__ = "conversation_insights"
    __table_args__ = {"schema": "analytics"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String, nullable=False)
    conversation_id = Column(String, nullable=False)

    # Sentiment
    sentiment = Column(String)
    sentiment_quote = Column(String)

    # Flags
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(String)
    flag_severity = Column(String)
    flag_type = Column(String)
    flag_quote = Column(String)

    # Feedback
    has_feedback = Column(Boolean, default=False)
    feedback_type = Column(String)
    feedback_impact = Column(String)
    feedback_quote = Column(String)

    # Metadata
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_seconds = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow) 