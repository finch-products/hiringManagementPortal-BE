from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.models.employees import EmployeeMaster
from hiringManagementTool.components.employees.serializers import EmployeeMasterSerializer

class EmployeeAPIView(ListCreateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer

class EmployeeDetailAPIView(RetrieveUpdateAPIView):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer
    lookup_field = 'lob_id'
    lookup_url_kwarg = 'id'