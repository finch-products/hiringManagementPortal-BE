from django.urls import path, include
from hiringManagementTool.components.candidates.views import CandidateAPIView, CandidateDetailAPIView, CandidateStatusUpdateAPIView, CandidateHistoryAPIView, AllCandidateAPIView, CandidateSearchView

urlpatterns = [
    path("update-candidate-status/", CandidateStatusUpdateAPIView.as_view(), name="update_candidate_status"), 
    path('search-candidates/', CandidateSearchView.as_view(), name='search_candidates'),
    path("candidate-list/", AllCandidateAPIView.as_view(), name="all-demand-ids"), 
    path("", CandidateAPIView.as_view(), name="all-candidates"),
    path("<str:id>/", CandidateDetailAPIView.as_view(), name="candidates-details"), 
    path("candidate-history/<str:candidate_id>/", CandidateHistoryAPIView.as_view(), name="candidate-history"),
    # path("all", AllCandidatesAPIView.as_view(), name="all-demand-ids"),
]