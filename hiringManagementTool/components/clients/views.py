from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.clients.serializers import ClientMasterSerializer
from hiringManagementTool.models.clients import ClientMaster

class ClientAPIView(ListCreateAPIView):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer


class ClientDetailAPIView(RetrieveUpdateAPIView):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer
    lookup_field = 'clm_id'
    lookup_url_kwarg = 'id'