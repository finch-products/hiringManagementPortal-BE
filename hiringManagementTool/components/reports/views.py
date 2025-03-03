from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .services import get_age_demand_data, get_open_demand_data, get_total_positions_opened_last_week, get_demand_fulfillment_metrics, get_lob_target_progress, get_demand_data_by_description
from .serializers import (
    AgedemandReportSerializer, OpenDemandSerializer, TotalPositionsOpenedLastWeekSerializer, DemandFulfillmentMetricsSerializer, LobTargetProgressSerializer, DemandByStatusSerializer

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


class OpenDemandCountReportView(APIView):
    """
    API endpoint that returns aggregated open demand statistics.
    """
    def get(self, request, format=None):
        data = get_open_demand_data()  # Fetch open demand statistics
        serializer = OpenDemandSerializer(data)
        return Response(serializer.data)
    
class TotalPositionsOpenedLastWeekView(APIView):
    """
    API endpoint that returns the total number of positions opened last week.
    """
    def get(self, request, format=None):
        data = get_total_positions_opened_last_week()
        serializer = TotalPositionsOpenedLastWeekSerializer(data)
        return Response(serializer.data)
    
class DemandFulfillmentMetricsView(APIView):
    """
    Fetch recruitment progress summary as percentages.
    """
    def get(self, request, format=None):
        data = get_demand_fulfillment_metrics()
        serializer = DemandFulfillmentMetricsSerializer(data)
        return Response(serializer.data)
    
class LobTargetProgressView(APIView):
    """
    Fetch LOB target progress data.  The 'id' field contains the percentage as a string.
    """
    def get(self, request, format=None):
        data = get_lob_target_progress()
        serializer = LobTargetProgressSerializer(data, many=True)  # Serialize a list of items
        return Response(serializer.data)
    
class DemandByStatusView(APIView):
    """
    API endpoint that returns demand count categorized by status.
    """

    def get(self, request, format=None):
        raw_data = get_demand_data_by_description()
        
        # Transform the data
        formatted_data = []
        for entry in raw_data:
            formatted_data.append({
                "category": entry["category"],
                "LOB": json.loads(entry["LOB"]),  # Convert JSON string to dictionary
                "total": int(entry["total"])  # Convert float to integer if applicable
            })

        return Response({"data": formatted_data})