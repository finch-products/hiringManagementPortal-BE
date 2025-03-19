from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster  # Import CandidateStatusMaster


@receiver(post_save, sender=CandidateDemandLink)
def track_candidate_status_change(sender, instance, created, **kwargs):
    """Tracks changes to CandidateDemandLink and logs them in CandidateDemandHistory"""

    print(f"🔍 Signal Triggered for Candidate Demand Link ID: {instance.pk}")  # Debug Log

    try:
        if created:
            print("✅ New Candidate-Demand Link Created - Logging Initial State")

            CandidateDemandHistory.objects.create(
                cdh_cdm_id=instance.cdl_cdm_id,
                cdh_dem_id=instance.cdl_dem_id,
                cdh_csm_id=instance.cdl_csm_id,  # Store the object
                cdh_fromdata={"id": "None", "value": "None"},
                cdh_todata={
                    "id": instance.cdl_csm_id.csm_id,
                    "value": {  # Create a dictionary with relevant fields
                        "csm_code": instance.cdl_csm_id.csm_code,
                        "csm_description": instance.cdl_csm_id.csm_description,
                        # Add other fields from CandidateStatusMaster as needed
                    },
                },
                cdh_insertdate=now(),
            )
            return  # Exit after handling new record creation

        # Fetch the latest history entry for this Candidate-Demand pair
        last_history = CandidateDemandHistory.objects.filter(
            cdh_cdm_id=instance.cdl_cdm_id, cdh_dem_id=instance.cdl_dem_id
        ).order_by("-cdh_insertdate").first()

        if last_history:
            previous_status = last_history.cdh_csm_id
        else:
            previous_status = None

        print(f"🔍 Previous Status: {previous_status}, New Status: {instance.cdl_csm_id}")

        # Check if cdl_csm_id has changed
        if (previous_status is None) or (instance.cdl_csm_id != previous_status):
            print(f"⚡ Status Change Detected: {previous_status} → {instance.cdl_csm_id}")

            from_data = {"id": previous_status.csm_id if previous_status else None, "value": None}  # Corrected

            if previous_status:  # Handle NoneType

                #try: #remove try expect as we are already handeling previous status is None or not

                #previous_status_instance = CandidateStatusMaster.objects.get(csm_id=previous_status) #remove this as you are not using this and it will create error
                from_data["id"] = previous_status.csm_id  # Store the csm_id, not the object
                from_data["value"] = {  # Create a dictionary with relevant fields
                    "csm_code": previous_status.csm_code,
                    "csm_description": previous_status.csm_description,
                    # Add other fields from CandidateStatusMaster as needed
                }
                #except CandidateStatusMaster.DoesNotExist: #remove this as we are already handeling previous status is None or not
                #   from_data["value"] = "CandidateStatusMaster object does not exist"


            CandidateDemandHistory.objects.create(
                cdh_cdm_id=instance.cdl_cdm_id,
                cdh_dem_id=instance.cdl_dem_id,
                cdh_csm_id=instance.cdl_csm_id,  # Store the object
                cdh_fromdata=from_data,
                cdh_todata={
                    "id": instance.cdl_csm_id.csm_id,
                    "value": {  # Create a dictionary with relevant fields
                        "csm_code": instance.cdl_csm_id.csm_code,
                        "csm_description": instance.cdl_csm_id.csm_description,
                        # Add other fields from CandidateStatusMaster as needed
                    },
                },
                cdh_insertdate=now(),
            )
        else:
            print("✅ No Changes Detected in Candidate Status")

    except Exception as e:
        print(f"❌ Error in signal handler: {e}")