# views.py for candidate-demand
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