from django.urls import path
from .views import AgedemandReportView, OpenDemandCountReportView

urlpatterns = [
    path('age-demand/', AgedemandReportView.as_view(), name='age-demand-report'),
    path('open-demand-count/', OpenDemandCountReportView.as_view(), name='open-demand-count-report'),
]