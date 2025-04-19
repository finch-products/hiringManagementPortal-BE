from rest_framework import serializers
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.constants import InterviewStatus, InterviewType
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from django.utils import timezone

class InterviewSchedulingSerializer(serializers.ModelSerializer):
    ist_interviewstatus_display = serializers.SerializerMethodField()
    ist_interviewtype_display = serializers.SerializerMethodField()
    ist_timezone_display = serializers.SerializerMethodField() 

    class Meta:
        model = InterviewSchedulingTable
        fields = '__all__' 

    def get_ist_interviewstatus_display(self, obj):
        try:
            if obj.ist_interviewstatus is not None:
                 return InterviewStatus(obj.ist_interviewstatus).name
            return "Not Set"
        except ValueError:
            return "Unknown Status" 

    def get_ist_interviewtype_display(self, obj):
        try:
            if obj.ist_interviewtype is not None:
                return InterviewType(obj.ist_interviewtype).name
            return "Not Set" 
        except ValueError:
            return "Unknown Type"

    def get_ist_timezone_display(self, obj):
        return obj.ist_timezone
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ist_interviewdate'] = instance.ist_interviewdate.isoformat()
        return representation


class InterviewSchedulingUpdateSerializer(serializers.ModelSerializer):
    ist_id = serializers.IntegerField(required=True, write_only=True)
    ist_interviewdate = serializers.DateField(required=False)
    ist_interview_start_time = serializers.TimeField(required=False)
    ist_interview_end_time = serializers.TimeField(required=False)
    ist_timezone = serializers.CharField(max_length=50, required=False)
    ist_interviewtype = serializers.ChoiceField(
    choices=[(type.value, type.name) for type in InterviewType],
    required=False
    )
    ist_interviewstatus = serializers.ChoiceField(
    choices=[(status.value, status.name) for status in InterviewStatus],
    required=False
    )

    ist_interviewround = serializers.IntegerField(required=False)
    ist_interviewers = serializers.JSONField(required=False) # For the JSON field
    ist_remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ist_meeting_details = serializers.CharField(required=False, allow_blank=True, allow_null=True) # Assuming text/link


    class Meta:
        model = InterviewSchedulingTable
        fields = [
            'ist_id',
            'ist_interviewdate',
            'ist_interview_start_time',
            'ist_interview_end_time',
            'ist_timezone',
            'ist_interviewtype',
            'ist_interviewstatus',
            'ist_interviewround',
            'ist_interviewers',
            'ist_remarks',
            'ist_meeting_details',
        ]
    
    def validate_ist_id(self, value):
        if not InterviewSchedulingTable.objects.filter(ist_id=value).exists():
            raise serializers.ValidationError(f"InterviewScheduling with ist_id {value} does not exist.")
        return value

    def validate(self, data):
        start_time = data.get('ist_interview_start_time')
        end_time = data.get('ist_interview_end_time')

        if start_time and end_time and start_time >= end_time:
             raise serializers.ValidationError("Interview end time must be after start time.")

        return data
    
class GetCdlIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateDemandLink
        fields = ['cdl_id']

class InterviewStatusSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()

class InterviewTypeSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()

from rest_framework import serializers

class TimezoneSerializer(serializers.Serializer):
    label = serializers.CharField()
    
class InterviewDetailsFilterSerializer(serializers.Serializer):
    filter_type = serializers.ChoiceField(choices=["all", "current", "next_one", "next_all"], required=False, default="all")
    candidate_id = serializers.CharField(required=False)
    demand_id = serializers.CharField(required=False)
    cdl_id = serializers.IntegerField(required=False)

    def get_interviews(self):
        filter_type = self.validated_data.get("filter_type", "all")
        candidate_id = self.validated_data.get("candidate_id", None)
        demand_id = self.validated_data.get("demand_id", None)
        cdl_id = self.validated_data.get("cdl_id", None)
        now = timezone.now()
        interviews = InterviewSchedulingTable.objects.all()

        if filter_type == "current":
            interviews = interviews.filter(ist_interviewdate=now.date())
        elif filter_type in ["next_one", "next_all"]:
            interviews = interviews.filter(ist_interviewdate__gt=now.date()).order_by('ist_interviewdate', 'ist_interview_start_time')

        if candidate_id:
            interviews = interviews.filter(
                ist_cdl_id__in=CandidateDemandLink.objects.filter(cdl_cdm_id=candidate_id).values_list('cdl_id', flat=True)
            )

        if demand_id:
            interviews = interviews.filter(
                ist_cdl_id__in=CandidateDemandLink.objects.filter(cdl_dem_id=demand_id).values_list('cdl_id', flat=True)
            )

        if cdl_id:
            interviews = interviews.filter(ist_cdl_id=cdl_id)

        if filter_type == "next_one":
            interviews = interviews[:1]

        return list(interviews)