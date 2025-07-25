#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных в базу данных календаря
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from connect.sqlite import SessionLocal, create_tables
from models.Calendar import Event


def load_events_from_json(filename: str = "test_events.json") -> List[Dict[str, Any]]:
    """
    Загружает события из JSON файла
    
    Args:
        filename: Имя JSON файла с событиями
        
    Returns:
        Список словарей с данными событий
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON: {e}")
        return []


def add_events_to_db(data_to_db: List[Dict[str, Any]]):
    """
    Добавляет события в базу данных
    
    Args:
        data_to_db: Список словарей с данными событий
    """
    # Создаем таблицы если их нет
    create_tables()
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        for event_data in data_to_db:
            # Парсим дату
            if isinstance(event_data["Start"], str):
                # Если дата в формате строки, парсим её
                date_part = datetime.strptime(event_data["Start"], "%Y-%m-%d").date()
                # Добавляем случайное время (от 8:00 до 20:00)
                random_hour = random.randint(8, 20)
                random_minute = random.choice([0, 15, 30, 45])
                start_datetime = datetime.combine(date_part, datetime.min.time().replace(
                    hour=random_hour, 
                    minute=random_minute
                ))
            else:
                start_datetime = event_data["Start"]
            
            # Создаем событие
            new_event = Event(
                start=start_datetime,
                name=event_data["Name"],
                note=event_data.get("Note", ""),
                type=event_data.get("Type", 0)
            )
            
            db.add(new_event)
            print(f"Добавлено событие: {new_event.name} на {start_datetime}")
        
        # Сохраняем изменения
        db.commit()
        print(f"\nУспешно добавлено {len(data_to_db)} событий в базу данных!")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        db.close()


def show_all_events():
    """
    Показывает все события в базе данных
    """
    db = SessionLocal()
    try:
        events = db.query(Event).order_by(Event.start).all()
        print(f"\nВсего событий в БД: {len(events)}")
        print("-" * 50)
        
        for event in events:
            print(f"ID: {event.id}")
            print(f"Дата: {event.start}")
            print(f"Название: {event.name}")
            print(f"Заметка: {event.note}")
            print(f"Тип: {event.type}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        db.close()


def clear_all_events():
    """
    Очищает все события из базы данных
    """
    db = SessionLocal()
    try:
        count = db.query(Event).count()
        db.query(Event).delete()
        db.commit()
        print(f"Удалено {count} событий из базы данных")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при очистке данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("=== Управление тестовыми данными календаря ===")
    
    # Загружаем события из JSON
    data_to_db = load_events_from_json()
    
    if not data_to_db:
        print("Нет данных для добавления")
        exit(1)
    
    print(f"Загружено {len(data_to_db)} событий из JSON файла")
    
    # Спрашиваем пользователя, что делать
    action = input("\nВыберите действие:\n1. Добавить события (сохранив существующие)\n2. Очистить БД и добавить события\n3. Показать текущие события\n4. Очистить БД\nВведите номер (1-4): ")
    
    if action == "1":
        print("\n=== Добавление новых событий ===")
        add_events_to_db(data_to_db)
        
    elif action == "2":
        print("\n=== Очистка БД и добавление событий ===")
        clear_all_events()
        add_events_to_db(data_to_db)
        
    elif action == "3":
        print("\n=== Все события в базе данных ===")
        show_all_events()
        
    elif action == "4":
        print("\n=== Очистка БД ===")
        clear_all_events()
        
    else:
        print("Неверный выбор!")
        exit(1)
    
    print("\n=== Анализ фильтрации ===")
    now = datetime.now()
    print(f"Текущее время: {now}")
    print(f"tf_days=1 означает: события начиная с {now + timedelta(days=1)}")
    print(f"after_days=7 означает: события до {now + timedelta(days=7)}")
    print("Для получения событий на сегодня используйте tf_days=0, after_days=1")
    print("Для получения событий за прошлую неделю используйте tf_days=-7, after_days=0")
