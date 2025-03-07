from django.db import models
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.employees import EmployeeMaster


class ClientMaster(models.Model):
    # Fields based on the "clientmaster" table definition and FE fields.
    clm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto Increment)")
    clm_clientid = models.CharField(max_length=50, unique=True,blank=True, 
        null=True,  help_text="Client unique ID (internal, manually inserted)")
    clm_name = models.CharField(max_length=50, help_text="Client Name")
    clm_managername = models.CharField(max_length=50,blank=True,  
        null=True,  help_text="Client Manager Name")
    clm_clientemail = models.EmailField(unique=True,blank=True,  
        null=True, help_text="Client Email Address")
    clm_clientphone = models.CharField(max_length=20,blank=True,  
        null=True, help_text="Client Phone Number (e.g., +91-9988770098)")
    clm_address = models.TextField(blank=True,  
        null=True,help_text="Client Full Address")
    clm_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,   
        related_name="location_client",
        db_column="clm_lcm_id",
        help_text="Reference to Location Master Table"
    )
    clm_isactive = models.BooleanField(default=True, help_text="Is Client Active Now")
    clm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    clm_updatedate = models.DateTimeField(auto_now=True, help_text="Last Updated Timestamp")
    
    clm_insertby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="clm_inserted_records",
        help_text="Reference to the employee who inserted this record"
    )
    clm_updateby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="clm_updated_records",
        help_text="Reference to the employee who last updated this record"
    )
    
    def _str_(self):
        return f"{self.clm_name} ({self.clm_clientId})"
    
    class Meta:
        managed = True
        db_table = 'clientmaster'