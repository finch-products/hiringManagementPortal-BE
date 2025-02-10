from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CandidateMaster, ClientMaster, InternalDepartmentMaster, LOBMaster, LocationMaster, OpenDemand, EmployeeMaster, ClientManagerMaster, RoleMaster, DemandStatusMaster
from .serializers import CandidateMasterSerializer, ClientMasterSerializer, ClientManagerMasterSerializer, InternalDepartmentMasterSerializer, LOBMasterSerializer, LocationMasterSerializer, OpenDemandSerializer, EmployeeMasterSerializer, RoleMasterSerializer,  LocationDetailsSerializer, DemandStatusDetailsSerializer, InternalDepartmentDetailsSerializer, LOBDetailSerializer, ClientDetailsSerializer

class OpenDemandViewSet(viewsets.ModelViewSet):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer

# Client Master API View
class ClientMasterViewSet(viewsets.ModelViewSet):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientMasterSerializer

class ClientDetailsViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnlyModelViewSet allows only GET requests
    queryset = ClientMaster.objects.all()
    serializer_class = ClientDetailsSerializer

    def list(self, request, *args, **kwargs):
        """Override list to return only required fields"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

#client details
class ClientDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClientMaster.objects.all()
    serializer_class = ClientDetailsSerializer

    def list(self, request, *args, **kwargs):
        """Override list to return only required fields"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class LocationDetailsViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnlyModelViewSet allows only GET requests
    queryset = LocationMaster.objects.all()
    serializer_class = LocationDetailsSerializer

    def list(self, request, *args, **kwargs):
        """Override list to return only required fields"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DemandStatusDetailsViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnlyModelViewSet allows only GET requests
    serializer_class = DemandStatusDetailsSerializer

    def get_queryset(self):
        """Sort records by dsm_sortid in ascending order"""
        return DemandStatusMaster.objects.all().order_by('dsm_sortid')

    def list(self, request, *args, **kwargs):
        """Override list to return only required fields"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class InternalDepartmentDetailsViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly API
    queryset = InternalDepartmentMaster.objects.select_related(
        'idm_deliverymanager_id__emp_lcm_id'  # Optimized query for related fields
    ).order_by('idm_id')
    serializer_class = InternalDepartmentDetailsSerializer

class LOBDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """API View to fetch LOB details with client partner & delivery manager."""
    queryset = LOBMaster.objects.all()
    serializer_class = LOBDetailSerializer
    
class CandidateMasterViewSet(viewsets.ModelViewSet):
    queryset = CandidateMaster.objects.all()
    serializer_class = CandidateMasterSerializer
    
class RoleMasterViewSet(viewsets.ModelViewSet):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
