
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.demandstatus.serializers import DemandStatusDetailsSerializer, DemandStatusSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from rest_framework.generics import ListAPIView

class DemandStatusDetailsAPIView(generics.ListAPIView):
    serializer_class = DemandStatusDetailsSerializer
    queryset = DemandStatusMaster.objects.filter(dsm_inactive=False).order_by('dsm_sortid')
    

class DemandStatusDropdownAPIView(ListAPIView):
    queryset = DemandStatusMaster.objects.filter(dsm_inactive=False)  # Exclude inactive statuses
    serializer_class = DemandStatusSerializer