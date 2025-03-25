from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.locations import LocationMaster
from .serializers import CandidateDemandLinkSerializer, OpenDemandResponseSerializer, NonlinkedResponseSerializer
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

        # Fetch linked candidates
        linked_candidates = CandidateDemandLink.objects.filter(cdl_dem_id=demand.dem_id)
        logger.info(f"Found {linked_candidates.count()} candidates for demand {dem_id}")

        response_data = {
            "cdl_dem_id": demand.dem_id,
            "demand_details": demand,
            "candidates": linked_candidates
        }

        serializer = OpenDemandResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetNonCandidatelistByDemandId(APIView):
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

        # Fetch linked candidates
        linked_candidates = CandidateDemandLink.objects.filter(cdl_dem_id=demand.dem_id)
        logger.info(f"Found {linked_candidates.count()} candidates for demand {dem_id}")

        # Fetch non-linked candidates
        linked_candidate_ids = linked_candidates.values_list('cdl_cdm_id', flat=True)
        non_linked_candidates = CandidateMaster.objects.exclude(cdm_id__in=linked_candidate_ids)
        logger.info(f"Found {non_linked_candidates.count()} candidates not linked to demand {dem_id}")

        response_data = {
            "cdl_dem_id": demand.dem_id,
            "demand_details": demand,
            "candidates_not_added": non_linked_candidates
        }

        serializer = NonlinkedResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from .serializers import CandidateDemandLinkSerializer'''

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
    

class GetCandidatesdetailByDemandID(APIView):
    def post(self, request):
        try:
            dem_id = request.data.get('dem_id')
            if not dem_id:
                return Response({"error": "dem_id is required"}, status=400)

            # Fetch candidate data with status and location details
            candidates_data = CandidateDemandLink.objects.filter(cdl_dem_id=dem_id)\
                .select_related('cdl_cdm_id', 'cdl_csm_id', 'cdl_cdm_id__cdm_location_id')\
                .values(
                    'cdl_cdm_id__cdm_id',
                    'cdl_cdm_id__cdm_name',
                    'cdl_cdm_id__cdm_email',
                    'cdl_cdm_id__cdm_phone',
                    'cdl_cdm_id__cdm_keywords',
                    'cdl_cdm_id__cdm_location_id',
                    'cdl_cdm_id__cdm_profile',
                    'cdl_cdm_id__cdm_insertdate',
                    'cdl_cdm_id__cdm_updatedate',
                    'cdl_csm_id__csm_code',
                    'cdl_csm_id__csm_id'
                )

            # Fetch location data
            location_data = {loc.lcm_id: loc.lcm_name for loc in LocationMaster.objects.all()}

            # Initialize status-based dictionary
            status_data = {status.csm_code: [] for status in CandidateStatusMaster.objects.all()}

            # Populate the data
            for candidate in candidates_data:
                candidate_info = {
                    "cdm_id": candidate['cdl_cdm_id__cdm_id'],
                    "name": candidate['cdl_cdm_id__cdm_name'],
                    "email": candidate['cdl_cdm_id__cdm_email'],
                    "phone": candidate['cdl_cdm_id__cdm_phone'],
                    "keywords": candidate['cdl_cdm_id__cdm_keywords'],
                    "status": {
                        "id": candidate['cdl_csm_id__csm_id'],
                        "text": candidate['cdl_csm_id__csm_code']
                    },
                    "location": location_data.get(candidate['cdl_cdm_id__cdm_location_id'], "Unknown"),
                    "profile": candidate['cdl_cdm_id__cdm_profile'],
                    "insertdate": candidate['cdl_cdm_id__cdm_insertdate'].strftime('%Y-%m-%d') if candidate['cdl_cdm_id__cdm_insertdate'] else None,
                    "updatedate": candidate['cdl_cdm_id__cdm_updatedate'].strftime('%Y-%m-%d') if candidate['cdl_cdm_id__cdm_updatedate'] else None,
                }
                status_data[candidate['cdl_csm_id__csm_code']].append(candidate_info)

            return Response({
                "dem_id": dem_id,
                "candidates_by_status": status_data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
