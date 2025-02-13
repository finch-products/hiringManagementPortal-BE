from django.db import models


class LocationMaster(models.Model):
    lcm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Location Manager)")
    lcm_name = models.CharField(max_length=50, help_text="Location Manager Name")
    lcm_state = models.CharField(max_length=50, help_text="State of the Location Manager")
    lcm_country = models.CharField(max_length=50, help_text="Country of the Location Manager")
    lcm_insertby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lcm_inserted_records",
        help_text="Reference to the employee who inserted this record"
    )
    lcm_updateby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lcm_updated_records",
        help_text="Reference to the employee who last updated this record"
    )

    def __str__(self):
        return f"{self.lcm_name} ({self.lcm_state}, {self.lcm_country})"
    
     
    class Meta:
        managed = True
        db_table = 'locationmaster'