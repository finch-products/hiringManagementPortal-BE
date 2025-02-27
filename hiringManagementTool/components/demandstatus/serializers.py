from rest_framework import serializers
from hiringManagementTool.models.demandstatus import DemandStatusMaster

class DemandStatusDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = ['dsm_sortid', 'dsm_code', 'dsm_description']

class DemandStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = ['dsm_code']