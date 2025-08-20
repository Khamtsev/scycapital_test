from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.tasks.models import Task
from app.tasks.schemas import TaskStatus, TaskCreate, TaskUpdate


class TaskService:
    """Сервис для работы с задачами."""

    @staticmethod
    def create_task(db: Session, task_data: TaskCreate) -> Task:
        """Создать новую задачу."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task(db: Session, task_id: UUID) -> Optional[Task]:
        """Получить задачу по ID."""
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_tasks(
        db: Session,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Получить список задач с фильтрацией и пагинацией."""
        query = db.query(Task)

        if status:
            query = query.filter(Task.status == status)

        return query.order_by(desc(Task.created_at)).offset(skip).limit(
            limit
        ).all()

    @staticmethod
    def update_task(
        db: Session, task_id: UUID, task_data: TaskUpdate
    ) -> Optional[Task]:
        """Обновить задачу."""
        task = TaskService.get_task(db, task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: UUID) -> bool:
        """Удалить задачу."""
        task = TaskService.get_task(db, task_id)
        if not task:
            return False

        db.delete(task)
        db.commit()
        return True
