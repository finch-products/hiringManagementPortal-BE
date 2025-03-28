from rest_framework import serializers
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster

class InterviewSchedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSchedulingTable
        fields = '__all__'