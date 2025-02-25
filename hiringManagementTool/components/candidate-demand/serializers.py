from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    clm_id = serializers.IntegerField(source='dem_clm_id.clm_id')
    clm_name = serializers.CharField(source='dem_clm_id.clm_name')

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
            'dem_ctooldate', 'position_name', 'dem_validtill', 'dem_skillset', 
            'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 
            'dem_gcblevel', 'dem_jd', 'dem_comment', 'dem_isreopened', 
            'dem_isactive', 'dem_insertdate', 'dem_updatedate', 'dem_insertby', 
            'dem_updateby'
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