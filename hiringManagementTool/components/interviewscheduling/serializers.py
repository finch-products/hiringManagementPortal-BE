from rest_framework import serializers
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.constants import InterviewStatus
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
import datetime


class InterviewSchedulingSerializer(serializers.ModelSerializer):
    ist_interviewstatus_display = serializers.SerializerMethodField()

    class Meta:
        model = InterviewSchedulingTable
        fields = '__all__'

    def get_ist_interviewstatus_display(self, obj):
        """Get human-readable name from enum."""
        try:
            return InterviewStatus(obj.ist_interviewstatus).name
        except ValueError:
            return "Unknown Status"  # In case the status doesn't match the enum
        
class InterviewSchedulingUpdateSerializer(serializers.ModelSerializer):
    ist_id = serializers.IntegerField(required=True)
    ist_interviewdate = serializers.DateField(required=False)
    ist_interviewtime = serializers.TimeField(required=False)
    ist_interviewtype = serializers.CharField(max_length=50, required=False)
    ist_interviewstatus = serializers.ChoiceField(choices=[(status.value, status.name) for status in InterviewStatus], required=False)

    class Meta:
        model = InterviewSchedulingTable
        fields = [
            'ist_id',
            'ist_interviewdate',
            'ist_interviewtime',
            'ist_interviewtype',
            'ist_interviewstatus',
        ]
        read_only_fields = ['ist_updatedate'] 

    def validate_ist_id(self, value):
        if not InterviewSchedulingTable.objects.filter(ist_id=value).exists():
            raise serializers.ValidationError(f"InterviewScheduling with ist_id {value} does not exist.")
        return value


class GetCdlIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateDemandLink
        fields = ['cdl_id']
