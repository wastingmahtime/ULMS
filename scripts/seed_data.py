"""
Скрипт для заполнения БД тестовыми данными.
Запуск: python manage.py shell < scripts/seed_data.py
"""
from apps.departments.models import Department
from apps.employees.models import Employee
from apps.leave_types.models import LeaveType
from apps.leave_requests.models import LeaveRequest
from datetime import date, timedelta

print("Создание подразделений...")
dept1, _ = Department.objects.get_or_create(name="Кафедра информатики")
dept2, _ = Department.objects.get_or_create(name="Кафедра математики")
dept3, _ = Department.objects.get_or_create(name="Отдел кадров")

print("Создание типов отпусков...")
lt1, _ = LeaveType.objects.get_or_create(name="Ежегодный оплачиваемый")
lt2, _ = LeaveType.objects.get_or_create(name="Учебный отпуск")
lt3, _ = LeaveType.objects.get_or_create(name="Без сохранения зарплаты")
lt4, _ = LeaveType.objects.get_or_create(name="По болезни")

print("Создание сотрудников...")
emp1, _ = Employee.objects.get_or_create(
    email="ivanov@university.kz",
    defaults={'full_name': "Иванов Иван Иванович", 'position': "Доцент", 'department': dept1}
)
emp2, _ = Employee.objects.get_or_create(
    email="petrova@university.kz",
    defaults={'full_name': "Петрова Мария Сергеевна", 'position': "Старший преподаватель", 'department': dept2}
)
emp3, _ = Employee.objects.get_or_create(
    email="sidorov@university.kz",
    defaults={'full_name': "Сидоров Алексей Петрович", 'position': "Профессор", 'department': dept1}
)

print("Создание заявок на отпуск...")
today = date.today()
LeaveRequest.objects.get_or_create(
    employee=emp1, leave_type=lt1,
    start_date=today + timedelta(days=10),
    end_date=today + timedelta(days=38),
    defaults={'reason': "Ежегодный отпуск", 'status': 'pending'}
)
LeaveRequest.objects.get_or_create(
    employee=emp2, leave_type=lt2,
    start_date=today + timedelta(days=5),
    end_date=today + timedelta(days=15),
    defaults={'reason': "Написание диссертации", 'status': 'approved'}
)
LeaveRequest.objects.get_or_create(
    employee=emp3, leave_type=lt3,
    start_date=today + timedelta(days=2),
    end_date=today + timedelta(days=7),
    defaults={'reason': "Семейные обстоятельства", 'status': 'rejected'}
)

print("✅ Тестовые данные успешно загружены!")
