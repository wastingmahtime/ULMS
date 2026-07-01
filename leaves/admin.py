from django.contrib import admin
from .models import Department, Employee, LeaveRequest, LeaveType


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'position', 'department']
    list_filter = ['department']
    search_fields = ['full_name', 'position']


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'leave_type']
    search_fields = ['employee__full_name']
    list_editable = ['status']
