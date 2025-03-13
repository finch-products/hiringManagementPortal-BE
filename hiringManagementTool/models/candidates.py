from django.db import models
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.employees import EmployeeMaster
from datetime import datetime
from django.db.models import Max
from pudb import set_trace

class CandidateMaster(models.Model):
    cdm_id = models.CharField(
        primary_key=True,
        db_column="cdm_id",
        max_length=50, 
        editable=False, 
        help_text="Auto-generated ID in format cdm_ddmmyyyy_1"
    )
    cdm_emp_id = models.IntegerField(null=True, blank=True, help_text="Employee ID for tracking (if internal)")
    cdm_name = models.CharField(max_length=50, help_text="Full name of the candidate")
    cdm_email = models.EmailField(unique=True, help_text="Candidate email (must be unique)")
    cdm_phone = models.CharField(max_length=20, help_text="Candidate phone number")
    cdm_location = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_candidate",
        help_text="Reference to Location Master Table"
    )

    cdm_profile = models.FileField(upload_to="uploads/candidate_profiles/", blank=True, null=True, help_text="Candidate profile file (resume)")
    cdm_description = models.TextField(blank=True, null=True, help_text="Cover letter or profile description")
    
    cdm_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidate_references",
        db_column="cdm_csm_id",
        help_text="Reference to another candidate (if applicable)"
    )

    cdm_keywords = models.TextField(blank=True, null=True, help_text="Technical keywords associated with the candidate")

    cdm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    cdm_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates_inserted",
        help_text="User ID (Employee) who created this record"
    )

    cdm_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    cdm_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates_updated",
        help_text="User ID (Employee) who last updated this record"
    )

    cdm_isinternal = models.BooleanField(default=False, help_text="1 for internal candidate, 0 for external")
    cdm_isactive = models.BooleanField(default=True, help_text="1 for active, 0 for inactive")
    cdm_comment = models.TextField(blank=True, null=True, help_text="Comment Entry")
    def save(self, *args, **kwargs):
    # Only generate a new cdm_id if this is a new record
        if not self.cdm_id:
            today = datetime.today().strftime('%d%m%Y')
            
            # Get the max numeric suffix
            latest_entry = CandidateMaster.objects.filter(cdm_id__startswith=f"cdm_{today}_").aggregate(
                max_id=Max("cdm_id")
            )

            if latest_entry["max_id"]:
                try:
                    last_number = int(latest_entry["max_id"].rsplit("_", 1)[-1])  # Extract last numeric part
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1  # Handle edge cases where ID format is incorrect
            else:
                new_number = 1  # Start from 1

            self.cdm_id = f"cdm_{today}_{new_number}"  # No zero-padding, pure integer sorting

        super().save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'candidatemaster'
