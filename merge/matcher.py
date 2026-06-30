
from typing import List, Tuple
from schema.canonical import FieldObservation


def get_field(candidate: List[FieldObservation], field_name: str):
    
    for obs in candidate:
        if obs.field == field_name:
            return obs.value

    return None


def normalize_name(name):
    
    if not name:
        return None

    return " ".join(str(name).strip().lower().split())


def emails_match(candidate1, candidate2):
    
    email1 = get_field(candidate1, "email")
    email2 = get_field(candidate2, "email")

    if email1 and email2:
        return email1.strip().lower() == email2.strip().lower()

    return False


def fallback_match(candidate1, candidate2):
    
    name1 = normalize_name(get_field(candidate1, "full_name"))
    name2 = normalize_name(get_field(candidate2, "full_name"))

    phone1 = get_field(candidate1, "phone")
    phone2 = get_field(candidate2, "phone")

    if (
        name1
        and name2
        and phone1
        and phone2
    ):
        return (
            name1 == name2
            and phone1 == phone2
        )

    return False


def candidates_match(candidate1, candidate2):
    
    # Rule 1
    if emails_match(candidate1, candidate2):
        return True

    # Rule 2
    if fallback_match(candidate1, candidate2):
        return True

    return False


def match_candidates(
    csv_candidates: List[List[FieldObservation]],
    resume_candidates: List[List[FieldObservation]]
) -> List[Tuple]:
    
    matches = []

    for csv_candidate in csv_candidates:

        matched = False

        for resume_candidate in resume_candidates:

            if candidates_match(
                csv_candidate,
                resume_candidate
            ):

                matches.append(
                    (
                        csv_candidate,
                        resume_candidate
                    )
                )

                matched = True
                break

        # CSV candidate with no matching resume
        if not matched:

            matches.append(
                (
                    csv_candidate,
                    []
                )
            )

    return matches


if __name__ == "__main__":

    from adapters.csv_adapter import parse_csv
    from adapters.resume_adapter import parse_resume

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
        resume_candidates
    )

    print("\nMatched Records")
    print("=" * 50)

    for i, (csv_record, resume_record) in enumerate(matches, start=1):

        print(f"\nMatch {i}")

        print("CSV Email:",
              get_field(csv_record, "email"))

        if resume_record:
            print(
                "Resume Email:",
                get_field(
                    resume_record,
                    "email"
                )
            )
        else:
            print("Resume: No Match")