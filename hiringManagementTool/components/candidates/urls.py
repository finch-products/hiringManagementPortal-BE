from django.urls import path, include
from hiringManagementTool.components.candidates.views import CandidateAPIView, CandidateDetailAPIView

urlpatterns = [
    path("", CandidateAPIView.as_view(), name="all-candidates"),
    path("<int:id>/", CandidateDetailAPIView.as_view(), name="candidates-details"),   
]