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

class DemandHistoryTrackingAPIView(APIView):
    def get(self, request, demand_id):
        from hiringManagementTool.components.demandhistory.log_message import (
            FIELD_LABELS, INTERVIEW_LABELS, STATIC_MESSAGES, get_enum_name
        )

        history_entries = []

        # --- Demand History Logs ---
        demand_logs = DemandHistory.objects.filter(dhs_dem_id=demand_id).order_by('dhs_dsm_insertdate')

        for log in demand_logs:
            log_msg = log.dhs_log_msg.lower()
            from_data = log.dhs_fromdata or {}
            to_data = log.dhs_todata or {}

            # Demand Created
            if "demand created" in log_msg:
                history_entries.append({
                    "message": STATIC_MESSAGES["demand_created"],
                    "date": log.dhs_dsm_insertdate
                })
                continue

            # JD Changes
            jd_from = from_data.get("jd")
            jd_to = to_data.get("jd")
            if jd_from != jd_to:
                msg = STATIC_MESSAGES["jd_attached"](jd_to) if not jd_from else STATIC_MESSAGES["jd_updated"](jd_to)
                history_entries.append({"message": msg, "date": log.dhs_dsm_insertdate})
                continue

            # Field Level Changes (Structured)
            if "value" in to_data and isinstance(to_data["value"], list):
                to_list = to_data["value"]
                from_list = from_data.get("value", [{}] * len(to_list))

                for from_item, to_item in zip(from_list, to_list):
                    from_val = from_item.get("value")
                    to_val = to_item.get("value")
                    field_key = to_item.get("label", "Unknown field")
                    if from_val != to_val:
                        label = FIELD_LABELS.get(field_key, field_key)
                        msg = STATIC_MESSAGES["field_updated"](label, from_val, to_val)
                        history_entries.append({"message": msg, "date": log.dhs_dsm_insertdate})
            else:
                for key, to_val in to_data.items():
                    if key.lower() == "id":
                        continue
                    from_val = from_data.get(key)
                    if from_val != to_val:
                        label = FIELD_LABELS.get(key, key)
                        msg = STATIC_MESSAGES["field_updated"](label, from_val, to_val)
                        history_entries.append({"message": msg, "date": log.dhs_dsm_insertdate})

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

            from_val = from_data.get("value")
            to_val = to_data.get("value")

            from_val_dict = from_val if isinstance(from_val, dict) else {}
            to_val_dict = to_val if isinstance(to_val, dict) else {}

            from_status = from_val_dict.get("csm_code")
            to_status = to_val_dict.get("csm_code")

            # Candidate Linked
            if not from_status and to_status:
                msg = STATIC_MESSAGES["candidate_linked"](candidate_name)
                history_entries.append({"message": msg, "date": log.cdh_insertdate})
                continue

            # Status Changed
            if from_status and to_status and from_status != to_status:
                msg = STATIC_MESSAGES["status_changed"](candidate_name, from_status, to_status)
                history_entries.append({"message": msg, "date": log.cdh_insertdate})

            # Interview Logs
            ist_keys = lambda d: {k for k in d if k.startswith("ist_")}
            is_new_interview = bool(ist_keys(to_data)) and not bool(ist_keys(from_data))

            if ist_keys(to_data):
                if is_new_interview:
                    interview_date = to_data.get("ist_interviewdate")
                    interview_round = to_data.get("ist_interviewround")
                    interview_type = get_enum_name(InterviewType, to_data.get("ist_interviewtype"))
                    interview_status = get_enum_name(InterviewStatus, to_data.get("ist_interviewstatus"))
                    meeting_link = to_data.get("ist_meeting_details") or "N/A"
                    timezone = to_data.get("ist_timezone") or "N/A"

                    msg = STATIC_MESSAGES["interview_scheduled"](
                        candidate_name, interview_date, interview_round, interview_type, interview_status, timezone, meeting_link
                    )
                    history_entries.append({"message": msg, "date": log.cdh_insertdate})
                else:
                    for field, label in INTERVIEW_LABELS.items():
                        from_val = from_data.get(field)
                        to_val = to_data.get(field)
                        if from_val != to_val:
                            # Handle enum fields
                            if field == "ist_interviewtype":
                                from_val = get_enum_name(InterviewType, from_val)
                                to_val = get_enum_name(InterviewType, to_val)
                            elif field == "ist_interviewstatus":
                                from_val = get_enum_name(InterviewStatus, from_val)
                                to_val = get_enum_name(InterviewStatus, to_val)

                            msg = STATIC_MESSAGES["interview_field_updated"](label, candidate_name, from_val, to_val)
                            history_entries.append({"message": msg, "date": log.cdh_insertdate})

        return Response(history_entries)
