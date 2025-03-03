from django.urls import path, include
from hiringManagementTool.components.departments.views import InternalDepartmentAPIView

urlpatterns = [
    path("", InternalDepartmentAPIView().as_view(), name="dept-details")
]