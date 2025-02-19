from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_age_demand_data
from .serializers import (
    AgedemandReportSerializer
)

class AgedemandReportView(APIView):
    """
    API endpoint that returns aggregated age cluster data as JSON.
    """
    def get(self, request, format=None):
        data = get_age_demand_data()  # Execute the raw SQL query
        serializer = AgedemandReportSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
