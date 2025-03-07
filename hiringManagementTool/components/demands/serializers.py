from hiringManagementTool.constants import DEMAND_STATUS
from hiringManagementTool.models.clients import ClientMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.lobs import LOBMaster
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.employees import EmployeeMaster
from rest_framework import serializers

class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_name', 'clm_managername'] 
class LocationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = ['lcm_id', 'lcm_name']

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']

class LOBMasterSerializer(serializers.ModelSerializer):
    client_partner = serializers.SerializerMethodField()
    delivery_manager = serializers.SerializerMethodField()

    def get_client_partner(self, obj):
        if obj.lob_clientpartner_id:
            employee = EmployeeMaster.objects.filter(emp_id=obj.lob_clientpartner_id).first()
            return EmployeeMasterSerializer(employee).data if employee else None
        return None

    def get_delivery_manager(self, obj):
        if obj.lob_deliverymanager_id:
            employee = EmployeeMaster.objects.filter(emp_id=obj.lob_deliverymanager_id).first()
            return EmployeeMasterSerializer(employee).data if employee else None
        return None

    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name', 'client_partner', 'delivery_manager']

class InternalDepartmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalDepartmentMaster
        fields = ['idm_id', 'idm_unitname']

class DemandStatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = ['dsm_id', 'dsm_code', 'dsm_description']
class OpenDemandSerializer(serializers.ModelSerializer):
    client_details = ClientMasterSerializer(source='dem_clm_id', read_only=True)
    location_details = LocationMasterSerializer(source='dem_lcm_id', read_only=True)
    lob_details = LOBMasterSerializer(source='dem_lob_id', read_only=True)
    department_details = InternalDepartmentMasterSerializer(source='dem_idm_id', read_only=True)
    status_details = DemandStatusMasterSerializer(source='dem_dsm_id', read_only=True)

    dem_clm_id = serializers.PrimaryKeyRelatedField(queryset=ClientMaster.objects.all(), write_only=True)
    dem_lcm_id = serializers.PrimaryKeyRelatedField(queryset=LocationMaster.objects.all(), write_only=True, required=False)
    dem_lob_id = serializers.PrimaryKeyRelatedField(queryset=LOBMaster.objects.all(), write_only=True, required=False)
    dem_idm_id = serializers.PrimaryKeyRelatedField(queryset=InternalDepartmentMaster.objects.all(), write_only=True, required=False)
    dem_dsm_id = serializers.PrimaryKeyRelatedField(queryset=DemandStatusMaster.objects.all(), write_only=True, required=False)  # ✅ FIXED
    
    def create(self, validated_data):
        jd_present = validated_data.get("dem_jd")
        status_key = "OPEN" if jd_present else "JD_NOT_RECEIVED"
        dsm_code = DEMAND_STATUS.get(status_key)

        try:
            dsm_status = DemandStatusMaster.objects.get(dsm_code__iexact=dsm_code)
            validated_data["dem_dsm_id"] = dsm_status  # Assign ForeignKey instance
        except DemandStatusMaster.DoesNotExist:
            raise serializers.ValidationError(
                {"dem_dsm_id": f"❌ ERROR: Demand status '{dsm_code}' not found in the database."}
             )

        return super().create(validated_data)

    class Meta:
        model = OpenDemand
        fields = '__all__'

class OpenDemandUpdateSerializer(serializers.ModelSerializer):
    dem_id = serializers.IntegerField(required=True)  # Mandatory
    dem_updateby_id = serializers.IntegerField(required=True)  # Mandatory

    class Meta:
        model = OpenDemand
        fields = '__all__'
        extra_kwargs = {field: {"required": False, "allow_null": True} for field in fields}

class AllOpenDemandsIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDemand
        fields = ['dem_id']