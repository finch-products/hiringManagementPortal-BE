from hiringManagementTool.models.lobs import LOBMaster
from rest_framework import serializers

class LOBMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOBMaster
        fields = '__all__'
