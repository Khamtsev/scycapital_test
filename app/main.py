from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.tasks.routes import router as tasks_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(
    tasks_router,
    prefix=f"{settings.API_V1_STR}/tasks",
    tags=["tasks"]
)


@app.get("/")
def read_root():
    """Корневой эндпоинт."""
    return {"message": "Task Manager API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Проверка приложения."""
    return {"status": "healthy"}
