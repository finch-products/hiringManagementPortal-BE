from django.urls import path
from hiringManagementTool.components.locations.views import LocationAPIView, LocationDetailAPIView, LocationMinimumDetailsAPIView

urlpatterns = [
    path("", LocationAPIView.as_view(), name="all-locations"),
    path("<int:id>/", LocationDetailAPIView.as_view(), name="location-details"),
    path("locations-details/", LocationMinimumDetailsAPIView.as_view(), name="locations-details")  
   
]
