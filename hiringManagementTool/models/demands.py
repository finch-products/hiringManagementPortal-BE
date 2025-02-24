from django.db import models
from .clients import ClientMaster
from .locations import LocationMaster
from .lobs import LOBMaster
from .departments import InternalDepartmentMaster
from .demandstatus import DemandStatusMaster
from .employees import EmployeeMaster
from datetime import datetime
from django.db.models import Max

class OpenDemand(models.Model):
    dem_id = models.CharField(
        max_length=50, 
        primary_key=True, 
        editable=False, 
        help_text="Formatted Primary Key (Auto-generated for Demand Entry) dem_ddmmyyyy_01"
    )
    dem_ctoolnumber = models.CharField(max_length=50, help_text="Client Tool Number from Client")
    dem_ctooldate = models.DateTimeField(help_text="Requirement/Demand Date from Client")
    position_name = models.TextField(blank=True, null=True, help_text="Name of the position")
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

    def save(self, *args, **kwargs):
     if not self.dem_id:
        today = datetime.today().strftime('%d%m%Y')
        
        # Get the highest numeric suffix for today's date
        latest_entry = OpenDemand.objects.filter(dem_id__startswith=f"dem_{today}_").aggregate(
            max_id=Max("dem_id")
        )

        if latest_entry["max_id"]:
            try:
                last_number = int(latest_entry["max_id"].rsplit("_", 1)[-1])  # Extract numeric suffix
                new_number = last_number + 1
            except ValueError:
                new_number = 1  # Handle unexpected format issues
        else:
            new_number = 1  # Start numbering from 1

        self.dem_id = f"dem_{today}_{new_number}"  # No zero-padding, keeps numeric order

     super().save(*args, **kwargs)

    def __str__(self):
        return f"Demand {self.dem_ctoolnumber} - {self.dem_positions} Positions"
    
    class Meta:
        managed = True
        db_table = 'opendemand'



# Signal to track demand status changes and store histor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

@receiver(post_save, sender=OpenDemand)
def track_status_change(sender, instance, created, **kwargs):
    """Tracks changes to OpenDemand and logs them in DemandHistory"""
    from .demandhistory import DemandHistory
    print(f"🔍 Signal Triggered for Demand ID: {instance.pk}")  # Debugging Log

    # Fetch last history record for this demand (to check previous data)
    last_history = DemandHistory.objects.filter(dhs_dem_id=instance.dem_id).order_by('-dhs_dsm_insertdate').first()
    
    tracked_fields = [
        'dem_ctoolnumber', 'dem_ctooldate', 'position_name', 'dem_clm_id', 'dem_lcm_id', 'dem_validtill', 'dem_skillset', 'dem_lob_id',
        'dem_idm_id', 'dem_dsm_id', 'dem_positions', 'dem_rrnumber', 'dem_jrnumber', 'dem_rrgade', 'dem_isactive',
        'dem_gcblevel', 'dem_assigned_to', 'dem_jd', 'dem_comment', 'dem_isreopened',
        'dem_insertdate', 'dem_insertby', 'dem_updatedate', 'dem_updateby'
        ]
    
    # Fetch the previous instance of OpenDemand (current state before update)
    """try:
        previous = OpenDemand.objects.get(pk=instance.pk)
    except OpenDemand.DoesNotExist:
        previous = None"""

    if created:
        print("✅ New Demand Created - Logging Initial State")

        # Store initial state for every tracked field
        for field in tracked_fields:
            field_value = getattr(instance, field, None)

            DemandHistory.objects.create(
                dhs_dem_id=instance,
                dhs_dsm_id=instance.dem_dsm_id,
                dhs_fromdata="None",  # No previous record since it's newly created
                dhs_todata=str(field_value) if field_value is not None else "None",
                dhs_dsm_insertdate=now(),
                dhs_log_msg=f"Initial state for {field.replace('_', ' ').title()} set to {field_value}",
            )

        return  # Exit after handling new demand creation
    
    changes_detected = False
     # Fields to track (Add/remove fields as needed) removed dem_id as it would be unique
    
    
    for field in tracked_fields:
             # Fetch the last recorded value for this specific field : dhs_log_msg__icontains=field.replace('_', ' ')
            last_field_history = DemandHistory.objects.filter(dhs_dem_id=instance.dem_id, dhs_log_msg__icontains=field.replace('_', ' ')).order_by('-dhs_dsm_insertdate').first()
            old_value = last_field_history.dhs_todata if last_history else None
            new_value = getattr(instance, field,None)

            if old_value != str(new_value):
                changes_detected = True  # Mark as changed

                print(f"⚡ Change Detected: {field} changed from {old_value} → {new_value}")

            # Store a history entry for each changed field
                DemandHistory.objects.create(
                    dhs_dem_id=instance,
                    dhs_dsm_id=instance.dem_dsm_id,
                    dhs_fromdata=str(old_value) ,
                    dhs_todata=str(new_value) ,
                    dhs_dsm_insertdate=now(),
                    dhs_log_msg=f"{field.replace('_', ' ').title()} changed from {old_value} to {new_value}",
                    )

    if not changes_detected:
            print("✅ No Changes Detected, No History Entry Created")
