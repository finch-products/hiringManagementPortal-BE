from django.db import models
from django.db.models import JSONField
from hiringManagementTool.models.candidatedemand import CandidateDemandLink
from hiringManagementTool.constants import InterviewStatus, InterviewType
import pytz
from datetime import datetime


class InterviewSchedulingTable(models.Model):
    ist_id = models.AutoField(primary_key=True)
    ist_cdl = models.ForeignKey(CandidateDemandLink, on_delete=models.CASCADE)
    ist_interviewdate = models.DateField()
    ist_interview_start_time = models.TimeField(null=True, blank=True)
    ist_interview_end_time = models.TimeField(null=True, blank=True)
    ist_timezone = models.CharField(
        max_length=50,
        default="UTC",
        help_text="Enter the time zone for the interview (e.g., Asia/Kolkata (IST))."
    )
    ist_interviewtype = models.PositiveSmallIntegerField(
        choices=[(interview_type.value, interview_type.name) for interview_type in InterviewType],
        default=InterviewType.VIDEO.value
    )
    ist_interviewround = models.IntegerField()
    ist_interviewers = JSONField(
        default=list,
        blank=True,
        help_text="JSON array of objects, e.g., [{'name': 'John Doe', 'email': 'john.doe@example.com'}]"
    )
    ist_meeting_details = models.TextField(
        blank=False,
        help_text="Stores physical address for ON_SITE, meeting link for VIDEO/GOOGLE_MEET/SKYPE, phone number for PHONE interviews."
    )
    ist_interviewstatus = models.PositiveSmallIntegerField(
        choices=[(status.value, status.name) for status in InterviewStatus],
        default=InterviewStatus.SCHEDULED.value
    )
    ist_remarks = models.TextField(blank=True, null=True)
    ist_createdate = models.DateField(auto_now_add=True)
    ist_updatedate= models.DateField(auto_now=True)

    def __str__(self):
        return f"Interview {self.ist_id} - Round {self.ist_interviewround}"
    
    class Meta:
        managed = True
        db_table = 'interviewschedulingtable'
