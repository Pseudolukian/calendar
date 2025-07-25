from fastapi import FastAPI, APIRouter
import uvicorn

from routers.calendar import calendar_router

# Создаем основной роутер
main_api_router = APIRouter()
app = FastAPI(title="Calendar API", version="0.1.0")

# Подключаем календарный роутер с префиксом и тегом
main_api_router.include_router(calendar_router, prefix="/api", tags=["calendar"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=False)