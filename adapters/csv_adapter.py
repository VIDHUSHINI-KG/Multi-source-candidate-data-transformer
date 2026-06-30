import pandas as pd

from schema.canonical import FieldObservation

from normalize.phone import normalize_phone
from normalize.country import normalize_country

from utils.constants import NORMALIZATION_NOT_APPLICABLE


SOURCE = "recruiter_csv"
METHOD = "csv_adapter"


def create_observation(field, value, raw_value, status):
    
    return FieldObservation(
        field=field,
        value=value,
        raw_value=raw_value,
        source=SOURCE,
        method=METHOD,
        normalization_status=status,
    )


def parse_csv(csv_path):
    
    df = pd.read_csv(csv_path)

    candidates = []

    for _, row in df.iterrows():

        observations = []

        # -------------------------
        # Full Name
        # -------------------------

        value = row.get("full_name")

        if pd.notna(value):

            observations.append(
                create_observation(
                    field="full_name",
                    value=str(value).strip(),
                    raw_value=str(value),
                    status=NORMALIZATION_NOT_APPLICABLE,
                )
            )

        # -------------------------
        # Email
        # -------------------------

        value = row.get("email")

        if pd.notna(value):

            observations.append(
                create_observation(
                    field="email",
                    value=str(value).strip(),
                    raw_value=str(value),
                    status=NORMALIZATION_NOT_APPLICABLE,
                )
            )

        # -------------------------
        # Phone
        # -------------------------

        value = row.get("phone")

        if pd.notna(value):

            normalized_phone, status = normalize_phone(str(value))

            observations.append(
                create_observation(
                    field="phone",
                    value=normalized_phone,
                    raw_value=str(value),
                    status=status,
                )
            )

        # -------------------------
        # Current Company
        # -------------------------

        value = row.get("current_company")

        if pd.notna(value):

            observations.append(
                create_observation(
                    field="current_company",
                    value=str(value).strip(),
                    raw_value=str(value),
                    status=NORMALIZATION_NOT_APPLICABLE,
                )
            )

        # -------------------------
        # Country
        # -------------------------

        value = row.get("country")

        if pd.notna(value):

            normalized_country, status = normalize_country(str(value))

            observations.append(
                create_observation(
                    field="country",
                    value=normalized_country,
                    raw_value=str(value),
                    status=status,
                )
            )

        candidates.append(observations)

    return candidates


if __name__ == "__main__":

    candidates = parse_csv("sample_inputs/recruiter.csv")

    for i, candidate in enumerate(candidates, start=1):

        print(f"\nCandidate {i}")
        print("-" * 50)

        for observation in candidate:
            print(observation)