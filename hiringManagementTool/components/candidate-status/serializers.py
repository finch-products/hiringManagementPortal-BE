from rest_framework import serializers
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster

class CandidateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateStatusMaster
        fields = ['csm_id', 'csm_code']  # Only returning csm_id and csm_code
