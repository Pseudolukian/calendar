# 🟢 GET {{ endpoints.calendar }}

## Общие сведения об {{ endpoints.calendar }}

**HTTP-метод**: GET  
**Endpoint**: `/{{ endpoints.calendar }}`  
**Описание**: `{{ endpoints.calendar }}` возвращает список отфильтрованных по дате старта записей календаря в JSON-формате.  
**Параметры**:  

- tf_days [int]: Количество дней от текущей даты для начала фильтрации (0 — с завтрашнего дня, -1 — с сегодняшнего дня, 1 — с завтрашнего дня), необязательный параметр.
- after_days [int]: Количество дней от текущей даты для окончания фильтрации (0 = до следующей недели, 1 = до завтра, 7 = до следующей недели и т.д.), необязательный параметр. 

По умалчанию возвращаются события с завтрашнего дня на неделю (tf_days = 0, after_days = 0):

```json
[
{
    "id": 46,
    "start": "2025-07-24T09:30:00",
    "name": "Планирование отпусков",
    "note": "Составление графика отпусков на август",
    "type": 1
},
{
    "id": 44,
    "start": "2025-07-24T11:45:00",
    "name": "Встреча с командой",
    "note": "Обсуждение проекта календаря",
    "type": 1
},
{
    "id": 45,
    "start": "2025-07-24T15:15:00",
    "name": "Код-ревью новых фич",
    "note": "Проверка FastAPI endpoints",
    "type": 2
}
]
```

## CURL: примеры использования {{ endpoints.calendar }}

=== "События с завтра на неделю (DEFAULT)"

    **Параметры**: `tf_days=0`, `after_days=0`.
    
    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Calendar?tf_days=0&after_days=0' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 49,
            "start": "2025-07-26T16:00:00",
            "name": "Демо для клиента",
            "note": "Показ готовой функциональности",
            "type": 3
        },
        {
            "id": 52,
            "start": "2025-07-28T11:00:00",
            "name": "Изучение GraphQL",
            "note": "Исследование возможности добавления GraphQL API",
            "type": 2
        }
    ]
    ```

=== "События с сегодня на неделю"

    **Параметры**: `tf_days=-1`, `after_days=0`.

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Calendar?tf_days=-1&after_days=0' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 44,
            "start": "2025-07-24T11:45:00",
            "name": "Встреча с командой",
            "note": "Обсуждение проекта календаря",
            "type": 1
        },
        {
            "id": 45,
            "start": "2025-07-24T15:15:00",
            "name": "Код-ревью новых фич",
            "note": "Проверка FastAPI endpoints",
            "type": 2
        }
    ]
    ```

=== "Cобытия за прошлую неделю до вчера"
    
    **Параметры**: `tf_days=-7`, `after_days=-1`.

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Calendar?tf_days=-7&after_days=-1' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 37,
            "start": "2025-07-18T16:00:00",
            "name": "Пятничные деплои",
            "note": "Еженедельный релиз в продакшн",
            "type": 2
        },
        {
            "id": 38,
            "start": "2025-07-21T16:15:00",
            "name": "Аналитика использования",
            "note": "Анализ метрик пользователей API",
            "type": 1
        }
    ]
    ```

=== "Cобытия с завтра на неделю"

    **Параметры**: `tf_days=1`, `after_days=7`.

    **Запрос**:
    ```curl
    curl -X 'GET' \
    'http://localhost:8000/api/Calendar?tf_days=1&after_days=7' \
    -H 'accept: application/json'
    ```

    **Ответ**:
    ```json
    [
        {
            "id": 53,
            "start": "2025-07-29T11:00:00",
            "name": "Разработка webhook'ов",
            "note": "Создание системы уведомлений через webhooks",
            "type": 2
        },
        {
            "id": 55,
            "start": "2025-07-30T18:30:00",
            "name": "Автоматизация тестов",
            "note": "Настройка автоматического тестирования",
            "type": 2
        }
    ]
    ```




Если событий в указанный период времени нет — вернётся пустой список:

```
[]
```

Если в параметр `tfdays` или `afterDays` будет передан не `int` — вернётся ошибка:

```json
{
    "detail":[{
            "type":"int_parsing",
            "loc":["query","tf_days"],
            "msg":"Input should be a valid integer, unable to parse string as an integer",
            "input":"\"dsada\""
        }]
}
```
## OpenAPI спецификация

[OAD(./docs/openapi/calendar.json)]