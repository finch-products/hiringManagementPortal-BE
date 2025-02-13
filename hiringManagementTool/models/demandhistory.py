from django.db import models
from hiringManagementTool.models.demandstatus import DemandStatusMaster


class DemandHistoryTable(models.Model):
    dhs_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Status History)")
    
    dhs_dsm = models.ForeignKey(
        'DemandStatusMaster',
        on_delete=models.CASCADE,
        related_name="demand_history",
        help_text="Reference to Demand Status Master"
    )

    dhs_dsm_code = models.CharField(max_length=50, help_text="Demand Status Code (from DemandStatusMaster)")
    dhs_dsm_description = models.TextField(blank=True, null=True, help_text="Demand Status Description (from DemandStatusMaster)")
    dhs_dsm_sortid = models.IntegerField(help_text="Sorting order (from DemandStatusMaster)")
    dhs_dsm_insertdate = models.DateTimeField(help_text="Status insert date (from DemandStatusMaster)")
    dhs_dsm_updateddate = models.DateTimeField(auto_now=True, help_text="Status last updated date & time")
    dhs_dsm_isclosed = models.BooleanField(default=False, help_text="Indicates if status is treated as closed")

    dhs_comments = models.TextField(blank=True, null=True, help_text="Comments regarding status change")
    dhs_fromdata = models.TextField(blank=True, null=True, help_text="Old value/data before update")
    dhs_todata = models.TextField(blank=True, null=True, help_text="New value/data after update")

    def __str__(self):
        return f"History ID: {self.dhs_id} - Status: {self.dhs_dsm_code}"
    
    class Meta:
        managed = True
        db_table = 'demandhistory'
