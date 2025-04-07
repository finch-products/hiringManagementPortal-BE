from hiringManagementTool.components.employees.serializers import EmployeeMasterSerializer
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.employees import EmployeeMaster
from rest_framework import serializers

class EmployeeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']  # Only these fields for nested employees

class InternalDepartmentMasterSerializer(serializers.ModelSerializer):
    idm_spoc_id = EmployeeMinimalSerializer()
    idm_deliverymanager_id = EmployeeMinimalSerializer()
    
    class Meta:
        model = InternalDepartmentMaster
        fields = '__all__' 

class InternalDepartmentSerializer(serializers.ModelSerializer):
    idm_spoc_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(),
        required=False, 
        allow_null=True 
    )
    idm_deliverymanager_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeMaster.objects.all(),
        required=False,  
        allow_null=True  
    )

    class Meta:
        model = InternalDepartmentMaster
        fields = '__all__'