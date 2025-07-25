from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import time
from pydantic import ValidationError

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
        description="Количество дней от текущей даты для начала фильтрации (0 — с завтрашнего дня, -1 — с сегодняшнего дня, 1 — с послезавтрашнего дня)"
    ),
    after_days: int = Query(
        default=0, 
        description="Количество дней от текущей даты для окончания фильтрации (0 = до следующей недели, 1 = до завтра, 7 = до следующей недели и т.д.)"
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
        description="ID событий через запятую (например, '1,2,3')"
    ),
    isArchive: Optional[bool] = Query(
        default=False, 
        description="Показывать прошедшие события"
    ),
    type: Optional[str] = Query(
        default=None, 
        description="Тип событий через запятую (например, '1,2')"
    ),
    db: Session = Depends(get_db)
) -> List[AcceptedEventData]:
    """
    Возвращает список событий с возможностью фильтрации по ID, архивному статусу и типу.
    
    Типы событий: 
    - 0 — Все
    - 1 — Личное
    - 2 — Семья
    - 3 — Работа
    - 4 — Нет типа.
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
        description="Unix timestamp в секундах (опционально, по умолчанию - текущее время)",
        ge=0
    ),
    Name: str = Query(..., description="Название события"),
    Note: Optional[str] = Query(default=None, description="Описание события"),
    Type: int = Query(default=0, description="Тип событий: 0 — Все, 1 — Личное, 2 — Семья, 3 — Работа, 4 — Нет типа.", ge=0, le=4),
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
    # Проверяем, что Start не в прошлом
    if Start is not None:
        current_timestamp = int(time.time())
        if Start < current_timestamp:
            raise HTTPException(
                status_code=400,
                detail=f"Вы ввели неверное время начала. Время начала не может быть в прошлом. Текущий timestamp: {current_timestamp}, указано: {Start}"
            )
    
    calendar_dal = CalendarDAL(db_session=db)
    calendar_control = CalendarControl(db_session=db, calendar_dal=calendar_dal)
    
    # Создаем объект без дополнительной валидации
    try:
        return calendar_control.create_calendar_event(
            start=Start,
            name=Name,
            note=Note,
            event_type=Type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания события: {str(e)}")

