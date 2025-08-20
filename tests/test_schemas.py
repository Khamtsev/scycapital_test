"""Тесты для Pydantic схем."""
import pytest
from pydantic import ValidationError

from app.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStatus


class TestTaskStatus:
    """Тесты для enum статусов задач."""

    def test_valid_statuses(self):
        """Тест валидных статусов."""
        assert TaskStatus.CREATED.value == "создано"
        assert TaskStatus.IN_PROGRESS.value == "в работе"
        assert TaskStatus.COMPLETED.value == "завершено"

    def test_status_enum_values(self):
        """Тест значений enum."""
        statuses = [status.value for status in TaskStatus]
        assert "создано" in statuses
        assert "в работе" in statuses
        assert "завершено" in statuses


class TestTaskCreate:
    """Тесты для схемы создания задачи."""

    def test_valid_task_create(self):
        """Тест валидного создания задачи."""
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание",
            "status": TaskStatus.IN_PROGRESS.value
        }

        task = TaskCreate(**task_data)
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.status == TaskStatus.IN_PROGRESS

    def test_task_create_minimal(self):
        """Тест создания задачи с минимальными данными."""
        task_data = {"title": "Минимальная задача"}

        task = TaskCreate(**task_data)
        assert task.title == task_data["title"]
        assert task.description is None
        assert task.status == TaskStatus.CREATED

    def test_task_create_with_whitespace(self):
        """Тест создания задачи с пробелами в названии."""
        task_data = {"title": "  Задача с пробелами  "}

        task = TaskCreate(**task_data)
        assert task.title == "Задача с пробелами"
        assert task.description is None
        assert task.status == TaskStatus.CREATED

    def test_task_create_invalid_title(self):
        """Тест невалидного названия."""
        # Пустая строка
        with pytest.raises(ValidationError):
            TaskCreate(title="")

        # Только пробелы
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

        # Слишком длинное название
        with pytest.raises(ValidationError):
            TaskCreate(title="a" * 101)

    def test_task_create_invalid_description(self):
        """Тест невалидного описания."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Задача", description="a" * 1001)

    def test_task_create_invalid_status(self):
        """Тест невалидного статуса."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Задача", status="неверный_статус")


class TestTaskUpdate:
    """Тесты для схемы обновления задачи."""

    def test_valid_task_update(self):
        """Тест валидного обновления задачи."""
        update_data = {
            "title": "Обновленное название",
            "status": TaskStatus.COMPLETED.value
        }

        task_update = TaskUpdate(**update_data)
        assert task_update.title == update_data["title"]
        assert task_update.status == TaskStatus.COMPLETED

    def test_task_update_partial(self):
        """Тест частичного обновления."""
        task_update = TaskUpdate(title="Новое название")
        assert task_update.title == "Новое название"
        assert task_update.description is None
        assert task_update.status is None

    def test_task_update_empty(self):
        """Тест пустого обновления."""
        task_update = TaskUpdate()
        assert task_update.title is None
        assert task_update.description is None
        assert task_update.status is None


class TestTaskResponse:
    """Тесты для схемы ответа задачи."""

    def test_task_response_creation(self):
        """Тест создания ответа задачи."""
        from datetime import datetime
        from uuid import uuid4

        task_id = uuid4()
        created_at = datetime.now()
        updated_at = datetime.now()

        response_data = {
            "id": task_id,
            "title": "Ответная задача",
            "description": "Описание",
            "status": TaskStatus.CREATED.value,
            "created_at": created_at,
            "updated_at": updated_at
        }

        task_response = TaskResponse(**response_data)
        assert task_response.id == task_id
        assert task_response.title == response_data["title"]
        assert task_response.created_at == created_at
        assert task_response.updated_at == updated_at
