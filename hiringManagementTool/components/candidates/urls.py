from django.urls import path, include
from hiringManagementTool.components.candidates.views import CandidateAPIView, CandidateDetailAPIView, CandidateStatusUpdateAPIView

urlpatterns = [
    path("update-candidate-status/", CandidateStatusUpdateAPIView.as_view(), name="update_candidate_status"),  
    path("", CandidateAPIView.as_view(), name="all-candidates"),
    path("<str:id>/", CandidateDetailAPIView.as_view(), name="candidates-details"), 
]