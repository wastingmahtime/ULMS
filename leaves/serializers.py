from datetime import date
from rest_framework import serializers
from .models import Department, Employee, LeaveRequest, LeaveType


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название не может быть пустым.')
        return value.strip()


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'full_name', 'position', 'department', 'department_name', 'user_email']

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('ФИО не может быть пустым.')
        return value.strip()

    def validate_position(self, value):
        if not value.strip():
            raise serializers.ValidationError('Должность не может быть пустой.')
        return value.strip()

    def validate_user(self, value):
        # Проверяем, что у пользователя ещё нет профиля (при создании)
        if self.instance is None and hasattr(value, 'employee_profile'):
            try:
                value.employee_profile
                raise serializers.ValidationError('У этого пользователя уже есть профиль сотрудника.')
            except Employee.DoesNotExist:
                pass
        return value


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название не может быть пустым.')
        return value.strip()


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name',
            'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'reason',
            'status', 'status_display',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')

        if start and end:
            if end < start:
                raise serializers.ValidationError({
                    'end_date': 'Дата окончания не может быть раньше даты начала.'
                })
            if start < date.today():
                raise serializers.ValidationError({
                    'start_date': 'Дата начала не может быть в прошлом.'
                })

        return data


class LeaveRequestStatusSerializer(serializers.ModelSerializer):
    """Только для смены статуса (Admin only)."""
    class Meta:
        model = LeaveRequest
        fields = ['status']

    def validate_status(self, value):
        allowed = [LeaveRequest.Status.APPROVED, LeaveRequest.Status.REJECTED]
        if value not in allowed:
            raise serializers.ValidationError('Можно установить только: approved или rejected.')
        return value
