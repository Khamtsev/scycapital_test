"""Тесты для API эндпоинтов."""
from fastapi.testclient import TestClient

from app.tasks.schemas import TaskStatus

# Константа для несуществующего UUID
NONEXISTENT_UUID = "00000000-0000-0000-0000-000000000000"


class TestTasksAPI:
    """Тесты для API задач."""

    def test_create_task(self, client: TestClient):
        """Тест создания задачи."""
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "status": TaskStatus.CREATED.value
        }

        response = client.post("/api/v1/tasks/", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_minimal(self, client: TestClient):
        """Тест создания задачи с минимальными данными."""
        task_data = {"title": "Минимальная задача"}

        response = client.post("/api/v1/tasks/", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] is None
        assert data["status"] == TaskStatus.CREATED.value

    def test_get_tasks_list(self, client: TestClient):
        """Тест получения списка задач."""
        # Создаем несколько задач
        tasks_data = [
            {"title": "Задача 1", "status": TaskStatus.CREATED.value},
            {"title": "Задача 2", "status": TaskStatus.IN_PROGRESS.value},
            {"title": "Задача 3", "status": TaskStatus.COMPLETED.value}
        ]

        for task_data in tasks_data:
            client.post("/api/v1/tasks/", json=task_data)

        response = client.get("/api/v1/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_get_task_by_id(self, client: TestClient):
        """Тест получения задачи по ID."""
        # Создаем задачу
        task_data = {
            "title": "Задача для получения",
            "description": "Описание",
            "status": TaskStatus.IN_PROGRESS.value
        }

        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Получаем задачу по ID
        response = client.get(f"/api/v1/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]

    def test_get_task_not_found(self, client: TestClient):
        """Тест получения несуществующей задачи."""
        response = client.get(f"/api/v1/tasks/{NONEXISTENT_UUID}")

        assert response.status_code == 404

    def test_update_task(self, client: TestClient):
        """Тест обновления задачи."""
        # Создаем задачу
        task_data = {"title": "Исходная задача"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Обновляем задачу
        update_data = {
            "title": "Обновленная задача",
            "status": TaskStatus.COMPLETED.value
        }

        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]

    def test_delete_task(self, client: TestClient):
        """Тест удаления задачи."""
        # Создаем задачу
        task_data = {"title": "Задача для удаления"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Удаляем задачу
        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 204

        # Проверяем, что задача удалена
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_update_task_not_found(self, client: TestClient):
        """Тест обновления несуществующей задачи."""
        # Пытаемся обновить несуществующую задачу
        update_data = {
            "title": "Обновленное название",
            "status": TaskStatus.COMPLETED.value
        }

        response = client.put(
            f"/api/v1/tasks/{NONEXISTENT_UUID}",
            json=update_data
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Задача не найдена"

    def test_delete_task_not_found(self, client: TestClient):
        """Тест удаления несуществующей задачи."""
        # Пытаемся удалить несуществующую задачу
        response = client.delete(
            f"/api/v1/tasks/{NONEXISTENT_UUID}"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Задача не найдена"

    def test_filter_by_status(self, client: TestClient):
        """Тест фильтрации по статусу."""
        # Создаем задачи с разными статусами
        tasks_data = [
            {"title": "Задача 1", "status": TaskStatus.CREATED.value},
            {"title": "Задача 2", "status": TaskStatus.IN_PROGRESS.value},
            {"title": "Задача 3", "status": TaskStatus.COMPLETED.value}
        ]

        for task_data in tasks_data:
            client.post("/api/v1/tasks/", json=task_data)

        # Фильтруем по статусу "в работе"
        response = client.get(
            f"/api/v1/tasks/?status={TaskStatus.IN_PROGRESS.value}"
        )

        assert response.status_code == 200
        data = response.json()
        assert all(task["status"] == TaskStatus.IN_PROGRESS.value for task in data)

    def test_pagination(self, client: TestClient):
        """Тест пагинации."""
        # Создаем 5 задач
        for i in range(5):
            task_data = {"title": f"Задача {i+1}"}
            client.post("/api/v1/tasks/", json=task_data)

        # Получаем первые 3 задачи
        response = client.get("/api/v1/tasks/?skip=0&limit=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_invalid_task_data(self, client: TestClient):
        """Тест валидации данных."""
        # Пустая строка
        task_data = {"title": ""}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422

        # Только пробелы
        task_data = {"title": "   "}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422

        # Слишком длинное название
        task_data = {"title": "a" * 101}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422

        # Неверный статус
        task_data = {"title": "Задача", "status": "неверный_статус"}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422
