import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/task_manager"
    )

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Manager API"

    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]


settings = Settings()
