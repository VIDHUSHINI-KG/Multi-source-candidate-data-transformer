from utils.constants import (
    NORMALIZATION_SUCCESS,
    NORMALIZATION_FAILED,
    NORMALIZATION_NOT_APPLICABLE,
)


# Canonical country mapping
COUNTRY_MAP = {

    # India
    "india": "IN",
    "ind": "IN",

    # United States
    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "us": "US",

    # United Kingdom
    "united kingdom": "GB",
    "great britain": "GB",
    "britain": "GB",
    "england": "GB",
    "uk": "GB",

    # Canada
    "canada": "CA",

    # Australia
    "australia": "AU",

    # Germany
    "germany": "DE",

    # France
    "france": "FR",

    # Singapore
    "singapore": "SG",

    # Japan
    "japan": "JP",

    # China
    "china": "CN",
}


def normalize_country(country):
    """
    Normalize a country name into ISO-3166 alpha-2 format.

    Returns:
        (normalized_country, normalization_status)
    """

    if country is None:
        return None, NORMALIZATION_NOT_APPLICABLE

    country = str(country).strip()

    if not country:
        return None, NORMALIZATION_NOT_APPLICABLE

    key = country.lower()

    if key in COUNTRY_MAP:
        return COUNTRY_MAP[key], NORMALIZATION_SUCCESS

    return None, NORMALIZATION_FAILED


if __name__ == "__main__":

    test_cases = [

        "India",
        "india",
        "IND",

        "USA",
        "United States",
        "United States of America",

        "UK",
        "England",
        "Great Britain",

        "Canada",

        "Mars",           # Invalid

        "",

        None

    ]

    print("Testing Country Normalizer\n")

    for test in test_cases:

        normalized, status = normalize_country(test)

        print(
            f"{repr(test):<30} -> "
            f"{str(normalized):<5} ({status})"
        )