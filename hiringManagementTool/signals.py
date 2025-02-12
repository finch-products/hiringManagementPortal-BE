from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OpenDemand, DemandStatusMaster

@receiver(post_save, sender=OpenDemand)
def update_demand_status(sender, instance, created, **kwargs):
    """
    Signal to update the demand status based on whether a JD file is provided.
    """
    if created:  # Only update when a new record is created
        if instance.dem_jd:  # JD is provided
            status_code = "Open"
        else:  # JD is not provided
            status_code = "JD Not Received"
        
        # Fetch the corresponding DemandStatusMaster entry
        try:
            status = DemandStatusMaster.objects.get(dsm_code=status_code)
            instance.dem_dsm_id = status  # Update the dem_dsm_id field
            instance.save(update_fields=['dem_dsm_id'])  # Prevent infinite loop
        except DemandStatusMaster.DoesNotExist:
            print(f"Status '{status_code}' not found in DemandStatusMaster")
