from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.interviewscheduling.serializers import InterviewSchedulingSerializer
from hiringManagementTool.models.interview import InterviewSchedulingTable

class InterviewSchedulingAPIView(ListCreateAPIView):
    queryset = InterviewSchedulingTable.objects.all()
    serializer_class = InterviewSchedulingSerializer