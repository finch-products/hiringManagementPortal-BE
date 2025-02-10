from rest_framework import serializers
from .models import ClientMaster, ClientManagerMaster, LOBMaster, LocationMaster, OpenDemand, InternalDepartmentMaster, EmployeeMaster, RoleMaster

class OpenDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDemand
        fields = '__all__'
        
# Client Master Serializer
class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = '__all__'

# Client Manager Master Serializer
class ClientManagerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientManagerMaster
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

# Sub Unit Master Serializer
class InternalDepartmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalDepartmentMaster
        fields = '__all__'

# Practice Unit Master Serializer
class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'
        
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = '__all__'
        