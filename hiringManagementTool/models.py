from django.db import models
from django.utils.timezone import now

# ============================
# Master Tables (Models)
# ============================
#employee master table
class EmployeeMaster(models.Model):
    emp_id = models.AutoField(primary_key=True, help_text="Unique ID for contact (Auto-generated)")
    emp_uniqueid = models.CharField(max_length=50, unique=True, help_text="Unique ID manually inserted from UI")
    emp_name = models.CharField(max_length=50, help_text="First name of the employee")
    emp_email = models.EmailField(unique=True, help_text="Email ID of the employee")
    emp_phone = models.CharField(max_length=20, help_text="Mobile or phone number (e.g., +91-9988770098)")
    emp_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_employee",
        db_column="emp_lcm_id",
        help_text="Reference to Location Master Table"
    )
    
    emp_rlm_id = models.ForeignKey(
        'RoleMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='role_employee',
        db_column="emp_rlm_id",
        help_text="Role ID associated with the employee"
    )
    
    emp_isactive = models.BooleanField(default=True, help_text="Indicates if the employee is active or not")
    emp_keyword = models.TextField(help_text="Keywords to find specific requirements")
    emp_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    emp_insertby = models.IntegerField(help_text="User ID who inserted the record (from connection table)")
    emp_updatedate = models.DateTimeField(auto_now=True, help_text="Last updated timestamp")
    emp_updateby = models.IntegerField(null=True, blank=True, help_text="User ID who updated the record")

    def __str__(self):
        return self.emp_name
    
    class Meta:
        managed = True
        db_table = 'employeemaster'
    
class ClientMaster(models.Model):
    # Fields based on the "clientmaster" table definition and FE fields.
    clm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto Increment)")
    clm_clientid = models.CharField(max_length=50, unique=True, help_text="Client unique ID (internal, manually inserted)")
    clm_name = models.CharField(max_length=50, help_text="Client Name")
    clm_managername = models.CharField(max_length=50, help_text="Client Manager Name")
    clm_clientemail = models.EmailField(unique=True, help_text="Client Email Address")
    clm_clientphone = models.CharField(max_length=20, help_text="Client Phone Number (e.g., +91-9988770098)")
    clm_address = models.TextField(help_text="Client Full Address")
    clm_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
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

class LOBMaster(models.Model):
    lob_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for LOB)")
    lob_name = models.CharField(max_length=50, help_text="LOB Name")
    lob_description = models.TextField(help_text="LOB Description")
    
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

# ============================
# Demand Table Model
# ============================

class OpenDemand(models.Model):
    dem_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Demand Entry)")
    dem_ctoolnumber = models.CharField(max_length=50, help_text="Client Tool Number from Client")
    dem_ctooldate = models.DateTimeField(help_text="Requirement/Demand Date from Client")

    dem_cmm_id = models.ForeignKey(
        'ClientManagerMaster',
        on_delete=models.CASCADE,
        related_name="demands",
        db_column="dem_cmm_id",
        help_text="Reference to Client Manager"
    )

    dem_clm_id = models.ForeignKey(
        'ClientMaster',
        on_delete=models.CASCADE,
        related_name="client_demands",
        db_column="dem_clm_id",
        help_text="Reference to Client Master Table"
    )

    dem_lcm_id = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_demands",
        db_column="dem_lcm_id",
        help_text="Reference to Location Master Table"
    )

    dem_validtill = models.DateTimeField(help_text="Requirement/Demand Closing Date")
    dem_skillset = models.TextField(help_text="Multiple skillsets separated by commas")

    dem_lob_id = models.ForeignKey(
        'LOBMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="lob_demands",
        db_column="dem_lob_id",
        help_text="Reference to LOB Master Table"
    )

    dem_idm_id = models.ForeignKey(
        'InternalDepartmentMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="idm_demands",
        db_column="dem_idm_id",
        help_text="Reference to Internal Department Master Table"
    )

    dem_dsm_id = models.ForeignKey(
        'DemandStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="dsm_demands",
        db_column="dem_dsm_id",
        help_text="Reference to Internal Department Master Table"
    )

    dem_positions = models.IntegerField(help_text="Number of Positions Required")
    dem_rrnumber = models.CharField(max_length=50, help_text="Request Number")
    dem_jrnumber = models.TextField(blank=True, null=True, help_text="JR Number if External")
    dem_rrgade = models.CharField(max_length=100, blank=True, null=True, help_text="RR Grade Entry")
    dem_gcblevel = models.CharField(max_length=100, blank=True, null=True, help_text="GCB Level Entry")

    dem_jd = models.FileField(upload_to="uploads/jd_files/", blank=True, null=True, help_text="Job Description File Upload")
    dem_comment = models.TextField(blank=True, null=True, help_text="Comment Entry")
    
    dem_isreopened = models.BooleanField(default=False, help_text="Indicates if Demand is Reopened (1 = Reopened, 0 = New)")
    dem_isactive = models.BooleanField(default=True, help_text="Indicates if Demand is Active (1 = Active, 0 = Inactive)")

    dem_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    dem_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="demands_inserted",
        help_text="User ID (Employee) who inserted this record"
    )

    dem_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    dem_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="demands_updated",
        help_text="User ID (Employee) who last updated this record"
    )

    def __str__(self):
        return f"Demand {self.dem_ctoolnumber} - {self.dem_positions} Positions"
    
    class Meta:
        managed = True
        db_table = 'opendemand'
    
class DemandStatusMaster(models.Model):
    dsm_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Demand Status)")
    dsm_code = models.CharField(max_length=50, unique=True, help_text="Status Name (e.g., Open, JD Received, Rejected, etc.)")
    dsm_description = models.TextField(blank=True, null=True, help_text="Detailed description of the status")
    dsm_sortid = models.IntegerField(help_text="Sorting order for statuses")

    dsm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    dsm_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_inserted",
        help_text="User ID (Employee) who created this status"
    )

    dsm_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    dsm_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_updated",
        help_text="User ID (Employee) who last updated this status"
    )

    dsm_isclosed = models.BooleanField(default=False, help_text="Indicates if the status is treated as closed")

    def __str__(self):
        return f"{self.dsm_code} - {'Closed' if self.dsm_isclosed else 'Open'}"
    
    class Meta:
        managed = True
        db_table = 'demandstatusmaster'
    
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

class CandidateMaster(models.Model):
    cdm_id = models.AutoField(primary_key=True, help_text="Unique Candidate ID (Auto-generated)")
    cdm_emp_id = models.IntegerField(null=True, blank=True, help_text="Employee ID for tracking (if internal)")
    cdm_name = models.CharField(max_length=50, help_text="Full name of the candidate")
    cdm_email = models.EmailField(unique=True, help_text="Candidate email (must be unique)")
    cdm_phone = models.CharField(max_length=20, help_text="Candidate phone number")
    cdm_location = models.ForeignKey(
        'LocationMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="location_candidate",
        help_text="Reference to Location Master Table"
    )
    cdm_profile = models.FileField(upload_to="uploads/candidate_profiles/", blank=True, null=True, help_text="Candidate profile file (resume)")
    cdm_description = models.TextField(blank=True, null=True, help_text="Cover letter or profile description")
    
    cdm_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidate_references",
        db_column="cdm_csm_id",
        help_text="Reference to another candidate (if applicable)"
    )

    cdm_keywords = models.TextField(blank=True, null=True, help_text="Technical keywords associated with the candidate")

    cdm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    cdm_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates_inserted",
        help_text="User ID (Employee) who created this record"
    )

    cdm_updatedate = models.DateTimeField(auto_now=True, help_text="Record Last Updated Timestamp")
    cdm_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates_updated",
        help_text="User ID (Employee) who last updated this record"
    )

    cdm_isinternal = models.BooleanField(default=False, help_text="1 for internal candidate, 0 for external")
    cdm_isactive = models.BooleanField(default=True, help_text="1 for active, 0 for inactive")

    def __str__(self):
        return f"{self.cdm_name} ({'Internal' if self.cdm_isinternal else 'External'})"
    
    class Meta:
        managed = True
        db_table = 'candidatemaster'
    
class CandidateStatusMaster(models.Model):
    csm_id = models.AutoField(primary_key=True, help_text="Unique Candidate Status ID (Auto-generated)")
    csm_code = models.CharField(max_length=50, unique=True, help_text="Candidate Status Name (e.g., Open, L1 Interview Scheduled, Selected, Rejected, On Hold, etc.)")
    csm_description = models.TextField(blank=True, null=True, help_text="Detailed description of the status")
    csm_sortid = models.IntegerField(help_text="Sorting order for statuses")

    csm_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    csm_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_created",
        help_text="User ID (Employee) who created this status"
    )

    def __str__(self):
        return f"{self.csm_code} - Status ID: {self.csm_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatestatusmaster'

class CandidateDemandHistory(models.Model):
    cdh_id = models.AutoField(primary_key=True, help_text="Unique Candidate Demand History ID (Auto-generated)")

    cdh_cdm_id = models.ForeignKey(
        'CandidateMaster',
        on_delete=models.CASCADE,
        related_name="demand_history",
        help_text="Reference to Candidate Master"
    )

    cdh_dem_id = models.ForeignKey(
        'OpenDemand',
        on_delete=models.CASCADE,
        related_name="candidate_demand_history",
        help_text="Reference to Demand Table"
    )

    cdh_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_history",
        help_text="Reference to Candidate Status Master"
    )

    cdh_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    
    cdh_fromdata = models.JSONField(blank=True, null=True, help_text="Old Value/Data before change")
    cdh_todata = models.JSONField(blank=True, null=True, help_text="New Value/Data after change")

    def __str__(self):
        return f"CDH-{self.cdh_id} | Candidate: {self.cdh_cdm.cdm_name} | Demand ID: {self.cdh_dem.dem_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatedemandhistory'

class CandidateDemandLink(models.Model):
    cdl_id = models.AutoField(primary_key=True, help_text="Unique Candidate Demand Link ID (Auto-generated)")

    cdl_cdm_id = models.ForeignKey(
        'CandidateMaster',
        on_delete=models.CASCADE,
        related_name="demand_links",
        help_text="Reference to Candidate Master"
    )

    cdl_dem_id = models.ForeignKey(
        'OpenDemand',
        on_delete=models.CASCADE,
        related_name="candidate_links",
        help_text="Reference to Demand Table"
    )

    cdl_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_candidates",
        help_text="Reference to Candidate Status Master"
    )

    cdl_joiningdate = models.DateField(help_text="Future Joining Date of Candidate")
    
    cdl_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")

    def __str__(self):
        return f"CDL-{self.cdl_id} | Candidate: {self.cdl_cdm.cdm_name} | Demand ID: {self.cdl_dem.dem_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatedemandlink'

class RoleMaster(models.Model):
    rlm_id = models.IntegerField(primary_key=True, help_text="Primary Key (Manually assigned for each role type)")
    rlm_name = models.CharField(max_length=50, unique=True, help_text="Role Type Name (e.g., Client Partner, Delivery Manager, PU Spoc)")

    def __str__(self):
        return self.rlm_name
    
    class Meta:
        managed = True
        db_table = 'rolemaster'


