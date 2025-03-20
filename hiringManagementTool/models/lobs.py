from django.db import models


class LOBMaster(models.Model):
    lob_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for LOB)")
    lob_name = models.CharField(max_length=50, help_text="LOB Name")
    lob_description = models.TextField(
        help_text="LOB Description", 
        null=True, 
        blank=True  # Makes it optional
    )
    
    lob_clientpartner = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lob_client_partners",
        help_text="Foreign Key - Employee who is the Client Partner"
    )

    lob_deliverymanager = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lob_delivery_managers",
        help_text="Foreign Key - Employee who is the Delivery Manager"
    )

    lob_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    lob_insertby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lob_inserted_records",
        help_text="User ID (Employee) who inserted this record"
    )

    lob_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    lob_updateby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="lob_updated_records",
        help_text="User ID (Employee) who last updated this record"
    )

    def __str__(self):
        return self.lob_name
    
    class Meta:
        managed = True
        db_table = 'lobmaster'