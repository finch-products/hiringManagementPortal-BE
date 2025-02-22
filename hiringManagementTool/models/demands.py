from django.db import models
from .clients import ClientMaster
from .locations import LocationMaster
from .lobs import LOBMaster
from .departments import InternalDepartmentMaster
from .demandstatus import DemandStatusMaster
from .employees import EmployeeMaster

class OpenDemand(models.Model):
    dem_id = models.AutoField(primary_key=True, help_text="Primary Key (Auto-generated for Demand Entry)")
    dem_ctoolnumber = models.CharField(max_length=50, help_text="Client Tool Number from Client")
    dem_ctooldate = models.DateTimeField(help_text="Requirement/Demand Date from Client")
    position_name = models.TextField(blank=True, null=True, help_text="Name of the position")
    # dem_cmm_id = models.ForeignKey(
    #     'ClientManagerMaster',
    #     on_delete=models.CASCADE,
    #     related_name="demands",
    #     db_column="dem_cmm_id",
    #     help_text="Reference to Client Manager"
    # )

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