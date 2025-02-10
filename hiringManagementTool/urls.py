from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientManagerMasterViewSet,
    ClientMasterViewSet,
    InternalDepartmentMasterViewSet,
    LOBMasterViewSet,
    LocationMasterViewSet,
    OpenDemandViewSet,
    EmployeeMasterViewSet,
    ClientDetailsViewSet,
    LocationDetailsViewSet,
    DemandStatusDetailsViewSet,
    InternalDepartmentDetailsViewSet,
    LOBDetailsViewSet,
)

router = DefaultRouter()
router.register(r'open-demands', OpenDemandViewSet)
router.register(r'client-master', ClientMasterViewSet)
router.register(r'lob-master', LOBMasterViewSet)
router.register(r'location-master', LocationMasterViewSet)
router.register(r'employee-master', EmployeeMasterViewSet)
router.register(r'internal-department-master', InternalDepartmentMasterViewSet)
router.register(r'client-manager-master', ClientManagerMasterViewSet)
router.register(r'clients-details', ClientDetailsViewSet, basename="client-details")
router.register(r'location-details', LocationDetailsViewSet, basename="location-details")
router.register(r'demand-status-details', DemandStatusDetailsViewSet, basename="demand-status-details")
router.register(r'internal-department-details', InternalDepartmentDetailsViewSet, basename='internal-department-details')
router.register(r'lob-details', LOBDetailsViewSet, basename="lob-details")

urlpatterns = [
    path('', include(router.urls)),
]
