from rest_framework import generics
from hiringManagementTool.models.clients import ClientMaster
from rest_framework import serializers

class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = '__all__'
        
    def to_internal_value(self, data):
     data = dict(data)  
     for key, value in data.items():
        if value == ['']:  
            data[key] = None
        elif isinstance(value, list):  # Handle list case
            data[key] = value[0]  # Take first value if list
     return super().to_internal_value(data)


class ClientMimimumDetailsSerializer(serializers.ModelSerializer):
    clm_lcm_name = serializers.SerializerMethodField()
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_clientid','clm_name', 'clm_managername', 'clm_clientemail',
                  'clm_clientphone', 'clm_lcm_id', 'clm_lcm_name', 'clm_isactive']

    def get_clm_lcm_name(self, obj):
        return obj.clm_lcm_id.lcm_name if obj.clm_lcm_id else None