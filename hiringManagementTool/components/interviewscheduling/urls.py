from django.urls import path, include
from hiringManagementTool.components.interviewscheduling.views import InterviewSchedulingAPIView

urlpatterns = [
    path("", InterviewSchedulingAPIView.as_view(), name="all-clients"),
   
]
