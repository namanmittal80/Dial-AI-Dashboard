import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base
from app.models import aggregated_totals, client_config, conversation_dump, messages

target_metadata = Base.metadata
