# models.py for candidate-demand-history

from django.db import models
from .demands import OpenDemand
from .candidates import CandidateMaster
from .candidatestatus import CandidateStatusMaster


class CandidateDemandHistory(models.Model):
    cdh_id = models.AutoField(primary_key=True, help_text="Unique Candidate Demand History ID (Auto-generated)")

    cdh_cdm_id = models.ForeignKey(
        'CandidateMaster',  # Ensure this is the correct referenced model
        on_delete=models.CASCADE,
        related_name="candidate_links",
        help_text="Reference to Open Demand",
        db_column="cdh_cdm_id"  # Explicitly define the column name
    )


    cdh_dem_id = models.ForeignKey(
        'OpenDemand',  # Ensure this is the correct referenced model
        on_delete=models.CASCADE,
        related_name="candidate_links",
        help_text="Reference to Open Demand",
        db_column="cdh_dem_id"  # Explicitly define the column name
    )


    cdh_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_history",
        help_text="Reference to Candidate Status Master",
        db_column="cdh_csm_id"
    )

    cdh_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")
    
    cdh_fromdata = models.JSONField(blank=True, null=True, help_text="Old Value/Data before change")
    cdh_todata = models.JSONField(blank=True, null=True, help_text="New Value/Data after change")

    def _str_(self):
        return f"CDH-{self.cdh_id} | Candidate: {self.cdh_cdm.cdm_name} | Demand ID: {self.cdh_dem.dem_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatedemandhistory'