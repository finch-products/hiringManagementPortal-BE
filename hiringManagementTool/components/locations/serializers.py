from rest_framework import serializers
from hiringManagementTool.models.locations import LocationMaster

class LocationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = '__all__'

class LocationMinimumDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = ['lcm_id', 'lcm_name']
