from django.db import models

from .demandstatus import DemandStatusMaster
from .demands import OpenDemand
from .employees import EmployeeMaster

class DemandHistory(models.Model):
    dhs_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Status History)")
    
    dhs_dsm_id = models.ForeignKey(
        'DemandStatusMaster',
        on_delete=models.CASCADE,
        related_name="demand_history",
        db_column="dhs_dsm_id",
        help_text="Reference to Demand Status Master"
    )
    
    dhs_dem_id = models.ForeignKey(
        'OpenDemand',
        on_delete=models.CASCADE,
        related_name="open_demand",
        db_column="dhs_dem_id",
        help_text="Reference to Open demand",
    )
    dhs_dsm_insertdate = models.DateTimeField(help_text="Status insert date (from DemandStatusMaster)")
    dhs_fromdata = models.TextField(blank=True, null=True, help_text="Old value/data before update")
    dhs_todata = models.TextField(blank=True, null=True, help_text="New value/data after update")
    dhs_log_msg = models.TextField(blank=True, null=True, help_text="Comments regarding status change")
    dhs_inserted_by=models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demand_inserted",
        db_column="dhs_inserted_by",
        help_text="User ID (Employee) who created this record"
    )

    def __str__(self):
        return f"History ID: {self.dhs_id} - Status: {self.dhs_dsm_code}"
    
    class Meta:
        managed = True
        db_table = 'demandhistory'