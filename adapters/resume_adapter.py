import re
import pdfplumber

from schema.canonical import FieldObservation

from normalize.phone import normalize_phone
from normalize.skills import canonicalize_skill_list

from utils.constants import NORMALIZATION_NOT_APPLICABLE


SOURCE = "resume"
METHOD = "resume_adapter"


def create_observation(field, value, raw_value, status):

    return FieldObservation(
        field=field,
        value=value,
        raw_value=raw_value,
        source=SOURCE,
        method=METHOD,
        normalization_status=status,
    )


def extract_text(pdf_path):
    
    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_name(text):
    
    for line in text.splitlines():

        line = line.strip()

        if line:
            return line

    return None


def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    return match.group(0) if match else None


def extract_phone(text):

    match = re.search(
        r"(\+?\d[\d\s\-\(\)]{8,}\d)",
        text,
    )

    return match.group(0) if match else None


def extract_skills(text):
    
    lines = text.splitlines()

    collecting = False

    skills = []

    stop_sections = {
        "PROJECTS",
        "EXPERIENCE",
        "EDUCATION",
        "WORK HISTORY",
        "SUMMARY",
        "ABOUT",
    }

    for line in lines:

        clean = line.strip()

        upper = clean.upper()

        if upper.startswith("SKILLS"):

            collecting = True

            if ":" in clean:

                clean = clean.split(":", 1)[1]

                if clean.strip():

                    skills.extend(clean.split(","))

            continue

        if collecting:

            if upper in stop_sections:

                break

            skills.extend(clean.split(","))

    return [s.strip() for s in skills if s.strip()]


def parse_resume(pdf_path):
    
    observations = []

    text = extract_text(pdf_path)

    # --------------------
    # Name
    # --------------------

    name = extract_name(text)

    if name:

        observations.append(
            create_observation(
                "full_name",
                name,
                name,
                NORMALIZATION_NOT_APPLICABLE,
            )
        )

    # --------------------
    # Email
    # --------------------

    email = extract_email(text)

    if email:

        observations.append(
            create_observation(
                "email",
                email,
                email,
                NORMALIZATION_NOT_APPLICABLE,
            )
        )

    # --------------------
    # Phone
    # --------------------

    phone = extract_phone(text)

    if phone:

        normalized_phone, status = normalize_phone(phone)

        observations.append(
            create_observation(
                "phone",
                normalized_phone,
                phone,
                status,
            )
        )

    # --------------------
    # Skills
    # --------------------

    skills = extract_skills(text)

    if skills:

        normalized_skills, status = canonicalize_skill_list(skills)

        observations.append(
            create_observation(
                "skills",
                normalized_skills,
                skills,
                status,
            )
        )

    return [observations]


if __name__ == "__main__":

    resumes = [
        "sample_inputs/resumes/resume1_normal.pdf",
        "sample_inputs/resumes/resume2_normal.pdf",
        "sample_inputs/resumes/resume3_edgecase.pdf",
    ]

    for resume in resumes:

        print("\n", "=" * 60)
        print(resume)

        observations = parse_resume(resume)

        for obs in observations:

            print(obs)