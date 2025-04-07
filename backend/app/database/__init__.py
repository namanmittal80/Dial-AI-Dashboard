# Import and expose database components
from sqlalchemy.ext.declarative import declarative_base

# Create Base instance that models will inherit from
Base = declarative_base()

# Export any database-related functions or classes
__all__ = ['Base']