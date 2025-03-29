from django.urls import path
from .views import InterviewSchedulingAPIView, InterviewUpdateAPIView, GetCdlIdAPIView

urlpatterns = [
    path("", InterviewSchedulingAPIView.as_view(), name='interview-list-create'),
    path('update/', InterviewUpdateAPIView.as_view(), name='update-interview'),
    path('get-cdl-id/', GetCdlIdAPIView.as_view(), name='get_cdl_id'),

]