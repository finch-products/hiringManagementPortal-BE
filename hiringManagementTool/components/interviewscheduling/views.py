from rest_framework import viewsets, generics, status, views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.utils.decorators import method_decorator
from hiringManagementTool.components.interviewscheduling.serializers import InterviewSchedulingSerializer, GetCdlIdSerializer, InterviewStatusSerializer, InterviewTypeSerializer, InterviewSchedulingUpdateSerializer, TimezoneSerializer, InterviewDetailsFilterSerializer
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.constants import InterviewStatus, InterviewType
from rest_framework.views import APIView
import pytz
from datetime import datetime, date, time

class InterviewSchedulingAPIView(ListCreateAPIView):
    queryset = InterviewSchedulingTable.objects.all()
    serializer_class = InterviewSchedulingSerializer

class InterviewUpdateAPIView(views.APIView):
    serializer_class = InterviewSchedulingUpdateSerializer

    @method_decorator(transaction.atomic)
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        ist_id = validated_data.pop('ist_id')

        try:
            interview = InterviewSchedulingTable.objects.select_related('ist_cdl').get(ist_id=ist_id)
        except InterviewSchedulingTable.DoesNotExist:
            return Response({'error': f'Interview with ist_id {ist_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        fields_to_track = [
            'ist_interviewdate', 'ist_interview_start_time', 'ist_interview_end_time',
            'ist_timezone', 'ist_interviewtype', 'ist_interviewstatus',
            'ist_interviewround', 'ist_interviewers', 'ist_meeting_details', 'ist_remarks'
        ]

        has_changes = any(
            field in validated_data and getattr(interview, field) != validated_data[field]
            for field in fields_to_track
        )

        if not has_changes:
            return Response({"message": "No changes detected. Update not performed."}, status=status.HTTP_200_OK)

        for field in validated_data:
            setattr(interview, field, validated_data[field])
        interview.ist_updatedate = timezone.now().date()
        interview.save()  

        return Response(InterviewSchedulingSerializer(interview).data, status=status.HTTP_200_OK)

    
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
            interviews_qs = filter_serializer.get_interviews() 
            interview_serializer = InterviewSchedulingSerializer(interviews_qs, many=True)
            serialized_data = interview_serializer.data
            cdl_id_map = {item.get('ist_cdl'): item for item in serialized_data if item.get('ist_cdl')}
            unique_cdl_ids = list(cdl_id_map.keys())
            candidate_data_map = {}
            demand_id_map = {}
            if unique_cdl_ids:
                cdl_links = CandidateDemandLink.objects.filter(
                    cdl_id__in=unique_cdl_ids
                ).select_related(
                    'cdl_cdm_id',
                    'cdl_dem_id'
                )

                for link in cdl_links:
                    related_demand = link.cdl_dem_id # This IS the OpenDemand object
                    if related_demand:
                        demand_id_map[link.cdl_id] = related_demand.dem_id
                    else:
                        demand_id_map[link.cdl_id] = None
                    related_candidate = link.cdl_cdm_id # This IS the CandidateMaster object
                    if related_candidate:
                        candidate_data_map[link.cdl_id] = {
                            "id": related_candidate.cdm_id,
                            "name": related_candidate.cdm_name,
                            "email": related_candidate.cdm_email,
                        }
                    else:
                        candidate_data_map[link.cdl_id] = None
            for interview_dict in serialized_data:
                cdl_id = interview_dict.get('ist_cdl')
                interview_dict['demand_id'] = demand_id_map.get(cdl_id)
                interview_dict['candidate_details'] = candidate_data_map.get(cdl_id)
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)