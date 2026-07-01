from django.db import models
from apps.employees.models import Employee
from apps.leave_types.models import LeaveType

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

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
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leave_requests'
        verbose_name = 'Заявка на отпуск'
        verbose_name_plural = 'Заявки на отпуск'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} — {self.leave_type.name} ({self.start_date} — {self.end_date})"
