from django.db import models


from .employees import EmployeeMaster

class DemandStatusMaster(models.Model):
    dsm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Demand Status)")
    dsm_code = models.CharField(max_length=50, unique=True, help_text="Status Name (e.g., Open, JD Received, Rejected, etc.)")
    dsm_description = models.TextField(blank=True, null=True, help_text="Detailed description of the status")
    dsm_sortid = models.IntegerField(help_text="Sorting order for statuses")

    dsm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")

    dsm_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    dsm_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_updated",
        db_column="dsm_updateby",
        help_text="User ID (Employee) who last updated this status"
    )
    
    dsm_isclosed = models.BooleanField(default=False, help_text="Indicates if the status is treated as closed")
    dsm_resstatus = models.TextField(
        blank=True, null=True,
        db_column="dsm_resstatus",
        help_text="Comma-separated list of demand status IDs that cannot transition to this status"
    )
    dsm_inactive = models.BooleanField(default=False, db_column="dsm_inactive", help_text="If True (1), this status will not be listed in the application")
    def __str__(self):
        return f"{self.dsm_code} - {'Closed' if self.dsm_isclosed else 'Open'}"
    
    class Meta:
        managed = True
        db_table = 'demandstatusmaster'
