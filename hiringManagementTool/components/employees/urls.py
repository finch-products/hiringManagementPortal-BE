from django.urls import path, include
from hiringManagementTool.components.employees.views import EmployeeAPIView, EmployeeDetailAPIView, EmployeeByRoleAPIView

urlpatterns = [
    path("", EmployeeAPIView.as_view(), name="all-employees"),
    path("<int:id>/", EmployeeDetailAPIView.as_view(), name="employees-details"),   
    path('employee-by-role/', EmployeeByRoleAPIView.as_view(), name='employee-by-role')
]