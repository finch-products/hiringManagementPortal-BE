from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import generics
from rest_framework import status, views
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.utils.decorators import method_decorator
import datetime
from hiringManagementTool.components.interviewscheduling.serializers import InterviewSchedulingSerializer, InterviewSchedulingUpdateSerializer, GetCdlIdSerializer
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.constants import InterviewStatus
from rest_framework.views import APIView

class InterviewSchedulingAPIView(ListCreateAPIView):
    queryset = InterviewSchedulingTable.objects.all()
    serializer_class = InterviewSchedulingSerializer

    @method_decorator(transaction.atomic)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            interview = serializer.save()

            # Fetch the CandidateDemandLink object
            cdl = interview.ist_cdl

            # Prepare history data
            history_data = {
                'ist_interviewdate': interview.ist_interviewdate,
                'ist_interviewtime': interview.ist_interviewtime,
                'ist_interviewtype': interview.ist_interviewtype,
                'ist_interviewround': interview.ist_interviewround,
                'ist_interviewername': interview.ist_interviewername,
                'ist_intervieweremail': interview.ist_intervieweremail,
                'ist_interviewstatus': interview.ist_interviewstatus,
                'ist_remarks': interview.ist_remarks,
            }

            # Convert datetime and time fields to ISO format
            processed_data = {key: (value.isoformat() if isinstance(value, (datetime.date, datetime.time, datetime.datetime)) else value) for key, value in history_data.items()}

            # Insert into CandidateDemandHistory
            CandidateDemandHistory.objects.create(
                cdh_insertdate=timezone.now(),
                cdh_fromdata= {"id": "None", "value": "None"},
                cdh_todata=processed_data,
                cdh_cdm_id=cdl.cdl_cdm_id,
                cdh_dem_id=cdl.cdl_dem_id,
                cdh_csm_id=None
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        except CandidateDemandLink.DoesNotExist:
            return Response({'error': f'Associated CandidateDemandLink for interview ist_id {ist_id} not found'}, status=status.HTTP_400_BAD_REQUEST)

        fields_to_track = ['ist_interviewdate', 'ist_interviewtime', 'ist_interviewtype', 'ist_interviewstatus']

        history_old_data = {
            field: getattr(interview, field) for field in fields_to_track
        }

        changed_fields_flag = False
        fields_actually_updated = {}

        for field_name in fields_to_track:
            if field_name in validated_data:
                old_value = getattr(interview, field_name)
                new_value = validated_data[field_name]

                # Convert status name to value using Enum
                if field_name == 'ist_interviewstatus' and isinstance(new_value, str):
                    try:
                        new_value = InterviewStatus[new_value].value
                    except KeyError:
                        return Response({'error': f'Invalid status: {new_value}'}, status=status.HTTP_400_BAD_REQUEST)

                if old_value != new_value:
                    setattr(interview, field_name, new_value)
                    changed_fields_flag = True
                    fields_actually_updated[field_name] = {'old': old_value, 'new': new_value}

        if not changed_fields_flag:
            return Response({"message": "No changes detected based on input. Update not performed."}, status=status.HTTP_200_OK)

        interview.save()
        history_new_data = {
            field: getattr(interview, field) for field in fields_to_track
        }

        processed_old_data = {key: (value.isoformat() if isinstance(value, (datetime.date, datetime.time, datetime.datetime)) else value) for key, value in history_old_data.items()}
        processed_new_data = {key: (value.isoformat() if isinstance(value, (datetime.date, datetime.time, datetime.datetime)) else value) for key, value in history_new_data.items()}

        cdl = interview.ist_cdl

        CandidateDemandHistory.objects.create(
            cdh_insertdate=timezone.now(),
            cdh_fromdata=processed_old_data,
            cdh_todata=processed_new_data,
            cdh_cdm_id=cdl.cdl_cdm_id,
            cdh_dem_id=cdl.cdl_dem_id,
            cdh_csm_id=None
        )

        response_serializer = InterviewSchedulingSerializer(interview)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

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
