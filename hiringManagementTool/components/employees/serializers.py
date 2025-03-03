from hiringManagementTool.models.clients import EmployeeMaster
from rest_framework import serializers

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'


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
    
class ClientPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']

class DeliveryManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']
