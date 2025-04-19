from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.models.candidatedemandhistory import CandidateDemandHistory
from hiringManagementTool.models.interview import InterviewSchedulingTable
from hiringManagementTool.constants import InterviewStatus, InterviewType

@receiver(post_save, sender=CandidateDemandLink)
def track_candidate_status_change(sender, instance, created, **kwargs):
    print(f"🔍 Signal Triggered for Candidate Demand Link ID: {instance.pk}")  
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
                    "value": { 
                        "csm_code": instance.cdl_csm_id.csm_code,
                        "csm_description": instance.cdl_csm_id.csm_description,
                    },
                },
                cdh_insertdate=now(),
            )
            return 
        last_history = CandidateDemandHistory.objects.filter(
            cdh_cdm_id=instance.cdl_cdm_id, cdh_dem_id=instance.cdl_dem_id
        ).order_by("-cdh_insertdate").first()

        if last_history:
            previous_status = last_history.cdh_csm_id
        else:
            previous_status = None

        print(f"🔍 Previous Status: {previous_status}, New Status: {instance.cdl_csm_id}")
        if (previous_status is None) or (instance.cdl_csm_id != previous_status):
            print(f"⚡ Status Change Detected: {previous_status} → {instance.cdl_csm_id}")

            from_data = {"id": previous_status.csm_id if previous_status else None, "value": None}  # Corrected

            if previous_status: 
                from_data["id"] = previous_status.csm_id  
                from_data["value"] = { 
                    "csm_code": previous_status.csm_code,
                    "csm_description": previous_status.csm_description,
                }

            CandidateDemandHistory.objects.create(
                cdh_cdm_id=instance.cdl_cdm_id,
                cdh_dem_id=instance.cdl_dem_id,
                cdh_csm_id=instance.cdl_csm_id,  
                cdh_fromdata=from_data,
                cdh_todata={
                    "id": instance.cdl_csm_id.csm_id,
                    "value": { 
                        "csm_code": instance.cdl_csm_id.csm_code,
                        "csm_description": instance.cdl_csm_id.csm_description,
                    },
                },
                cdh_insertdate=now(),
            )
        else:
            print("✅ No Changes Detected in Candidate Status")

    except Exception as e:
        print(f"❌ Error in signal handler: {e}")


@receiver(post_save, sender=InterviewSchedulingTable)
def log_interview_insert(sender, instance, created, **kwargs):
    if not created or not instance.ist_cdl:
        return

    try:
        serialize = lambda v: v.value if isinstance(v, (InterviewStatus, InterviewType)) else v.isoformat() if hasattr(v, 'isoformat') else v
        fields = [
            'ist_interviewdate', 'ist_interview_start_time', 'ist_interview_end_time',
            'ist_timezone', 'ist_interviewtype', 'ist_interviewround',
            'ist_interviewers', 'ist_meeting_details', 'ist_interviewstatus', 'ist_remarks'
        ]
        data = {f: serialize(getattr(instance, f)) for f in fields}

        print(f"🟢 Logging new interview (ID: {instance.ist_id}) to history.")
        CandidateDemandHistory.objects.create(
            cdh_insertdate=now(),
            cdh_fromdata={"id": "None", "value": "None"},
            cdh_todata=data,
            cdh_cdm_id=instance.ist_cdl.cdl_cdm_id,
            cdh_dem_id=instance.ist_cdl.cdl_dem_id,
            cdh_csm_id=None,
        )
    except Exception as e:
        print(f"❌ Error logging interview history: {e}")


@receiver(pre_save, sender=InterviewSchedulingTable)
def log_interview_update(sender, instance, **kwargs):
    if not instance.ist_id or not instance.ist_cdl:
        return

    try:
        old = InterviewSchedulingTable.objects.get(pk=instance.pk)
        serialize = lambda v: v.value if isinstance(v, (InterviewStatus, InterviewType)) else v.isoformat() if hasattr(v, 'isoformat') else v
        fields = [
            'ist_interviewdate', 'ist_interview_start_time', 'ist_interview_end_time',
            'ist_timezone', 'ist_interviewtype', 'ist_interviewround',
            'ist_interviewers', 'ist_meeting_details', 'ist_interviewstatus', 'ist_remarks'
        ]

        changed = {
            f: serialize(getattr(instance, f)) for f in fields
            if serialize(getattr(instance, f)) != serialize(getattr(old, f))
        }

        if changed:
            CandidateDemandHistory.objects.create(
                cdh_insertdate=now(),
                cdh_fromdata={f: serialize(getattr(old, f)) for f in changed},
                cdh_todata=changed,
                cdh_cdm_id=instance.ist_cdl.cdl_cdm_id,
                cdh_dem_id=instance.ist_cdl.cdl_dem_id,
                cdh_csm_id=None,
            )
            print(f"🟡 Interview update logged (ID: {instance.ist_id})")

    except InterviewSchedulingTable.DoesNotExist:
        pass
    except Exception as e:
        print(f"❌ Error logging interview update: {e}")
