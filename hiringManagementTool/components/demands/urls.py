from django.urls import path, include
from hiringManagementTool.components.demands.views import DemandDetailAPIView, DemandAPIView, OpenDemandUpdateAPIView, FilterDemandsAPIView, AllDemandsAPIView

urlpatterns = [
    path("", DemandAPIView.as_view(), name="all-demands"),
    path("all", AllDemandsAPIView.as_view(), name="all-demand-ids"),
    path("id/<str:id>/", DemandDetailAPIView.as_view(), name="demand-details"), 
    path('update-demand-status/', OpenDemandUpdateAPIView.as_view(), name='update-demand-status'),
    path('filter/', FilterDemandsAPIView.as_view(), name='filter-demands'),
]


