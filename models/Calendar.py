from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import time
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
    tf_days: int = Field(default=0, description="Количество дней от текущей даты для начала фильтрации")
    after_days: int = Field(default=0, description="Количество дней от текущей даты для окончания фильтрации")

class EventGetByFilters(BaseModel):
    ids: Optional[str] = Field(default=None, description="ID событий через запятую")
    isArchive: Optional[bool] = Field(default=False, description="Показывать прошедшие события")
    type: Optional[str] = Field(default=None, description="Тип событий через запятую")

class EventCreate(BaseModel):
    Start: Optional[int] = Field(default=None, description="Unix timestamp в секундах (по умолчанию - текущее время)")
    Name: str = Field(..., description="Название события")
    Note: Optional[str] = Field(default=None, description="Описание события")
    Type: int = Field(default=0, description="Тип события (0-4)", ge=0, le=4)
    
    @field_validator('Start')
    @classmethod
    def validate_start_time(cls, v):
        if v is not None:
            current_timestamp = int(time.time())
            if v < current_timestamp:
                raise ValueError(f'Время начала не может быть в прошлом. Текущий timestamp: {current_timestamp}, указано: {v}')
        return v

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