# {{ endpoints.events }}

**HTTP-метод**: 🟢 GET  
**Endpoint**: `/{{ endpoints.events }}`  
**Описание**: `{{ endpoints.events }}` возвращает список событий с возможностью фильтрации по полям: `ids`, `isArchive`, `type`.  
**Параметры**:  

| Название | Тип | Описание | Обязательность |
|----------|-----|----------|----------------|
|`ids`     |`int`| `id` событий через запятую. Если `id` события или событий в базе нет — будет возвращён пустой список.| Нет |  
|`isArchive` | `bool` | Показывать прошедшие события. | Нет. |  
| `type` | `int` | Тип событий: 0 — Все, 1 — Личное, 2 — Семья, 3 — Работа, 4 — Нет типа. Если значение будет указано вне диапозона 0-4 — будет возвращена ошибка: `Input should be less than or equal to 4`. | Нет. | 

Если не передать параметры в {{ endpoints.events }} — будут возвращены все события календаря.

## CURL: примеры использования {{ endpoints.events }}

=== "Запрос без параметров"

    **Параметры**:  
        - `ids` = None  
        - `isArchive` = None  
        - `type` = None  

    **Запрос**:  
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Events' \
    -H 'accept: application/json'
    ``` 

    **Ответ**:  
    ```json
    [
        {
            "id": 1,
            "start": "2025-07-24T16:28:25.285145",
            "name": "Meeting",
            "note": "My meeting",
            "type": 1
        },
        {
            "id": 2,
            "start": "2025-07-24T16:28:54.590199",
            "name": "FunChart",
            "note": "Simple fun",
            "type": 2
        }
    ]
    ```

=== "IDs = (2,3), остальные параметры None"

    **Параметры**:  
        - `ids` = 2,3  
        - `isArchive` = None  
        - `type` = None  

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Events?ids=2%2C3' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 2,
            "start": "2025-07-24T16:28:54.590199",
            "name": "FunChart",
            "note": "Simple fun",
            "type": 2
        },
        {
            "id": 3,
            "start": "2025-06-24T10:00:00",
            "name": "Планирование спринта",
            "note": "Планирование задач на июльский спринт",
            "type": 1
        }
    ]
    ```

=== "Ids = None, isArchive = false, type = 1,2"

    **Параметры**:  
        - `ids` = None  
        - `isArchive` = false  
        - `type` = 1,2  

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Events?isArchive=false&type=1%2C2' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 1,
            "start": "2025-07-24T16:28:25.285145",
            "name": "Meeting",
            "note": "My meeting",
            "type": 1
        },
        {
            "id": 2,
            "start": "2025-07-24T16:28:54.590199",
            "name": "Code Review",
            "note": "Review new features",
            "type": 2
        }
    ]
    ```

=== "Все типы событий"

    **Параметры**:  
        - `ids` = None  
        - `isArchive` = false  
        - `type` = 0,1,2,3,4  

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Events?isArchive=false&type=0%2C1%2C2%2C3%2C4' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 10,
            "start": "2025-07-25T09:00:00",
            "name": "General Event",
            "note": "Default type event",
            "type": 0
        },
        {
            "id": 11,
            "start": "2025-07-25T10:30:00",
            "name": "Team Meeting",
            "note": "Weekly planning session",
            "type": 1
        },
        {
            "id": 12,
            "start": "2025-07-25T14:00:00",
            "name": "Bug Fix Session",
            "note": "Fix critical issues",
            "type": 2
        },
        {
            "id": 13,
            "start": "2025-07-25T16:00:00",
            "name": "Product Demo",
            "note": "Show new features to stakeholders",
            "type": 3
        },
        {
            "id": 14,
            "start": "2025-07-25T18:00:00",
            "name": "Team Dinner",
            "note": "Informal team building",
            "type": 4
        }
    ]
    ```

=== "Архивные события (isArchive = true)"

    **Параметры**:  
        - `ids` = None  
        - `isArchive` = true  
        - `type` = None  

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Events?isArchive=true' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 5,
            "start": "2025-07-20T10:00:00",
            "name": "Past Meeting",
            "note": "Completed planning session",
            "type": 1
        },
        {
            "id": 6,
            "start": "2025-07-21T15:00:00",
            "name": "Old Demo",
            "note": "Previous sprint demo",
            "type": 3
        }
    ]
    ```    

## OpenAPI спецификация

[OAD(./docs/openapi/events.json)]    