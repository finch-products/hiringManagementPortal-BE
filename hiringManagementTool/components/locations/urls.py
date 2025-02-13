from django.urls import path
from hiringManagementTool.components.locations.views import LocationAPIView, LocationDetailAPIView

urlpatterns = [
    path("", LocationAPIView.as_view(), name="all-locations"),
    path("<int:id>/", LocationDetailAPIView.as_view(), name="locations-details"),   
]
