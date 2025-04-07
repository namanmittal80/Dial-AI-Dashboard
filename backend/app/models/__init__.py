# Import and expose all model classes
from app.models.aggregated_totals import AggregatedTotals
from app.models.messages import Message  # Assuming this file exists
from app.models.conversation_dump import ConversationDump  # Assuming this file exists
from app.models.client_config import ClientConfig  # Assuming this file exists
from app.models.conversation_insights import ConversationInsights  # Assuming this file exists
# You can add __all__ to control what's imported with "from app.models import *"
__all__ = ['Base', 'AggregatedTotals', 'Message', 'ConversationDump', 'ClientConfig']

# If Base is defined in one of your model files, import it here as well
# For example: from app.models.base import Base
# OR if Base is from SQLAlchemy and defined in database:
from app.database import Base