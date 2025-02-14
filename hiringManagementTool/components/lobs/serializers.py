from hiringManagementTool.components.employees.serializers import EmployeeDetailSerializer
from hiringManagementTool.models.lobs import LOBMaster
from rest_framework import serializers

class LOBMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOBMaster
        fields = '__all__'

class LOBMinimumDetailsSerializer(serializers.ModelSerializer):
    lob_clientpartner = EmployeeDetailSerializer()
    lob_deliverymanager = EmployeeDetailSerializer()

    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name', 'lob_clientpartner', 'lob_deliverymanager']
