from datetime import datetime
from dateutil import parser

from utils.constants import (
    NORMALIZATION_SUCCESS,
    NORMALIZATION_FAILED,
    NORMALIZATION_NOT_APPLICABLE,
)

from utils.config import DATE_FORMAT


def normalize_date(date_string):
    """
    Normalize a date into YYYY-MM format.

    Returns:
        (normalized_date, normalization_status)
    """

    if date_string is None:
        return None, NORMALIZATION_NOT_APPLICABLE

    date_string = str(date_string).strip()

    if not date_string:
        return None, NORMALIZATION_NOT_APPLICABLE

    try:
        # Parse twice using different defaults.
        # If a component changes between parses,
        # it means that component was inferred rather than
        # explicitly present in the input.
        dt1 = parser.parse(
            date_string,
            default=datetime(1, 1, 1)
        )

        dt2 = parser.parse(
            date_string,
            default=datetime(2, 2, 2)
        )

    except Exception:
        return None, NORMALIZATION_FAILED

    year_present = dt1.year == dt2.year
    month_present = dt1.month == dt2.month

    if not (year_present and month_present):
        return None, NORMALIZATION_FAILED

    return dt1.strftime(DATE_FORMAT), NORMALIZATION_SUCCESS


if __name__ == "__main__":

    test_cases = [
        "Jan 2024",
        "January 2024",
        "01/2024",
        "2024-01",
        "2024-01-15",
        "15 Jan 2024",
        "2021",          # Missing month
        "March",         # Missing year
        "abcd",          # Invalid
        "",
        None,
    ]

    print("Testing Date Normalizer\n")

    for test in test_cases:

        normalized, status = normalize_date(test)

        print(
            f"{repr(test):<20} -> "
            f"{str(normalized):<10} ({status})"
        )