from django.db import models
from django.contrib.auth.models import User
from apps.departments.models import Department

class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True,
        related_name='employee', verbose_name='Пользователь'
    )
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    position = models.CharField(max_length=255, verbose_name='Должность')
    email = models.EmailField(unique=True, verbose_name='Email')
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True,
        related_name='employees', verbose_name='Подразделение'
    )

    class Meta:
        db_table = 'employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name
