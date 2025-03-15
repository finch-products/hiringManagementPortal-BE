from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
import unicodedata

@receiver(post_save, sender=CandidateDemandLink)
def track_candidate_status_change(sender, instance, created, **kwargs):
    """Tracks changes to CandidateDemandLink and logs them in CandidateDemandHistory"""
    print(f"🔍 Signal Triggered for Candidate Demand Link ID: {instance.pk}")  # Debugging Log

    # Tracked fields (excluding IDs)
    tracked_fields = [
        'cdl_cdm_id', 'cdl_dem_id', 'cdl_csm_id', 'cdl_joiningdate', 'cdl_insertdate'
    ]

    fields_with_id = ['cdl_cdm_id', 'cdl_dem_id', 'cdl_csm_id']
    
    if created:
        print("✅ New Candidate-Demand Link Created - Logging Initial State")
        for field in tracked_fields:
            field_value = getattr(instance, field, None)
            field_value_id = getattr(instance, f"{field}_id", None) if field in fields_with_id else "Null"

            CandidateDemandHistory.objects.create(
                cdh_cdm_id=instance.cdl_cdm_id,
                cdh_dem_id=instance.cdl_dem_id,
                cdh_csm_id=instance.cdl_csm_id,
                cdh_fromdata={"id": "None", "value": "None"},
                cdh_todata={"id": field_value_id, "value": str(field_value)},
                cdh_insertdate=now(),
            )
        return  # Exit after handling new record creation
    
    # Check for updates only to cdl_csm_id (candidate status)
    last_history = CandidateDemandHistory.objects.filter(
        cdh_cdm_id=instance.cdl_cdm_id, cdh_dem_id=instance.cdl_dem_id
    ).order_by('-cdh_insertdate').first()
    
    if last_history and last_history.cdh_csm_id != instance.cdl_csm_id:
        print(f"⚡ Status Change Detected: {last_history.cdh_csm_id} → {instance.cdl_csm_id}")
        CandidateDemandHistory.objects.create(
            cdh_cdm_id=instance.cdl_cdm_id,
            cdh_dem_id=instance.cdl_dem_id,
            cdh_csm_id=instance.cdl_csm_id,
            cdh_fromdata={"id": last_history.cdh_csm_id, "value": str(last_history.cdh_csm_id)},
            cdh_todata={"id": instance.cdl_csm_id, "value": str(instance.cdl_csm_id)},
            cdh_insertdate=now(),
        )
    else:
        print("✅ No Changes Detected in Candidate Status")