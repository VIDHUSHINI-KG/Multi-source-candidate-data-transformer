from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResolutionReason:
    
    code: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldObservation:
    
    field: str
    value: Any

    source: str         
    method: str         

    raw_value: Optional[Any] = None

    normalization_status: str = "pending"
    


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
