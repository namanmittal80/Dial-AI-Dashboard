from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from database.connection import Base

class ClientConfig(Base):
    __tablename__ = "client_config"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    client_name = Column(String)
    client_config = Column(JSONB)

class AggregatedTotals(Base):
    __tablename__ = "aggregated_totals"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    total_tokens = Column(Float)
    avg_execution_time = Column(Float)
    total_conversations = Column(Integer)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    timestamp = Column(DateTime)
    tokens = Column(Integer)
    llm_time = Column(Float)
    user_message = Column(String)
    system_message = Column(String) 