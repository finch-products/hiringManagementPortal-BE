from django.db import models

class OpenDemand(models.Model):
    ctool_number = models.CharField(max_length=50, unique=True)
    ctool_date = models.DateField()
    client_manager_name = models.CharField(max_length=100)
    client_location = models.CharField(max_length=100)
    position_location = models.CharField(max_length=100)
    tentative_required_by = models.DateField()
    skillset = models.TextField(max_length=500)
    lob_name = models.CharField(max_length=100)
    practice_unit_name = models.CharField(max_length=100)
    job_description = models.FileField(upload_to='job_descriptions/')
    no_of_positions = models.IntegerField()
    rr_numbers = models.CharField(max_length=100)
    rr_grade = models.CharField(max_length=50)
    gcb_level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.ctool_number} - {self.client_manager_name}"


class ClientMaster(models.Model):
    client_name = models.CharField(max_length=50)
    client_manager_name = models.CharField(max_length=50)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)
    client_location = models.CharField(max_length=100)
    client_department = models.CharField(max_length=100)

    def __str__(self):
        return self.client_name
    
class LOBMaster(models.Model):
    lob_name = models.CharField(max_length=100)
    lob_delivery_manager = models.CharField(max_length=100)
    lob_client_partner = models.CharField(max_length=100)

    def __str__(self):
        return self.lob_name
    
class LocationMaster(models.Model):
    location_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.location_name
    
class PracticeUnitMaster(models.Model):
    practice_unit_name = models.CharField(max_length=100)
    practice_unit_sales = models.CharField(max_length=100)
    practice_unit_delivery = models.CharField(max_length=100)
    practice_unit_solution = models.CharField(max_length=100)

    def __str__(self):
        return self.practice_unit_name