
from schema.canonical import CanonicalRecord


def project_record(
    record: CanonicalRecord,
    include_confidence=True,
    include_provenance=True,
):
    

    output = {}

    for field_name, resolved in record.fields.items():

        field_data = {
            "value": resolved.value
        }

        if include_confidence:

            field_data["confidence"] = (
                resolved.confidence
            )

        if include_provenance:

            field_data["provenance"] = [
                obs.source
                for obs in resolved.provenance
            ]

        output[field_name] = field_data

    output["candidate_id"] = (
        record.candidate_id
    )

    output["overall_confidence"] = (
        record.overall_confidence
    )

    return output


def project_records(
    records,
    include_confidence=True,
    include_provenance=True,
):

    projected = []

    for record in records:

        projected.append(
            project_record(
                record,
                include_confidence,
                include_provenance,
            )
        )

    return projected


if __name__ == "__main__":

    from adapters.csv_adapter import parse_csv
    from adapters.resume_adapter import parse_resume

    from merge.matcher import match_candidates
    from merge.resolver import resolve_matches

    from confidence.scorer import score_records

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

    scored = score_records(
        resolved
    )

    projected = project_records(
        scored
    )

    from pprint import pprint

    pprint(projected)