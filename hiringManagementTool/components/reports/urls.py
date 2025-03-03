from django.urls import path
from .views import AgedemandReportView, OpenDemandCountReportView, TotalPositionsOpenedLastWeekView, DemandFulfillmentMetricsView

urlpatterns = [
    path('age-demand/', AgedemandReportView.as_view(), name='age-demand-report'),
    path('open-demand-count/', OpenDemandCountReportView.as_view(), name='open-demand-count-report'),
    path('total-open-positions-last-week/', TotalPositionsOpenedLastWeekView.as_view(), name='total-positions-last-week'),
    path('demand-fulfillment-metric/', DemandFulfillmentMetricsView.as_view(), name='demand-fulfillment-metric-report'),
]