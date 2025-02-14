from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.models.roles import RoleMaster
from hiringManagementTool.components.roles.serializers import RoleMasterSerializer

class RoleAPIView(ListCreateAPIView):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer

class RoleDetailAPIView(RetrieveUpdateAPIView):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
    lookup_field = 'rlm_id'
    lookup_url_kwarg = 'id'