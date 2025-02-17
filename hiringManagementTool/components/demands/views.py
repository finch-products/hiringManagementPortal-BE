from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.components.demands.serializers import OpenDemandSerializer

class DemandAPIView(APIView):
    """Handles GET and POST requests for OpenDemand"""
    
    def get(self, request):
        """Retrieve all OpenDemands"""
        demands = OpenDemand.objects.all()
        serializer = OpenDemandSerializer(demands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new OpenDemand"""
        serializer = OpenDemandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DemandDetailAPIView(RetrieveUpdateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer
    lookup_field = 'dem_id'
    lookup_url_kwarg = 'id'