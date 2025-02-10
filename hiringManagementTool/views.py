from rest_framework import viewsets
from .models import ClientMaster, InternalDepartmentMaster, LOBMaster, LocationMaster, OpenDemand, EmployeeMaster, ClientManagerMaster, RoleMaster
from .serializers import ClientMasterSerializer, ClientManagerMasterSerializer, InternalDepartmentMasterSerializer, LOBMasterSerializer, LocationMasterSerializer, OpenDemandSerializer, EmployeeMasterSerializer, RoleMasterSerializer

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
class InternalDepartmentMasterViewSet(viewsets.ModelViewSet):
    queryset = InternalDepartmentMaster.objects.all()
    serializer_class = InternalDepartmentMasterSerializer

# Practice Unit Master API View
class EmployeeMasterViewSet(viewsets.ModelViewSet):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer
    
class RoleMasterViewSet(viewsets.ModelViewSet):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer