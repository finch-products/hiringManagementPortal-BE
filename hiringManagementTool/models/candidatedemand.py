from django.db import models
from hiringManagementTool.models.candidates import CandidateMaster
from hiringManagementTool.models.demands import OpenDemand
from hiringManagementTool.models.candidatestatus import CandidateStatusMaster

class CandidateDemandLink(models.Model):
    cdl_id = models.AutoField(primary_key=True, help_text="Unique Candidate Demand Link ID (Auto-generated)")

    cdl_cdm_id = models.ForeignKey(
        'CandidateMaster',
        on_delete=models.CASCADE,
        related_name="demand_links",
        db_column="cdl_cdm_id",
        to_field= "cdm_id",
        help_text="Reference to Candidate Master"
    )

    cdl_dem_id = models.ForeignKey(
        'OpenDemand',
        on_delete=models.CASCADE,
        related_name="candidate_links",
        db_column="cdl_dem_id",
        to_field="dem_id",
        help_text="Reference to Demand Table"
    )

    cdl_csm_id = models.ForeignKey(
        'CandidateStatusMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_candidates",
        db_column="cdl_csm_id",
        help_text="Reference to Candidate Status Master"
    )

    cdl_joiningdate = models.DateField(null=True,help_text="Future Joining Date of Candidate")
    
    cdl_insertdate = models.DateTimeField(auto_now_add=True, help_text="Record Creation Timestamp")

    def __str__(self):
        return f"CDL-{self.cdl_id} | Candidate: {self.cdl_cdm.cdm_name} | Demand ID: {self.cdl_dem.dem_id}"
    
    class Meta:
        managed = True
        db_table = 'candidatedemandlink'