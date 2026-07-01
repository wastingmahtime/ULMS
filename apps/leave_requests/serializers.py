from rest_framework import serializers
from datetime import date
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    duration_days = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name',
            'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'duration_days',
            'reason', 'status', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_duration_days(self, obj):
        return (obj.end_date - obj.start_date).days + 1

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата начала не может быть в прошлом.")
        return value

    def validate_status(self, value):
        allowed = ['pending', 'approved', 'rejected']
        if value not in allowed:
            raise serializers.ValidationError(f"Недопустимый статус. Допустимые значения: {', '.join(allowed)}.")
        return value

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end:
            if end < start:
                raise serializers.ValidationError(
                    {"end_date": "Дата окончания не может быть раньше даты начала."}
                )
            if (end - start).days > 365:
                raise serializers.ValidationError(
                    {"end_date": "Длительность отпуска не может превышать 365 дней."}
                )
        return data
