import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.tasks.schemas import TaskStatus

# Московский timezone (UTC+3)
MOSCOW_TZ = timezone(timedelta(hours=3))


class Task(Base):
    """Модель задачи."""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(
        Enum(*[e.value for e in TaskStatus], name="task_status"),
        default=TaskStatus.CREATED.value,
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(MOSCOW_TZ),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(MOSCOW_TZ),
        onupdate=lambda: datetime.now(MOSCOW_TZ),
        nullable=False
    )
