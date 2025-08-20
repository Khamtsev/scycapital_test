from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from enum import Enum


class TaskStatus(str, Enum):
    """Enum для статусов задачи."""
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class TaskBase(BaseModel):
    """Базовая схема для задачи."""
    title: str = Field(max_length=100, description="Название задачи")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание задачи"
    )
    status: TaskStatus = Field(
        default=TaskStatus.CREATED, description="Статус задачи"
    )

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v):
        """Валидация названия задачи - не может быть пустым или содержать только пробелы."""
        stripped = v.strip()
        if not stripped:
            raise ValueError(
                'Заголовок не может быть пустым или содержать только пробелы.'
            )
        return stripped


class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи."""
    title: Optional[str] = Field(
        None, max_length=100, description="Название задачи"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание задачи"
    )
    status: Optional[TaskStatus] = Field(None, description="Статус задачи")


class TaskResponse(TaskBase):
    """Схема для ответа с задачей."""
    id: UUID = Field(description="UUID задачи")
    created_at: datetime = Field(description="Дата создания")
    updated_at: datetime = Field(description="Дата обновления")

    model_config = {
        "from_attributes": True
    }
