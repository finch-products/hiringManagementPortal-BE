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
} 
