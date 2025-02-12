from rest_framework import serializers
from .models import CandidateMaster, ClientMaster, ClientManagerMaster, LOBMaster, LocationMaster, OpenDemand, InternalDepartmentMaster, EmployeeMaster, RoleMaster, DemandStatusMaster


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

class LocationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMaster
        fields = ['lcm_id', 'lcm_name']

class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMaster
        fields = ['clm_id', 'clm_name', 'clm_managername']

class DemandStatusDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = ['dsm_sortid', 'dsm_code', 'dsm_description']


class InternalDepartmentDetailsSerializer(serializers.ModelSerializer):
    delivery_manager = serializers.SerializerMethodField()  # Fetch delivery manager details

    class Meta:
        model = InternalDepartmentMaster
        fields = ['idm_id', 'idm_unitname', 'delivery_manager']

    def get_delivery_manager(self, obj):
        """Fetch delivery manager details along with location name"""
        if obj.idm_deliverymanager_id:
            delivery_manager = obj.idm_deliverymanager_id
            return {
                "emp_id": delivery_manager.emp_id,
                "emp_uniqueid": delivery_manager.emp_uniqueid,
                "emp_name": delivery_manager.emp_name,
                "emp_email": delivery_manager.emp_email,
                "emp_phone": delivery_manager.emp_phone,
                "emp_location": delivery_manager.emp_lcm_id.lcm_name if delivery_manager.emp_lcm_id else None
            }
        return None
    
class LocationDetailSerializer(serializers.ModelSerializer):
    """Serializer for fetching Location details (only name)."""
    class Meta:
        model = LocationMaster
        fields = ['lcm_name']

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

class LOBDetailSerializer(serializers.ModelSerializer):
    lob_clientpartner = EmployeeDetailSerializer()
    lob_deliverymanager = EmployeeDetailSerializer()

    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name', 'lob_clientpartner', 'lob_deliverymanager']

class CandidateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateMaster
        fields = '__all__'

        
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = '__all__'


class DemandStatusforstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandStatusMaster
        fields = "__all__"  # Include all fields from DemandStatusMaster

class OpenDemandwithstatusSerializer(serializers.ModelSerializer):
    demand_status = DemandStatusforstatusSerializer(source="dem_dsm_id", read_only=True)  # Nested serializer

    class Meta:
        model = OpenDemand
        fields = [
            "dem_id",
            "dem_ctoolnumber",
            "dem_ctooldate",
            "dem_cmm_id",
            "dem_clm_id",
            "dem_lcm_id",
            "dem_validtill",
            "dem_skillset",
            "dem_lob_id",
            "dem_idm_id",
            "dem_positions",
            "dem_rrnumber",
            "dem_jrnumber",
            "dem_rrgade",
            "dem_gcblevel",
            "dem_jd",
            "dem_comment",
            "dem_isreopened",
            "dem_isactive",
            "dem_insertdate",
            "dem_insertby",
            "dem_updatedate",
            "dem_updateby",
            "demand_status",  # This will include demand status details
        ]