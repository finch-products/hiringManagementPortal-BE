from django.urls import path
from .views import CandidateStatusAPIView, CandidateStatusAPIViewbyid

urlpatterns = [
    path('list/', CandidateStatusAPIView.as_view(), name='candidate-status-list'),
     path('list/<str:id>/', CandidateStatusAPIViewbyid.as_view(), name='candidate-status-list'),
]
