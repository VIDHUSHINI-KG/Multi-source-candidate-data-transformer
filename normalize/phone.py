import phonenumbers
from phonenumbers import NumberParseException


def normalize_phone(phone: str, default_region: str = "IN"):
    

    if not phone:
        return None, "not_applicable"

    try:
        parsed = phonenumbers.parse(phone, default_region)

        if not phonenumbers.is_valid_number(parsed):
            return None, "failed"

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        ), "success"

    except NumberParseException:
        return None, "failed"


if __name__ == "__main__":

    tests = [
        "9876543210",
        "+91 9876543210",
        "(987)-654-3210",
        "123",
        "",
        None
    ]

    for t in tests:
        normalized, status = normalize_phone(t)
        print(f"{t}  --->  {normalized} ({status})")