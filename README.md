# University Leave Management System (ULMS)

Система управления отпусками сотрудников университета.  
Backend на Django REST Framework + MySQL.

---

## Стек технологий

| Слой | Технология |
|---|---|
| Backend | Python 3.11, Django 4.2 |
| API | Django REST Framework |
| База данных | MySQL |
| Тестирование API | Postman |

---

## Структура проекта

```
ulms/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── scripts/
│   └── seed_data.py        # Тестовые данные
├── ulms/                   # Конфигурация проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── departments/        # Подразделения
    ├── employees/          # Сотрудники
    ├── leave_types/        # Типы отпусков
    └── leave_requests/     # Заявки на отпуск
```

---

## Схема базы данных (ER)

```
Departments          Employees
----------           ---------
id (PK)    <──1:N── id (PK)
name                 full_name
                     position
                     email
                     department_id (FK)

LeaveTypes           LeaveRequests
----------           -------------
id (PK)    <──1:N── id (PK)
name                 employee_id (FK) ──> Employees
                     leave_type_id (FK) -> LeaveTypes
                     start_date
                     end_date
                     reason
                     status
                     created_at
```

---

## Инструкция по запуску

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/ulms.git
cd ulms
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

```bash
cp .env.example .env
# Отредактировать .env — указать DB_NAME, DB_USER, DB_PASSWORD
```

### 5. Создать базу данных в MySQL

```sql
CREATE DATABASE ulms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Применить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Загрузить тестовые данные

```bash
python manage.py shell < scripts/seed_data.py
```

### 8. Создать суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 9. Запустить сервер

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: **http://127.0.0.1:8000**

---

## REST API

### Подразделения

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/departments/` | Список всех подразделений |
| POST | `/api/departments/` | Создать подразделение |
| GET | `/api/departments/{id}/` | Получить подразделение |
| PUT | `/api/departments/{id}/` | Обновить подразделение |
| DELETE | `/api/departments/{id}/` | Удалить подразделение |

### Сотрудники

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/employees/` | Список всех сотрудников |
| POST | `/api/employees/` | Создать сотрудника |
| GET | `/api/employees/{id}/` | Получить сотрудника |
| PUT | `/api/employees/{id}/` | Обновить сотрудника |
| DELETE | `/api/employees/{id}/` | Удалить сотрудника |

### Типы отпусков

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/leave-types/` | Список типов отпусков |
| POST | `/api/leave-types/` | Создать тип |
| GET | `/api/leave-types/{id}/` | Получить тип |
| PUT | `/api/leave-types/{id}/` | Обновить тип |
| DELETE | `/api/leave-types/{id}/` | Удалить тип |

### Заявки на отпуск

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/leave-requests/` | Список заявок |
| GET | `/api/leave-requests/?status=pending` | Фильтр по статусу |
| GET | `/api/leave-requests/?employee_id=1` | Фильтр по сотруднику |
| POST | `/api/leave-requests/` | Создать заявку |
| GET | `/api/leave-requests/{id}/` | Получить заявку |
| PUT | `/api/leave-requests/{id}/` | Обновить заявку |
| PATCH | `/api/leave-requests/{id}/` | Частичное обновление (напр. статус) |
| DELETE | `/api/leave-requests/{id}/` | Удалить заявку |

---

## Примеры запросов (Postman)

### Создать сотрудника

```
POST /api/employees/
Content-Type: application/json

{
  "full_name": "Иванов Иван Иванович",
  "position": "Доцент",
  "email": "ivanov@university.kz",
  "department": 1
}
```

### Создать заявку на отпуск

```
POST /api/leave-requests/
Content-Type: application/json

{
  "employee": 1,
  "leave_type": 1,
  "start_date": "2025-07-01",
  "end_date": "2025-07-28",
  "reason": "Ежегодный отпуск"
}
```

### Сменить статус заявки

```
PATCH /api/leave-requests/1/
Content-Type: application/json

{
  "status": "approved"
}
```

---

## Валидация данных

- `full_name` — обязательное, минимум 3 символа
- `email` — уникальный, корректный формат
- `start_date` — не может быть в прошлом
- `end_date` — не может быть раньше `start_date`
- Длительность отпуска — не более 365 дней
- `status` — только `pending`, `approved`, `rejected`

---

## Коды ответов

| Код | Описание |
|---|---|
| 200 | OK — успешный запрос |
| 201 | Created — ресурс создан |
| 204 | No Content — успешное удаление |
| 400 | Bad Request — ошибка валидации |
| 404 | Not Found — ресурс не найден |
| 500 | Internal Server Error — ошибка сервера |
