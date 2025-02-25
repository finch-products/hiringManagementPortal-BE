# serializers.py for candidate-demand
from rest_framework import serializers
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.candidatedemand import CandidateDemandLink

class CandidateDemandLinkSerializer(serializers.ModelSerializer):
    cdl_cdm_id = serializers.CharField(required=True)  # Accept string input
    cdl_dem_id = serializers.CharField(required=True)  

    cdl_csm_id = serializers.PrimaryKeyRelatedField(
        queryset=CandidateStatusMaster.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CandidateDemandLink
        fields = ["cdl_cdm_id", "cdl_dem_id", "cdl_csm_id"]

    def create(self, validated_data):
        # Convert cdl_cdm_id string into CandidateMaster instance
        try:
            validated_data['cdl_cdm_id'] = CandidateMaster.objects.get(cdm_id=validated_data['cdl_cdm_id'])
        except CandidateMaster.DoesNotExist:
            raise serializers.ValidationError({"cdl_cdm_id": "Invalid CandidateMaster ID"})

        # Convert cdl_dem_id string into OpenDemand instance
        try:
            validated_data['cdl_dem_id'] = OpenDemand.objects.get(dem_id=validated_data['cdl_dem_id'])
        except OpenDemand.DoesNotExist:
            raise serializers.ValidationError({"cdl_dem_id": "Invalid OpenDemand ID"})

        # Default status handling
        if 'cdl_csm_id' not in validated_data or validated_data['cdl_csm_id'] is None:
            default_status = CandidateStatusMaster.objects.filter(pk=1).first()
            validated_data['cdl_csm_id'] = default_status

        return super().create(validated_data)
