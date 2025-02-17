from hiringManagementTool.components.employees.serializers import EmployeeMasterSerializer
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.employees import EmployeeMaster
from rest_framework import serializers

# class InternalDepartmentDetailsSerializer(serializers.ModelSerializer):
#     delivery_manager = serializers.SerializerMethodField()  # Fetch delivery manager details

#     class Meta:
#         model = InternalDepartmentMaster
#         fields = ['idm_id', 'idm_unitname', 'delivery_manager']

#     def get_delivery_manager(self, obj):
#         """Fetch delivery manager details along with location name"""
#         if obj.idm_deliverymanager_id:
#             delivery_manager = obj.idm_deliverymanager_id
#             return {
#                 "emp_id": delivery_manager.emp_id,
#                 "emp_uniqueid": delivery_manager.emp_uniqueid,
#                 "emp_name": delivery_manager.emp_name,
#                 "emp_email": delivery_manager.emp_email,
#                 "emp_phone": delivery_manager.emp_phone,
#                 "emp_location": delivery_manager.emp_lcm_id.lcm_name if delivery_manager.emp_lcm_id else None
#             }
#         return None
    

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']

class InternalDepartmentSerializer(serializers.ModelSerializer):

    idm_spoc_id = EmployeeMasterSerializer(read_only=True)
    idm_deliverymanager_id = EmployeeMasterSerializer(read_only=True)

    class Meta:
        model = InternalDepartmentMaster
        fields = '__all__'