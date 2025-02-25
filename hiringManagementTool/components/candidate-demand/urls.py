# urls.py for candidate-demand
from django.urls import path
from .views import CandidateDemandLinkAPIView

urlpatterns = [
    path("", CandidateDemandLinkAPIView.as_view(), name="all-candiate-demand-links"),
]
 