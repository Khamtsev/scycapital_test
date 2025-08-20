"""Общие фикстуры для тестов."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base


@pytest.fixture
def db_engine():
    """Создание движка для тестовой БД PostgreSQL."""
    # Используем отдельную тестовую БД
    database_url = (
        "postgresql://postgres:password@localhost:5433/test_task_manager"
    )

    # Создаем движок
    engine = create_engine(database_url)

    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture
def db_session(db_engine):
    """Сессия тестовой БД."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )

    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    """Тестовый клиент FastAPI."""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
