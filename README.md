# Task Manager API

Веб-API для управления задачами.

## Функциональность

- CRUD операции для управления задачами
- Фильтрация задач по статусу
- Сортировка по дате создания
- Пагинация результатов
- Автоматическая документация API (Swagger)

## Технологии

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM
- **Alembic** - миграции базы данных
- **Pydantic** - валидация данных
- **Pytest** - тестирование

## Установка и запуск (Docker)

### 1. Клонирование репозитория

```bash
git clone git@github.com:Khamtsev/scycapital_test.git
cd task_manager
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

### 3. Запуск с Docker Compose

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## API Документация

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура проекта

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── main.py          # Главный файл приложения
│   ├── config.py        # Конфигурация
│   ├── database.py      # Настройка базы данных
│   └── tasks/
│       ├── __init__.py
│       ├── models.py    # SQLAlchemy модели
│       ├── schemas.py   # Pydantic схемы
│       ├── service.py   # Бизнес-логика
│       └── routes.py    # API эндпоинты
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Фикстуры pytest
│   ├── test_api.py      # Тесты API
│   └── test_schemas.py  # Тесты схем
├── alembic/             # Миграции базы данных
├── docker-compose.yml   # Docker Compose конфигурация
├── Dockerfile           # Docker образ приложения
├── .dockerignore        # Исключения для Docker
├── .env.example         # Пример переменных окружения
├── requirements.txt     # Зависимости
├── pytest.ini          # Конфигурация pytest
└── README.md
```

## API Эндпоинты

### Задачи

- `POST /api/v1/tasks/` - Создать задачу
- `GET /api/v1/tasks/` - Получить список задач
- `GET /api/v1/tasks/{task_id}` - Получить задачу по ID
- `PUT /api/v1/tasks/{task_id}` - Обновить задачу
- `DELETE /api/v1/tasks/{task_id}` - Удалить задачу

### Параметры запросов

- `status` - фильтр по статусу (created, in_progress, completed)
- `skip` - количество записей для пропуска (пагинация)
- `limit` - максимальное количество записей (по умолчанию 100)

## Модель данных

### Task

- `id` (UUID) - уникальный идентификатор
- `title` (str, max 100) - название задачи
- `description` (str, max 1000, optional) - описание задачи
- `status` (enum) - статус задачи (created, in_progress, completed)
- `created_at` (datetime) - дата создания
- `updated_at` (datetime) - дата обновления

## Тестирование

### Запуск тестов

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей для тестирования
pip install -r requirements.txt

# Запуск тестовой БД
docker-compose -f docker-compose.test.yml up -d

# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov=app --cov-report=html

# Запуск только unit тестов
pytest tests/test_schemas.py

# Запуск только API тестов
pytest tests/test_api.py

# Остановка тестовой БД
docker-compose -f docker-compose.test.yml down
```

### Структура тестов

- `tests/test_api.py` - тесты API эндпоинтов
- `tests/test_schemas.py` - тесты валидации данных
- `tests/conftest.py` - общие фикстуры

### Тестовая база данных

Тесты используют отдельную PostgreSQL БД в контейнере (порт 5433), которая не конфликтует с основной БД.

### Покрытие кода

После запуска тестов с покрытием, отчет будет доступен в `htmlcov/index.html`
