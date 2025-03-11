from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from .services import get_age_demand_data, get_open_demand_data, get_total_positions_opened_last_week, get_demand_fulfillment_metrics, get_lob_target_progress, get_demand_data_by_description, get_client_selection_percentage, get_time_taken_for_profile_submission, get_average_time_taken_for_clients, fetch_report_data
from .serializers import (
    AgedemandReportSerializer, OpenDemandSerializer, TotalPositionsOpenedLastWeekSerializer, DemandFulfillmentMetricsSerializer, LobTargetProgressSerializer, DemandByStatusSerializer, ClientSelectionPercentageSerializer, demandTimeTakenSerializer, AverageTimeTakenbyClientsSerializer, ReportSerializer

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
    
class ClientSelectionPercentageView(APIView):
    """
    API view to fetch client selection percentage data.
    """
    def get(self, request, format=None):
        data = get_client_selection_percentage()
      
        serializer = ClientSelectionPercentageSerializer(data, many=True)
        return Response(serializer.data, status=200)
    
class TimeTakenForProfileSubmissionView(APIView):
    def get(self, request, format=None):
     
     data = get_time_taken_for_profile_submission()
     serializer = demandTimeTakenSerializer(data, many=True)
     return Response(serializer.data, status=200)

class TimeTakenFromInterviewToFeedbackView(APIView):
    def get(self, request, format=None):
     
     data = get_average_time_taken_for_clients()
     serializer = AverageTimeTakenbyClientsSerializer(data, many=True)
     return Response(serializer.data, status=200)
    

class ReportView(APIView):
    def get(self, request, *args, **kwargs):
        report_type = request.query_params.get("reportType")
        
        if report_type == "custom":
            # For custom reports, only start_date and end_date are required.
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            if not start_date or not end_date:
                return Response(
                    {"error": "start_date and end_date are required for custom reports."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Call fetch_report_data with custom parameters only.
            data = fetch_report_data(report_type=report_type, start_date=start_date, end_date=end_date)
            # Return custom report data as is (it already includes "Date range" and "report")
            return Response(data)
        else:
            # Validate and extract year
            year = request.query_params.get("year")
            if not year or not year.isdigit():
                return Response(
                    {"error": "Year parameter is required and must be a valid number."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            year = int(year)
            
            # Validate and extract month if provided (used for weekly report)
            month = request.query_params.get("month")
            if month:
                if not month.isdigit() or int(month) not in range(1, 13):
                    return Response(
                        {"error": "Invalid month provided."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                month = int(month)
            
            data = fetch_report_data(report_type=report_type, year=year, month=month)
            
            # For standard report types, the data is expected to have "year" and "report" keys.
            serializer = ReportSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
