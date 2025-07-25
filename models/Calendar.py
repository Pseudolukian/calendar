from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from connect.sqlite import Base

#================== SQLAlchemy model =======================#

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime, nullable=False, index=True)
    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    type = Column(Integer, nullable=False)

#================== Input data models =======================#

class EventGetByDateRange(BaseModel):
    tf_days: int = Field(default=0, description="Days from today to start filtering")
    after_days: int = Field(default=0, description="Days from today to end filtering")

class EventGetByFilters(BaseModel):
    ids: Optional[str] = Field(default=None, description="Comma-separated list of event IDs")
    isArchive: Optional[bool] = Field(default=False, description="Filter archived events")
    type: Optional[str] = Field(default=None, description="Comma-separated list of event types")

class EventCreate(BaseModel):
    Start: Optional[int] = Field(default=None, description="Event start date as Unix timestamp (seconds)")
    Name: str = Field(..., description="Event name")
    Note: Optional[str] = Field(default=None, description="Event note")
    Type: int = Field(default=0, description="Event type")

#=================== Response data models =======================#

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class AcceptedEventData(TunedModel):
    id: int
    start: datetime 
    name: str
    note: Optional[str] = None
    type: int

class AcceptedEventCreated(TunedModel):
    message: str