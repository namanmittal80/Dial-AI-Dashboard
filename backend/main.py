from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from datetime import datetime
from pydantic import BaseModel
import uvicorn

from database.connection import get_db, SessionLocal
from models.models import ClientConfig, AggregatedTotals, Message

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class DateRangeRequest(BaseModel):
    client_id: str
    start_date: datetime
    end_date: datetime

@app.post("/api/dashboard-data")
async def get_dashboard_data(
    request: DateRangeRequest,
    db: SessionLocal = Depends(get_db)
):
    try:
        # Get client configuration
        client_config = db.query(ClientConfig).filter(
            ClientConfig.client_id == request.client_id
        ).first()

        # Get aggregated totals for the client
        totals = db.query(AggregatedTotals).filter(
            AggregatedTotals.client_id == request.client_id
        ).first()

        # Get messages for the date range
        messages = db.query(Message).filter(
            Message.conversation_id.like(f"{request.client_id}%"),
            Message.timestamp.between(request.start_date, request.end_date)
        ).order_by(Message.timestamp.desc()).all()

        # Calculate statistics for the date range
        message_stats = db.query(
            func.count(Message.id).label('total_messages'),
            func.sum(Message.tokens).label('total_tokens'),
            func.avg(Message.llm_time).label('avg_llm_time')
        ).filter(
            Message.conversation_id.like(f"{request.client_id}%"),
            Message.timestamp.between(request.start_date, request.end_date)
        ).first()

        # Get unique conversations in the date range
        unique_conversations = db.query(
            func.count(func.distinct(Message.conversation_id))
        ).filter(
            Message.conversation_id.like(f"{request.client_id}%"),
            Message.timestamp.between(request.start_date, request.end_date)
        ).scalar()

        return {
            "client_info": {
                "client_id": client_config.client_id if client_config else None,
                "client_name": client_config.client_name if client_config else None,
                "client_config": client_config.client_config if client_config else None
            },
            "period_statistics": {
                "total_messages": message_stats[0] or 0,
                "total_tokens": message_stats[1] or 0,
                "avg_llm_time": float(message_stats[2]) if message_stats[2] else 0,
                "unique_conversations": unique_conversations or 0
            },
            "overall_statistics": {
                "total_tokens": totals.total_tokens if totals else 0,
                "avg_execution_time": totals.avg_execution_time if totals else 0,
                "total_conversations": totals.total_conversations if totals else 0
            },
            "recent_messages": [
                {
                    "conversation_id": msg.conversation_id,
                    "timestamp": msg.timestamp.isoformat(),
                    "tokens": msg.tokens,
                    "llm_time": msg.llm_time,
                    "user_message": msg.user_message,
                    "system_message": msg.system_message
                } for msg in messages[:100]  # Limiting to last 100 messages
            ]
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 