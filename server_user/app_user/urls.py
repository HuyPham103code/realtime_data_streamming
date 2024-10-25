from django.urls import path
from .views import EmployeeAPIView

urlpatterns = [
    path('employees/', EmployeeAPIView.as_view(), name='employee_api'),
]
