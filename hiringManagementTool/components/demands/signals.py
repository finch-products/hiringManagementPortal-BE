import traceback
import unicodedata
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandhistory import DemandHistory

@receiver(post_save, sender=OpenDemand)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to OpenDemand and logs them in DemandHistory"""

    try:
        print(f"🔍 Signal Triggered for Demand ID: {instance.pk}")

        tracked_fields = [
            'dem_ctoolnumber', 'dem_ctooldate', 'dem_position_name', 'dem_clm_id', 'dem_lcm_id', 'dem_validtill',
            'dem_skillset', 'dem_lob_id', 'dem_idm_id', 'dem_dsm_id', 'dem_positions', 'dem_rrnumber',
            'dem_jrnumber', 'dem_rrgade', 'dem_isactive', 'dem_gcblevel', 'dem_assigned_to', 'dem_jd',
            'dem_comment', 'dem_isreopened', 'dem_insertdate', 'dem_insertby_id', 'dem_updatedate',
            'dem_updateby_id', 'dem_position_location', 'dem_mandatoryskill'
        ]

        field_log_messages = {
            "dem_ctoolnumber": "Tool Number", "dem_ctooldate": "Tool Date", "dem_position_name": "Position Name",
            "dem_clm_id": "Client", "dem_lcm_id": "Location", "dem_validtill": "Valid Till", "dem_skillset": "Skill Set",
            "dem_lob_id": "LOB", "dem_idm_id": "Internal Dept", "dem_dsm_id": "Status", "dem_positions": "Positions",
            "dem_rrnumber": "RR Number", "dem_jrnumber": "JR Number", "dem_rrgade": "RR Grade", "dem_isactive": "Active",
            "dem_gcblevel": "GCB Level", "dem_assigned_to": "Assigned To", "dem_jd": "Job Description",
            "dem_comment": "Comments", "dem_isreopened": "Reopened", "dem_insertdate": "Insert Date",
            "dem_insertby_id": "Inserted By", "dem_updatedate": "Update Date", "dem_updateby_id": "Updated By",
            "dem_position_location": "Position Location", "dem_mandatoryskill": "Mandatory Skills"
        }

        foreign_key_display_map = {
            "dem_clm_id": "clm_name",
            "dem_lcm_id": "lcm_location",
            "dem_lob_id": "lob_name",
            "dem_idm_id": "idm_name",
            "dem_dsm_id": "dsm_name",
            "dem_insertby_id": "emp_name",
            "dem_updateby_id": "emp_name"
        }

        def get_display_value(field, value):
            if field in foreign_key_display_map and value:
                return getattr(value, foreign_key_display_map[field], str(value))
            return str(value) if value is not None else None

        def normalize(value):
            if value is None:
                return None
            return unicodedata.normalize("NFKC", str(value)).replace("\xa0", " ")

        # 📌 If new demand is created
        if created:
            print("✅ New Demand Created - Logging Initial State")

            to_data_values = []
            for field in tracked_fields:
                raw_value = getattr(instance, field, None)
                readable_value = get_display_value(field, raw_value)
                normalized_value = normalize(readable_value)

                to_data_values.append({
                    "label": field,
                    "value": normalized_value
                })

            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id,
                dhs_fromdata={"label": "Null", "value": None},
                dhs_todata={"id": instance.dem_id, "value": to_data_values},
                dhs_dsm_insertdate=now(),
                dhs_log_msg="Demand created",
            )
            return

        # 🔍 Compare with previous record
        last_history = DemandHistory.objects.filter(dhs_dem_id=instance).order_by('-dhs_dsm_insertdate').first()
        last_data = last_history.dhs_todata["value"] if last_history else []

        last_values_map = {entry["label"]: entry["value"] for entry in last_data}

        changed_fields = []
        for field in tracked_fields:
            current_raw_value = getattr(instance, field, None)
            current_value = get_display_value(field, current_raw_value)
            current_value = normalize(current_value)

            old_value = last_values_map.get(field)

            if current_value != old_value:
                print(f"⚡ Change Detected: {field} → {old_value} ➝ {current_value}")
                changed_fields.append({
                    "label": field,
                    "value": current_value
                })

        if changed_fields:
            updated_fromdata = []
            for field in [f["label"] for f in changed_fields]:
                updated_fromdata.append({
                    "label": field,
                    "value": last_values_map.get(field)
                })

            # 📝 Generate grammatically correct log message
            changed_labels = [field_log_messages.get(f["label"], f["label"]) for f in changed_fields]
            if len(changed_labels) == 1:
                log_msg = f"{changed_labels[0]} is updated"
            else:
                log_msg = f"{', '.join(changed_labels)} are updated"

            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id,
                dhs_fromdata={"id": instance.dem_id, "value": updated_fromdata},
                dhs_todata={"id": instance.dem_id, "value": changed_fields},
                dhs_dsm_insertdate=now(),
                dhs_log_msg=log_msg,
            )
            print(f"✅ Changes Logged: {log_msg}")

        else:
            print("✅ No Changes Detected")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print(traceback.format_exc())
