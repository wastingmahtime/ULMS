from django.urls import path
from .views import LeaveTypeListCreateView, LeaveTypeDetailView

urlpatterns = [
    path('leave-types/', LeaveTypeListCreateView.as_view()),
    path('leave-types/<int:pk>/', LeaveTypeDetailView.as_view()),
]
