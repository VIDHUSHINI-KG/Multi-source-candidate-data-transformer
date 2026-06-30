
from typing import List, Dict

from schema.canonical import (
    CanonicalRecord,
    FieldObservation,
    ResolvedField,
    ResolutionReason,
)

# Source priority
SOURCE_PRIORITY = {
    "recruiter_csv": 2,
    "resume": 1,
}


def resolve_candidate(candidate_pair, candidate_id):
    
    csv_candidate, resume_candidate = candidate_pair

    observations = csv_candidate + resume_candidate

    grouped: Dict[str, List[FieldObservation]] = {}

    for obs in observations:
        grouped.setdefault(obs.field, []).append(obs)

    record = CanonicalRecord(candidate_id=candidate_id)

    for field_name, values in grouped.items():

        winner = max(
            values,
            key=lambda x: SOURCE_PRIORITY.get(x.source, 0),
        )

        if len(values) == 1:

            reason = ResolutionReason(
                code="ONLY_SOURCE",
                details={
                    "selected_source": winner.source
                }
            )

        else:

            reason = ResolutionReason(
                code="SOURCE_PRIORITY",
                details={
                    "selected_source": winner.source,
                    "all_sources": [
                        v.source for v in values
                    ]
                }
            )

        record.fields[field_name] = ResolvedField(
            value=winner.value,
            confidence=0.0,
            provenance=values,
            resolution_reason=reason,
        )

    return record


def resolve_matches(matches):
    
    resolved = []

    for index, pair in enumerate(matches, start=1):

        record = resolve_candidate(
            pair,
            candidate_id=f"candidate_{index}",
        )

        resolved.append(record)

    return resolved


if __name__ == "__main__":

    from adapters.csv_adapter import parse_csv
    from adapters.resume_adapter import parse_resume
    from merge.matcher import match_candidates

    csv_candidates = parse_csv(
        "sample_inputs/recruiter.csv"
    )

    resume_candidates = []

    resumes = [
        "sample_inputs/resumes/resume1_normal.pdf",
        "sample_inputs/resumes/resume2_normal.pdf",
        "sample_inputs/resumes/resume3_edgecase.pdf",
    ]

    for resume in resumes:
        resume_candidates.extend(
            parse_resume(resume)
        )

    matches = match_candidates(
        csv_candidates,
        resume_candidates,
    )

    resolved = resolve_matches(matches)

    print("\nResolved Candidates")
    print("=" * 60)

    for record in resolved:

        print(f"\n{record.candidate_id}")

        print("-" * 40)

        for field, resolved_field in record.fields.items():

            print(f"{field}: {resolved_field.value}")

            print(
                f"Reason: {resolved_field.resolution_reason.code}"
            )

            print(
                f"Sources: {[p.source for p in resolved_field.provenance]}"
            )

            print()