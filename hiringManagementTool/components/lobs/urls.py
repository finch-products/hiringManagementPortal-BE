from django.urls import path
from hiringManagementTool.components.lobs.views import LOBAPIView, LOBDetailAPIView, LOBMinimumDetailsAPIView

urlpatterns = [
    path("", LOBAPIView.as_view(), name="all-lobs"),
    path("<int:id>/", LOBDetailAPIView.as_view(), name="lob-details"),   
    path("lobs-details/", LOBMinimumDetailsAPIView.as_view(), name="lob-details")
]