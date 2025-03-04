from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.components.demands.serializers import OpenDemandSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.locations import LocationMaster
from .serializers import OpenDemandUpdateSerializer, AllOpenDemandsIdSerializer
from datetime import datetime
from django.db.models import Count, Q
from hiringManagementTool.models.clients import ClientMaster
from hiringManagementTool.models.lobs import LOBMaster

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

class AllDemandsAPIView(APIView):
    def get(self, request):
        queryset = OpenDemand.objects.all()
        serializer = AllOpenDemandsIdSerializer(queryset, many=True)
        return Response(serializer.data)

class DemandDetailAPIView(RetrieveUpdateAPIView):
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandSerializer
    lookup_field = 'dem_id'
    lookup_url_kwarg = 'id'
class OpenDemandUpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        dem_id = request.data.get("dem_id")
        dem_updateby_id = request.data.get("dem_updateby_id")

        # Ensure that update_fields is initialized before use
        update_fields = {key: value for key, value in request.data.items() if key not in ["dem_id", "dem_updateby_id"]}

        if not dem_id or not dem_updateby_id:
            return Response({"error": "dem_id and dem_updateby_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not update_fields:
            return Response({"error": "At least one field must be provided for update."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            open_demand = OpenDemand.objects.get(dem_id=dem_id)

            # Handle ForeignKey field: Convert dem_dsm_id to an instance of DemandStatusMaster
            if "dem_dsm_id" in update_fields:
                dsm_instance = DemandStatusMaster.objects.get(dsm_id=update_fields["dem_dsm_id"])
                update_fields["dem_dsm_id"] = dsm_instance  # Assign instance, not integer
            
            # Handle ForeignKey field: Convert dem_clm_id to a ClientMaster instance
            if "dem_clm_id" in update_fields:
                clm_instance = ClientMaster.objects.get(clm_id=update_fields["dem_clm_id"])
                update_fields["dem_clm_id"] = clm_instance  # Assign instance, not integer

            if "dem_lob_id" in update_fields:
                lob_instance = LOBMaster.objects.get(lob_id=update_fields["dem_lob_id"])
                update_fields["dem_lob_id"] = lob_instance  # Assign instance, not integer

            if "dem_idm_id" in update_fields:
                idm_instance = InternalDepartmentMaster.objects.get(idm_id=update_fields["dem_idm_id"])
                update_fields["dem_idm_id"] = idm_instance  # Assign instance, not integer

            if "dem_lcm_id" in update_fields:
                lcm_instance = LocationMaster.objects.get(lcm_id=update_fields["dem_lcm_id"])
                update_fields["dem_lcm_id"] = lcm_instance
                
            # Update fields dynamically
            for field, value in update_fields.items():
                setattr(open_demand, field, value)

            open_demand.dem_updateby_id = dem_updateby_id
            open_demand.dem_updatedate = datetime.now()
            open_demand.save()

            return Response({"message": "Demand updated successfully"}, status=status.HTTP_200_OK)

        except OpenDemand.DoesNotExist:
            return Response({"error": "OpenDemand with the provided dem_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except DemandStatusMaster.DoesNotExist:
            return Response({"error": "Invalid dem_dsm_id: No such DemandStatusMaster found."}, status=status.HTTP_400_BAD_REQUEST)
        except ClientMaster.DoesNotExist:
            return Response({"error": "Invalid dem_clm_id: No such ClientMaster found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class FilterDemandsAPIView(APIView):
    def get(self, request):
        # Extract query parameters
        delivery_manager_id = request.GET.get('Dilevery_DM')
        client_partner_id = request.GET.get('CP')
        hiring_manager = request.GET.get('manager')
        skills = request.GET.get('skills')
        location = request.GET.get('location')

        # Start with an empty filter (Q object)
        filters = Q()

        # Apply filters based on query params
        if delivery_manager_id:
            filters &= Q(dem_lob_id__lob_deliverymanager_id=delivery_manager_id)

        if client_partner_id:
            filters &= Q(dem_lob_id__lob_clientpartner_id=client_partner_id)

        if hiring_manager:
            filters &= Q(dem_clm_id__clm_managername__icontains=hiring_manager)

        if skills:
            filters &= Q(dem_skillset__icontains=skills)

        if location:
            filters &= Q(dem_lcm_id__lcm_name__icontains=location)

        # Get filtered records with count of submitted profiles
        demands = OpenDemand.objects.filter(filters).annotate(
            profiles_submitted=Count('candidate_links')  # Counting profiles per demand
        )

        # Process and format response
        results = []
        for demand in demands:
            delivery_manager = None
            client_partner = None

            # Fetch Delivery Manager details if available
            if demand.dem_lob_id and demand.dem_lob_id.lob_deliverymanager:
                delivery_manager = {
                    "Id": demand.dem_lob_id.lob_deliverymanager.emp_id,
                    "Name": demand.dem_lob_id.lob_deliverymanager.emp_name
                }

            # Fetch Client Partner details if available
            if demand.dem_lob_id and demand.dem_lob_id.lob_clientpartner:
                client_partner = {
                    "Id": demand.dem_lob_id.lob_clientpartner.emp_id,
                    "Name": demand.dem_lob_id.lob_clientpartner.emp_name
                }

            # Append demand details to the response list
            results.append({
                "Hiring Manager Name": demand.dem_clm_id.clm_managername if demand.dem_clm_id else "",
                "Skills": demand.dem_skillset,
                "Location": demand.dem_lcm_id.lcm_name if demand.dem_lcm_id else "",
                "DeliveryManager": delivery_manager,
                "ClientPartner": client_partner,
                "Ctool ID": demand.dem_ctoolnumber,
                "Position Name": demand.position_name,
                "Profiles Submitted": demand.profiles_submitted  # Adding profile count
            })

        return Response(results)