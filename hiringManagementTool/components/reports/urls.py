from django.urls import path
from .views import AgedemandReportView

urlpatterns = [
    path('age-demand/', AgedemandReportView.as_view(), name='age-demand-report'),
    
]