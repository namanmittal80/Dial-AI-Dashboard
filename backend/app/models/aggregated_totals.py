from sqlalchemy import Column, String, Float, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class AggregatedTotals(Base):
    __tablename__ = "aggregated_totals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    total_tokens = Column(BigInteger, default=0)
    avg_execution_time = Column(Float, default=0.0)
    total_conversations = Column(BigInteger, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)
    updated_by = Column(String)
