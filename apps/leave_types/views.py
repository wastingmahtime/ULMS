from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import LeaveType
from .serializers import LeaveTypeSerializer

class LeaveTypeListCreateView(APIView):
    def get(self, request):
        leave_types = LeaveType.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaveTypeDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(LeaveType, pk=pk)

    def get(self, request, pk):
        leave_type = self.get_object(pk)
        serializer = LeaveTypeSerializer(leave_type)
        return Response(serializer.data)

    def put(self, request, pk):
        leave_type = self.get_object(pk)
        serializer = LeaveTypeSerializer(leave_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leave_type = self.get_object(pk)
        leave_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
