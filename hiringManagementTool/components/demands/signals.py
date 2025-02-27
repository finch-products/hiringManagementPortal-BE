# Signal to track demand status changes and store histor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandhistory import DemandHistory
from deepdiff import DeepDiff
import json
import unicodedata
@receiver(post_save, sender=OpenDemand)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to OpenDemand and logs them in DemandHistory"""
    print(f"🔍 Signal Triggered for Demand ID: {instance.pk}")  # Debugging Log

    # Fetch last history record for this demand (to check previous data)
    last_history = DemandHistory.objects.filter(dhs_dem_id=instance.dem_id).order_by('-dhs_dsm_insertdate').first()
    
    #fields to tracked for updates and dem_id not included .
    tracked_fields = [
        'dem_ctoolnumber', 'dem_ctooldate', 'position_name', 'dem_clm_id', 'dem_lcm_id', 'dem_validtill', 'dem_skillset', 'dem_lob_id',
        'dem_idm_id', 'dem_dsm_id', 'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 'dem_isactive',
        'dem_gcblevel', 'dem_assigned_to', 'dem_jd', 'dem_comment', 'dem_isreopened',
        'dem_insertdate', 'dem_insertby_id', 'dem_updatedate', 'dem_updateby_id'
        ]
    # Dictionary to map fields to their log messages
    field_log_messages = {
    "dem_ctoolnumber": "Tool Number",
    "dem_ctooldate": "Tool Date",
    "position_name": "Position Name",
    "dem_clm_id": "Client ID",
    "dem_lcm_id": "LCM ID",
    "dem_validtill": "Valid Till Date",
    "dem_skillset": "Skill Set",
    "dem_lob_id": "LOB ID",
    "dem_idm_id": "IDM ID",
    "dem_dsm_id": "Status ID",
    "dem_positions": "Positions",
    "dem_rrnumber": "RR Number",
    "dem_jrnumber": "JR Number",
    "dem_rrgade": "RR Grade",
    "dem_isactive": "Active Status",
    "dem_gcblevel": "GCB Level",
    "dem_assigned_to": "Assigned To",
    "dem_jd": "Job Description",
    "dem_comment": "Comments",
    "dem_isreopened": "Reopened Status",
    "dem_insertdate": "Insert Date",
    "dem_insertby_id": "Inserted by Employee",
    "dem_updatedate": "Update Date",
    "dem_updateby_id": "Updated by Employee"
    }

    fields_with_id = [ 'dem_dsm_id', 'dem_clm_id', 'dem_idm_id', 'dem_insertby_id', 'dem_lcm_id', 'dem_lob_id', 'dem_updateby_id' ]
    # Fetch the previous instance of OpenDemand (current state before update)
    """try:
        previous = OpenDemand.objects.get(pk=instance.pk)
    except OpenDemand.DoesNotExist:
        previous = None"""
          
    if created:
        print("✅ New Demand Created - Logging Initial State")

        # Store initial state for every tracked field
        for field in tracked_fields:
            field_value = getattr(instance, field, None)
            if hasattr(instance, f"{field}_id"):
                field_value_id = getattr(instance, f"{field}_id")

            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id,
                dhs_fromdata = {
                            "id":"None",  # Store actual field  ID
                            "value": "None"
                            },
    
                dhs_todata = {
                            "id": field_value_id if field in fields_with_id else "Null",  # Store actual field  ID
                            "value": str(field_value)
                            },
                #dhs_fromdata="None",  # No previous record since it's newly created
                #dhs_todata=str(field_value) if field_value is not None else "None",
                dhs_dsm_insertdate=now(),
                dhs_log_msg=field_log_messages.get(field,field.title()),
            )

        return  # Exit after handling new demand creation
    
    changes_detected = False
     # Fields to track (Add/remove fields as needed) removed dem_id as it would be unique
    
    
    for field in tracked_fields:
             # Fetch the last recorded value for this specific field : dhs_log_msg_icontains=field.replace('', ' ')
            last_field_history = DemandHistory.objects.filter(dhs_dem_id=instance.dem_id, dhs_log_msg__icontains=field_log_messages.get(field).replace('_', ' ')).order_by('-dhs_dsm_insertdate').first()
            old_value = last_field_history.dhs_todata if last_history else None

            if hasattr(instance, f"{field}_id"):
                field_value_id2 = getattr(instance, f"{field}_id")
            
            field_value_str=str(getattr(instance,field,None))
            fields_value = unicodedata.normalize("NFKC", field_value_str).replace("\xa0", " ")

            new_value = str({"id":field_value_id2 if field in fields_with_id else "Null" , "value":str(getattr(getattr(instance, field), "clm_name", None) ) if field=='dem_clm_id' else fields_value})


            '''if field=="dem_dsm_id":
                 old_id=last_field_history.dhs_dsm_id
            if field=='dem_clm_id':
                 old_id=last_field_history.dhs_todata.id
                 new_id=instance.dem_clm_id'''
            '''try:
             old_value_dict = json.loads(old_value)  # Convert only if it's a valid JSON string
            except json.JSONDecodeError:
             old_value_dict = {}  '''
            if old_value != new_value:
                changes_detected = True  # Mark as changed

                print(f"⚡ Change Detected: {field} changed from {old_value} → {new_value}")
                #print(old_value.__class__," and class" ,new_value.__class__)

            # Store a history entry for each changed field
                DemandHistory.objects.create(
                    dhs_dem_id=instance,
                    dhs_dsm_id=instance.dem_dsm_id,
                    dhs_fromdata = old_value,
                    dhs_todata = new_value,
                    #dhs_fromdata=str(old_value) ,
                    #dhs_todata=str(new_value) ,
                    dhs_dsm_insertdate=now(),
                    dhs_log_msg=field_log_messages.get(field,field.title()),
                    )

    if not changes_detected:
            print("✅ No Changes Detected, No History Entry Created")


