import json
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,serializers
from rest_framework.parsers import MultiPartParser, FormParser
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.components.demands.serializers import OpenDemandSerializer
from hiringManagementTool.models.demandstatus import DemandStatusMaster
from hiringManagementTool.models.departments import InternalDepartmentMaster
from hiringManagementTool.models.locations import LocationMaster
from .serializers import OpenDemandUpdateSerializer, AllOpenDemandsIdSerializer
from rest_framework.generics import UpdateAPIView
from datetime import datetime
from django.db.models import Count, Q
from hiringManagementTool.models.clients import ClientMaster
from hiringManagementTool.models.lobs import LOBMaster

class DemandAPIView(APIView):
    """Handles GET and POST requests for OpenDemand"""
    
    def get(self, request):
        """Retrieve all OpenDemands"""
        demands = OpenDemand.objects.select_related(
            'dem_clm_id', 'dem_lcm_id', 'dem_lob_id', 'dem_idm_id', 'dem_dsm_id'
        ).order_by('-dem_insertdate') 
        serializer = OpenDemandSerializer(demands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new demand and auto-assign status"""
        print("\n📥 Incoming Request Data:", request.data)
        print("\n📥 dem_jd value:", request.data.get('dem_jd'))  # Log the value of dem_jd

         # Handle dem_position_location if it's coming as a JSON string
        data = request.data.copy()  # Create a mutable copy
         # Handle dem_position_location
        if 'dem_position_location' in data:
            position_location = data['dem_position_location']
    
        if isinstance(position_location, str):
         try:
            # Parse the string to Python object
            if position_location.startswith('[') and position_location.endswith(']'):
                # It's a JSON string
                parsed_data = json.loads(position_location)
            else:
                # It might be comma-separated values
                parsed_data = [x.strip() for x in position_location.split(',') if x.strip()]
            
            # Convert to list of integers and assign back
            data['dem_position_location'] = [int(item) for item in parsed_data]
         except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing: {e}")
            data['dem_position_location'] = []

        print("\n📥 Final Parsed dem_position_location:", data['dem_position_location'])  # Debug final data


        serializer = OpenDemandSerializer(data=data)
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

class OpenDemandUpdateAPIView(UpdateAPIView):
    """Efficiently updates OpenDemand"""
    queryset = OpenDemand.objects.all()
    serializer_class = OpenDemandUpdateSerializer
    #lookup_field = "dem_id"
    #lookup_url_kwarg = 'id'
    def get_object(self):
        dem_id = self.request.data.get("dem_id")  # Get dem_id from request body
        if not dem_id:
            raise serializers.ValidationError({"dem_id": "This field is required."})
        
        try:
            return OpenDemand.objects.get(dem_id=dem_id)
        except OpenDemand.DoesNotExist:
            raise serializers.ValidationError({"dem_id": "OpenDemand with this ID does not exist."})
    
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

