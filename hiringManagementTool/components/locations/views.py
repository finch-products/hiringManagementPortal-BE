from rest_framework import generics
from flask import Response
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.locations.serializers import LocationMasterSerializer, LocationMinimumDetailsSerializer
from hiringManagementTool.models.locations import LocationMaster

class LocationAPIView(ListCreateAPIView):
    queryset = LocationMaster.objects.all()
    serializer_class = LocationMasterSerializer


class LocationDetailAPIView(RetrieveUpdateAPIView):
    queryset = LocationMaster.objects.all()
    serializer_class = LocationMasterSerializer
    lookup_field = 'lcm_id'
    lookup_url_kwarg = 'id'

class LocationMinimumDetailsAPIView(generics.ListAPIView):
    queryset = LocationMaster.objects.all()
    serializer_class = LocationMinimumDetailsSerializer
