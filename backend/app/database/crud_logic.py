from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models import Message, ConversationDump, AggregatedTotals, ClientConfig, ConversationInsights as ConversationInsightsModel
from app.insights import ConversationInsights as ConversationAnalyzer
import json

def insert_messages(db: Session, payload):
    now = datetime.utcnow()
    for msg in payload.messages:
        message = Message(
            id=uuid4(),
            client_id=payload.client_id,
            conversation_id=payload.session_id,
            message_index=msg.message_index,
            timestamp=payload.start_time,
            role=msg.role,
            text=msg.text,
            created_at=now,
            updated_at=now,
            created_by="api",
            updated_by="api"
        )
        db.add(message)

def insert_conversation_dump(db: Session, payload):
    # Convert message objects to dict
    message_dicts = []
    for m in payload.messages:
        message_dicts.append(m.dict())
    
    content = {
        "messages": message_dicts,
    }

    dump = ConversationDump(
        id=uuid4(),
        client_id=payload.client_id,
        conversation_id=payload.session_id,
        content=content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by="api",
        updated_by="api"
    )
    db.add(dump)


def generate_conversation_insights_data(db: Session, payload):
    # Initialize insights object with the analyzer class
    insights = ConversationAnalyzer()
    
    # Format conversation history for analysis
    conversation_text = ""
    for msg in payload.messages:
        conversation_text += f"{msg.role.capitalize()}: {msg.text}\n"
    
    # Get sentiment analysis
    sentiment_result = insights._get_conversation_sentiment(conversation_text, payload.session_id)
    sentiment = sentiment_result["sentiment"] if sentiment_result else "negative"
    sentiment_quote = sentiment_result["supporting_quotes"][0] if sentiment_result and sentiment_result["supporting_quotes"] else ""

    # Get flags analysis
    flag_result = insights._get_conversation_flags(conversation_text, payload.session_id)
    is_flagged = bool(flag_result)
    flag_reason = flag_result["flag_reason"] if flag_result else ""
    flag_severity = flag_result["severity"] if flag_result else ""
    flag_type = flag_result["issue_type"] if flag_result else ""
    flag_quote = flag_result["relevant_quotes"][0] if flag_result and flag_result["relevant_quotes"] else ""

    # Get feedback analysis
    feedback_result = insights._get_conversation_feedback(conversation_text, payload.session_id)
    has_feedback = bool(feedback_result)
    feedback_type = feedback_result["feedback_type"] if feedback_result else ""
    feedback_impact = feedback_result["impact"] if feedback_result else ""
    feedback_quote = feedback_result["supporting_quotes"][0] if feedback_result and feedback_result["supporting_quotes"] else ""

    # Use provided timestamps and calculate duration
    start_time = payload.start_time
    end_time = payload.end_time
    duration_seconds = int((end_time - start_time).total_seconds())

    return {
        "client_id": payload.client_id,
        "conversation_id": payload.session_id,
        "sentiment": sentiment,
        "sentiment_quote": sentiment_quote,
        "is_flagged": is_flagged,
        "flag_reason": flag_reason,
        "flag_severity": flag_severity,
        "flag_type": flag_type,
        "flag_quote": flag_quote,
        "has_feedback": has_feedback,
        "feedback_type": feedback_type,
        "feedback_impact": feedback_impact,
        "feedback_quote": feedback_quote,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration_seconds
    }


def insert_conversation_insights(db: Session, payload):
    insights_data = generate_conversation_insights_data(db, payload)
    
    # Create ConversationInsights instance with generated data
    now = datetime.utcnow()
    insights = ConversationInsightsModel(  # Use the model class here
        client_id=insights_data["client_id"],
        conversation_id=insights_data["conversation_id"],
        sentiment=insights_data["sentiment"],
        sentiment_quote=insights_data["sentiment_quote"],
        is_flagged=insights_data["is_flagged"],
        flag_reason=insights_data["flag_reason"],
        flag_severity=insights_data["flag_severity"],
        flag_type=insights_data["flag_type"],
        flag_quote=insights_data["flag_quote"],
        has_feedback=insights_data["has_feedback"],
        feedback_type=insights_data["feedback_type"],
        feedback_impact=insights_data["feedback_impact"],
        feedback_quote=insights_data["feedback_quote"],
        start_time=insights_data["start_time"],
        end_time=insights_data["end_time"],
        duration_seconds=insights_data["duration_seconds"],
        created_at=now,
        updated_at=now
    )
    db.add(insights)

def update_aggregated_totals(db: Session, payload):
    now = datetime.utcnow()
    # Calculate total metrics from message data
    total_tokens = 0
    
    existing = db.query(AggregatedTotals).filter_by(client_id=payload.client_id).first()

    if existing:
        # update values
        existing.total_tokens += total_tokens
        existing.total_conversations += 1
        existing.updated_at = now
        existing.updated_by = "api"
    else:
        # insert new
        new = AggregatedTotals(
            id=uuid4(),
            client_id=payload.client_id,
            client_name=payload.client_name,
            total_tokens=total_tokens,
            total_conversations=1,
            created_at=now,
            updated_at=now,
            created_by="api",
            updated_by="api"
        )
        db.add(new)

def initialize_client(db: Session, payload):
    config = ClientConfig(
        id=uuid4(),
        client_id=payload.client_id,
        client_name=payload.client_name,
        client_config=payload.client_config,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by="api",
        updated_by="api"
    )
    db.add(config)
