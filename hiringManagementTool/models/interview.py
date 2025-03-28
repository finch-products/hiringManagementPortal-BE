from django.db import models
from hiringManagementTool.models.candidatedemand import CandidateDemandLink

class InterviewSchedulingTable(models.Model):
    ist_id = models.AutoField(primary_key=True)
    ist_cdl = models.ForeignKey(CandidateDemandLink, on_delete=models.CASCADE)
    ist_interviewdate = models.DateField()
    ist_interviewtime = models.TimeField()
    ist_interviewtype = models.CharField(max_length=50, choices=[
        ('Phone', 'Phone'),
        ('Video', 'Video'),
        ('On-site', 'On-site'),
        ('Other', 'Other'),
    ])
    ist_interviewround = models.IntegerField()
    ist_interviewername = models.CharField(max_length=255)
    ist_intervieweremail = models.CharField(max_length=255)
    ist_interviewstatus = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),
    ])
    ist_remarks = models.TextField(blank=True, null=True)
    ist_createdate = models.DateTimeField(auto_now_add=True)
    ist_updatedate= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Interview {self.ist_id} - Round {self.ist_interviewround}"
    
    class Meta:
        managed = True
        db_table = 'interviewschedulingtable'
