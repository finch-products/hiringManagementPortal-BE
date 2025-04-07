from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework import serializers
from hiringManagementTool.models.employees import EmployeeMaster
from hiringManagementTool.models.lobs import LOBMaster
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.locations import LocationMaster

class ClientSerializer(serializers.Serializer):
    clm_id = serializers.IntegerField(source='dem_clm_id.clm_id')
    clm_name = serializers.CharField(source='dem_clm_id.clm_name')
    clm_managername = serializers.CharField(source='dem_clm_id.clm_managername')

class LocationSerializer(serializers.Serializer):
    lcm_id = serializers.IntegerField(source='dem_lcm_id.lcm_id',allow_null=True, default=None)
    lcm_name = serializers.CharField(source='dem_lcm_id.lcm_name',allow_null=True, default=None)


class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['emp_id', 'emp_name']

class LOBSerializer(serializers.Serializer):
    lob_id = serializers.IntegerField(source='dem_lob_id.lob_id')
    lob_name = serializers.CharField(source='dem_lob_id.lob_name')
    client_partner = serializers.SerializerMethodField()
    delivery_manager = serializers.SerializerMethodField()

    def get_client_partner(self, obj):
        if obj.dem_lob_id and obj.dem_lob_id.lob_clientpartner_id:
            employee = EmployeeMaster.objects.filter(emp_id=obj.dem_lob_id.lob_clientpartner_id).first()
            return EmployeeMasterSerializer(employee).data if employee else None
        return None

    def get_delivery_manager(self, obj):
        if obj.dem_lob_id and obj.dem_lob_id.lob_deliverymanager_id:
            employee = EmployeeMaster.objects.filter(emp_id=obj.dem_lob_id.lob_deliverymanager_id).first()
            return EmployeeMasterSerializer(employee).data if employee else None
        return None
    
    class Meta:
        model = LOBMaster
        fields = ['lob_id', 'lob_name', 'client_partner', 'delivery_manager']

class DepartmentSerializer(serializers.Serializer):
    idm_id = serializers.IntegerField(source='dem_idm_id.idm_id',allow_null=True, default=None)
    idm_unitname = serializers.CharField(source='dem_idm_id.idm_unitname',allow_null=True, default=None)

class StatusSerializer(serializers.Serializer):
    dsm_id = serializers.IntegerField(source='dem_dsm_id.dsm_id')
    dsm_code = serializers.CharField(source='dem_dsm_id.dsm_code')
    dsm_description = serializers.CharField(source='dem_dsm_id.dsm_description')

class PositionLocationSerializer(serializers.Serializer):
    lcm_id = serializers.IntegerField()
    lcm_name = serializers.SerializerMethodField()

    def get_lcm_name(self, obj):
        try:
            location = LocationMaster.objects.get(lcm_id=obj)
            return location.lcm_name
        except LocationMaster.DoesNotExist:
            return None

class DemandSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='*')
    location_details = LocationSerializer(source='*')
    lob_details = LOBSerializer(source='*')
    department_details = DepartmentSerializer(source='*')
    status_details = StatusSerializer(source='*')
    position_locations = serializers.SerializerMethodField()
    
    class Meta:
        model = OpenDemand
        fields = [
            'dem_id', 'client_details', 'location_details', 'lob_details',
            'department_details', 'status_details', 'dem_ctoolnumber', 
            'dem_ctooldate', 'dem_position_name', 'dem_validtill', 'dem_skillset', 
            'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 
            'dem_gcblevel', 'dem_jd', 'dem_comment', 'dem_isreopened', 
            'dem_isactive', 'dem_insertdate', 'dem_updatedate', 'dem_insertby', 
            'dem_updateby', "dem_mandatoryskill", "position_locations"
        ]

    def get_position_locations(self, obj):
        if not obj.dem_position_location:
            return []
        
        # Get all location IDs from the JSON field
        location_ids = obj.dem_position_location
        
        # Prepare data for serialization
        locations_data = []
        for loc_id in location_ids:
            try:
                location = LocationMaster.objects.get(lcm_id=loc_id)
                locations_data.append({
                    'lcm_id': location.lcm_id,
                    'lcm_name': location.lcm_name
                })
            except LocationMaster.DoesNotExist:
                continue
                
        return locations_data



class CandidateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateStatusMaster
        fields = ["csm_id", "csm_code"]

class CandidateSerializer(serializers.ModelSerializer):
    candidate_status = CandidateStatusSerializer(source='cdl_csm_id', read_only=True)
    name = serializers.CharField(source='cdl_cdm_id.cdm_name')
    email = serializers.EmailField(source='cdl_cdm_id.cdm_email')
    phone = serializers.CharField(source='cdl_cdm_id.cdm_phone')
    location_id = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    description = serializers.CharField(source='cdl_cdm_id.cdm_description')
    keywords = serializers.CharField(source='cdl_cdm_id.cdm_keywords')

    class Meta:
        model = CandidateDemandLink
        fields = [
            'cdl_id', 'cdl_cdm_id', 'name', 'email', 'phone', 
            'location_id', 'location_name', 'description', 
            'keywords', 'cdl_joiningdate', 'cdl_insertdate', 'candidate_status'
        ]

    def get_location_id(self, obj):
        """Handle None values for location_id"""
        if obj.cdl_cdm_id and obj.cdl_cdm_id.cdm_location:
            return obj.cdl_cdm_id.cdm_location.lcm_id
        return None  # Return None if no location

    def get_location_name(self, obj):
        """Handle None values for location_name"""
        if obj.cdl_cdm_id and obj.cdl_cdm_id.cdm_location:
            return obj.cdl_cdm_id.cdm_location.lcm_name
        return None  # Return None if no location


class CandidateMasterSerializer(serializers.ModelSerializer):
    cdl_id = serializers.SerializerMethodField()
    cdl_cdm_id = serializers.CharField(source='cdm_id')
    cdl_joiningdate = serializers.SerializerMethodField()
    cdl_insertdate = serializers.SerializerMethodField()
    candidate_status = serializers.SerializerMethodField()
    location_id = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()

    class Meta:
        model = CandidateMaster
        fields = [
            'cdl_id', 'cdl_cdm_id', 'cdm_name', 'cdm_email', 'cdm_phone', 
            'location_id', 'location_name', 'cdm_description', 
            'cdm_keywords', 'cdl_joiningdate', 'cdl_insertdate', 'candidate_status'
        ]

    def get_cdl_id(self, obj):
        # Check if the candidate is linked to any demand
        linked_demand = CandidateDemandLink.objects.filter(cdl_cdm_id=obj).first()
        return linked_demand.cdl_id if linked_demand else None

    def get_cdl_joiningdate(self, obj):
        # Check if the candidate is linked to any demand
        linked_demand = CandidateDemandLink.objects.filter(cdl_cdm_id=obj).first()
        return linked_demand.cdl_joiningdate if linked_demand else None

    def get_cdl_insertdate(self, obj):
        # Check if the candidate is linked to any demand
        linked_demand = CandidateDemandLink.objects.filter(cdl_cdm_id=obj).first()
        return linked_demand.cdl_insertdate if linked_demand else None

    def get_candidate_status(self, obj):
        # Check if the candidate is linked to any demand
        linked_demand = CandidateDemandLink.objects.filter(cdl_cdm_id=obj).first()
        if linked_demand and linked_demand.cdl_csm_id:
            return CandidateStatusSerializer(linked_demand.cdl_csm_id).data
        return None

    def get_location_id(self, obj):
        if obj.cdm_location:
            return obj.cdm_location.lcm_id
        return None

    def get_location_name(self, obj):
        if obj.cdm_location:
            return obj.cdm_location.lcm_name
        return None

class OpenDemandResponseSerializer(serializers.Serializer):
    cdl_dem_id = serializers.CharField()
    demand_details = DemandSerializer()
    candidates = CandidateSerializer(many=True) 


class NonlinkedResponseSerializer(serializers.Serializer):
    cdl_dem_id = serializers.CharField()
    demand_details = DemandSerializer()
    candidates_not_added = CandidateMasterSerializer(many=True) 

from rest_framework import serializers
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.candidatedemand import CandidateDemandLink

class CandidateDemandLinkSerializer(serializers.ModelSerializer):
    cdl_cdm_id = serializers.CharField(required=True)  # Accept string input
    cdl_dem_id = serializers.CharField(required=True)  

    cdl_csm_id = serializers.PrimaryKeyRelatedField(
        queryset=CandidateStatusMaster.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CandidateDemandLink
        fields = ["cdl_cdm_id", "cdl_dem_id", "cdl_csm_id"]

    def create(self, validated_data):
        # Convert cdl_cdm_id string into CandidateMaster instance
        try:
            validated_data['cdl_cdm_id'] = CandidateMaster.objects.get(cdm_id=validated_data['cdl_cdm_id'])
        except CandidateMaster.DoesNotExist:
            raise serializers.ValidationError({"cdl_cdm_id": "Invalid CandidateMaster ID"})

        # Convert cdl_dem_id string into OpenDemand instance
        try:
            validated_data['cdl_dem_id'] = OpenDemand.objects.get(dem_id=validated_data['cdl_dem_id'])
        except OpenDemand.DoesNotExist:
            raise serializers.ValidationError({"cdl_dem_id": "Invalid OpenDemand ID"})

        # Default status handling
        if 'cdl_csm_id' not in validated_data or validated_data['cdl_csm_id'] is None:
            default_status = CandidateStatusMaster.objects.filter(pk=1).first()
            validated_data['cdl_csm_id'] = default_status

        return super().create(validated_data)

class CandidatesetailSerializer(serializers.Serializer):
    cdm_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    keywords = serializers.CharField()
    status = serializers.DictField()
    location = serializers.CharField()
    profile = serializers.CharField(allow_blank=True, required=False)
    insertdate = serializers.DateField(format='%Y-%m-%d', required=False)
    updatedate = serializers.DateField(format='%Y-%m-%d', required=False)

class CandidatesDetailbyDemIdSerializer(serializers.Serializer):
    dem_id = serializers.CharField()
    candidates_by_status = serializers.DictField()

    def get_candidates_by_demand(self, dem_id):
        candidates_data = CandidateDemandLink.objects.filter(cdl_dem_id=dem_id) \
            .select_related('cdl_cdm_id', 'cdl_csm_id', 'cdl_cdm_id__cdm_location_id') \
            .values(
                'cdl_cdm_id__cdm_id',  # Corrected: Access related model fields
                'cdl_cdm_id__cdm_name',
                'cdl_cdm_id__cdm_email',
                'cdl_cdm_id__cdm_phone',
                'cdl_cdm_id__cdm_keywords',
                'cdl_cdm_id__cdm_location_id',
                'cdl_cdm_id__cdm_profile',
                'cdl_cdm_id__cdm_insertdate',
                'cdl_cdm_id__cdm_updatedate',
                'cdl_csm_id__csm_code',
                'cdl_csm_id__csm_id'
            )

        location_data = {loc.lcm_id: loc.lcm_name for loc in LocationMaster.objects.all()}
        status_data = {}  # Initialize as a regular dictionary

        # Get all status codes upfront to handle cases where a status might have no candidates
        for status in CandidateStatusMaster.objects.all():
            status_data[status.csm_code] = []

        for candidate in candidates_data:
            candidate_info = {
                "cdm_id": candidate['cdl_cdm_id__cdm_id'],
                "name": candidate['cdl_cdm_id__cdm_name'],
                "email": candidate['cdl_cdm_id__cdm_email'],
                "phone": candidate['cdl_cdm_id__cdm_phone'],
                "keywords": candidate['cdl_cdm_id__cdm_keywords'],
                "status": {
                    "id": candidate['cdl_csm_id__csm_id'],
                    "text": candidate['cdl_csm_id__csm_code']
                },
                "location": location_data.get(candidate['cdl_cdm_id__cdm_location_id'], "Unknown"),
                "profile": candidate['cdl_cdm_id__cdm_profile'],
                "insertdate": candidate['cdl_cdm_id__cdm_insertdate'].strftime('%Y-%m-%d') if candidate['cdl_cdm_id__cdm_insertdate'] else None,
                "updatedate": candidate['cdl_cdm_id__cdm_updatedate'].strftime('%Y-%m-%d') if candidate['cdl_cdm_id__cdm_updatedate'] else None,
            }
            # Use the status code directly as the key
            status_data[candidate['cdl_csm_id__csm_code']].append(candidate_info)

        return {"dem_id": dem_id, "candidates_by_status": status_data}