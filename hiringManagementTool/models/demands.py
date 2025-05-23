import re
from django.db import models
from .clients import ClientMaster
from .locations import LocationMaster
from .lobs import LOBMaster
from .departments import InternalDepartmentMaster
from .demandstatus import DemandStatusMaster
from .employees import EmployeeMaster
from datetime import datetime
from django.db.models import Max
import json

class OpenDemand(models.Model):
    dem_id = models.CharField(
        max_length=50, 
        primary_key=True, 
        editable=False, 
        help_text="Formatted Primary Key (Auto-generated for Demand Entry) dem_ddmmyyyy_01"
    )
    dem_ctoolnumber = models.CharField(max_length=50, blank=True, null=True,help_text="Client Tool Number from Client")
    dem_ctooldate = models.DateTimeField(blank=True, null=True,help_text="Requirement/Demand Date from Client")
    dem_position_name = models.TextField(blank=True, null=True, help_text="Name of the position")
    # dem_cmm_id = models.ForeignKey(
    #     'ClientManagerMaster',
    #     on_delete=models.CASCADE,
    #     related_name="demands",
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
         null=True,  # Allows NULL values in the database
         blank=True,
        related_name="location_demands",
        db_column="dem_lcm_id",
        help_text="Reference to Location Master Table"
    )

    dem_validtill = models.DateTimeField(blank=True, null=True,help_text="Requirement/Demand Closing Date")
    dem_skillset = models.TextField(blank=True, null=True,help_text="Multiple skillsets separated by commas")

    dem_lob_id = models.ForeignKey(
        'LOBMaster',
        on_delete=models.SET_NULL,
        null=True, # Allows NULL values in the database
         #blank=True,
        related_name="lob_demands",
        db_column="dem_lob_id",
        help_text="Reference to LOB Master Table"
    )

    dem_idm_id = models.ForeignKey(
        'InternalDepartmentMaster',
        on_delete=models.SET_NULL,
         null=True,  # Allows NULL values in the database
         blank=True,
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

    dem_positions = models.IntegerField(#blank=True, null=True,
                                        default=0,
                                        help_text="Number of Positions Required")
    dem_rrnumber = models.CharField(blank=True, null=True,max_length=50, help_text="Request Number")
    dem_jrnumber = models.TextField(blank=True, null=True, help_text="JR Number if External")
    dem_rrgade = models.CharField(max_length=100, blank=True, null=True, help_text="RR Grade Entry")
    dem_gcblevel = models.CharField(max_length=100, blank=True, null=True, help_text="GCB Level Entry")

    dem_jd = models.FileField(upload_to="jd_files/", blank=True, null=True, help_text="Job Description File Upload")
    dem_comment = models.TextField(blank=True, null=True, help_text="Comment Entry")
    
    dem_isreopened = models.BooleanField(blank=True, null=True,default=False, help_text="Indicates if Demand is Reopened (1 = Reopened, 0 = New)")
    dem_isactive = models.BooleanField(blank=True, null=True,default=True, help_text="Indicates if Demand is Active (1 = Active, 0 = Inactive)")
    dem_insertdate = models.DateTimeField(blank=True, null=True,auto_now_add=True, help_text="Record Creation Timestamp")
    dem_insertby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="demands_inserted",
        help_text="User ID (Employee) who inserted this record"
    )

    dem_updatedate = models.DateTimeField(blank=True, null=True,auto_now=True, help_text="Record Last Updated Timestamp")
    dem_updateby = models.ForeignKey(
        'EmployeeMaster',
        on_delete=models.SET_NULL,
        null=True,
        related_name="demands_updated",
        help_text="User ID (Employee) who last updated this record"
    )
    dem_position_location = models.JSONField(default=list, blank=True,null=True)  # New field for multiple locations
    dem_mandatoryskill = models.TextField(blank=True, null=True,help_text="Multiple mandatory skillsets separated by commas")

    def save(self, *args, **kwargs):
        if not self.dem_id:
            today = datetime.today().strftime('%d%m%Y')

            # Fetch all demand IDs for today and extract numeric suffixes
            existing_ids = OpenDemand.objects.filter(dem_id__startswith=f"dem_{today}_").values_list("dem_id", flat=True)

            # Extract numeric suffixes safely
            numeric_suffixes = [int(re.search(r"_(\d+)$", dem_id).group(1)) for dem_id in existing_ids if re.search(r"_(\d+)$", dem_id)]

            new_number = max(numeric_suffixes, default=0) + 1  # Get the next number

            self.dem_id = f"dem_{today}_{new_number}"

        # Ensure dem_position_location is a valid JSON list
        if isinstance(self.dem_position_location, str):
            try:
                self.dem_position_location = json.loads(self.dem_position_location)
            except json.JSONDecodeError:
                self.dem_position_location = []

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Demand {self.dem_ctoolnumber} - {self.dem_positions} Positions"

    class Meta:
        managed = True
        db_table = "opendemand"

    # def save(self, *args, **kwargs):
    #  if not self.dem_id:
    #     today = datetime.today().strftime('%d%m%Y')
        
    #     latest_entry = OpenDemand.objects.filter(dem_id__startswith=f"dem_{today}_").aggregate(
    #         max_id=Max("dem_id")
    #     )

    #     if latest_entry["max_id"]:
    #         try:
    #             last_number = int(latest_entry["max_id"].rsplit("_", 1)[-1]) 
    #             new_number = last_number + 1
    #         except ValueError:
    #             new_number = 1 
    #     else:
    #         new_number = 1 

    #     self.dem_id = f"dem_{today}_{new_number}"

    #  super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Demand {self.dem_ctoolnumber} - {self.dem_positions} Positions"
    
    # class Meta:
    #     managed = True
    #     db_table = 'opendemand'

