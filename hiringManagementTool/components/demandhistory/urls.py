# urls.py for demand-history
from django.urls import path
from .views import DemandHistoryDetailAPIView, DemandHistoryTrackingAPIView

urlpatterns = [
    path("<str:id>/", DemandHistoryDetailAPIView.as_view(), name="demand-history-details"),
    path('demand-history/<str:demand_id>/', DemandHistoryTrackingAPIView.as_view(), name='demand-history-tracking'),
]
