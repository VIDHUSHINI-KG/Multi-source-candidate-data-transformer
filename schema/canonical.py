from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResolutionReason:
    """
    Stores the reason why a particular value was selected
    during conflict resolution.
    """

    code: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldObservation:
    "
    field: str
    value: Any

    source: str          # recruiter_csv, resume
    method: str          # csv_adapter, resume_adapter

    raw_value: Optional[Any] = None

    normalization_status: str = "pending"
    # pending | success | failed | not_applicable


@dataclass
class ResolvedField:
    
    value: Any

    confidence: float

    provenance: List[FieldObservation] = field(default_factory=list)

    resolution_reason: Optional[ResolutionReason] = None


@dataclass
class CanonicalRecord:
    
    candidate_id: str

    fields: Dict[str, ResolvedField] = field(default_factory=dict)

    overall_confidence: float = 0.0