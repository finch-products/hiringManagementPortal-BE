from django.urls import path, include
from hiringManagementTool.components.departments.views import InternalDepartmentAPIView, EmployeeByRoleAPIView

urlpatterns = [
    path("", InternalDepartmentAPIView().as_view(), name="dept-details"),
    path('employee-by-role/', EmployeeByRoleAPIView.as_view(), name='employee-by-role')
]