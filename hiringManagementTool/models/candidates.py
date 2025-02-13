from django.db import models
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster
from hiringManagementTool.models.employees import EmployeeMaster


class CandidateMaster(models.Model):
    cdm_id = models.AutoField(primary_key=True, help_text="Unique Candidate ID (Auto-generated)")
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

    def __str__(self):
        return f"{self.cdm_name} ({'Internal' if self.cdm_isinternal else 'External'})"
    
    class Meta:
        managed = True
        db_table = 'candidatemaster'
