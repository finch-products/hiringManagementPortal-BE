from django.db import models
from django.utils.timezone import now

# ============================
# Master Tables (Models)
# ============================
#employee master table
class EmployeeMaster(models.Model):
    emp_id = models.AutoField(primary_key=True, help_text="Unique ID for contact")
    emp_uniqueid = models.CharField(max_length=255, unique=True, help_text="Unique ID for employee")
    emp_name = models.CharField(max_length=255, help_text="First name of the employee")
    emp_emailid = models.EmailField(unique=True, help_text="Email ID of the employee")
    emp_phone = models.CharField(max_length=20, help_text="Mobile or phone number of the employee")
    emp_location = models.CharField(max_length=255, help_text="Location of the employee")
    emp_rlm_id = models.IntegerField(help_text="Role ID associated with the employee")
    isActive = models.BooleanField(default=True, help_text="Indicates if the employee is active or not")

    def __str__(self):
        return self.emp_name
    
class ClientMaster(models.Model):
    # Fields based on the "clientmaster" table definition and FE fields.
    clm_id = models.CharField(max_length=50, default="Not provided")  # Choose an appropriate default value
    clm_name = models.CharField(max_length=255)
    clm_name = models.CharField(max_length=50)
    clm_manager_name = models.CharField(max_length=50)
    clm_email = models.EmailField(help_text="Client Email")
    clm_phone = models.CharField(max_length=15)
    clm_address = models.CharField(max_length=500, default="Not Provided")
    clm_location = models.CharField(max_length=100)
    clm_insertdate = models.DateTimeField(default=now)
    clm_updatedate = models.DateTimeField(auto_now=True)
    clm_IsActive = models.BooleanField(default=True)
    clm_department = models.CharField(max_length=100)
    clm_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="clm_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    clm_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="clm_updated_record_by",
        help_text="Reference to the employee who last updated this record")
    def _str_(self):
        return self.client_name


class ClientManagerMaster(models.Model):
    # Fields based on the "ClientMangerMaster(clm)" table definition and FE fields.
    cmm_clientId = models.ForeignKey(ClientMaster, on_delete=models.CASCADE,
                                       help_text="Reference to the Client Master")
    cmm_name = models.CharField(max_length=100)
    cmm_email = models.EmailField(help_text="Client Manager Email")
    cmm_phone = models.CharField(max_length=15)
    cmm_location = models.CharField(max_length=100)
    cmm_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="cmm_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    cmm_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="cmm_updated_record_by",
        help_text="Reference to the employee who last updated this record")

    def _str_(self):
        return self.cmm_name

class LocationMaster(models.Model):
    lcm_name = models.CharField(max_length=100)
    lcm_state = models.CharField(max_length=100)
    lcm_country = models.CharField(max_length=100)
    lcm_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="lcm_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    lcm_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="lcm_updated_record_by",
        help_text="Reference to the employee who last updated this record")

    def _str_(self):
        return self.location_name

class LOBMaster(models.Model):
    lob_name = models.CharField(max_length=100)
    lob_description = models.TextField(blank=True, null=True, help_text="LOB Description")
    lob_clientPartner = models.CharField(max_length=255, default="Not Provided")
    lob_delivery_manager = models.CharField(max_length=100)
    lob_client_partner = models.CharField(max_length=100)
    lob_insertdate = models.DateTimeField(default=now)  # Sets default for existing records
    lob_updatedate = models.DateTimeField(default=now)
    lob_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="lob_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    lob_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="lob_updated_record_by",
        help_text="Reference to the employee who last updated this record")

    def _str_(self):
        return self.lob_name


class SubUnitMaster(models.Model):
    sum_unitName = models.CharField(max_length=100)
    sum_unitSales = models.CharField(max_length=100)
    sum_unitDelivery = models.CharField(max_length=100)
    sum_unitSolution = models.CharField(max_length=100)
    sum_spoc = models.IntegerField(help_text="Employee ID for SPOC")
    sum_sbuId = models.IntegerField(help_text="SBU ID")
    sum_deliveryManager = models.IntegerField(help_text="Employee ID for Delivery Manager")
    sum_isActive = models.BooleanField(default=True, help_text="Is this Sub Unit active?")
    sum_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="sum_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    sum_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="sum_updated_record_by",
        help_text="Reference to the employee who last updated this record")

    def _str_(self):
        return self.sum_unitName

# ============================
# Demand Table Model
# ============================

class OpenDemand(models.Model):
    # Mapping DemandTable fields to model fields with foreign key references where applicable.
    
    # FE Field: Ctool number (dem_ctoolnumber)
    dem_ctoolnumber = models.CharField(max_length=50, unique=True, help_text="Client Tool Number")
    
    # FE Field: ctool date (dem_ctooldate)
    dem_ctooldate = models.DateField(help_text="Requirement Date from Client")
    
    # FE Field: Client (dropdown - service call)
    dem_cmm_id = models.ForeignKey(ClientManagerMaster, on_delete=models.CASCADE, null=True, blank=True,help_text="Reference to Client Master")
    
    # FE Field: Client Manager (dropdown - service call)
    dem_clm_id = models.ForeignKey(ClientMaster, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to Client Master")

    # FE Field: Location (from LocationMaster) and Poition location (if different, you can add a separate text field)
    # Here we use the LocationMaster reference.
    dem_lcm_id = models.ForeignKey(LocationMaster, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to Location Master")

    
    # If you need to capture a separate position location (e.g. a specific site for the position),
    # you can add an extra CharField:
    dem_positionlocation = models.CharField(max_length=100, help_text="Position Location", blank=True, null=True)
    
    # FE Field: Valid till (change the field name to tentative_required_by) → (dem_validtill)
    dem_validtill = models.DateField(help_text="Requirement Closing Date")
    
    # FE Field: Skillset (dem_skillset)
    dem_skillset = models.TextField(max_length=500, help_text="Multiple skillsets separated by commas")
    
    # FE Field: LOB (dropdown and service call) → (dem_lob_id)
    dem_lob_id = models.ForeignKey(LOBMaster, on_delete=models.CASCADE, null=True, blank=True, help_text="Reference to LOB Master")
    
    # FE Field: Sub unit (dropdown - service call) → (dem_sub_id)
    dem_sub_id = models.ForeignKey(SubUnitMaster, on_delete=models.CASCADE, default=1)  # Use a valid ID


    # FE Field: Positions (dem_positions)
    dem_positions = models.IntegerField(help_text="Number of Positions Required")
    
    # FE Field: Rr number (dem_rrnumber)
    dem_rrnumber = models.CharField(max_length=100, default="TEMP-001", help_text="Request Number")  # Replace with a meaningful default

    # FE Field: rr grade (dem_rrgade)
    dem_rrgrade = models.CharField(max_length=50, help_text="RR Grade Entry")
    
    # FE Field: GCB level (dem_gcblevel)
    dem_gcblevel = models.CharField(max_length=50, help_text="GCB Level Entry")
    
    # FE Field: Job description (dem_jd)
    dem_jd = models.FileField(upload_to='job_descriptions/', help_text="Job Description File")
    
    # FE Field: Comment (dem_comment)
    dem_comment = models.TextField(blank=True, null=True, help_text="Additional Comments")
    dem_insertedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="dem_inserted_record_by",
        help_text="Reference to the employee who inserted this record")
    dem_updatedby = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, related_name="dem_updated_record_by",
        help_text="Reference to the employee who last updated this record")

    def _str_(self):
        return f"{self.ctool_number} - {self.client_manager.cmm_name}"
    
    

