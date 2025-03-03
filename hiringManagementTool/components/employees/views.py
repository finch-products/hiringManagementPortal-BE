from hiringManagementTool.models.roles import RoleMaster
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from hiringManagementTool.models.employees import EmployeeMaster
from hiringManagementTool.components.employees.serializers import EmployeeMasterSerializer, EmployeeRolesSerializer
from rest_framework.decorators import api_view

class EmployeeAPIView(ListCreateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer

class EmployeeDetailAPIView(RetrieveUpdateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer
    lookup_field = 'lob_id'
    lookup_url_kwarg = 'id'

class EmployeeByRoleAPIView(APIView):
    def get(self, request):
        # Mapping role names to desired snake_case format
        role_mapping = {
            "SPOC": "spoc",
            "Delivery Manager": "delivery_manager",
            "Client Partner": "client_partner"
        }
        
        # Get roles that match the given names
        roles = RoleMaster.objects.filter(rlm_name__in=role_mapping.keys())

        response_data = {}

        for role in roles:
            # Get employees associated with this role
            employees = EmployeeMaster.objects.filter(emp_rlm_id=role)
            serialized_employees = EmployeeRolesSerializer(employees, many=True).data
            
            # Use the mapped role name in snake_case
            response_data[role_mapping[role.rlm_name]] = serialized_employees

        return Response(response_data)
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
