from rest_framework import serializers
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.constants import InterviewStatus, InterviewType
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
import datetime
import json 
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from django.utils import timezone

class InterviewSchedulingSerializer(serializers.ModelSerializer):
    ist_interviewstatus_display = serializers.SerializerMethodField()
    ist_interviewtype_display = serializers.SerializerMethodField()
    ist_timezone_display = serializers.SerializerMethodField() # Added timezone display method (optional but good practice)

    class Meta:
        model = InterviewSchedulingTable
        fields = '__all__' # Includes all fields from the model

    def get_ist_interviewstatus_display(self, obj):
        try:
            # Ensure obj.ist_interviewstatus is not None before creating Enum
            if obj.ist_interviewstatus is not None:
                 return InterviewStatus(obj.ist_interviewstatus).name
            return "Not Set" # Or None, or ""
        except ValueError:
            return "Unknown Status" # Or f"Invalid Status Value: {obj.ist_interviewstatus}"

    def get_ist_interviewtype_display(self, obj):
        try:
            # Ensure obj.ist_interviewtype is not None before creating Enum
            if obj.ist_interviewtype is not None:
                return InterviewType(obj.ist_interviewtype).name
            return "Not Set" # Or None, or ""
        except ValueError:
            return "Unknown Type" # Or f"Invalid Type Value: {obj.ist_interviewtype}"

    def get_ist_timezone_display(self, obj):
        # Assuming ist_timezone is stored directly as a string
        return obj.ist_timezone


# --- Updated InterviewSchedulingUpdateSerializer ---
class InterviewSchedulingUpdateSerializer(serializers.ModelSerializer):
    # Required field to identify the interview
    ist_id = serializers.IntegerField(required=True, write_only=True) # write_only=True if you don't want it in response schema hints

    # Optional fields for update
    ist_interviewdate = serializers.DateField(required=False)
    ist_interview_start_time = serializers.TimeField(required=False) # Renamed from ist_interviewtime
    ist_interview_end_time = serializers.TimeField(required=False)   # Added end time
    ist_timezone = serializers.CharField(max_length=50, required=False)
    ist_interviewtype = serializers.ChoiceField(
        choices=[(type.name, type.name) for type in InterviewType], # Accept name input
        required=False
    )
    ist_interviewstatus = serializers.ChoiceField(
        choices=[(status.name, status.name) for status in InterviewStatus], # Accept name input
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
            # 'ist_updatedate' is handled automatically or in the view
        ]
        # read_only_fields = ['ist_updatedate'] # ist_updatedate is usually handled by auto_now=True or manually in the view

    def validate_ist_id(self, value):
        """Check if the interview instance exists."""
        if not InterviewSchedulingTable.objects.filter(ist_id=value).exists():
            raise serializers.ValidationError(f"InterviewScheduling with ist_id {value} does not exist.")
        return value

    def validate(self, data):
        """
        Optional: Add cross-field validation, e.g., end_time after start_time.
        Requires accessing potentially non-updated instance values if not all fields are provided.
        It's often easier to do this validation in the view where you have the instance.
        """
        # Example: Check if start_time and end_time are provided together and valid
        start_time = data.get('ist_interview_start_time')
        end_time = data.get('ist_interview_end_time')

        # If only one is provided, we might need the existing value from the instance
        # which isn't directly available here without context.
        # If both are provided:
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
