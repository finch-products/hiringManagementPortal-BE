# urls.py for demand-history
from django.urls import path
from .views import DemandHistoryDetailAPIView

urlpatterns = [
    path("<str:id>/", DemandHistoryDetailAPIView.as_view(), name="demand-history-details"),
]
