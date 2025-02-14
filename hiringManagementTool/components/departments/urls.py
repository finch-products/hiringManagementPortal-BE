from django.urls import path, include
from hiringManagementTool.components.departments.views import InternalDepartmentDetailsViewSet

urlpatterns = [
    path("", InternalDepartmentDetailsViewSet.as_view(), name="dept-details")  
]