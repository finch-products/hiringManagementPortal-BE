from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.models.lobs import LOBMaster
from hiringManagementTool.components.lobs.serializers import LOBMasterSerializer, LOBMinimumDetailsSerializer

class LOBAPIView(ListCreateAPIView):
    queryset = LOBMaster.objects.all()
    serializer_class = LOBMasterSerializer

class LOBDetailAPIView(RetrieveUpdateAPIView):
    queryset = LOBMaster.objects.all()
    serializer_class = LOBMasterSerializer
    lookup_field = 'lob_id'
    lookup_url_kwarg = 'id'


class LOBMinimumDetailsAPIView(generics.ListAPIView):
    queryset = LOBMaster.objects.all()
    serializer_class = LOBMinimumDetailsSerializer