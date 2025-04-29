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
    clm_logo = serializers.ImageField(source='dem_clm_id.clm_logo')

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
        return getattr(LocationMaster.objects.filter(lcm_id=obj).first(), 'lcm_name', None)

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
            'dem_updateby', 'dem_mandatoryskill', 'position_locations'
        ]
    def get_position_locations(self, obj):
        return [
            {'lcm_id': loc.lcm_id, 'lcm_name': loc.lcm_name}
            for loc in LocationMaster.objects.filter(lcm_id__in=obj.dem_position_location or [])
        ]
    
class CandidateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateStatusMaster
        fields = ["csm_id", "csm_code"]

class CandidateSerializer(serializers.ModelSerializer): 
    candidate_status = CandidateStatusSerializer(source='cdl_csm_id', read_only=True)
    name = serializers.CharField(source='cdl_cdm_id.cdm_name')
    email = serializers.EmailField(source='cdl_cdm_id.cdm_email')
    phone = serializers.CharField(source='cdl_cdm_id.cdm_phone')
    description = serializers.CharField(source='cdl_cdm_id.cdm_description')
    keywords = serializers.CharField(source='cdl_cdm_id.cdm_keywords')
    cdm_profile = serializers.FileField(source='cdl_cdm_id.cdm_profile')
    cdm_image = serializers.ImageField(source='cdl_cdm_id.cdm_image')
    location_id = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()

    class Meta:
        model = CandidateDemandLink
        fields = [
            'cdl_id', 'cdl_cdm_id', 'name', 'email', 'phone', 'location_id', 'location_name', 'description', 
            'keywords', 'cdl_joiningdate', 'cdl_insertdate','candidate_status', 'cdm_profile', 'cdm_image'
        ]

    def _get_location_attr(self, obj, attr):
        location = getattr(getattr(obj.cdl_cdm_id, 'cdm_location', None), attr, None)
        return location

    def get_location_id(self, obj):
        return self._get_location_attr(obj, 'lcm_id')

    def get_location_name(self, obj):
        return self._get_location_attr(obj, 'lcm_name')

class CandidateMasterSerializer(serializers.ModelSerializer):
    cdl_id = serializers.SerializerMethodField()
    cdl_cdm_id = serializers.CharField(source='cdm_id')
    cdl_joiningdate = serializers.SerializerMethodField()
    cdl_insertdate = serializers.SerializerMethodField()
    candidate_status = serializers.SerializerMethodField()
    location_id = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    cdm_profile = serializers.FileField()
    cdm_image = serializers.ImageField()

    class Meta:
        model = CandidateMaster
        fields = [
            'cdl_id', 'cdl_cdm_id', 'cdm_name', 'cdm_email', 'cdm_phone', 
            'location_id', 'location_name', 'cdm_description', 'cdm_keywords', 
            'cdl_joiningdate', 'cdl_insertdate', 'candidate_status', 'cdm_profile', 'cdm_image'
        ]

    def _get_linked_demand(self, obj):
        return CandidateDemandLink.objects.filter(cdl_cdm_id=obj).first()

    def get_cdl_id(self, obj):
        return self._get_linked_demand(obj).cdl_id if self._get_linked_demand(obj) else None

    def get_cdl_joiningdate(self, obj):
        return self._get_linked_demand(obj).cdl_joiningdate if self._get_linked_demand(obj) else None

    def get_cdl_insertdate(self, obj):
        return self._get_linked_demand(obj).cdl_insertdate if self._get_linked_demand(obj) else None

    def get_candidate_status(self, obj):
        linked_demand = self._get_linked_demand(obj)
        return CandidateStatusSerializer(linked_demand.cdl_csm_id).data if linked_demand and linked_demand.cdl_csm_id else None

    def get_location_id(self, obj):
        return obj.cdm_location.lcm_id if obj.cdm_location else None

    def get_location_name(self, obj):
        return obj.cdm_location.lcm_name if obj.cdm_location else None

class OpenDemandResponseSerializer(serializers.Serializer):
    cdl_dem_id = serializers.CharField()
    application_count = serializers.SerializerMethodField()
    demand_details = DemandSerializer()
    candidates = CandidateSerializer(many=True)

    def get_application_count(self, obj):
        return len(obj['candidates']) 

class NonlinkedResponseSerializer(serializers.Serializer):
    cdl_dem_id = serializers.CharField()
    demand_details = DemandSerializer()
    candidates_not_added = CandidateMasterSerializer(many=True) 

class CandidateDemandLinkSerializer(serializers.ModelSerializer):
    cdl_cdm_id = serializers.CharField(required=True)
    cdl_dem_id = serializers.CharField(required=True)
    cdl_csm_id = serializers.PrimaryKeyRelatedField(queryset=CandidateStatusMaster.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CandidateDemandLink
        fields = ["cdl_cdm_id", "cdl_dem_id", "cdl_csm_id"]

    def create(self, validated_data):
        # Retrieve CandidateMaster and OpenDemand instances, or raise validation errors
        validated_data['cdl_cdm_id'] = self._get_instance(CandidateMaster, validated_data['cdl_cdm_id'], 'cdl_cdm_id')
        validated_data['cdl_dem_id'] = self._get_instance(OpenDemand, validated_data['cdl_dem_id'], 'cdl_dem_id')

        # Set default status if not provided
        validated_data['cdl_csm_id'] = validated_data.get('cdl_csm_id', CandidateStatusMaster.objects.filter(pk=1).first())
        return super().create(validated_data)

    def _get_instance(self, model, instance_id, field_name):
        """Helper method to retrieve model instance or raise validation error."""
        try:
            return model.objects.get(**{model._meta.pk.name: instance_id})
        except model.DoesNotExist:
            raise serializers.ValidationError({field_name: f"Invalid {model.__name__} ID"})

class CandidatesDetailbyDemIdSerializer(serializers.Serializer):
    dem_id = serializers.CharField()
    candidates_by_status = serializers.DictField()

    def get_candidates_by_demand(self, dem_id):
        candidates = CandidateDemandLink.objects.filter(cdl_dem_id=dem_id).select_related(
            'cdl_cdm_id', 'cdl_csm_id', 'cdl_cdm_id__cdm_location_id'
        ).values(
            'cdl_cdm_id__cdm_id', 'cdl_cdm_id__cdm_name', 'cdl_cdm_id__cdm_email',
            'cdl_cdm_id__cdm_phone', 'cdl_cdm_id__cdm_keywords', 'cdl_cdm_id__cdm_location_id',
            'cdl_cdm_id__cdm_profile', 'cdl_cdm_id__cdm_insertdate', 'cdl_cdm_id__cdm_updatedate',
            'cdl_csm_id__csm_code', 'cdl_csm_id__csm_id'
        )

        location_map = {loc.lcm_id: loc.lcm_name for loc in LocationMaster.objects.all()}
        status_map = {status.csm_code: [] for status in CandidateStatusMaster.objects.all()}

        for c in candidates:
            status_map[c['cdl_csm_id__csm_code']].append({
                "cdm_id": c['cdl_cdm_id__cdm_id'],
                "name": c['cdl_cdm_id__cdm_name'],
                "email": c['cdl_cdm_id__cdm_email'],
                "phone": c['cdl_cdm_id__cdm_phone'],
                "keywords": c['cdl_cdm_id__cdm_keywords'],
                "status": {"id": c['cdl_csm_id__csm_id'], "text": c['cdl_csm_id__csm_code']},
                "location": location_map.get(c['cdl_cdm_id__cdm_location_id'], "Unknown"),
                "profile": c['cdl_cdm_id__cdm_profile'],
                "insertdate": c['cdl_cdm_id__cdm_insertdate'].strftime('%Y-%m-%d') if c['cdl_cdm_id__cdm_insertdate'] else None,
                "updatedate": c['cdl_cdm_id__cdm_updatedate'].strftime('%Y-%m-%d') if c['cdl_cdm_id__cdm_updatedate'] else None,
            })
        return {"dem_id": dem_id, "candidates_by_status": status_map}
