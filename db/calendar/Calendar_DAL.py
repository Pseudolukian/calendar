from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import List, Optional

from models.Calendar import Event, AcceptedEventData, AcceptedEventCreated


class CalendarDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_events_by_date_range(self, tf_days: int, after_days: int) -> List[AcceptedEventData]:
        """
        Получает события в указанном диапазоне дат
        Логика соответствует оригинальной C# версии:
        - tf_days = 0 означает tf_days = 1 (завтра)
        - after_days = 0 означает after_days = 7 (неделя вперед)
        """
        # Применяем оригинальную логику из C#
        actual_tf_days = 1 if tf_days == 0 else tf_days
        actual_after_days = 7 if after_days == 0 else after_days
        
        start_date = datetime.now() + timedelta(days=actual_tf_days)
        end_date = datetime.now() + timedelta(days=actual_after_days)
        
        query = select(Event).where(
            Event.start > start_date,
            Event.start < end_date
        )
        
        events = self.db_session.execute(query).scalars().all()
        return [AcceptedEventData.model_validate(event) for event in events]

    def get_events_by_filters(self, ids: Optional[List[int]] = None, 
                             types: Optional[List[int]] = None) -> List[AcceptedEventData]:
        """
        Получает события по фильтрам
        """
        query = select(Event)
        
        if ids:
            query = query.where(Event.id.in_(ids))
        
        if types:
            query = query.where(Event.type.in_(types))
        
        events = self.db_session.execute(query).scalars().all()
        return [AcceptedEventData.model_validate(event) for event in events]

    def create_event(self, start_datetime: datetime, name: str, 
                    note: Optional[str], event_type: int) -> AcceptedEventCreated:
        """
        Создает новое событие
        """
        new_event = Event(
            start=start_datetime,
            name=name,
            note=note,
            type=event_type
        )
        
        self.db_session.add(new_event)
        self.db_session.commit()
        self.db_session.refresh(new_event)
        
        return AcceptedEventCreated(message=f"Success created event id {new_event.id}")
