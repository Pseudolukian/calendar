# {{ endpoints.event }}

**HTTP-метод**: 🔴 POST  
**Endpoint**: `/{{ endpoints.event }}`  
**Описание**: `{{ endpoints.event }}` записывает объект `event` в базу данных и возвращает сообщение об успешном создании события:
```json
{
  "message": "Success created event id 88"
}
```
**Параметры**:  

| Название | Тип | Описание | Обязательность |
|----------|-----|----------|----------------|
|`Start`   | `int` | Unix timestamp в секундах (по умолчанию - текущее время). При значении поля меньше текущего времени пользователя — будет возвращена ошибка: `You input wrong Start time`. | Нет. |
| `Name`  | `str` | Название события. | Да. |  
| `Note`  | `str` | Описание события. | Нет. |  
| `Type`  | `int` | Тип событий: 0 — Все, 1 — Личное, 2 — Семья, 3 — Работа, 4 — Нет типа. Если значение будет указано вне диапазона 0-4 — будет возвращена ошибка: `Input should be less than or equal to 4`. | Нет. | 

## CURL: примеры использования {{ endpoints.event }}


!!! note "В календаре могут быть созданы несколько событий с одинаковым временем начала"

    {{ endpoints.event }} не предоставляет механизм предотвращения наложения событий по времени.
    

=== "Создать событие 26.07.2025 в 12:00"

    **Параметры**:  
        - `Start`=1721988000  
        - `Name`=Meeting  
        - `Note`=Prepare slides  
        - `Type`=1  

    **Запрос**:
    ```curl
    curl -X 'POST' \
    'http://localhost:8000/api/Event?Start=1721988000&Name=Meeting&Note=Prepare%20slides&Type=1' \
    -H 'accept: application/json' \
    -d ''
    ```

    **Ответ**:
    ```json
    {
    "message": "Success created event id 90"
    }
    ```

=== "Создать событие 30 июля 2025, 13:00:00"

    **Параметры**:  
        - `Start`=1722339600  
        - `Name`=Python lection  
        - `Note`=Decorators  
        - `Type`=3  
    
    **Запрос**:
    ```curl
    curl -X 'POST' \
    'http://localhost:8000/api/Event?Start=1722339600&Name=Python%20lection&Note=Decorators&Type=3' \
    -H 'accept: application/json' \
    -d ''
    ```

    **Ответ**:
    ```json
    {
    "message": "Success created event id 91"
    }
    ```

## OpenAPI спецификация

[OAD(./docs/openapi/event.json)]