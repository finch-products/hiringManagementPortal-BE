# views.py for demand-history
from rest_framework import generics
from hiringManagementTool.models.demandhistory import DemandHistory
from .serializers import DemandHistorySerializer

class DemandHistoryDetailAPIView(generics.ListAPIView):
    serializer_class = DemandHistorySerializer

    def get_queryset(self):
        dem_id = self.kwargs['id']  # Get dem_id from URL
        return DemandHistory.objects.filter(dhs_dem_id=dem_id).order_by('dhs_dsm_insertdate')
