from django.urls import path
from .views import (
    DepartmentDetailView, DepartmentListView,
    EmployeeDetailView, EmployeeListView,
    LeaveRequestDetailView, LeaveRequestListView,
    LeaveTypeDetailView, LeaveTypeListView,
)

urlpatterns = [
    # Departments
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),

    # Employees
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Leave Types
    path('leave-types/', LeaveTypeListView.as_view(), name='leave-type-list'),
    path('leave-types/<int:pk>/', LeaveTypeDetailView.as_view(), name='leave-type-detail'),

    # Leave Requests
    path('leave-requests/', LeaveRequestListView.as_view(), name='leave-request-list'),
    path('leave-requests/<int:pk>/', LeaveRequestDetailView.as_view(), name='leave-request-detail'),
]
