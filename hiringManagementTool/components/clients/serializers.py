from rest_framework import generics
from hiringManagementTool.models.clients import ClientMaster
from rest_framework import serializers

class ClientMasterSerializer(serializers.ModelSerializer):
    clm_logo = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = ClientMaster
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.clm_logo and request:
            data['clm_logo'] = request.build_absolute_uri(instance.clm_logo.url)
        return data
    
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