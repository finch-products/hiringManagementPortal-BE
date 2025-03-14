from django.db import models
from hiringManagementTool.models.employees import EmployeeMaster


class CandidateStatusMaster(models.Model):
    csm_id = models.AutoField(primary_key=True, help_text="Unique Candidate Status ID (Auto-generated)")
    csm_code = models.CharField(max_length=50, unique=True, help_text="Candidate Status Name (e.g., Open, L1 Interview Scheduled, Selected, Rejected, On Hold, etc.)")
    csm_description = models.TextField(blank=True, null=True, help_text="Detailed description of the status")
    csm_sortid = models.IntegerField(help_text="Sorting order for statuses")

    csm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    csm_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_created",
        help_text="User ID (Employee) who created this status"
    )
    csm_inactive = models.BooleanField(default=False, db_column="csm_inactive", help_text="If True (1), this status will not be listed in the application")
    
    csm_resstatus = models.TextField(
        blank=True, null=True,
        db_column="csm_resstatus",
        help_text="Comma-separated list of candidate status IDs that cannot transition to this status"
    )
    def __str__(self):
        return f"{self.csm_code} - Status ID: {self.csm_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatestatusmaster'