from django.urls import path, include
from hiringManagementTool.components.demands.views import DemandDetailAPIView, DemandAPIView

urlpatterns = [
    path("", DemandAPIView.as_view(), name="all-demands"),
    path("<int:id>/", DemandDetailAPIView.as_view(), name="demand-details"), 
]