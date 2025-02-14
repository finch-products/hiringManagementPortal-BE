from hiringManagementTool.models.roles import RoleMaster
from rest_framework import serializers

class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = '__all__'