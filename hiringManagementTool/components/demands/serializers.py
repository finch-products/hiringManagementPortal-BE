from hiringManagementTool.models.clients import ClientMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.lobs import LOBMaster
from hiringManagementTool.models.locations import LocationMaster
from rest_framework import serializers

class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_name'] 
class LocationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = ['lcm_id', 'lcm_name']

class LOBMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name']
class InternalDepartmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalDepartmentMaster
        fields = ['idm_id', 'idm_unitname']

class DemandStatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = ['dsm_id', 'dsm_code', 'dsm_description']

class OpenDemandSerializer(serializers.ModelSerializer):

    dem_clm_id = ClientMasterSerializer(read_only=True)
    dem_lcm_id = LocationMasterSerializer(read_only=True)
    dem_lob_id = LOBMasterSerializer(read_only=True)
    dem_idm_id = InternalDepartmentMasterSerializer(read_only=True)
    dem_dsm_id = DemandStatusMasterSerializer(read_only=True)
    class Meta:
        model = OpenDemand
        fields = '__all__'
