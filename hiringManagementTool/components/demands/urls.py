from django.urls import path, include
from hiringManagementTool.components.demands.views import DemandDetailAPIView, DemandAPIView, OpenDemandUpdateAPIView

urlpatterns = [
    path("", DemandAPIView.as_view(), name="all-demands"),
    # path("/all", DemandsAPIView.as_view(), name="all-demands"),
    path("<int:id>/", DemandDetailAPIView.as_view(), name="demand-details"), 
    path('update-demand-status/', OpenDemandUpdateAPIView.as_view(), name='update-demand-status'),
]
