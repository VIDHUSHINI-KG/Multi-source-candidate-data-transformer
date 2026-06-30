"""
cli.py

Runs the complete candidate transformation pipeline.
"""

import json
import os

from adapters.csv_adapter import parse_csv
from adapters.resume_adapter import parse_resume

from merge.matcher import match_candidates
from merge.resolver import resolve_matches

from confidence.scorer import score_records

from schema.validator import validate_records

from project.projector import project_records


OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "candidate.json",
)


def main():

    print("=" * 70)
    print("Eightfold Candidate Transformation Pipeline")
    print("=" * 70)

    # -------------------------------------------------
    # CSV
    # -------------------------------------------------

    print("\nReading recruiter CSV...")

    csv_candidates = parse_csv(
        "sample_inputs/recruiter.csv"
    )

    print(
        f"✓ Parsed {len(csv_candidates)} recruiter candidate(s)"
    )

    # -------------------------------------------------
    # Resumes
    # -------------------------------------------------

    print("\nReading resumes...")

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

        print(f"✓ Parsed {resume}")

    # -------------------------------------------------
    # Matching
    # -------------------------------------------------

    print("\nMatching candidates...")

    matches = match_candidates(
        csv_candidates,
        resume_candidates,
    )

    print(
        f"✓ Matched {len(matches)} candidate pair(s)"
    )

    # -------------------------------------------------
    # Resolve
    # -------------------------------------------------

    print("\nResolving conflicts...")

    resolved = resolve_matches(matches)

    # -------------------------------------------------
    # Confidence
    # -------------------------------------------------

    print("\nComputing confidence...")

    scored = score_records(resolved)

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    print("\nValidating records...")

    validated = validate_records(scored)

    for item in validated:

        if item["valid"]:

            print(
                f"✓ {item['record'].candidate_id} valid"
            )

        else:

            print(
                f"⚠ {item['record'].candidate_id}"
            )

            for err in item["errors"]:
                print("   -", err)

    # -------------------------------------------------
    # Projection
    # -------------------------------------------------

    print("\nGenerating output JSON...")

    records = [
        item["record"]
        for item in validated
    ]

    output = project_records(records)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\n✓ Output written to:")
    print(OUTPUT_FILE)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()