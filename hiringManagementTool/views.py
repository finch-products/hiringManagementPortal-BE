from rest_framework import viewsets
from .models import ClientMaster, LOBMaster, LocationMaster, OpenDemand, EmployeeMaster, ClientManagerMaster, SubUnitMaster
from .serializers import ClientMasterSerializer, ClientManagerMasterSerializer, LOBMasterSerializer, LocationMasterSerializer, OpenDemandSerializer, EmployeeMasterSerializer, SubUnitMasterSerializer

class OpenDemandViewSet(viewsets.ModelViewSet):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer

# Client Master API View
class ClientMasterViewSet(viewsets.ModelViewSet):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer

# Client Manager Master API View
class ClientManagerMasterViewSet(viewsets.ModelViewSet):
    queryset = ClientManagerMaster.objects.all()
    serializer_class = ClientManagerMasterSerializer

# LOB Master API View
class LOBMasterViewSet(viewsets.ModelViewSet):
    queryset = LOBMaster.objects.all()
    serializer_class = LOBMasterSerializer

# Location Master API View
class LocationMasterViewSet(viewsets.ModelViewSet):
    queryset = LocationMaster.objects.all()
    serializer_class = LocationMasterSerializer

# Sub Unit Master API View
class SubUnitMasterViewSet(viewsets.ModelViewSet):
    queryset = SubUnitMaster.objects.all()
    serializer_class = SubUnitMasterSerializer

# Practice Unit Master API View
class EmployeeMasterViewSet(viewsets.ModelViewSet):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer