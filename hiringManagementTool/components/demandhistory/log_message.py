import json
from hiringManagementTool.constants import InterviewStatus, InterviewType

# 1. Demand Field Labels
FIELD_LABELS = {
    "dem_ctoolnumber": "Tool Number",
    "dem_ctooldate": "Tool Date",
    "dem_position_name": "Position Name",
    "dem_clm_id": "Client",
    "dem_lcm_id": "Location",
    "dem_validtill": "Valid Till",
    "dem_skillset": "Skill Set",
    "dem_lob_id": "LOB",
    "dem_idm_id": "Internal Dept",
    "dem_dsm_id": "Status",
    "dem_positions": "Positions",
    "dem_rrnumber": "RR Number",
    "dem_jrnumber": "JR Number",
    "dem_rrgade": "RR Grade",
    "dem_isactive": "Active",
    "dem_gcblevel": "GCB Level",
    "dem_assigned_to": "Assigned To",
    "dem_jd": "Job Description",
    "dem_comment": "Comments",
    "dem_isreopened": "Reopened",
    "dem_insertdate": "Insert Date",
    "dem_insertby_id": "Inserted By",
    "dem_updatedate": "Update Date",
    "dem_updateby_id": "Updated By",
    "dem_position_location": "Position Location",
    "dem_mandatoryskill": "Mandatory Skills",
}

# 2. Interview Labels
INTERVIEW_LABELS = {
    "ist_interviewdate": "Interview Date",
    "ist_interviewtype": "Interview Type",
    "ist_interviewround": "Interview Round",
    "ist_interviewstatus": "Interview Status",
    "ist_remarks": "Remarks",
    "ist_interview_start_time": "Interview Start Time",
    "ist_interview_end_time": "Interview End Time",
    "ist_interviewers": "Interviewers",
    "ist_meeting_details": "Meeting Link",
    "ist_timezone": "Timezone",
}

# 3. Static Templates
STATIC_MESSAGES ={
    "demand_created": "Demand created",
    "jd_attached": lambda jd: f"JD attached: {jd}",
    "jd_updated": lambda jd: f"JD updated to: {jd}",
    "field_updated": lambda label, from_val, to_val: f"Field '{label}' updated from '{from_val}' to '{to_val}'",
    "candidate_linked": lambda name: f"Candidate linked: {name}",
    "status_changed": lambda name, from_s, to_s: f"Status changed for {name} from '{from_s}' to '{to_s}'",
    "interview_scheduled": lambda name, date, round, itype, status, tz, link: (
        f"Interview scheduled for candidate {name} on {date} (Round {round}, Type: {itype}, Status: {status}, "
        f"Timezone: {tz}, Meeting: {link})"
    ),
    "interview_field_updated": lambda label, name, from_val, to_val: (
        f"Field '{label}' updated for {name} from '{from_val}' to '{to_val}'"
    )
}


# 4. Enum Display Utility
def get_enum_name(enum_class, value):
    try:
        return enum_class(int(value)).name.replace("_", " ").title()
    except Exception:
        return "None"
