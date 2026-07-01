from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer

class LeaveRequestListCreateView(APIView):
    def get(self, request):
        queryset = LeaveRequest.objects.select_related('employee', 'leave_type').all()
        # Фильтрация по статусу
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        # Фильтрация по сотруднику
        employee_id = request.query_params.get('employee_id')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        serializer = LeaveRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaveRequestDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(LeaveRequest, pk=pk)

    def get(self, request, pk):
        leave_request = self.get_object(pk)
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data)

    def put(self, request, pk):
        leave_request = self.get_object(pk)
        serializer = LeaveRequestSerializer(leave_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        leave_request = self.get_object(pk)
        serializer = LeaveRequestSerializer(leave_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leave_request = self.get_object(pk)
        leave_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
