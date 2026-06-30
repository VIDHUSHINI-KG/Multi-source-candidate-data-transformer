
from schema.canonical import CanonicalRecord

# Reliability of each source
SOURCE_RELIABILITY = {
    "recruiter_csv": 0.90,
    "resume": 0.60,
}


def calculate_field_confidence(resolved_field):
   
    provenance = resolved_field.provenance

    if not provenance:
        return 0.0

    # Average source reliability
    reliabilities = []

    for obs in provenance:
        reliabilities.append(
            SOURCE_RELIABILITY.get(
                obs.source,
                0.5
            )
        )

    avg_reliability = (
        sum(reliabilities)
        / len(reliabilities)
    )

    # Agreement

    selected_value = resolved_field.value

    agreement_count = 0

    for obs in provenance:

        if obs.value == selected_value:
            agreement_count += 1

    agreement = (
        agreement_count
        / len(provenance)
    )

    confidence = (
        0.7 * avg_reliability
        + 0.3 * agreement
    )

    return round(confidence, 2)


def score_record(record: CanonicalRecord):
    
    scores = []

    for resolved_field in record.fields.values():

        confidence = calculate_field_confidence(
            resolved_field
        )

        resolved_field.confidence = confidence

        scores.append(confidence)

    if scores:

        record.overall_confidence = round(
            sum(scores) / len(scores),
            2,
        )

    else:

        record.overall_confidence = 0.0

    return record


def score_records(records):

    scored = []

    for record in records:

        scored.append(
            score_record(record)
        )

    return scored


if __name__ == "__main__":

    from adapters.csv_adapter import parse_csv
    from adapters.resume_adapter import parse_resume

    from merge.matcher import match_candidates
    from merge.resolver import resolve_matches

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

    resolved = resolve_matches(
        matches
    )

    scored = score_records(
        resolved
    )

    print("\nConfidence Scores")
    print("=" * 60)

    for record in scored:

        print(
            f"\n{record.candidate_id}"
        )

        print(
            f"Overall Confidence: {record.overall_confidence}"
        )

        for field, resolved in record.fields.items():

            print(
                f"{field}: {resolved.confidence}"
            )