from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.calendar.Calendar_DAL import CalendarDAL
from models.Calendar import AcceptedEventData, AcceptedEventCreated


class CalendarControl:
    def __init__(self, db_session: Session, calendar_dal: CalendarDAL):
        self.db_session = db_session
        self.calendar_dal = calendar_dal

    def get_calendar_events(self, tf_days: int, after_days: int) -> List[AcceptedEventData]:
        """
        Возвращает список записей календаря по диапазону дат
        """
        try:
            return self.calendar_dal.get_events_by_date_range(tf_days, after_days)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail="Нет событий за указанную дату!"
            )

    def get_events_with_filters(self, ids: Optional[str], types: Optional[str]) -> List[AcceptedEventData]:
        """
        Возвращает список событий с фильтрацией
        """
        try:
            # Парсим ID события
            id_list = None
            if ids and ids.strip():
                try:
                    id_list = [int(id_str.strip()) for id_str in ids.split(',') if id_str.strip()]
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Неверный формат ID. Используйте числа через запятую (например: '1,2,3')"
                    )

            # Парсим типы событий
            type_list = None
            if types and types.strip():
                try:
                    type_list = [int(type_str.strip()) for type_str in types.split(',') if type_str.strip()]
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Неверный формат типа. Используйте числа через запятую (например: '1,2')"
                    )

            return self.calendar_dal.get_events_by_filters(ids=id_list, types=type_list)
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Ошибка при получении событий"
            )

    def create_calendar_event(self, start: Optional[int], name: str, 
                             note: Optional[str], event_type: int) -> AcceptedEventCreated:
        """
        Создает новое событие календаря
        """
        try:
            # Конвертируем Unix timestamp в datetime или используем текущее время
            if start is not None:
                start_datetime = datetime.fromtimestamp(start)
            else:
                start_datetime = datetime.now()

            return self.calendar_dal.create_event(start_datetime, name, note, event_type)
            
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail="Неверный формат даты. Используйте Unix timestamp в секундах"
            )
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Ошибка при создании события"
            )
