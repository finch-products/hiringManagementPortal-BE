import traceback
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandhistory import DemandHistory
import unicodedata

@receiver(post_save, sender=OpenDemand)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to OpenDemand and logs them in DemandHistory"""
    try:
        print(f"🔍 Signal Triggered for Demand ID: {instance.pk}")  # Debugging Log

        last_history = DemandHistory.objects.filter(dhs_dem_id=instance.dem_id).order_by('-dhs_dsm_insertdate').first()

        tracked_fields = [
            'dem_ctoolnumber', 'dem_ctooldate', 'dem_position_name', 'dem_clm_id', 'dem_lcm_id', 'dem_validtill', 
            'dem_skillset', 'dem_lob_id', 'dem_idm_id', 'dem_dsm_id', 'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 
            'dem_rrgade', 'dem_isactive', 'dem_gcblevel', 'dem_assigned_to', 'dem_jd', 'dem_comment', 'dem_isreopened',
            'dem_insertdate', 'dem_insertby_id', 'dem_updatedate', 'dem_updateby_id', 'dem_position_location'
        ]

        field_log_messages = {
            "dem_ctoolnumber": "Tool Number", "dem_ctooldate": "Tool Date", "dem_position_name": "Position Name",
            "dem_clm_id": "Client ID", "dem_lcm_id": "LCM ID", "dem_validtill": "Valid Till Date", "dem_skillset": "Skill Set",
            "dem_lob_id": "LOB ID", "dem_idm_id": "IDM ID", "dem_dsm_id": "Status ID", "dem_positions": "Positions",
            "dem_rrnumber": "RR Number", "dem_jrnumber": "JR Number", "dem_rrgade": "RR Grade", "dem_isactive": "Active Status",
            "dem_gcblevel": "GCB Level", "dem_assigned_to": "Assigned To", "dem_jd": "Job Description",
            "dem_comment": "Comments", "dem_isreopened": "Reopened Status", "dem_insertdate": "Insert Date",
            "dem_insertby_id": "Inserted by Employee", "dem_updatedate": "Update Date",
            "dem_updateby_id": "Updated by Employee", "dem_position_location": "Position Location"
        }

        fields_with_id = ['dem_dsm_id', 'dem_clm_id', 'dem_idm_id', 'dem_insertby_id', 'dem_lcm_id', 'dem_lob_id', 'dem_updateby_id']

        if created:
            print("✅ New Demand Created - Logging Initial State")
            for field in tracked_fields:
                try:
                    field_value = str(getattr(instance, field, None))
                    field_value_normalized = unicodedata.normalize("NFKC", field_value).replace("\xa0", " ")
                    field_value_id = getattr(instance, f"{field}_id", None) if hasattr(instance, f"{field}_id") else None

                    DemandHistory.objects.create(
                        dhs_dem_id=instance,
                        dhs_dsm_id=instance.dem_dsm_id,
                        dhs_fromdata={"id": None, "value": ""},
                        dhs_todata={"id": field_value_id if field in fields_with_id else None, "value": field_value_normalized},
                        dhs_dsm_insertdate=now(),
                        dhs_log_msg=field_log_messages.get(field, field.title()),
                    )
                except Exception as e:
                    print(f"❌ Error in Creating Initial History for {field}: {e}")
                    print(traceback.format_exc())

            return  # Exit after handling new demand creation

        changes_detected = False

        for field in tracked_fields:
            try:
                field_value_msg = field_log_messages.get(field, " ")
                print(f"Looking for log message: '{field_value_msg}' in DemandHistory for ID: {instance.dem_id}")

                last_field_history = DemandHistory.objects.filter(
                 dhs_dem_id=instance.dem_id, 
                 dhs_log_msg__icontains=field_value_msg
                ).order_by('-dhs_dsm_insertdate').first()

                if last_field_history:
                    print("History found:", last_field_history)
                else:
                    print("No history found.")
                old_value = last_field_history.dhs_todata if last_field_history else None
                field_value_id2 = getattr(instance, f"{field}_id", None) if hasattr(instance, f"{field}_id") else None
                field_value_str = str(getattr(instance, field, None))
                fields_value = unicodedata.normalize("NFKC", field_value_str).replace("\xa0", " ")
                
                new_value = str({
                    "id": field_value_id2 if field in fields_with_id else "Null",
                    "value": str(getattr(getattr(instance, field), "clm_name", None)) if field == 'dem_clm_id' else fields_value
                })

                if old_value != new_value:
                    changes_detected = True
                    print(f"⚡ Change Detected: {field} changed from {old_value} → {new_value}")

                    DemandHistory.objects.create(
                        dhs_dem_id=instance,
                        dhs_dsm_id=instance.dem_dsm_id,
                        dhs_fromdata=old_value,
                        dhs_todata=new_value,
                        dhs_dsm_insertdate=now(),
                        dhs_log_msg=field_log_messages.get(field, field.title()),
                    )
                    print(f"✅ Changes saved: {field} changed from {old_value} → {new_value}")

            except Exception as e:
                print(f"❌ Error in Tracking Change for {field}: {e}")
                print(traceback.format_exc())

        if not changes_detected:
            print("✅ No Changes Detected, No History Entry Created")

    except Exception as main_error:
        print(f"❌ Critical Error in Signal Execution: {main_error}")
        print(traceback.format_exc())
