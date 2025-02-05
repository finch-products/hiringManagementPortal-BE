from rest_framework import serializers
from .models import ClientMaster, LOBMaster, LocationMaster, OpenDemand, PracticeUnitMaster

class OpenDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDemand
        fields = '__all__'
        
# Client Master Serializer
class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = '__all__'

# LOB Master Serializer
class LOBMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOBMaster
        fields = '__all__'

# Location Master Serializer
class LocationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = '__all__' 

# Practice Unit Master Serializer
class PracticeUnitMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeUnitMaster
        fields = '__all__'
