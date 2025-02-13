from hiringManagementTool.models.locations import LocationMaster
from rest_framework import serializers

class LocationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = '__all__'
