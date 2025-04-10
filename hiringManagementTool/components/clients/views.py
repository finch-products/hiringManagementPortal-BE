from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.clients.serializers import ClientMasterSerializer, ClientMimimumDetailsSerializer
from hiringManagementTool.models.clients import ClientMaster
from rest_framework.parsers import MultiPartParser, FormParser

class ClientAPIView(ListCreateAPIView):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer
    parser_classes = (MultiPartParser, FormParser)
    def get_serializer_context(self):
        return {'request': self.request}

class ClientDetailAPIView(RetrieveUpdateAPIView):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer
    lookup_field = 'clm_id'
    lookup_url_kwarg = 'id'


class ClientMinimumDetailsAPIView(generics.ListAPIView):  # ReadOnlyModelViewSet allows only GET requests
    queryset = ClientMaster.objects.filter(clm_isactive=True)
    serializer_class = ClientMimimumDetailsSerializer

    # def list(self, request, *args, **kwargs):
    #     """Override list to return only required fields"""
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
