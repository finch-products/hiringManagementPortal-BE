from datetime import datetime
from hiringManagementTool.constants import DEMAND_STATUS
from hiringManagementTool.models.clients import ClientMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.lobs import LOBMaster
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.employees import EmployeeMaster
from rest_framework import serializers
import json

class ClientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_name', 'clm_managername','clm_clientemail'] 
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

    dem_clm_id = serializers.PrimaryKeyRelatedField(queryset=ClientMaster.objects.only("clm_id"), write_only=True)
    dem_lcm_id = serializers.PrimaryKeyRelatedField(queryset=LocationMaster.objects.only("lcm_id"), write_only=True, required=False)
    dem_lob_id = serializers.PrimaryKeyRelatedField(queryset=LOBMaster.objects.only("lob_id"), write_only=True, required=True)
    dem_idm_id = serializers.PrimaryKeyRelatedField(queryset=InternalDepartmentMaster.objects.only("idm_id"), write_only=True, required=False)
    dem_dsm_id = serializers.PrimaryKeyRelatedField(queryset=DemandStatusMaster.objects.only("dsm_id"), write_only=True, required=False)
    dem_position_location = serializers.JSONField(required=False, default=list)

    def validate(self, data):
        """Custom validation to handle empty values properly"""
         # Handle dem_jd: set to None if empty string, blank, or not present
        if 'dem_jd' in data and data['dem_jd'] in ['', None]:
             data['dem_jd'] = None
            
        # Handle empty list for dem_position_location
        if 'dem_position_location' in data and data['dem_position_location'] == []:
            data['dem_position_location'] = None
            
        return data
    
    def to_representation(self, instance):
        """Custom representation to fetch location names from LocationMaster based on IDs"""
        data = super().to_representation(instance)

        # Fetching the stored location IDs
        location_ids = data.get("dem_position_location", [])

        if isinstance(location_ids, list):
            locations = LocationMaster.objects.filter(lcm_id__in=location_ids).values("lcm_id", "lcm_name")
            data["dem_location_position"] = list(locations)  # Format it as required
        else:
            data["dem_location_position"] = None

        return data
    
    def create(self, validated_data):
        jd_present = validated_data.get("dem_jd")
        status_key = "OPEN" if jd_present else "JD_NOT_RECEIVED"
        dsm_code = DEMAND_STATUS.get(status_key)

        try:
            dsm_status = DemandStatusMaster.objects.only("dsm_id").get(dsm_code__iexact=dsm_code)
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
    """Serializer to validate and update OpenDemand"""
    
    dem_id = serializers.CharField(write_only=True)
    dem_updateby_id = serializers.PrimaryKeyRelatedField(queryset=EmployeeMaster.objects.all(), write_only=True)
    
    class Meta:
        model = OpenDemand
        fields = ['dem_id', 'dem_updateby_id', 'dem_dsm_id', 'dem_clm_id', 'dem_lob_id', 
                  'dem_idm_id', 'dem_lcm_id', 'dem_updatedate', 'dem_ctooldate', 'dem_validtill', 'dem_skillset',
    'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 'dem_gcblevel',
    'dem_jd', 'dem_comment', 'dem_isreopened', 'dem_isactive', 'dem_position_name', 'dem_position_location','dem_mandatoryskill','dem_ctoolnumber']

    def validate(self, data):
        """Custom validation for demand status and foreign keys"""
        dem_id = data.get("dem_id")
        new_dsm_id = data.get("dem_dsm_id")

        try:
            open_demand = OpenDemand.objects.select_related("dem_dsm_id").get(dem_id=dem_id)
        except OpenDemand.DoesNotExist:
            raise serializers.ValidationError({"dem_id": "OpenDemand with the provided ID does not exist."})

        # Check status restrictions
        if new_dsm_id:
            current_status = open_demand.dem_dsm_id
            restricted_statuses = current_status.dsm_resstatus.split(",") if current_status.dsm_resstatus else []
            if str(new_dsm_id.dsm_id) in restricted_statuses:
                raise serializers.ValidationError({"dem_dsm_id": "This status cannot be assigned to this demand."})

        return data

    def update(self, instance, validated_data):
        """Update only the provided fields while keeping others unchanged"""
        validated_data.pop('dem_id', None)  # ✅ Remove `dem_id` from update
        
        # Track which fields to update
        fields_to_update = []

        for attr, value in validated_data.items():
            if value not in [None, "",' ',[],'']:  # ✅ Only update explicitly provided fields
                setattr(instance, attr, value)
                fields_to_update.append(attr)
                
        instance.dem_updatedate = datetime.now()  # ✅ Always update timestamp
        fields_to_update.append('dem_updatedate')
        instance.save(update_fields=validated_data.keys())  # ✅ Save only changed fields

        return instance  # ✅ Return updated object with full data

class AllOpenDemandsIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDemand
        fields = ['dem_id']