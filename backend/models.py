from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    variant = Column(String, index=True)
    event_type = Column(String)  # "click", "conversion"
    plan = Column(String, nullable=True)
    revenue = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
