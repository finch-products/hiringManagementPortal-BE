from django.urls import path
from hiringManagementTool.components.demandstatus.views import DemandStatusDetailsAPIView

urlpatterns = [
    path("", DemandStatusDetailsAPIView.as_view(), name="demands-status-details") 
]
