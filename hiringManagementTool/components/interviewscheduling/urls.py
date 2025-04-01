from django.urls import path
from .views import InterviewSchedulingAPIView, GetCdlIdAPIView, InterviewStatusDropdownView, InterviewTypeDropdownView, TimezoneDropdownAPIView, InterviewUpdateAPIView

urlpatterns = [
    path("", InterviewSchedulingAPIView.as_view(), name='interview-list-create'),
    path('update/', InterviewUpdateAPIView.as_view(), name='update-interview'),
    path('get-cdl-id/', GetCdlIdAPIView.as_view(), name='get_cdl_id'),
    path('interview-status-dropdown/', InterviewStatusDropdownView.as_view(), name='interview-status-dropdown'),
    path('interview-type-dropdown/', InterviewTypeDropdownView.as_view(), name='interview-type-dropdown'),
    path('timezone-dropdown/', TimezoneDropdownAPIView.as_view(), name='timezone-dropdown'),
]
