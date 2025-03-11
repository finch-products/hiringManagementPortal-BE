from django.urls import path
from .views import CandidateStatusAPIView

urlpatterns = [
    path('list/', CandidateStatusAPIView.as_view(), name='candidate-status-list'),
]
