
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.demandstatus.serializers import DemandStatusDetailsSerializer, DemandStatusSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from hiringManagementTool.models.demands import OpenDemand
from django.db.models import Q

class DemandStatusDetailsAPIView(generics.ListAPIView):
    serializer_class = DemandStatusDetailsSerializer
    queryset = DemandStatusMaster.objects.filter(dsm_inactive=False).order_by('dsm_sortid')
    

class DemandStatusDropdownAPIView(ListAPIView):
    serializer_class = DemandStatusSerializer

    def get_queryset(self):
        dem_id = self.kwargs.get('id')
        try:
            demand = OpenDemand.objects.get(dem_id=dem_id)
        except OpenDemand.DoesNotExist:
            return DemandStatusMaster.objects.none()
        
        current_status = demand.dem_dsm_id
        if not current_status:
            return DemandStatusMaster.objects.filter(dsm_inactive=False)
        
        restricted_status_ids = current_status.dsm_resstatus.split(',') if current_status.dsm_resstatus else []
        restricted_status_ids = [int(status_id.strip()) for status_id in restricted_status_ids if status_id.strip().isdigit()]
        
        return DemandStatusMaster.objects.filter(~Q(dsm_id__in=restricted_status_ids), dsm_inactive=False)