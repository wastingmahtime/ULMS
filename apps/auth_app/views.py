from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.employees.models import Employee
from apps.departments.models import Department
 
 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}
 
 
class RegisterView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        role = request.data.get('role', 'employee')
        employee_data = request.data.get('employee', None)
 
        if not username or not email or not password:
            return Response({'error': 'Заполните все поля'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'error': 'Пароль минимум 6 символов'}, status=status.HTTP_400_BAD_REQUEST)
 
        user = User.objects.create_user(username=username, email=email, password=password, is_staff=(role == 'admin'))
 
        employee_id = None
        if role == 'employee' and employee_data:
            try:
                dept = Department.objects.get(id=employee_data.get('department'))
                employee = Employee.objects.create(
                    user=user,
                    full_name=employee_data.get('full_name', username),
                    position=employee_data.get('position', ''),
                    email=email,
                    department=dept
                )
                employee_id = employee.id
            except Department.DoesNotExist:
                pass
 
        tokens = get_tokens_for_user(user)
        return Response({
            'user': {
                'id': user.id, 'username': user.username, 'email': user.email,
                'role': 'admin' if user.is_staff else 'employee', 'employee_id': employee_id,
            }, **tokens
        }, status=status.HTTP_201_CREATED)
 
 
class LoginView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
 
        if not username or not password:
            return Response({'error': 'Введите логин и пароль'}, status=status.HTTP_400_BAD_REQUEST)
 
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
 
        tokens = get_tokens_for_user(user)
        employee_id = None
        try:
            employee_id = user.employee.id
        except:
            pass
 
        return Response({
            'user': {
                'id': user.id, 'username': user.username, 'email': user.email,
                'role': 'admin' if user.is_staff else 'employee', 'employee_id': employee_id,
            }, **tokens
        })
 
 
class MeView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        user = request.user
        employee_id = None
        try:
            employee_id = user.employee.id
        except:
            pass
        return Response({
            'id': user.id, 'username': user.username, 'email': user.email,
            'role': 'admin' if user.is_staff else 'employee', 'employee_id': employee_id,
        })
 
 
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
 
    def put(self, request):
        user = request.user
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
 
        if not username or not email:
            return Response({'error': 'Заполните все поля'}, status=status.HTTP_400_BAD_REQUEST)
 
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            return Response({'error': 'Этот логин уже занят'}, status=status.HTTP_400_BAD_REQUEST)
 
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({'error': 'Этот email уже занят'}, status=status.HTTP_400_BAD_REQUEST)
 
        user.username = username
        user.email = email
        user.save()
 
        return Response({'message': 'Профиль обновлён', 'username': user.username, 'email': user.email})
 
 
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
 
        if not current_password or not new_password:
            return Response({'error': 'Заполните все поля'}, status=status.HTTP_400_BAD_REQUEST)
 
        if not user.check_password(current_password):
            return Response({'error': 'Неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)
 
        if len(new_password) < 6:
            return Response({'error': 'Пароль минимум 6 символов'}, status=status.HTTP_400_BAD_REQUEST)
 
        user.set_password(new_password)
        user.save()
 
        return Response({'message': 'Пароль изменён'})
 