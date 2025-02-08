from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientMasterViewSet, LOBMasterViewSet, LocationMasterViewSet, OpenDemandViewSet, EmployeeMasterViewSet, SubUnitMasterViewSet,ClientManagerMasterViewSet

router = DefaultRouter()
router.register(r'open-demands', OpenDemandViewSet)
router.register(r'client-master', ClientMasterViewSet)
router.register(r'lob-master', LOBMasterViewSet)
router.register(r'location-master', LocationMasterViewSet)
router.register(r'employee-master', EmployeeMasterViewSet)
router.register(r'sub-unit-master', SubUnitMasterViewSet)
router.register(r'client-manager-master', ClientManagerMasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]