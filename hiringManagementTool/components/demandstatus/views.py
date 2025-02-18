
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.demandstatus.serializers import DemandStatusDetailsSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster


class DemandStatusDetailsAPIView(generics.ListAPIView):
    serializer_class = DemandStatusDetailsSerializer

    def get_queryset(self):
        """Sort records by dsm_sortid in ascending order"""
        return DemandStatusMaster.objects.all().order_by('dsm_sortid')

    def get(self, request, *args, **kwargs):
        """Fetch and return demand status data as a Django response"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data, status=200)