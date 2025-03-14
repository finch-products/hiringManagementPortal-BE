from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from hiringManagementTool.components.candidates.serializers import CandidateMasterSerializer
from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.employees import EmployeeMaster

class CandidateAPIView(ListCreateAPIView):
    queryset = CandidateMaster.objects.all()

    serializer_class = CandidateMasterSerializer


class CandidateDetailAPIView(RetrieveUpdateAPIView):
    queryset = CandidateMaster.objects.all()
    serializer_class = CandidateMasterSerializer
    lookup_field = 'cdm_id'
    lookup_url_kwarg = 'id'


class CandidateStatusUpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        cdm_id = request.data.get("cdm_id")
        cdm_updateby_id = request.data.get("cdm_updateby_id")
        csm_id = request.data.get("csm_id")
        cdm_comment = request.data.get("cdm_comment", None)

        if not cdm_id or not cdm_updateby_id or not csm_id:
            return Response({"error": "cdm_id, cdm_updateby_id, and csm_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the candidate record
            candidate = CandidateMaster.objects.get(cdm_id=cdm_id)
            current_csm_id = candidate.cdm_csm_id.csm_id if candidate.cdm_csm_id else None

            # Fetch the new status instance
            new_csm_instance = CandidateStatusMaster.objects.get(csm_id=csm_id)

            # Validate status transition
            if current_csm_id:
                current_status = CandidateStatusMaster.objects.get(csm_id=current_csm_id)
                restricted_statuses = (
                    current_status.csm_resstatus.split(",") if current_status.csm_resstatus else []
                )

                # Check if the new status is in the restricted statuses
                if str(csm_id) in restricted_statuses:
                    return Response(
                        {"error": f"This status ({new_csm_instance.csm_code}) cannot be assigned to this candidate."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Update the candidate status and comment
            candidate.cdm_csm_id = new_csm_instance
            if cdm_comment is not None:
                candidate.cdm_comment = cdm_comment

            # Update the updateby and updatedate fields
            candidate.cdm_updateby = EmployeeMaster.objects.get(emp_id=cdm_updateby_id)
            candidate.cdm_updatedate = datetime.now()

            # Save the candidate (this will not generate a new cdm_id because it's an update)
            candidate.save()

            # Update the CandidateDemandLink table
            CandidateDemandLink.objects.filter(cdl_cdm_id=cdm_id).update(cdl_csm_id=new_csm_instance)

            return Response({"message": "Candidate status and comment updated successfully"}, status=status.HTTP_200_OK)

        except CandidateMaster.DoesNotExist:
            return Response({"error": "Candidate with the provided cdm_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except CandidateStatusMaster.DoesNotExist:
            return Response({"error": "Invalid csm_id: No such CandidateStatusMaster found."}, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeMaster.DoesNotExist:
            return Response({"error": "Invalid cdm_updateby_id: No such EmployeeMaster found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)