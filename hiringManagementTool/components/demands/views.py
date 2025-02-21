from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.components.demands.serializers import OpenDemandSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from .serializers import OpenDemandUpdateSerializer
from datetime import datetime

class DemandAPIView(APIView):
    """Handles GET and POST requests for OpenDemand"""
    
    def get(self, request):
        """Retrieve all OpenDemands"""
        demands = OpenDemand.objects.all()
        serializer = OpenDemandSerializer(demands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new demand and auto-assign status"""
        print("\n📥 Incoming Request Data:", request.data)
        print("\n📥 dem_jd value:", request.data.get('dem_jd'))  # Log the value of dem_jd

        serializer = OpenDemandSerializer(data=request.data)
        if serializer.is_valid():
            print("\n✅ Serializer Validated Data:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        print("\n❌ Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DemandDetailAPIView(RetrieveUpdateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer
    lookup_field = 'dem_id'
    lookup_url_kwarg = 'id'



class OpenDemandUpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        dem_id = request.data.get("dem_id")
        dem_updateby_id = request.data.get("dem_updateby_id")

        # At least one column should be provided for update
        update_fields = {key: value for key, value in request.data.items() if key not in ["dem_id", "dem_updateby_id"]}

        if not dem_id or not dem_updateby_id or not update_fields:
            return Response({"error": "dem_id, dem_updateby_id, and at least one field to update are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            open_demand = OpenDemand.objects.get(dem_id=dem_id)

            # Handle ForeignKey field: Convert dem_dsm_id to an instance of DemandStatusMaster
            if "dem_dsm_id" in update_fields:
                dsm_instance = DemandStatusMaster.objects.get(dsm_id=update_fields["dem_dsm_id"])
                update_fields["dem_dsm_id"] = dsm_instance  # Assign instance, not integer

            # Update the fields
            for field, value in update_fields.items():
                setattr(open_demand, field, value)

            open_demand.dem_updateby_id = dem_updateby_id
            open_demand.dem_updatedate = datetime.now()  # Set the updated date
            open_demand.save()

            return Response({"message": "Demand updated successfully"}, status=status.HTTP_200_OK)

        except OpenDemand.DoesNotExist:
            return Response({"error": "OpenDemand with the provided dem_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)
        except DemandStatusMaster.DoesNotExist:
            return Response({"error": "Invalid dem_dsm_id: No such DemandStatusMaster found."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)