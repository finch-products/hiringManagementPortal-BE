from hiringManagementTool.components.departments.serializers import InternalDepartmentDetailsSerializer
from hiringManagementTool.models.departments import InternalDepartmentMaster
from rest_framework import viewsets


class InternalDepartmentDetailsViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly API
    queryset = InternalDepartmentMaster.objects.select_related(
        'idm_deliverymanager_id__emp_lcm_id'  # Optimized query for related fields
    ).order_by('idm_id')
    serializer_class = InternalDepartmentDetailsSerializer