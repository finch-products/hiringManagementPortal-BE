from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.candidates.serializers import CandidateMasterSerializer
from hiringManagementTool.models.candidates import CandidateMaster

class CandidateAPIView(ListCreateAPIView):
    queryset = CandidateMaster.objects.all()

    serializer_class = CandidateMasterSerializer


class CandidateDetailAPIView(RetrieveUpdateAPIView):
    queryset = CandidateMaster.objects.all()
    serializer_class = CandidateMasterSerializer
    lookup_field = 'cdm_id'
    lookup_url_kwarg = 'cdm_id'