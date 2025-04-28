# views.py for demand-history
from rest_framework import generics
from hiringManagementTool.models.demandhistory import DemandHistory
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from .serializers import DemandHistorySerializer, DemandHistoryapiSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import Q
from datetime import datetime
from hiringManagementTool.constants import InterviewStatus, InterviewType

class DemandHistoryDetailAPIView(generics.ListAPIView):
    serializer_class = DemandHistorySerializer

    def get_queryset(self):
        dem_id = self.kwargs['id']  # Get dem_id from URL
        return DemandHistory.objects.filter(dhs_dem_id=dem_id).order_by('dhs_dsm_insertdate')


from hiringManagementTool.components.demandhistory.log_message import (
    FIELD_LABELS, INTERVIEW_LABELS, STATIC_MESSAGES, get_enum_name
)
class DemandHistoryTrackingAPIView(APIView):
    def get(self, request, demand_id):
        history_entries = []
        last_known_updater = None  # Keep track of the updater across logs

        try:
            demand_logs = list(DemandHistory.objects.filter(dhs_dem_id=demand_id).order_by('dhs_dsm_insertdate'))
        except DemandHistory.DoesNotExist:
            return Response({"error": "Demand not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error fetching demand history"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for log in demand_logs:
            log_msg_lower = log.dhs_log_msg.lower() if log.dhs_log_msg else ""
            from_data = log.dhs_fromdata or {}
            to_data = log.dhs_todata or {}

            current_updater = None
            to_value_list = to_data.get("value", [])
            to_data_map = {item.get("label"): item.get("value") for item in to_value_list if isinstance(item, dict) and "label" in item}

            current_updater = to_data_map.get("dem_updateby_id", None)
            if not current_updater:
                current_updater = last_known_updater
            else:
                last_known_updater = current_updater

            if "demand created" in log_msg_lower:
                creator = to_data_map.get("dem_insertby_id", current_updater)
                history_entries.append({
                    "Message": STATIC_MESSAGES["demand_created"],
                    "Date": log.dhs_dsm_insertdate,
                    "Updated by": creator
                })
                last_known_updater = creator
                continue

            from_value_list = from_data.get("value", [])
            if not isinstance(from_value_list, list):
                continue

            for from_item in from_value_list:
                if not isinstance(from_item, dict) or "label" not in from_item:
                    continue

                field_key = from_item.get("label")
                from_val = from_item.get("value")
                to_val = to_data_map.get(field_key)

                if field_key in ["dem_updatedate", "dem_updateby_id"]:
                    continue

                label_display = FIELD_LABELS.get(field_key, field_key)
                msg = None

                if field_key == "dem_jd":
                    if from_val and to_val and from_val != to_val:
                        msg = STATIC_MESSAGES["jd_updated"](to_val)
                    elif not from_val and to_val:
                        msg = STATIC_MESSAGES["jd_attached"](to_val)
                elif from_val and to_val and from_val != to_val:
                    msg = STATIC_MESSAGES["field_updated"](label_display, from_val, to_val)

                if msg:
                    history_entries.append({
                        "Message": msg,
                        "Date": log.dhs_dsm_insertdate,
                        "Updated by": current_updater
                    })

        # --- Candidate Demand History Logs ---
        candidate_logs = CandidateDemandHistory.objects.filter(cdh_dem_id=demand_id).order_by('cdh_insertdate')

        for log in candidate_logs:
            from_data = log.cdh_fromdata or {}
            to_data = log.cdh_todata or {}

            candidate_obj = log.cdh_cdm_id
            candidate_id = candidate_obj.cdm_id if hasattr(candidate_obj, "cdm_id") else candidate_obj

            try:
                candidate_name = candidate_obj.cdm_name if hasattr(candidate_obj, "cdm_name") else CandidateMaster.objects.get(cdm_id=candidate_id).cdm_name
            except CandidateMaster.DoesNotExist:
                candidate_name = str(candidate_id)

            from_val_dict = from_data.get("value", {}) if isinstance(from_data.get("value"), dict) else {}
            to_val_dict = to_data.get("value", {}) if isinstance(to_data.get("value"), dict) else {}

            from_status = from_val_dict.get("csm_code")
            to_status = to_val_dict.get("csm_code")

            if not from_status and to_status:
                msg = STATIC_MESSAGES["candidate_linked"](candidate_name)
                history_entries.append({
                    "Message": msg,
                    "Date": log.cdh_insertdate,
                    "Updated by": None
                })
                continue

            if from_status and to_status and from_status != to_status:
                msg = STATIC_MESSAGES["status_changed"](candidate_name, from_status, to_status)
                history_entries.append({
                    "Message": msg,
                    "Date": log.cdh_insertdate,
                    "Updated by": None
                })

            ist_keys = lambda d: {k for k in d if k.startswith("ist_")}
            is_new_interview = bool(ist_keys(to_data)) and not bool(ist_keys(from_data))

            if ist_keys(to_data):
                if is_new_interview:
                    msg = STATIC_MESSAGES["interview_scheduled"](
                        candidate_name,
                        to_data.get("ist_interviewdate"),
                        to_data.get("ist_interviewround"),
                        get_enum_name(InterviewType, to_data.get("ist_interviewtype")),
                        get_enum_name(InterviewStatus, to_data.get("ist_interviewstatus")),
                        to_data.get("ist_timezone") or "N/A",
                        to_data.get("ist_meeting_details") or "N/A"
                    )
                    history_entries.append({
                        "Message": msg,
                        "Date": log.cdh_insertdate,
                        "Updated by": None
                    })
                else:
                    for field, label in INTERVIEW_LABELS.items():
                        from_val = from_data.get(field)
                        to_val = to_data.get(field)
                        if from_val != to_val:
                            if field == "ist_interviewtype":
                                from_val = get_enum_name(InterviewType, from_val)
                                to_val = get_enum_name(InterviewType, to_val)
                            elif field == "ist_interviewstatus":
                                from_val = get_enum_name(InterviewStatus, from_val)
                                to_val = get_enum_name(InterviewStatus, to_val)

                            msg = STATIC_MESSAGES["interview_field_updated"](label, candidate_name, from_val, to_val)
                            history_entries.append({
                                "Message": msg,
                                "Date": log.cdh_insertdate,
                                "Updated by": None
                            })

        return Response(history_entries, status=status.HTTP_200_OK)
