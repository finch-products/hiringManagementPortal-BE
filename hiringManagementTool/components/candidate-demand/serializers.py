from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    clm_id = serializers.IntegerField(source='dem_clm_id.clm_id')
    clm_name = serializers.CharField(source='dem_clm_id.clm_name')
    clm_managername = serializers.CharField(source='dem_clm_id.clm_managername')

class LocationSerializer(serializers.Serializer):
    lcm_id = serializers.IntegerField(source='dem_lcm_id.lcm_id')
    lcm_name = serializers.CharField(source='dem_lcm_id.lcm_name')

class LOBSerializer(serializers.Serializer):
    lob_id = serializers.IntegerField(source='dem_lob_id.lob_id')
    lob_name = serializers.CharField(source='dem_lob_id.lob_name')

class DepartmentSerializer(serializers.Serializer):
    idm_id = serializers.IntegerField(source='dem_idm_id.idm_id')
    idm_unitname = serializers.CharField(source='dem_idm_id.idm_unitname')

class StatusSerializer(serializers.Serializer):
    dsm_id = serializers.IntegerField(source='dem_dsm_id.dsm_id')
    dsm_code = serializers.CharField(source='dem_dsm_id.dsm_code')
    dsm_description = serializers.CharField(source='dem_dsm_id.dsm_description')
class DemandSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='*')
    location_details = LocationSerializer(source='*')
    lob_details = LOBSerializer(source='*')
    department_details = DepartmentSerializer(source='*')
    status_details = StatusSerializer(source='*')

    class Meta:
        model = OpenDemand
        fields = [
            'dem_id', 'client_details', 'location_details', 'lob_details',
            'department_details', 'status_details', 'dem_ctoolnumber', 
            'dem_ctooldate', 'dem_position_name', 'dem_validtill', 'dem_skillset', 
            'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 
            'dem_gcblevel', 'dem_jd', 'dem_comment', 'dem_isreopened', 
            'dem_isactive', 'dem_insertdate', 'dem_updatedate', 'dem_insertby', 
            'dem_updateby',
        ]

class CandidateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='cdl_cdm_id.cdm_name')
    email = serializers.EmailField(source='cdl_cdm_id.cdm_email')
    phone = serializers.CharField(source='cdl_cdm_id.cdm_phone')
    location_id = serializers.IntegerField(source='cdl_cdm_id.cdm_location.lcm_id')
    location_name = serializers.CharField(source='cdl_cdm_id.cdm_location.lcm_name')
    description = serializers.CharField(source='cdl_cdm_id.cdm_description')
    keywords = serializers.CharField(source='cdl_cdm_id.cdm_keywords')

    class Meta:
        model = CandidateDemandLink
        fields = [
            'cdl_id', 'cdl_cdm_id', 'name', 'email', 'phone', 
            'location_id', 'location_name', 'description', 
            'keywords', 'cdl_joiningdate', 'cdl_insertdate'
        ]

class OpenDemandResponseSerializer(serializers.Serializer):
    cdl_dem_id = serializers.CharField()
    demand_details = DemandSerializer()
    candidates = CandidateSerializer(many=True)

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
