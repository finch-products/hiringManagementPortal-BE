from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from hiringManagementTool.models.demandhistory import DemandHistory
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from rest_framework import serializers
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from rest_framework import serializers
from hiringManagementTool.components.locations.serializers import LocationMasterSerializer
from django.db.models import F
from itertools import groupby
from operator import itemgetter

class CandidateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateStatusMaster
        fields = ["csm_id", "csm_code"]


class CandidateMasterSerializer(serializers.ModelSerializer):
    candidate_status = CandidateStatusSerializer(source='cdm_csm_id', read_only=True)
    lcm_name =serializers.CharField(source="cdm_location.lcm_name",read_only=True)
    cdm_insertby = serializers.CharField(source='cdm_insertby.emp_id', read_only=True)
    cdm_updateby = serializers.CharField(source='cdm_updateby.emp_id', read_only=True)

    class Meta:
        model = CandidateMaster
        fields = [
            "cdm_id",
            "cdm_emp_id",
            "cdm_name",
            "cdm_email",
            "cdm_phone",
            "cdm_profile",
            "cdm_description",
            "cdm_keywords",
            "cdm_insertdate",
            "cdm_updatedate",
            "cdm_isinternal",
            "cdm_isactive",
            "cdm_location",
            "lcm_name",
            "candidate_status",
            "cdm_insertby",
            "cdm_updateby"
        ]


class StatusHistorySerializer(serializers.ModelSerializer):
    cdm_comment = serializers.SerializerMethodField()  
    status = serializers.SerializerMethodField()
    cdh_insertdate = serializers.SerializerMethodField()  # Extract only the date

    class Meta:
        model = CandidateDemandHistory
        fields = ["cdm_comment", "status", "cdh_insertdate"]
    
    def get_cdm_comment(self, obj):
        return obj.cdh_cdm_id.cdm_comment if obj.cdh_cdm_id else None  

    def get_status(self, obj):
        return obj.cdh_csm_id.csm_code if obj.cdh_csm_id else None

    def get_cdh_insertdate(self, obj):
        return obj.cdh_insertdate.date() if obj.cdh_insertdate else None  # Extract only the date



class DemandStatusHistorySerializer(serializers.ModelSerializer):
    dem_comment = serializers.SerializerMethodField()  
    status = serializers.SerializerMethodField()
    dhs_dsm_insertdate = serializers.SerializerMethodField()  # Custom formatting

    class Meta:
        model = DemandHistory
        fields = ["dem_comment", "status", "dhs_dsm_insertdate"]

    def get_dem_comment(self, obj):
        return obj.dhs_dem_id.dem_comment if obj.dhs_dem_id else None  

    def get_status(self, obj):
        return obj.dhs_dsm_id.dsm_code if obj.dhs_dsm_id else None

    def get_dhs_dsm_insertdate(self, obj):
        return obj.dhs_dsm_insertdate.date() if obj.dhs_dsm_insertdate else None  # Extract only the date


class DemandDetailsSerializer(serializers.ModelSerializer):
    candidate_status_history = serializers.SerializerMethodField()
    demand_status_history = serializers.SerializerMethodField()
    current_demand_status = serializers.SerializerMethodField()

    class Meta:
        model = OpenDemand
        fields = [
            "dem_id", "dem_position_name", "dem_skillset", "dem_positions",
            "dem_rrnumber", "dem_jd", "dem_validtill", "dem_insertdate", "dem_updatedate",
            "current_demand_status", "demand_status_history", "candidate_status_history"
        ]

    def get_current_demand_status(self, obj):
        latest_status = DemandHistory.objects.filter(dhs_dem_id=obj.dem_id).order_by('-dhs_dsm_insertdate').first()
        return latest_status.dhs_dsm_id.dsm_code if latest_status and latest_status.dhs_dsm_id else None

    def get_demand_status_history(self, obj):
        history_qs = (
            DemandHistory.objects
            .filter(dhs_dem_id=obj.dem_id)
            .values(
                dem_comment=F('dhs_dem_id__dem_comment'),  # Missing comma fixed
                status=F('dhs_dsm_id__dsm_code'), 
                insertdate=F('dhs_dsm_insertdate'),               
            )
            .order_by('-insertdate')  
        )

        history_list = list(history_qs)

        unique_history = []
        seen = set()
        for entry in history_list:
            key = (entry["dem_comment"], entry["status"], entry["insertdate"].date())
            if key not in seen:
                unique_history.append({
                    "dem_comment": entry["dem_comment"],  # Missing comma fixed
                    "status": entry["status"], 
                    "dhs_dsm_insertdate": entry["insertdate"].date(),
                })
                seen.add(key)

        return unique_history

    def get_candidate_status_history(self, obj):
        history_qs = (
            CandidateDemandHistory.objects
            .filter(cdh_dem_id=obj.dem_id)
            .values(
                cdm_comment=F('cdh_cdm_id__cdm_comment'),  # Missing comma fixed
                status=F('cdh_csm_id__csm_code'), 
                insertdate=F('cdh_insertdate'),
            )
            .order_by('-insertdate')
        )

        history_list = list(history_qs)

        unique_history = []
        seen = set()
        for entry in history_list:
            key = (entry["cdm_comment"], entry["status"], entry["insertdate"].date())
            if key not in seen:
                unique_history.append({
                    "cdm_comment": entry["cdm_comment"],  # Missing comma fixed
                    "status": entry["status"], 
                    "cdh_insertdate": entry["insertdate"].date(),
                })
                seen.add(key)

        return unique_history

class CandidateHistorySerializer(serializers.ModelSerializer):
    demands = serializers.SerializerMethodField()
    current_status = serializers.SerializerMethodField()

    class Meta:
        model = CandidateMaster
        fields = ["cdm_id", "cdm_name", "cdm_email", "cdm_phone", "cdm_profile", "cdm_description", "current_status", "demands"]

    def get_current_status(self, obj):
        latest_status = CandidateDemandHistory.objects.filter(cdh_cdm_id=obj.cdm_id).order_by('-cdh_insertdate').first()
        return latest_status.cdh_csm_id.csm_code if latest_status and latest_status.cdh_csm_id else None

    def get_demands(self, obj):
        demand_ids = CandidateDemandLink.objects.filter(cdl_cdm_id=obj.cdm_id).values_list('cdl_dem_id', flat=True)
        unique_demand_ids = set(demand_ids)
        demands = OpenDemand.objects.filter(dem_id__in=unique_demand_ids)
        return DemandDetailsSerializer(demands, many=True).data
    
class AllCandidateMasterIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateMaster
        fields = ['cdm_id']