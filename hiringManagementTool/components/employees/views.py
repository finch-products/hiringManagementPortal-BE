from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.models.employees import EmployeeMaster
from hiringManagementTool.components.employees.serializers import EmployeeMasterSerializer, ClientPartnerSerializer, DeliveryManagerSerializer
from hiringManagementTool.models.roles import RoleMaster
from rest_framework.response import Response
from rest_framework.decorators import api_view

class EmployeeAPIView(ListCreateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer

class EmployeeDetailAPIView(RetrieveUpdateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer
    lookup_field = 'lob_id'
    lookup_url_kwarg = 'id'

@api_view(['GET'])
def get_client_partners(request):
    try:
        client_partner_role = RoleMaster.objects.get(rlm_name="Client Partner")
        client_partners = EmployeeMaster.objects.filter(emp_rlm_id=client_partner_role, emp_isactive=True)
        serializer = ClientPartnerSerializer(client_partners, many=True)
        return Response(serializer.data, status=200)
    except RoleMaster.DoesNotExist:
        return Response({"error": "Role 'Client Partner' not found"}, status=404)
    
@api_view(['GET'])
def get_delivery_managers(request):
    try:
        delivery_manager_role = RoleMaster.objects.get(rlm_name="Delivery Manager")
        delivery_managers = EmployeeMaster.objects.filter(emp_rlm_id=delivery_manager_role, emp_isactive=True)
        serializer = DeliveryManagerSerializer(delivery_managers, many=True)
        return Response(serializer.data, status=200)
    except RoleMaster.DoesNotExist:
        return Response({"error": "Role 'Delivery Manager' not found"}, status=404)