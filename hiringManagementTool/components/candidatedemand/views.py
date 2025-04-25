from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
from .serializers import CandidateDemandLinkSerializer, OpenDemandResponseSerializer, NonlinkedResponseSerializer, CandidatesDetailbyDemIdSerializer
import logging
logger = logging.getLogger(__name__)

class GetCandidatelistByDemandId(APIView):
    def post(self, request):
        dem_id = request.data.get("dem_id")
        if not dem_id:
            logger.error("dem_id not provided in the request body")
            return Response({"error": "dem_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received request for dem_id: {dem_id}")
        demand = OpenDemand.objects.filter(dem_id=dem_id).first()
        if not demand:
            logger.error(f"Demand ID {dem_id} not found in OpenDemand table")
            return Response({"error": "Demand not found"}, status=status.HTTP_404_NOT_FOUND)

        linked_candidates = CandidateDemandLink.objects.filter(cdl_dem_id=dem_id)
        logger.info(f"Found {linked_candidates.count()} candidates for demand {dem_id}")

        serializer = OpenDemandResponseSerializer({
            "cdl_dem_id": demand.dem_id,
            "demand_details": demand,
            "candidates": linked_candidates
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetNonCandidatelistByDemandId(APIView):
    def post(self, request):
        dem_id = request.data.get("dem_id")
        if not dem_id:
            logger.error("dem_id not provided in the request body")
            return Response({"error": "dem_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received request for dem_id: {dem_id}")
        demand = OpenDemand.objects.filter(dem_id=dem_id).first()
        if not demand:
            logger.error(f"Demand ID {dem_id} not found in OpenDemand table")
            return Response({"error": "Demand not found"}, status=status.HTTP_404_NOT_FOUND)

        linked_ids = CandidateDemandLink.objects.filter(cdl_dem_id=dem_id).values_list('cdl_cdm_id', flat=True)
        non_linked = CandidateMaster.objects.exclude(cdm_id__in=linked_ids)

        logger.info(f"Found {non_linked.count()} candidates not linked to demand {dem_id}")

        serializer = NonlinkedResponseSerializer({
            "cdl_dem_id": demand.dem_id,
            "demand_details": demand,
            "candidates_not_added": non_linked
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

class CandidateDemandLinkAPIView(APIView):
    def post(self, request):
        data = request.data  # Expecting a list of candidates under a demand
        
        if not isinstance(data, list):
            return Response({"error": "Expected a list of candidates"}, status=status.HTTP_400_BAD_REQUEST)

        if len(data) > 5:
            return Response({"error": "A demand can have up to 5 candidates"}, status=status.HTTP_400_BAD_REQUEST)

         # Check if demand linking is allowed
        if data and 'cdl_dem_id' in data[0]:  # Assuming each candidate data has a 'demand' field
            demand_id = data[0]['cdl_dem_id']
            try:
                demand = OpenDemand.objects.select_related('dem_dsm_id').get(id=demand_id)
                if demand.dem_dsm_id == 4 and demand.dem_dsm_id.dsm_inactive == 1:
                    return Response({"error": "Cannot link candidates to an inactive demand"}, status=status.HTTP_400_BAD_REQUEST)
            except OpenDemand.DoesNotExist:
                return Response({"error": "Demand not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CandidateDemandLinkSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidates linked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCandidatesDetailByDemandID(APIView):
    def post(self, request):
        try:
            dem_id = request.data.get('dem_id')
            if not dem_id:
                return Response({"error": "dem_id is required"}, status=400)

            serializer = CandidatesDetailbyDemIdSerializer()  # Initialize the serializer
            result = serializer.get_candidates_by_demand(dem_id)

            return Response(result)
        except Exception as e:
            # More specific error handling
            return Response({"error": str(e)}, status=500)
