from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework import serializers
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.components.locations.serializers import LocationMasterSerializer

class CandidateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateStatusMaster
        fields = ["csm_id", "csm_code"]


class CandidateMasterSerializer(serializers.ModelSerializer):
    candidate_status = CandidateStatusSerializer(source='cdm_csm_id', read_only=True)
    lcm_name =serializers.CharField(source="cdm_location.lcm_name",read_only=True)
    cdm_insertby = serializers.CharField(source='cdm_insertby.emp_id', read_only=True)
    cdm_updateby = serializers.CharField(source='cdm_updateby.emp_id', read_only=True)

    class Meta:
        model = CandidateMaster
        fields = [
            "cdm_id",
            "cdm_emp_id",
            "cdm_name",
            "cdm_email",
            "cdm_phone",
            "cdm_profile",
            "cdm_description",
            "cdm_keywords",
            "cdm_insertdate",
            "cdm_updatedate",
            "cdm_isinternal",
            "cdm_isactive",
            "cdm_location",
            "lcm_name",
            "candidate_status",
            "cdm_insertby",
            "cdm_updateby"
        ]