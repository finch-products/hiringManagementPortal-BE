from rest_framework import generics
from hiringManagementTool.models.clients import ClientMaster
from rest_framework import serializers

class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = '__all__'


class ClientMimimumDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_name', 'clm_managername']
