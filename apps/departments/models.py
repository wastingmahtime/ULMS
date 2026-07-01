from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'departments'
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.name
