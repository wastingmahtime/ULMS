from rest_framework import serializers
from .models import LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название типа отпуска не может быть пустым.")
        return value
