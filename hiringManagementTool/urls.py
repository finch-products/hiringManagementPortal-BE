from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientManagerMasterViewSet, ClientMasterViewSet, InternalDepartmentMasterViewSet, LOBMasterViewSet, LocationMasterViewSet, OpenDemandViewSet, EmployeeMasterViewSet, RoleMasterViewSet

router = DefaultRouter()
router.register(r'open-demands', OpenDemandViewSet)
router.register(r'client-master', ClientMasterViewSet)
router.register(r'lob-master', LOBMasterViewSet)
router.register(r'location-master', LocationMasterViewSet)
router.register(r'employee-master', EmployeeMasterViewSet)
router.register(r'internal-department-master', InternalDepartmentMasterViewSet)
router.register(r'client-manager-master', ClientManagerMasterViewSet)
router.register(r'role-master', RoleMasterViewSet)


urlpatterns = [
    path('', include(router.urls)),
]