
from schema.canonical import CanonicalRecord


# Required fields
REQUIRED_FIELDS = [
    "full_name",
    "email",
    "phone",
]


def validate_record(record: CanonicalRecord):
    
    errors = []

    for field in REQUIRED_FIELDS:

        if field not in record.fields:

            errors.append(
                f"Missing required field: {field}"
            )

            continue

        value = record.fields[field].value

        if value is None:

            errors.append(
                f"Null value for required field: {field}"
            )

    return len(errors) == 0, errors


def validate_records(records):
    

    validated = []

    for record in records:

        valid, errors = validate_record(record)

        validated.append(
            {
                "record": record,
                "valid": valid,
                "errors": errors,
            }
        )

    return validated


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

    scored = score_records(resolved)

    validated = validate_records(scored)

    print("\nValidation Results")
    print("=" * 60)

    for item in validated:

        print(
            f"\n{item['record'].candidate_id}"
        )

        print(
            f"Valid: {item['valid']}"
        )

        if item["errors"]:

            for error in item["errors"]:
                print(" -", error)

        else:

            print(" No validation errors.")