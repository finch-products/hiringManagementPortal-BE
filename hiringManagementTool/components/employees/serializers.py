from hiringManagementTool.models.clients import EmployeeMaster
from hiringManagementTool.components.roles.serializers import RoleMasterSerializer
from rest_framework import serializers

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'

    def validate(self, data):
        required_fields = ['emp_uniqueid', 'emp_name', 'emp_email', 'emp_insertby']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f"{field} is required")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['rlm_name'] = instance.emp_rlm_id.rlm_name if instance.emp_rlm_id else None
        data['lcm_name'] = instance.emp_lcm_id.lcm_name if instance.emp_lcm_id else None
        return data

class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Serializer for Employee details with Location name."""
    emp_location = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_uniqueid', 'emp_name', 'emp_email', 'emp_phone', 'emp_location']

    def get_emp_location(self, obj):
        """Fetch location name from LocationMaster using emp_lcm_id."""
        if obj.emp_lcm_id:  # emp_lcm_id is ForeignKey to LocationMaster(lcm_id)
            return obj.emp_lcm_id.lcm_name  
        return None  # If no location is assigned
    

class EmployeeRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']