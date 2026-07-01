from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название подразделения не может быть пустым.")
        if len(value) < 2:
            raise serializers.ValidationError("Название должно содержать минимум 2 символа.")
        return value
