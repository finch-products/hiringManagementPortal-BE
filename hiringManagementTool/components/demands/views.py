from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.components.demands.serializers import DemandSerializer


# class DemandViewSet(viewsets.ModelViewSet):
#     queryset = Demands.objects.all()
#     serializer_class = DemandSerializer


class DemandAPIView(ListCreateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = DemandSerializer


class DemandDetailAPIView(RetrieveUpdateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = DemandSerializer
    lookup_field = 'dem_id'
    lookup_url_kwarg = 'id'