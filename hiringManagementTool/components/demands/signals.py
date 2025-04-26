import traceback
import unicodedata
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.demandhistory import DemandHistory
from hiringManagementTool.models.employees import EmployeeMaster

# Define tracked fields and mappings outside the function for clarity and efficiency
TRACKED_FIELDS = [
    'dem_ctoolnumber', 'dem_ctooldate', 'dem_position_name', 'dem_clm_id', 'dem_lcm_id', 'dem_validtill',
    'dem_skillset', 'dem_lob_id', 'dem_idm_id', 'dem_dsm_id', 'dem_positions', 'dem_rrnumber',
    'dem_jrnumber', 'dem_rrgade', 'dem_isactive', 'dem_gcblevel', 'dem_assigned_to', 'dem_jd',
    'dem_comment', 'dem_isreopened', 'dem_insertdate', 'dem_insertby_id', 'dem_updatedate',
    'dem_updateby_id', 'dem_position_location', 'dem_mandatoryskill'
]

FIELD_LOG_MESSAGES = {
    "dem_ctoolnumber": "Tool Number", "dem_ctooldate": "Tool Date", "dem_position_name": "Position Name",
    "dem_clm_id": "Client", "dem_lcm_id": "Location", "dem_validtill": "Valid Till", "dem_skillset": "Skill Set",
    "dem_lob_id": "LOB", "dem_idm_id": "Internal Dept", "dem_dsm_id": "Status", "dem_positions": "Positions",
    "dem_rrnumber": "RR Number", "dem_jrnumber": "JR Number", "dem_rrgade": "RR Grade", "dem_isactive": "Active",
    "dem_gcblevel": "GCB Level", "dem_assigned_to": "Assigned To", "dem_jd": "Job Description",
    "dem_comment": "Comments", "dem_isreopened": "Reopened", "dem_insertdate": "Insert Date",
    "dem_insertby_id": "Inserted By", "dem_updatedate": "Update Date", "dem_updateby_id": "Updated By",
    "dem_position_location": "Position Location", "dem_mandatoryskill": "Mandatory Skills"
}

FOREIGN_KEY_DISPLAY_MAP = {
    "dem_clm_id": "clm_name",
    "dem_lcm_id": "lcm_location",
    "dem_lob_id": "lob_name",
    "dem_idm_id": "idm_name",
    "dem_dsm_id": "dsm_name",
    "dem_insertby_id": "emp_name",
    "dem_updateby_id": "emp_name"
    # Note: dem_assigned_to might also be a foreign key to EmployeeMaster? Add if needed.
    # "dem_assigned_to": "emp_name",
}

def get_display_value(field, value):
    """Helper to get readable value, handling ForeignKeys and None."""
    if value is None:
        return None
    # Handle EmployeeMaster specifically if emp_id might be passed directly
    if field in ['dem_insertby_id', 'dem_updateby_id', 'dem_assigned_to'] and value:
        try:
            # Check if value is already an EmployeeMaster instance or just an ID
            emp_id_to_lookup = value.emp_id if hasattr(value, 'emp_id') else value
            employee = EmployeeMaster.objects.get(emp_id=emp_id_to_lookup)
            return employee.emp_name
        except (EmployeeMaster.DoesNotExist, ValueError, TypeError): # Catch potential errors if value is not an ID or object
             print(f"⚠ Warning: Could not find EmployeeMaster for field {field} with value {value}")
             return str(value) # Fallback to string representation

    # Handle other mapped foreign keys
    if field in FOREIGN_KEY_DISPLAY_MAP and value:
         # Check if value is the related object or just the ID (might happen during save)
        if hasattr(value, FOREIGN_KEY_DISPLAY_MAP[field]):
             return getattr(value, FOREIGN_KEY_DISPLAY_MAP[field], str(value))
        else:
            # If it's just an ID, we might need to fetch the object, but that's less efficient in signals.
            # Let's try a simpler approach first: returning the ID as string.
            # If you NEED the name here even if only ID is present, you'd fetch the related object.
            # Example (less efficient):
            # related_model = OpenDemand._meta.get_field(field).related_model
            # try:
            #     obj = related_model.objects.get(pk=value)
            #     return getattr(obj, FOREIGN_KEY_DISPLAY_MAP[field], str(value))
            # except related_model.DoesNotExist:
            #     return str(value)
             return str(value) # Fallback for now

    # Handle boolean fields for better readability
    if isinstance(value, bool):
        return "Yes" if value else "No"

    # Default: return string representation
    return str(value)

def normalize(value):
    """Normalize unicode and strip extra spaces."""
    if value is None:
        return None
    # Ensure value is string before normalizing
    str_value = str(value)
    # Normalize unicode characters (e.g., handle different space types)
    normalized = unicodedata.normalize("NFKC", str_value)
    # Replace non-breaking space with regular space and strip leading/trailing whitespace
    return normalized.replace("\xa0", " ").strip()

@receiver(post_save, sender=OpenDemand)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to OpenDemand and logs them in DemandHistory"""
    try:
        print(f"🔍 Signal Triggered for Demand ID: {instance.pk} | Created: {created}")

        # --- 1. Calculate the FULL current state of all tracked fields ---
        current_full_state_list = []
        for field in TRACKED_FIELDS:
            raw_value = getattr(instance, field, None)
            readable_value = get_display_value(field, raw_value)
            normalized_value = normalize(readable_value)
            current_full_state_list.append({
                "label": field,
                "value": normalized_value
            })

        # --- 2. Handle CREATION ---
        if created:
            print("✅ New Demand Created - Logging Initial State")
            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id, # Current status
                dhs_fromdata={"label": "Null", "value": None}, # Represents 'no previous state'
                dhs_todata={"id": instance.dem_id, "value": current_full_state_list}, # Store FULL initial state
                dhs_dsm_insertdate=now(),
                dhs_log_msg="Demand created",
            )
            print(f"✅ Initial state logged for Demand ID: {instance.pk}")
            return # Exit after handling creation

        # --- 3. Handle UPDATE ---
        print(f"🔄 Demand Updated - Comparing with previous state for Demand ID: {instance.pk}")
        last_history = DemandHistory.objects.filter(dhs_dem_id=instance).order_by('-dhs_dsm_insertdate').first()

        # Safety check: What if history is missing? (Shouldn't happen after creation works)
        if not last_history:
            print(f"⚠ Warning: No previous history found for updated demand ID: {instance.pk}. Logging current state with error message.")
            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id,
                dhs_fromdata={"label": "Error", "value": "Previous History Missing"}, # Indicate error
                dhs_todata={"id": instance.dem_id, "value": current_full_state_list}, # Log current state anyway
                dhs_dsm_insertdate=now(),
                dhs_log_msg="Demand updated (previous history missing)",
            )
            return

        # --- 4. Compare Current State with LAST FULL State ---
        # The previous dhs_todata should contain the full state from the last save
        previous_full_state_data = last_history.dhs_todata.get("value", [])
        if not isinstance(previous_full_state_data, list): # Basic sanity check
             print(f"⚠ Warning: Previous dhs_todata['value'] is not a list for history ID: {last_history.pk}. Skipping comparison.")
             # Optionally log an error state or just return
             return

        previous_values_map = {entry.get("label"): entry.get("value") for entry in previous_full_state_data if isinstance(entry, dict)}

        changed_fields_details = [] # Stores {label, old_value, new_value} for log msg
        from_data_for_update = []   # Stores {label, value} for dhs_fromdata (only old values of changed fields)

        current_values_map = {entry["label"]: entry["value"] for entry in current_full_state_list} # Create map for easy lookup

        for field in TRACKED_FIELDS:
            current_value = current_values_map.get(field) # Get current normalized value
            old_value = previous_values_map.get(field)    # Get OLD normalized value from the previous full state

            # Compare normalized values
            if current_value != old_value:
                print(f"⚡ Change Detected: {field} | Old: '{old_value}' ({type(old_value)}) → New: '{current_value}' ({type(current_value)})")
                changed_fields_details.append({
                    "label": field,
                    "old_value": old_value,
                    "new_value": current_value
                })
                from_data_for_update.append({ # Store the old value for the fromdata field
                    "label": field,
                    "value": old_value
                })

        # --- 5. Log Changes if any were detected ---
        if changed_fields_details:
            # Generate grammatically correct log message
            changed_labels = [FIELD_LOG_MESSAGES.get(f["label"], f["label"]) for f in changed_fields_details]
            if len(changed_labels) == 1:
                log_msg = f"{changed_labels[0]} is updated"
            elif len(changed_labels) > 1:
                 # Join all but the last with comma, then add " and " before the last one
                log_msg = f"{', '.join(changed_labels[:-1])} and {changed_labels[-1]} are updated"
            else: # Should not happen if changed_fields_details is populated, but safety first
                log_msg = "Demand updated (details unavailable)"

            print(f"📝 Logging update: {log_msg}")

            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id, # Current status
                dhs_fromdata={"id": instance.dem_id, "value": from_data_for_update}, # Contains OLD values of ONLY changed fields
                dhs_todata={"id": instance.dem_id, "value": current_full_state_list}, # Contains FULL NEW state of ALL tracked fields
                dhs_dsm_insertdate=now(),
                dhs_log_msg=log_msg,
            )
            print(f"✅ Changes logged successfully for Demand ID: {instance.pk}")

        else:
            print(f"✅ No Changes Detected for Demand ID: {instance.pk}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR in track_status_change signal for Demand ID {instance.pk if instance else 'Unknown'}: {e}")
        print(traceback.format_exc())