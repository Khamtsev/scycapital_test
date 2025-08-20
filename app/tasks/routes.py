from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.tasks.schemas import TaskStatus, TaskCreate, TaskResponse, TaskUpdate
from app.tasks.service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """Создать новую задачу."""
    task = TaskService.create_task(db, task_data)
    return TaskResponse.model_validate(task)


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[TaskStatus] = Query(
        None, description="Фильтр по статусу"
    ),
    skip: int = Query(
        0, ge=0, description="Количество записей для пропуска"
    ),
    limit: int = Query(
        100, ge=1, le=1000, description="Максимальное количество записей"
    ),
    db: Session = Depends(get_db)
) -> List[TaskResponse]:
    """Получить список задач с фильтрацией и пагинацией."""
    tasks = TaskService.get_tasks(db, status=status, skip=skip, limit=limit)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """Получить задачу по ID."""
    task = TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """Обновить задачу."""
    task = TaskService.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """Удалить задачу."""
    success = TaskService.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
