from django.urls import path
from hiringManagementTool.components.demandstatus.views import DemandStatusDetailsAPIView, DemandStatusDropdownAPIView

urlpatterns = [
    path("", DemandStatusDetailsAPIView.as_view(), name="demands-status-details"),
    path('demand-status/<str:id>/', DemandStatusDropdownAPIView.as_view(), name='demand-status-dropdown')
]
