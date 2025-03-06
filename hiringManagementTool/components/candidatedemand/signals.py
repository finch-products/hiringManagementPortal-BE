# Signal to track demand status changes and store histor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
#from deepdiff import DeepDiff
import json
import unicodedata
@receiver(post_save, sender=CandidateDemandLink)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to CandidateDemandLink and logs them in DemandHistory"""
    print(f"🔍 Signal Triggered for Demand ID: {instance.pk}")  # Debugging Log

    # Fetch last history record for this demand (to check previous data)
   # last_history = CandidateDemandHistory.objects.filter(dhs_dem_id=instance.dem_id).order_by('-cdh_insertdate').first()
    
    #fields to tracked for updates and dem_id not included .
    tracked_fields = [
        'cdl_cdm_id', 'cdl_dem_id', 'cdl_csm_id', 'cdl_joiningdate', 'cdl_insertdate'
        ]
    # Dictionary to map fields to their log messages
    ''' field_log_messages = {
    "cdl_cdm_id": "Candidate ID",
    "cdl_dem_id": "Demand ID",
    "cdl_csm_id": "Status ID",
    "dem_clm_id": "Client ID",
    "cdl_joiningdate": "Joining Date",
    "cdl_insertdate": "Insert Date"
    }'''

    fields_with_id = [ 'cdl_cdm_id', 'cdl_dem_id', 'cdl_csm_id' ]
    # Fetch the previous instance of CandidateDemandLink(current state before update)
    """try:
        previous = CandidateDemandLink.objects.get(pk=instance.pk)
    except CandidateDemandLink.DoesNotExist:
        previous = None"""
          
    if created:
        print("✅ New Demand Created - Logging Initial State")

        # Store initial state for every tracked field
        for field in tracked_fields:
            field_value = getattr(instance, field, None)
            if hasattr(instance, f"{field}_id"):
                field_value_id = getattr(instance, f"{field}_id")

            CandidateDemandHistory.objects.create(
                cdh_cdm_id=instance.cdl_cdm_id,
                cdh_dem_id=instance.cdl_dem_id,
                cdh_csm_id=instance.cdl_csm_id,
                cdh_fromdata = {
                            "id":"None",  # Store actual field  ID
                            "value": "None"
                            },
    
                cdh_todata = {
                            "id": field_value_id if field in fields_with_id else "Null",  # Store actual field  ID
                            "value": str(field_value)
                            },
                #dhs_fromdata="None",  # No previous record since it's newly created
                #dhs_todata=str(field_value) if field_value is not None else "None",
                cdh_insertdate=now(),
               # dhs_log_msg=field_log_messages.get(field,field.title()),
            )

        return  # Exit after handling new demand creation