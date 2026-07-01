from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Employee, LeaveRequest, LeaveType
from .permissions import IsAdmin, IsAdminOrReadOwn
from .serializers import (
    DepartmentSerializer,
    EmployeeSerializer,
    LeaveRequestSerializer,
    LeaveRequestStatusSerializer,
    LeaveTypeSerializer,
)


# ─── Departments ───────────────────────────────────────────────────────────────

class DepartmentListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        departments = Department.objects.all()
        return Response(DepartmentSerializer(departments, many=True).data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise NotFound(f'Подразделение с id={pk} не найдено.')

    def get(self, request, pk):
        return Response(DepartmentSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        serializer = DepartmentSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Employees ─────────────────────────────────────────────────────────────────

class EmployeeListView(APIView):
    permission_classes = [IsAdminOrReadOwn]

    def get(self, request):
        if request.user.is_admin:
            employees = Employee.objects.select_related('user', 'department').all()
        else:
            employees = Employee.objects.select_related('user', 'department').filter(user=request.user)
        return Response(EmployeeSerializer(employees, many=True).data)

    def post(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('Создание сотрудников доступно только администратору.')
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    permission_classes = [IsAdminOrReadOwn]

    def get_object(self, pk, user):
        try:
            obj = Employee.objects.select_related('user', 'department').get(pk=pk)
        except Employee.DoesNotExist:
            raise NotFound(f'Сотрудник с id={pk} не найден.')
        if not user.is_admin and obj.user != user:
            raise PermissionDenied('Нет доступа к данным другого сотрудника.')
        return obj

    def get(self, request, pk):
        return Response(EmployeeSerializer(self.get_object(pk, request.user)).data)

    def put(self, request, pk):
        if not request.user.is_admin:
            raise PermissionDenied('Редактирование доступно только администратору.')
        serializer = EmployeeSerializer(self.get_object(pk, request.user), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_admin:
            raise PermissionDenied('Удаление доступно только администратору.')
        self.get_object(pk, request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Leave Types ───────────────────────────────────────────────────────────────

class LeaveTypeListView(APIView):
    permission_classes = [IsAdminOrReadOwn]

    def get(self, request):
        return Response(LeaveTypeSerializer(LeaveType.objects.all(), many=True).data)

    def post(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('Создание типов отпуска доступно только администратору.')
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveTypeDetailView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return LeaveType.objects.get(pk=pk)
        except LeaveType.DoesNotExist:
            raise NotFound(f'Тип отпуска с id={pk} не найден.')

    def get(self, request, pk):
        return Response(LeaveTypeSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        serializer = LeaveTypeSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Leave Requests ────────────────────────────────────────────────────────────

class LeaveRequestListView(APIView):
    permission_classes = [IsAdminOrReadOwn]

    def get(self, request):
        if request.user.is_admin:
            qs = LeaveRequest.objects.select_related('employee', 'leave_type').all()
        else:
            try:
                employee = request.user.employee_profile
            except Employee.DoesNotExist:
                return Response([])
            qs = LeaveRequest.objects.select_related('employee', 'leave_type').filter(employee=employee)
        return Response(LeaveRequestSerializer(qs, many=True).data)

    def post(self, request):
        try:
            employee = request.user.employee_profile
        except Employee.DoesNotExist:
            raise PermissionDenied('У вас нет профиля сотрудника. Обратитесь к администратору.')
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestDetailView(APIView):
    permission_classes = [IsAdminOrReadOwn]

    def get_object(self, pk, user):
        try:
            obj = LeaveRequest.objects.select_related('employee__user', 'leave_type').get(pk=pk)
        except LeaveRequest.DoesNotExist:
            raise NotFound(f'Заявка с id={pk} не найдена.')
        if not user.is_admin and obj.employee.user != user:
            raise PermissionDenied('Нет доступа к этой заявке.')
        return obj

    def get(self, request, pk):
        return Response(LeaveRequestSerializer(self.get_object(pk, request.user)).data)

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        # Admin меняет только статус
        if request.user.is_admin:
            serializer = LeaveRequestStatusSerializer(obj, data=request.data, partial=True)
        else:
            if obj.status != LeaveRequest.Status.PENDING:
                raise PermissionDenied('Нельзя редактировать рассмотренную заявку.')
            serializer = LeaveRequestSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(LeaveRequestSerializer(obj).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not request.user.is_admin and obj.status != LeaveRequest.Status.PENDING:
            raise PermissionDenied('Нельзя удалить рассмотренную заявку.')
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
