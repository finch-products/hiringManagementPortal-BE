from hiringManagementTool.models.clients import EmployeeMaster
from rest_framework import serializers

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'