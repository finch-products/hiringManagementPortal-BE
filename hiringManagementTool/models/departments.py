from django.utils.timezone import now
from django.db import models


class InternalDepartmentMaster(models.Model):
    idm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-incremented for Internal Department Master)")
    idm_unitname = models.CharField(max_length=50, help_text="Name of the Internal Department Name")
    idm_unitsales = models.CharField(max_length=50, help_text="Sales associated with the Internal Department")
    idm_unitdelivery = models.CharField(max_length=50, help_text="Delivery associated with the Internal Department")
    idm_unitsolution = models.CharField(max_length=50, help_text="Solution associated with the Internal Department")

    idm_spoc_id = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="employee_master",
        db_column="idm_spoc_id",
        help_text="Single Point of Contact (SPOC) from Employee Master"
    )

    idm_deliverymanager_id = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="internaldepartment_delivery_manager",
         db_column="idm_deliverymanager_id",
        help_text="Delivery Manager from Employee Master"
    )

    idm_isactive = models.BooleanField(default=True, help_text="Indicates if the Internal Department is currently active")

    idm_insertdate = models.DateTimeField(default=now, help_text="Timestamp when the Internal Department record was created")
    idm_updatedate = models.DateTimeField(default=now, help_text="Timestamp when the Internal Department record was last updated")

    idm_insertby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="internaldepartment_inserted_records",
        help_text="Reference to the employee who inserted this record"
    )

    idm_updateby = models.ForeignKey(
        'EmployeeMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="internaldepartment_updated_records",
        help_text="Reference to the employee who last updated this record"
    )

    def __str__(self):
        return self.sum_unitName
    
    class Meta:
        managed = True
        db_table = 'internaldepartmentmaster'