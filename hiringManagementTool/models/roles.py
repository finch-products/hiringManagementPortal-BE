from django.db import models

class RoleMaster(models.Model):
    rlm_id = models.IntegerField(primary_key=True, help_text="Primary Key (Manually assigned for each role type)")
    rlm_name = models.CharField(max_length=50, unique=True, help_text="Role Type Name (e.g., Client Partner, Delivery Manager, PU Spoc)")

    def __str__(self):
        return self.rlm_name
    
    class Meta:
        managed = True
        db_table = 'rolemaster'
