from django.db import models


class ClientManagerMaster(models.Model):
    # Fields based on the "ClientMangerMaster(clm)" table definition and FE fields.
    cmm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Client Manager)")
    cmm_clm_id = models.ForeignKey(
        'ClientMaster', 
        on_delete=models.CASCADE, 
        related_name='client_managers',
        db_column="cmm_clm_id",
        help_text="Foreign Key from ClientMaster table"
    )
    cmm_name = models.CharField(max_length=50, help_text="Client Manager Name")
    cmm_email = models.EmailField(unique=True, help_text="Client Manager Email Address")
    cmm_phone = models.CharField(max_length=20, help_text="Client Manager Phone Number (e.g., +91-9988770098)")
    cmm_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_clientmanager",
        help_text="Reference to Location Master Table"
    )
    cmm_isactive = models.BooleanField(default=True, help_text="Is Client Manager Active Now")
    cmm_insertby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='inserted_client_managers',
        help_text="User ID (Employee) who inserted this record"
    )
    cmm_updateby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='updated_client_managers',
        help_text="User ID (Employee) who last updated this record"
    )

    def __str__(self):
        return f"{self.cmm_name} ({self.cmm_email})"
    
    class Meta:
        managed = True
        db_table = 'clientmanagermaster'
