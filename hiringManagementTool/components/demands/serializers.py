from hiringManagementTool.models.demands import OpenDemand
from rest_framework import serializers


class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDemand
        fields = '__all__'