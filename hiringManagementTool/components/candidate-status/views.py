from rest_framework.response import Response
from rest_framework.views import APIView
from hiringManagementTool.models.candidatestatus  import CandidateStatusMaster
from .serializers import CandidateStatusSerializer
from django.shortcuts import get_object_or_404
from hiringManagementTool.models.candidates import CandidateMaster

class CandidateStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        statuses = CandidateStatusMaster.objects.filter(csm_inactive=False)  # Exclude inactive statuses
        serializer = CandidateStatusSerializer(statuses, many=True)
        return Response(serializer.data)
    
class CandidateStatusAPIViewbyid(APIView):
    def get(self, request, id, *args, **kwargs):
        # Get the candidate's current status
        candidate = get_object_or_404(CandidateMaster, cdm_id=id)
        current_status = candidate.cdm_csm_id

        if not current_status:
            return Response({"error": "Candidate has no status assigned"}, status=400)

        # Get the list of restricted statuses from csm_resstatus
        restricted_status_ids = (
            [int(csm_id) for csm_id in current_status.csm_resstatus.split(",") if csm_id.strip().isdigit()]
            if current_status.csm_resstatus else []
        )

        # Filter out inactive statuses and those in the restricted list
        available_statuses = CandidateStatusMaster.objects.filter(
            csm_inactive=False
        ).exclude(csm_id__in=restricted_status_ids)

        serializer = CandidateStatusSerializer(available_statuses, many=True)
        return Response(serializer.data)