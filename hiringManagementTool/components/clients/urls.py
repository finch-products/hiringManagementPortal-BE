from django.urls import path, include
from hiringManagementTool.components.clients.views import ClientAPIView, ClientDetailAPIView, ClientMinimumDetailsAPIView

urlpatterns = [
    path("", ClientAPIView.as_view(), name="all-clients"),
    path("<int:id>/", ClientDetailAPIView.as_view(), name="clients-detail"),
    path("clients-details/", ClientMinimumDetailsAPIView.as_view(), name="client-details")  
]
