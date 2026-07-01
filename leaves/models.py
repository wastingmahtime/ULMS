from django.db import models
from users.models import User


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'departments'
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employee_profile',
        verbose_name='Пользователь'
    )
    full_name = models.CharField(max_length=300, verbose_name='ФИО')
    position = models.CharField(max_length=200, verbose_name='Должность')
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT,
        related_name='employees', verbose_name='Подразделение'
    )

    class Meta:
        db_table = 'employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} — {self.position}'


class LeaveType(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'leave_types'
        verbose_name = 'Тип отпуска'
        verbose_name_plural = 'Типы отпусков'
        ordering = ['name']

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'На рассмотрении'
        APPROVED = 'approved', 'Одобрено'
        REJECTED = 'rejected', 'Отклонено'

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='leave_requests', verbose_name='Сотрудник'
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.PROTECT,
        related_name='leave_requests', verbose_name='Тип отпуска'
    )
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    reason = models.TextField(blank=True, verbose_name='Причина')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leave_requests'
        verbose_name = 'Заявка на отпуск'
        verbose_name_plural = 'Заявки на отпуск'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee.full_name} | {self.start_date} – {self.end_date} [{self.get_status_display()}]'
