from rest_framework import viewsets
from .models import ClientMaster, LOBMaster, LocationMaster, OpenDemand, PracticeUnitMaster
from .serializers import ClientMasterSerializer, LOBMasterSerializer, LocationMasterSerializer, OpenDemandSerializer, PracticeUnitMasterSerializer

class OpenDemandViewSet(viewsets.ModelViewSet):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer

# Client Master API View
class ClientMasterViewSet(viewsets.ModelViewSet):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer

# LOB Master API View
class LOBMasterViewSet(viewsets.ModelViewSet):
    queryset = LOBMaster.objects.all()
    serializer_class = LOBMasterSerializer

# Location Master API View
class LocationMasterViewSet(viewsets.ModelViewSet):
    queryset = LocationMaster.objects.all()
    serializer_class = LocationMasterSerializer

# Practice Unit Master API View
class PracticeUnitMasterViewSet(viewsets.ModelViewSet):
    queryset = PracticeUnitMaster.objects.all()
    serializer_class = PracticeUnitMasterSerializer

