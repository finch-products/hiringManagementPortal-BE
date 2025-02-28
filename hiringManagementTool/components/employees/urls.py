from django.urls import path, include
from hiringManagementTool.components.employees.views import EmployeeAPIView, EmployeeDetailAPIView, get_client_partners, get_delivery_managers

urlpatterns = [
    path("", EmployeeAPIView.as_view(), name="all-employees"),
    path("<int:id>/", EmployeeDetailAPIView.as_view(), name="employees-details"),
    path('client-partners/', get_client_partners, name='client-partners'),
    path('delivery-managers/', get_delivery_managers, name='delivery-managers'),
]