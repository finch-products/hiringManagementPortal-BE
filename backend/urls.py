"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('hiringManagementTool.urls')),
# ]

urlpatterns = [
    path('api/demands/', include('hiringManagementTool.components.demands.urls')),
    path('api/clients/', include('hiringManagementTool.components.clients.urls')),
    path('api/locations/', include('hiringManagementTool.components.locations.urls')),
    path('api/lobs/', include('hiringManagementTool.components.lobs.urls')),
    path('api/departments/', include('hiringManagementTool.components.departments.urls')),
    path('api/roles/', include('hiringManagementTool.components.roles.urls')),
    path('api/employees/', include('hiringManagementTool.components.employees.urls')),
    path('api/candidates/', include('hiringManagementTool.components.candidates.urls')),
     path('api/reports/', include('hiringManagementTool.components.reports.urls')),
    # path('api/demand-status/', include('hiringManagementTool.components.demandstatus.urls'))
    path('api/demand-history/', include('hiringManagementTool.components.demand-history.urls')),
    path('api/candidate-demand-link/', include('hiringManagementTool.components.candidate-demand.urls'))
]

