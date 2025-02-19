from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
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
        """Create a new demand and auto-assign status"""
        print("\n📥 Incoming Request Data:", request.data)
        print("\n📥 dem_jd value:", request.data.get('dem_jd'))  # Log the value of dem_jd

        serializer = OpenDemandSerializer(data=request.data)
        if serializer.is_valid():
            print("\n✅ Serializer Validated Data:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        print("\n❌ Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DemandDetailAPIView(RetrieveUpdateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer
    lookup_field = 'dem_id'
    lookup_url_kwarg = 'id'