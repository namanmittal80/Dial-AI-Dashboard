from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .db_connection import SessionLocal, engine
from .schemas.transcript import TranscriptPayload, ClientConfigPayload
from .database.crud_logic import insert_messages, insert_conversation_dump, update_aggregated_totals, initialize_client, insert_conversation_insights
from .models import Base, Message, ConversationDump, AggregatedTotals, ClientConfig, ConversationInsights
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Initialize DB metadata
Base.metadata.create_all(bind=engine)

# Custom middleware for request timing
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()

# Add CORS middleware with specific configuration
origins = [
    "http://localhost:5173",    # Vite dev server
    "http://localhost:3000",    # React dev server (if needed)
    "http://localhost:80",      # Production server
    "http://localhost"          # Base localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=86400,  # Cache preflight requests for 24 hours
)

# Add Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add timing middleware
app.add_middleware(TimingMiddleware)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_transcript")
def upload_transcript(payload: TranscriptPayload, db: Session = Depends(get_db)):
    try:
        insert_conversation_dump(db, payload)
        insert_messages(db, payload)
        update_aggregated_totals(db, payload)
        insert_conversation_insights(db, payload)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/initialize-client/")
def init_client(payload: ClientConfigPayload, db: Session = Depends(get_db)):
    try:
        initialize_client(db, payload)
        db.commit()
        return {"status": "client registered"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/client-config")
async def get_client_config(db: Session = Depends(get_db)):
    try:
        # Add your logic to fetch client configuration
        # For example:
        configs = db.query(ClientConfig).all()
        return [config.client_config for config in configs]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

class AggregatedTotalsRequest(BaseModel):
    start_date: str
    end_date: str
    client_id: Optional[str] = None

@app.post("/fetch-aggregated-totals")
async def get_aggregated_totals(
    request: AggregatedTotalsRequest,
    db: Session = Depends(get_db)
):
    try:
        # Convert string dates to datetime objects
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        end = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Build the query
        query = db.query(AggregatedTotals).filter(
            AggregatedTotals.created_at >= start,
            AggregatedTotals.created_at <= end
        )
        
        # Add client_id filter if provided
        if request.client_id:
            query = query.filter(AggregatedTotals.client_id == request.client_id)
            
        # Get results
        results = query.all()
        
        if not results:
            return {
                "total_conversations": 0,
                "total_tokens": 0,
                "avg_execution_time": 0
            }
            
        # Aggregate the results
        total_conversations = sum(r.total_conversations for r in results)
        total_tokens = sum(r.total_tokens for r in results)
        
        # Calculate weighted average execution time
        total_weighted_time = sum(r.avg_execution_time * r.total_conversations for r in results)
        avg_execution_time = total_weighted_time / total_conversations if total_conversations > 0 else 0
        
        return {
            "total_conversations": total_conversations,
            "total_tokens": total_tokens,
            "avg_execution_time": avg_execution_time
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

class TimeSeriesRequest(BaseModel):
    start_date: str
    end_date: str
    client_id: Optional[str] = None

@app.post("/time-series-data")
async def get_time_series_data(
    request: TimeSeriesRequest,
    db: Session = Depends(get_db)
):
    try:
        # Convert string dates to datetime objects
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        end = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        # Build the query
        query = db.query(
            AggregatedTotals.created_at,
            AggregatedTotals.total_conversations,
            AggregatedTotals.total_tokens,
            AggregatedTotals.avg_execution_time
        ).filter(
            AggregatedTotals.created_at >= start,
            AggregatedTotals.created_at <= end
        ).order_by(AggregatedTotals.created_at)
        
        # Add client_id filter if provided
        if request.client_id:
            query = query.filter(AggregatedTotals.client_id == request.client_id)
            
        results = query.all()
        
        # Format the results for the chart
        return [{
            "date": result.created_at.strftime("%Y-%m-%d"),
            "conversations": result.total_conversations,
            "tokens": result.total_tokens,
            "avg_duration": result.avg_execution_time
        } for result in results]
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

class RecentConversationsRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    client_id: Optional[str] = None
    limit: Optional[int] = 10

@app.post("/recent-conversations")
async def get_recent_conversations(
    request: RecentConversationsRequest,
    db: Session = Depends(get_db)
):
    try:
        # Build base query
        query = db.query(ConversationDump).order_by(ConversationDump.created_at.desc())
        
        # Apply filters if provided
        if request.client_id:
            query = query.filter(ConversationDump.client_id == request.client_id)
            
        if request.start_date:
            start = datetime.strptime(request.start_date, "%Y-%m-%d")
            query = query.filter(ConversationDump.created_at >= start)
            
        if request.end_date:
            end = datetime.strptime(request.end_date, "%Y-%m-%d")
            query = query.filter(ConversationDump.created_at <= end)
        
        # Apply limit
        results = query.limit(request.limit).all()
        
        # Format the results
        return [{
            "conversation_id": conv.conversation_id,
            "content": conv.content,
            "created_at": conv.created_at.isoformat(),
            "client_id": conv.client_id
        } for conv in results]
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

class ConversationInsightsRequest(BaseModel):
    conversation_ids: List[str]
    client_id: Optional[str] = None

@app.post("/conversation-insights")
async def get_conversation_insights(
    request: ConversationInsightsRequest,
    db: Session = Depends(get_db)
):
    try:
        # Build base query
        query = db.query(ConversationInsights).filter(
            ConversationInsights.conversation_id.in_(request.conversation_ids)
        )
        
        # Add client_id filter if provided
        if request.client_id:
            query = query.filter(ConversationInsights.client_id == request.client_id)
            
        results = query.all()
        
        # Format the results
        return [{
            "conversation_id": insight.conversation_id,
            "client_id": insight.client_id,
            "sentiment": insight.sentiment,
            "sentiment_quote": insight.sentiment_quote,
            "is_flagged": insight.is_flagged,
            "flag_reason": insight.flag_reason,
            "flag_severity": insight.flag_severity,
            "flag_type": insight.flag_type,
            "flag_quote": insight.flag_quote,
            "has_feedback": insight.has_feedback,
            "feedback_type": insight.feedback_type,
            "feedback_impact": insight.feedback_impact,
            "feedback_quote": insight.feedback_quote,
            "start_time": insight.start_time.isoformat(),
            "end_time": insight.end_time.isoformat(),
            "duration_seconds": insight.duration_seconds
        } for insight in results]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
