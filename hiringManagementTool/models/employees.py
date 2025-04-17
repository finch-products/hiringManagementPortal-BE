from django.db import models
from hiringManagementTool.models.locations import LocationMaster
from hiringManagementTool.models.roles import RoleMaster
from datetime import datetime
from django.db.models import Max
import re

class EmployeeMaster(models.Model):
    emp_id = models.CharField(
        primary_key=True, 
        max_length=50, 
        editable=False, 
        help_text="Auto-generated ID in format emp_ddmmyyyy_1"
    )
    emp_uniqueid = models.CharField(max_length=50, unique=True, help_text="Unique ID manually inserted from UI")
    emp_name = models.CharField(max_length=50, help_text="First name of the employee")
    emp_email = models.EmailField(unique=True, help_text="Email ID of the employee")
    emp_phone = models.CharField(max_length=20, help_text="Mobile or phone number (e.g., +91-9988770098)", null=True, blank=True)
    emp_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="location_employee",
        db_column="emp_lcm_id",
        help_text="Reference to Location Master Table"
    )
    
    emp_rlm_id = models.ForeignKey(
        'RoleMaster', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='role_employee',
        db_column="emp_rlm_id",
        help_text="Role ID associated with the employee"
    )
    emp_image = models.ImageField(
    upload_to='employee_images/',
    blank=True,
    null=True,
    help_text="Employee image"
    )
    emp_isactive = models.BooleanField(default=True, help_text="Indicates if the employee is active or not")
    emp_keyword = models.TextField(help_text="Keywords to find specific requirements", null=True, blank=True)
    emp_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    emp_insertby = models.CharField( max_length=50,help_text="User ID who inserted the record (from connection table)")
    emp_updatedate = models.DateTimeField(auto_now=True, help_text="Last updated timestamp")
    emp_updateby = models.CharField(null=True,  max_length=50, blank=True, help_text="User ID who updated the record")

    def save(self, *args, **kwargs):
        if not self.emp_id:
            all_ids = EmployeeMaster.objects.values_list('emp_id', flat=True)

            max_number = 0
            for eid in all_ids:
                try:
                    if eid.startswith("emp_"):
                        num = int(eid.split("_")[1])
                        if num > max_number:
                            max_number = num
                except (IndexError, ValueError):
                    continue  # skip malformed ids

            new_number = max_number + 1
            self.emp_id = f"emp_{new_number}"

        super().save(*args, **kwargs)


    def __str__(self):
        return self.emp_name
    
    class Meta:
        managed = True
        db_table = 'employeemaster'
