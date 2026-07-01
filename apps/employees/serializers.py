from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'email', 'department', 'department_name']

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("ФИО не может быть пустым.")
        if len(value) < 3:
            raise serializers.ValidationError("ФИО должно содержать минимум 3 символа.")
        return value

    def validate_position(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Должность не может быть пустой.")
        return value

    def validate_email(self, value):
        instance = self.instance
        qs = Employee.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Сотрудник с таким email уже существует.")
        return value
