from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from models.Calendar import (
    AcceptedEventData, 
    AcceptedEventCreated, 
    EventCreate
)
from connect.sqlite import get_db
from db.calendar.Calendar_DAL import CalendarDAL
from controls.calendar.Calendar_controls import CalendarControl

calendar_router = APIRouter()


@calendar_router.get("/Calendar", response_model=List[AcceptedEventData])
def get_calendar(
    tf_days: int = Query(
        default=0, 
        description="Days from today to start filtering (0 = tomorrow, -1 = today, 1 = tomorrow, etc.)"
    ),
    after_days: int = Query(
        default=0, 
        description="Days from today to end filtering (0 = next week, 1 = tomorrow, 7 = next week)"
    ),
    db: Session = Depends(get_db)
) -> List[AcceptedEventData]:
    
    calendar_dal = CalendarDAL(db_session=db)
    calendar_control = CalendarControl(db_session=db, calendar_dal=calendar_dal)
    
    return calendar_control.get_calendar_events(
        tf_days=tf_days,
        after_days=after_days
    )


@calendar_router.get("/Events", response_model=List[AcceptedEventData])
def get_events(
    ids: Optional[str] = Query(
        default=None, 
        description="Comma-separated list of event IDs (e.g., '1,2,3')"
    ),
    isArchive: Optional[bool] = Query(
        default=False, 
        description="Filter archived events (currently not implemented)"
    ),
    type: Optional[str] = Query(
        default=None, 
        description="Comma-separated list of event types (e.g., '1,2')"
    ),
    db: Session = Depends(get_db)
) -> List[AcceptedEventData]:
    """
    Возвращает список событий с возможностью фильтрации по ID, архивному статусу и типу.
    
    Типы событий:
    - 1: Встречи/планерки
    - 2: Разработка/техническая работа  
    - 3: Демо/презентации
    - 4: Неформальные события
    """
    calendar_dal = CalendarDAL(db_session=db)
    calendar_control = CalendarControl(db_session=db, calendar_dal=calendar_dal)
    
    return calendar_control.get_events_with_filters(
        ids=ids,
        types=type
    )


@calendar_router.post("/Event", response_model=AcceptedEventCreated)
def create_event(
    Start: Optional[int] = Query(
        default=None, 
        description="Event start date as Unix timestamp (seconds). If not provided - current time"
    ),
    Name: str = Query(..., description="Event name"),
    Note: Optional[str] = Query(default=None, description="Event note"),
    Type: int = Query(default=0, description="Event type (0=default, 1=meeting, 2=development, 3=demo, 4=informal)"),
    db: Session = Depends(get_db)
) -> AcceptedEventCreated:
    """
    Записывает event в BD и возвращает сообщение об успешном создании события
    
    Параметры:
    - Start: Unix timestamp в секундах (опционально, по умолчанию - текущее время)
    - Name: Название события (обязательно)
    - Note: Описание события (опционально)
    - Type: Тип события (0-4)
    """
    calendar_dal = CalendarDAL(db_session=db)
    calendar_control = CalendarControl(db_session=db, calendar_dal=calendar_dal)
    
    event_data = EventCreate(Start=Start, Name=Name, Note=Note, Type=Type)
    
    return calendar_control.create_calendar_event(
        start=event_data.Start,
        name=event_data.Name,
        note=event_data.Note,
        event_type=event_data.Type
    )

