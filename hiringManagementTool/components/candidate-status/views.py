from rest_framework.response import Response
from rest_framework.views import APIView
from hiringManagementTool.models.candidatestatus  import CandidateStatusMaster
from .serializers import CandidateStatusSerializer

class CandidateStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        statuses = CandidateStatusMaster.objects.filter(csm_inactive=False)  # Exclude inactive statuses
        serializer = CandidateStatusSerializer(statuses, many=True)
        return Response(serializer.data)