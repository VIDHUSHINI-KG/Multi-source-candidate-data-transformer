from schema.canonical import (
    FieldObservation,
    ResolutionReason,
    ResolvedField,
    CanonicalRecord,
)

obs = FieldObservation(
    field="phone",
    value="+919876543210",
    source="resume",
    method="resume_adapter",
    raw_value="9876543210",
    normalization_status="success",
)

reason = ResolutionReason(
    code="HIGHER_RELIABILITY",
    details={
        "winner": "resume",
        "loser": "csv",
    },
)

resolved = ResolvedField(
    value="+919876543210",
    confidence=0.91,
    provenance=[obs],
    resolution_reason=reason,
)

record = CanonicalRecord(
    candidate_id="candidate_001",
    fields={
        "phone": resolved
    },
    overall_confidence=0.91,
)

print(record)