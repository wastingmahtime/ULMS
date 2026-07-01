from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.employees.urls')),
    path('api/', include('apps.departments.urls')),
    path('api/', include('apps.leave_types.urls')),
    path('api/', include('apps.leave_requests.urls')),
    path('api/', include('apps.auth_app.urls')),
]