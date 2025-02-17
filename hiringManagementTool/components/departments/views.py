from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hiringManagementTool.components.departments.serializers import InternalDepartmentSerializer
from hiringManagementTool.models.departments import InternalDepartmentMaster

# class InternalDepartmentAPIView(APIView):  # ReadOnly API
#     queryset = InternalDepartmentMaster.objects.select_related(
#         'idm_deliverymanager_id__emp_lcm_id'  # Optimized query for related fields
#     ).order_by('idm_id')
#     serializer_class = InternalDepartmentDetailsSerializer

class InternalDepartmentAPIView(APIView):
    """Handles GET and POST requests for InternalDepartment"""
    
    def get(self, request):
        """Retrieve all InternalDepartment"""
        demands = InternalDepartmentMaster.objects.all()
        serializer = InternalDepartmentSerializer(demands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new OpenDemand"""
        serializer = InternalDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)