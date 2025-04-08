# serializers.py for demand-history
from rest_framework import serializers
from hiringManagementTool.models.demandhistory import DemandHistory

class DemandHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandHistory
        fields = '__all__'


class DemandHistoryapiSerializer(serializers.Serializer):
    message = serializers.CharField()
    date = serializers.DateTimeField()
