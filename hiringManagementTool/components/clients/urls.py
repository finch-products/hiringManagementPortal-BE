from django.urls import path, include
from hiringManagementTool.components.clients.views import ClientAPIView, ClientDetailAPIView

urlpatterns = [
    path("", ClientAPIView.as_view(), name="all-clients"),
    path("<int:id>/", ClientDetailAPIView.as_view(), name="clients-details"),   
]