from django.db import models

class LeaveType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Тип отпуска')

    class Meta:
        db_table = 'leave_types'
        verbose_name = 'Тип отпуска'
        verbose_name_plural = 'Типы отпусков'

    def __str__(self):
        return self.name
