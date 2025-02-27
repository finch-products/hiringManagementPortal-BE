from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from .serializers import OpenDemandResponseSerializer
import logging
logger = logging.getLogger(__name__)

class GetCandidatelistByDemandId(APIView):
    def post(self, request):
        # Extract dem_id from request body
        dem_id = request.data.get("dem_id")

        # Validate if dem_id is provided
        if not dem_id:
            logger.error("dem_id not provided in the request body")
            return Response({"error": "dem_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received request for dem_id: {dem_id}")

        try:
            demand = OpenDemand.objects.get(dem_id=dem_id)
        except OpenDemand.DoesNotExist:
            logger.error(f"Demand ID {dem_id} not found in OpenDemand table")
            return Response({"error": "Demand not found"}, status=status.HTTP_404_NOT_FOUND)

        candidates = CandidateDemandLink.objects.filter(cdl_dem_id=demand.dem_id)
        logger.info(f"Found {candidates.count()} candidates for demand {dem_id}")

        response_data = {
            "cdl_dem_id": demand.dem_id,
            "demand_details": demand,
            "candidates": candidates
        }

        serializer = OpenDemandResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from .serializers import CandidateDemandLinkSerializer

class CandidateDemandLinkAPIView(APIView):
    def post(self, request):
        data = request.data  # Expecting a list of candidates under a demand
        
        if not isinstance(data, list):
            return Response({"error": "Expected a list of candidates"}, status=status.HTTP_400_BAD_REQUEST)

        if len(data) > 5:
            return Response({"error": "A demand can have up to 5 candidates"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CandidateDemandLinkSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidates linked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)