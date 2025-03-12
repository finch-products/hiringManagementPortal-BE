# Define Role Names for Easy Management
ROLE_PMO = "PMO"
ROLE_CLIENT_PARTNER = "Client Partner"
ROLE_DELIVERY_MANAGER = "Delivery Manager"
ROLE_SPOC = "SPOC"
ROLE_ACCOUNT_HEAD = "Account Head"
ROLE_ADMIN = "Admin"

# Store in a Dictionary for Easy Access
ROLE_MAPPING = {
    "CP": ROLE_CLIENT_PARTNER,
    "DM": ROLE_DELIVERY_MANAGER,
    "SPOC": ROLE_SPOC,
    "AH": ROLE_ACCOUNT_HEAD,
    "ADMIN": ROLE_ADMIN   
}

DEMAND_STATUS = {
    "OPEN": "Open",
    "REQ_NOT_CLEAR": "Req Not Clear",
    "JD_NOT_RECEIVED": "JD Not Received",
    "CLOSED": "Closed",
    "EXTERNAL_HIRING": "External Hiring",
    "CANDIDATE_SCREENING": "Candidate Screening",
    "REJECTED": "Rejected",
    "CLIENT_FEEDBACK_AWAITED": "Client Feedback Awaited",
    "ON_HOLD": "On Hold",
}

CANDIDATE_STATUS = {
    "APPLIED": "Applied",
    "SCREENING": "Screening",
    "SHORTLISTED": "Shortlisted",
    "INTERVIEW_SCHEDULED": "Interview Scheduled",
    "L1_SCHEDULED": "L1 Scheduled",
    "L1_REJECTED": "L1 Rejected",
    "SENT_TO_CLIENT": "Sent to Client",
    "CLIENT_EVALUATION_PENDING": "Client Evaluation Pending",
    "CLIENT_INTERVIEW_SCHEDULED": "Client Interview Scheduled",
    "SELECTED_BY_CLIENT": "Selected by Client",
    "REJECTED_BY_CLIENT": "Rejected by Client",
    "ON_HOLD": "On Hold",
    "CLIENT_FEEDBACK_PROVIDED": "Client Feedback Provided",
}
