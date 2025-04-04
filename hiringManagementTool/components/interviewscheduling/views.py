from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import generics
from rest_framework import status, views
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.utils.decorators import method_decorator
from datetime import datetime
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.components.interviewscheduling.serializers import InterviewSchedulingSerializer, GetCdlIdSerializer, InterviewStatusSerializer, InterviewTypeSerializer, InterviewSchedulingUpdateSerializer, TimezoneSerializer, InterviewDetailsFilterSerializer
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.constants import InterviewStatus, InterviewType
from rest_framework.views import APIView
import pytz
import json
from datetime import datetime, date, time


class InterviewSchedulingAPIView(ListCreateAPIView):
    queryset = InterviewSchedulingTable.objects.all()
    serializer_class = InterviewSchedulingSerializer  # Add this line

    def get(self, request):
        interviews = InterviewSchedulingTable.objects.all()
        serializer = self.serializer_class(interviews, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            interview = serializer.save()
            cdl = interview.ist_cdl

            # Convert date and time fields to ISO format
            history_data = {
                'ist_interviewdate': interview.ist_interviewdate.isoformat() if interview.ist_interviewdate else None,
                'ist_interview_start_time': interview.ist_interview_start_time.isoformat() if interview.ist_interview_start_time else None,
                'ist_interview_end_time': interview.ist_interview_end_time.isoformat() if interview.ist_interview_end_time else None,
                'ist_timezone': interview.ist_timezone,
                'ist_interviewtype': interview.ist_interviewtype,
                'ist_interviewround': interview.ist_interviewround,
                'ist_interviewers': interview.ist_interviewers,
                'ist_meeting_details': interview.ist_meeting_details,
                'ist_interviewstatus': interview.ist_interviewstatus,
                'ist_remarks': interview.ist_remarks,
            }

            # Insert into CandidateDemandHistory
            CandidateDemandHistory.objects.create(
                cdh_insertdate=timezone.now(),
                cdh_fromdata={"id": "None", "value": "None"},
                cdh_todata=history_data,
                cdh_cdm_id=cdl.cdl_cdm_id,
                cdh_dem_id=cdl.cdl_dem_id,
                cdh_csm_id=None
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterviewUpdateAPIView(views.APIView):
    serializer_class = InterviewSchedulingUpdateSerializer

    @method_decorator(transaction.atomic)
    def put(self, request, *args, **kwargs):
        # Use the context to pass the instance for partial updates if needed,
        # but for this approach, we fetch it after validation.
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        ist_id = validated_data.pop('ist_id') # Get ID and remove from data to update

        try:
            # Fetch the existing interview instance
            # Use select_for_update() for locking if high concurrency is expected
            interview = InterviewSchedulingTable.objects.select_related('ist_cdl').get(ist_id=ist_id)
            # interview = InterviewSchedulingTable.objects.select_for_update().select_related('ist_cdl').get(ist_id=ist_id) # With locking
        except InterviewSchedulingTable.DoesNotExist:
            return Response({'error': f'Interview with ist_id {ist_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        fields_to_track = [
            'ist_interviewdate',
            'ist_interview_start_time', # Updated name
            'ist_interview_end_time',   # Added field
            'ist_timezone',             # Added field
            'ist_interviewtype',
            'ist_interviewstatus',
            'ist_interviewround',       # Added field
            'ist_interviewers',         # Added field
            'ist_remarks',              # Added field
            'ist_meeting_details',      # Added field
        ]

        # Store old values for history tracking *before* making changes
        history_old_data = {}
        for field in fields_to_track:
             # Use gettatr default value None in case field doesn't exist (though it should)
             history_old_data[field] = getattr(interview, field, None)

        changed_fields_flag = False
        fields_actually_updated_for_history = {} # Store detailed old/new for history record

        # Iterate through the fields defined in the serializer that are present in validated_data
        for field_name, new_value in validated_data.items():
            # Skip if the field is not meant to be tracked or updated directly this way
            if field_name not in fields_to_track:
                continue

            old_value = getattr(interview, field_name, None)

            # --- Handle Enum Conversions (Name from request to Value for DB) ---
            converted_new_value = new_value # Start with the validated value
            if field_name == 'ist_interviewstatus' and isinstance(new_value, str):
                try:
                    converted_new_value = InterviewStatus[new_value].value
                except KeyError:
                    # This should ideally be caught by serializer choices, but double-check
                    return Response({'error': {field_name: f'Invalid status name: {new_value}'}}, status=status.HTTP_400_BAD_REQUEST)
            elif field_name == 'ist_interviewtype' and isinstance(new_value, str):
                try:
                    converted_new_value = InterviewType[new_value].value
                except KeyError:
                     # This should ideally be caught by serializer choices, but double-check
                    return Response({'error': {field_name: f'Invalid type name: {new_value}'}}, status=status.HTTP_400_BAD_REQUEST)

            # --- Compare old and new values ---
            # Special handling for JSON comparison might be needed if order matters or complex structures
            # Default Python comparison usually works well for dicts/lists if order isn't significant.
            if old_value != converted_new_value:
                setattr(interview, field_name, converted_new_value)
                changed_fields_flag = True
                # Store old/new values for the history record's 'todata' field
                fields_actually_updated_for_history[field_name] = {
                    'old': self.format_for_history(old_value),
                    'new': self.format_for_history(converted_new_value)
                }

        if not changed_fields_flag:
            return Response({"message": "No changes detected based on input. Update not performed."}, status=status.HTTP_200_OK)

        # --- Update timestamp and save ---
        interview.ist_updatedate = timezone.now().date() # Or use auto_now=True in model
        interview.save()

        # --- Create History Record ---
        # Fetch new values *after* saving, especially if model defaults/triggers exist
        history_new_data_from_db = {
            field: getattr(interview, field, None) for field in fields_to_track
        }

        # Prepare data for JSON storage in history model
        processed_old_data_for_history = {
        field: self.format_for_history(history_old_data[field])
        for field in fields_actually_updated_for_history
        }

        # Use the detailed changes for the 'todata' field if that's the requirement
        # Or use the full new state like the old data if needed
        processed_new_data_for_history = {
        field: self.format_for_history(getattr(interview, field))
        for field in fields_actually_updated_for_history
        }

        cdl = interview.ist_cdl
        if cdl: # Ensure cdl is not None
            CandidateDemandHistory.objects.create(
                cdh_insertdate=timezone.now(),
                # Store *only* the fields that changed, or the full before/after state?
                # Option 1: Store full state before change
                cdh_fromdata=processed_old_data_for_history,
                 # Option 2: Store detailed changes OR full state after change
                cdh_todata=processed_new_data_for_history, # Store only changes
                # cdh_todata=processed_new_data_for_history, # Store full state after change
                cdh_cdm_id=cdl.cdl_cdm_id,
                cdh_dem_id=cdl.cdl_dem_id,
                cdh_csm_id=None # Assuming this is correct based on original code
                # Add user tracking if available: cdh_updated_by=request.user
            )
        else:
             # Log a warning or handle cases where cdl might be missing unexpectedly
             print(f"Warning: CandidateDemandLink (ist_cdl) missing for Interview ist_id {ist_id}. History not recorded.")


        # --- Return Success Response ---
        response_serializer = InterviewSchedulingSerializer(interview) # Use the read serializer
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def format_for_history(self, value):
        """Helper function to format values consistently for JSON history field."""
        if isinstance(value, (date, time, datetime)):
            return value.isoformat()
        # Add specific handling for Enums if they are stored directly
        elif isinstance(value, (InterviewStatus, InterviewType)):
             return value.value # Store the numeric value
        # elif isinstance(value, (list, dict)):
             # return json.dumps(value) # Ensure complex types are stored as JSON strings if needed
        # For most other types (int, str, bool, None, simple JSON), direct use is fine
        return value
    
class GetCdlIdAPIView(APIView):
    def post(self, request, *args, **kwargs):
        candidate_id = request.data.get('candidate_id')
        demand_id = request.data.get('demand_id')

        if not candidate_id or not demand_id:
            return Response({'error': 'Both candidate_id and demand_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cdl = CandidateDemandLink.objects.get(cdl_cdm_id=candidate_id, cdl_dem_id=demand_id)
            serializer = GetCdlIdSerializer(cdl)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CandidateDemandLink.DoesNotExist:
            return Response({'error': 'CandidateDemandLink not found.'}, status=status.HTTP_404_NOT_FOUND)

class InterviewStatusDropdownView(APIView):
    def get(self, request):
        statuses = [{'value': status.value, 'label': status.name} for status in InterviewStatus]
        serializer = InterviewStatusSerializer(statuses, many=True)
        return Response(serializer.data)

class InterviewTypeDropdownView(APIView):
    def get(self, request):
        types = [{'value': interview_type.value, 'label': interview_type.name} for interview_type in InterviewType]
        serializer = InterviewTypeSerializer(types, many=True)
        return Response(serializer.data)

class TimezoneDropdownAPIView(APIView):
    def get(self, request):
        now = datetime.utcnow()
        timezone_choices = []

        for tz in pytz.all_timezones:
            timezone = pytz.timezone(tz)
            localized_time = now.astimezone(timezone)
            timezone_name = localized_time.tzname()
            display_name = f"{tz} ({timezone_name})"
            timezone_choices.append({"label": display_name})

        serializer = TimezoneSerializer(timezone_choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
class InterviewDetailsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        filter_serializer = InterviewDetailsFilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            interviews_qs = filter_serializer.get_interviews() # Get the base queryset

            # Serialize using the unmodified serializer
            interview_serializer = InterviewSchedulingSerializer(interviews_qs, many=True)
            serialized_data = interview_serializer.data

            # --- Data Enrichment Step ---
            # Extract cdl_ids from the initially serialized data
            # Assumes 'ist_cdl' is present in the unmodified serializer output
            cdl_id_map = {item.get('ist_cdl'): item for item in serialized_data if item.get('ist_cdl')}
            unique_cdl_ids = list(cdl_id_map.keys())

            candidate_data_map = {}
            demand_id_map = {}
            if unique_cdl_ids:
                # Fetch CandidateDemandLink objects, pre-fetching the related objects
                # using the *actual field names* from your model (cdl_cdm_id, cdl_dem_id)
                cdl_links = CandidateDemandLink.objects.filter(
                    cdl_id__in=unique_cdl_ids
                ).select_related(
                    'cdl_cdm_id',  # Tells Django to fetch the related CandidateMaster
                    'cdl_dem_id'   # Tells Django to fetch the related OpenDemand
                )

                for link in cdl_links:
                    # --- FIX FOR DEMAND ID ---
                    # Access the related OpenDemand object via link.cdl_dem_id
                    # Then get its primary key or the specific ID field (e.g., .dem_id)
                    related_demand = link.cdl_dem_id # This IS the OpenDemand object
                    if related_demand:
                        # Replace 'dem_id' with the actual primary key field name on your OpenDemand model
                        demand_id_map[link.cdl_id] = related_demand.dem_id
                    else:
                        demand_id_map[link.cdl_id] = None

                    # --- FIX FOR CANDIDATE DETAILS ---
                    # Access the related CandidateMaster object via link.cdl_cdm_id
                    related_candidate = link.cdl_cdm_id # This IS the CandidateMaster object
                    if related_candidate:
                        candidate_data_map[link.cdl_id] = {
                            # Get attributes from the related_candidate object
                            "id": related_candidate.cdm_id,
                            "name": related_candidate.cdm_name,
                            "email": related_candidate.cdm_email,
                        }
                    else:
                        candidate_data_map[link.cdl_id] = None

            # Modify the serialized data list in place
            for interview_dict in serialized_data:
                cdl_id = interview_dict.get('ist_cdl')
                # Use .get() for safe dictionary access
                interview_dict['demand_id'] = demand_id_map.get(cdl_id)
                interview_dict['candidate_details'] = candidate_data_map.get(cdl_id)

            # --- End Data Enrichment Step ---

            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)