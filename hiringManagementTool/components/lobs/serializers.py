from hiringManagementTool.components.employees.serializers import EmployeeDetailSerializer,EmployeeRolesSerializer,EmployeeMasterSerializer
from hiringManagementTool.models.lobs import LOBMaster
from rest_framework import serializers

class LOBMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOBMaster
        fields = '__all__'

class LOBMinimumDetailsSerializer(serializers.ModelSerializer):
    lob_clientpartner = EmployeeDetailSerializer()
    lob_deliverymanager = EmployeeDetailSerializer()
    lob_insertby_id = EmployeeRolesSerializer(source='lob_insertby', many=False, read_only=True)
    lob_updateby_id = EmployeeMasterSerializer(source='lob_updateby', many=False, read_only=True)

    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name','lob_description', 'lob_clientpartner', 'lob_deliverymanager','lob_insertby_id','lob_updateby_id']
