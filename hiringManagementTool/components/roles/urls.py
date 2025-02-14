from django.urls import path
from hiringManagementTool.components.roles.views import RoleAPIView, RoleDetailAPIView

urlpatterns = [
    path("", RoleAPIView.as_view(), name="all-roles"),
    path("<int:id>/", RoleDetailAPIView.as_view(), name="role-details"),   
]