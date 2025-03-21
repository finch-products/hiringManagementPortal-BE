from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hiringManagementTool.components.departments.serializers import InternalDepartmentSerializer
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.employees import EmployeeMaster
from hiringManagementTool.models.roles import RoleMaster
from .serializers import EmployeeMasterSerializer
# class InternalDepartmentAPIView(APIView):  # ReadOnly API
#     queryset = InternalDepartmentMaster.objects.select_related(
#         'idm_deliverymanager_id__emp_lcm_id'  # Optimized query for related fields
#     ).order_by('idm_id')
#     serializer_class = InternalDepartmentDetailsSerializer

class InternalDepartmentAPIView(APIView):
    """Handles GET and POST requests for InternalDepartment"""
    
    def get(self, request):
        """Retrieve all InternalDepartment"""
        demands = InternalDepartmentMaster.objects.all().order_by('-idm_insertdate')
        serializer = InternalDepartmentSerializer(demands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new OpenDemand"""
        serializer = InternalDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeByRoleAPIView(APIView):
    def get(self, request):
        # Get roles that match 'SPOC' and 'Delivery Manager'
        roles = RoleMaster.objects.filter(rlm_name__in=["SPOC", "Delivery Manager", "Client Partner"])
        
        response_data = {}

        for role in roles:
            # Get employees associated with this role
            employees = EmployeeMaster.objects.filter(emp_rlm_id=role)
            serialized_employees = EmployeeMasterSerializer(employees, many=True).data
            
            # Add data to response dictionary
            response_data[role.rlm_name] = serialized_employees
        
        return Response(response_data)