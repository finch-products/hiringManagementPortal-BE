from django.urls import path
from .views import GetCandidatelistByDemandId
from .views import CandidateDemandLinkAPIView, GetNonCandidatelistByDemandId

urlpatterns = [
    path('candidateby_opendemand/', GetCandidatelistByDemandId.as_view(), name='candidate-by-open-demand-api'),
    path("", CandidateDemandLinkAPIView.as_view(), name="all-candiate-demand-links"),
    path('not_added_candidatebydemandid/', GetNonCandidatelistByDemandId.as_view(), name='non-added-candidate-by-open-demand-api'),
]


 