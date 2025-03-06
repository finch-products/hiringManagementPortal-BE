from django.urls import path
from .views import AgedemandReportView, OpenDemandCountReportView, TotalPositionsOpenedLastWeekView,DemandByStatusView, DemandFulfillmentMetricsView, LobTargetProgressView, ClientSelectionPercentageView, TimeTakenForProfileSubmissionView, TimeTakenFromInterviewToFeedbackView

urlpatterns = [
    path('age-demand/', AgedemandReportView.as_view(), name='age-demand-report'),
    path('open-demand-count/', OpenDemandCountReportView.as_view(), name='open-demand-count-report'),
    path('total-open-positions-last-week/', TotalPositionsOpenedLastWeekView.as_view(), name='total-positions-last-week'),
    path('demand-fulfillment-metric/', DemandFulfillmentMetricsView.as_view(), name='demand-fulfillment-metric-report'),
    path('LOB-Target-Progress/', LobTargetProgressView.as_view(), name='LOB-Target-Progress-report'),
    path('DemandBycategory/', DemandByStatusView.as_view(), name='DemandBycategory-report'),
    path('client-selection/', ClientSelectionPercentageView.as_view(), name='client-selection-percentage'),
    path('demand-time-taken-for-profile-submission/', TimeTakenForProfileSubmissionView.as_view(), name='demand-time-taken-for-profile-submission-report'),
    path('TimeTakenFromInterviewToFeedbackView/', TimeTakenFromInterviewToFeedbackView.as_view() , name='time-taken-from-interview-to-feedback-report'),
]