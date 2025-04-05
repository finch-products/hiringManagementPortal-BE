from django.urls import path, include
from hiringManagementTool.components.departments.views import InternalDepartmentAPIView, InternalDepartmentMasterListAPI

urlpatterns = [
    path("", InternalDepartmentAPIView().as_view(), name="dept-details"),
    path('details/', InternalDepartmentMasterListAPI.as_view(), name='internal-department-with-emp-details'),
]