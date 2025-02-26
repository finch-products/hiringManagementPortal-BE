from django.urls import path
from .views import GetCandidatelistByDemandId

urlpatterns = [
    path('candidateby_opendemand/', GetCandidatelistByDemandId.as_view(), name='candidate-by-open-demand-api'),
]
from django.urls import path
from .views import CandidateDemandLinkAPIView

urlpatterns = [
    path("", CandidateDemandLinkAPIView.as_view(), name="all-candiate-demand-links"),
]
 