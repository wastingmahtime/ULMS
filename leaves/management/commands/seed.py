from django.core.management.base import BaseCommand
from users.models import User
from leaves.models import Department, Employee, LeaveRequest, LeaveType
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка старых данных...')
        LeaveRequest.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        LeaveType.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        deps = [
            Department.objects.create(name='Кафедра информатики'),
            Department.objects.create(name='Кафедра математики'),
            Department.objects.create(name='Отдел кадров'),
        ]

        lt_annual = LeaveType.objects.create(name='Ежегодный оплачиваемый')
        lt_sick   = LeaveType.objects.create(name='Больничный')
        lt_study  = LeaveType.objects.create(name='Учебный')

        User.objects.create_user(username='admin', email='admin@ulms.kz', password='admin1234', role=User.Role.ADMIN)

        u1 = User.objects.create_user(username='aibek', email='aibek@ulms.kz', password='pass1234')
        u2 = User.objects.create_user(username='dana',  email='dana@ulms.kz',  password='pass1234')
        u3 = User.objects.create_user(username='zarina',email='zarina@ulms.kz',password='pass1234')

        e1 = Employee.objects.create(user=u1, full_name='Айбек Сейткали',  position='Преподаватель',          department=deps[0])
        e2 = Employee.objects.create(user=u2, full_name='Дана Омарова',    position='Старший преподаватель',  department=deps[1])
        e3 = Employee.objects.create(user=u3, full_name='Зарина Бекова',   position='Инспектор',              department=deps[2])

        today = date.today()
        LeaveRequest.objects.create(employee=e1, leave_type=lt_annual, start_date=today+timedelta(10), end_date=today+timedelta(24), reason='Плановый отпуск',     status='pending')
        LeaveRequest.objects.create(employee=e2, leave_type=lt_sick,   start_date=today+timedelta(3),  end_date=today+timedelta(7),  reason='Больничный лист',     status='approved')
        LeaveRequest.objects.create(employee=e3, leave_type=lt_study,  start_date=today+timedelta(20), end_date=today+timedelta(25), reason='Защита диссертации',  status='pending')

        self.stdout.write(self.style.SUCCESS(
            'Готово!\nAdmin: admin@ulms.kz / admin1234\nEmployee: aibek@ulms.kz / pass1234'
        ))
