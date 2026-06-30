
# Normalization Status

NORMALIZATION_PENDING = "pending"
NORMALIZATION_PARTIAL = "partial"
NORMALIZATION_SUCCESS = "success"
NORMALIZATION_FAILED = "failed"
NORMALIZATION_NOT_APPLICABLE = "not_applicable"

# Source Reliability

SOURCE_RELIABILITY = {
    "ats": 0.90,
    "recruiter_csv": 0.85,
    "resume": 0.60,
    "notes": 0.40,
}

# Resolution Reason Codes

HIGHER_RELIABILITY = "HIGHER_RELIABILITY"
HIGHER_AGREEMENT = "HIGHER_AGREEMENT"
ONLY_SOURCE = "ONLY_SOURCE"
TIE_BREAKER = "TIE_BREAKER"

# Missing Field Policies

ON_MISSING_NULL = "null"
ON_MISSING_OMIT = "omit"
ON_MISSING_ERROR = "error"