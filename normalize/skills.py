
from utils.constants import (
    NORMALIZATION_SUCCESS,
    NORMALIZATION_PARTIAL,
    NORMALIZATION_NOT_APPLICABLE,
)

# Canonical Skill Mapping
SKILL_MAP = {

    # Python
    "python": "Python",
    "python3": "Python",
    "python programming": "Python",

    # Java
    "java": "Java",

    # JavaScript
    "javascript": "JavaScript",
    "js": "JavaScript",

    # React
    "react": "React",
    "react.js": "React",
    "reactjs": "React",

    # Machine Learning
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    # Artificial Intelligence
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    # SQL
    "sql": "SQL",

    # C
    "c": "C",

    # C++
    "c++": "C++",

    # HTML
    "html": "HTML",

    # CSS
    "css": "CSS",

    # Git
    "git": "Git",

    # Docker
    "docker": "Docker",
}


def canonicalize_skill(skill):
    """
    Normalize a single skill.

    Returns:
        (canonical_skill, normalization_status)

    Status:
        success          -> mapped using synonym dictionary
        partial          -> retained unchanged (unknown skill)
        not_applicable   -> empty input
    """

    if skill is None:
        return None, NORMALIZATION_NOT_APPLICABLE

    skill = str(skill).strip()

    if not skill:
        return None, NORMALIZATION_NOT_APPLICABLE

    key = skill.lower()

    if key in SKILL_MAP:
        return SKILL_MAP[key], NORMALIZATION_SUCCESS

    # Unknown skill:
    # Keep it unchanged instead of guessing.
    return skill, NORMALIZATION_PARTIAL


def canonicalize_skill_list(skills):
    """
    Normalize a list of skills and remove duplicates.

    Returns:
        (unique_skills, overall_status)
    """

    if not skills:
        return [], NORMALIZATION_NOT_APPLICABLE

    normalized_skills = []
    seen = set()

    overall_status = NORMALIZATION_SUCCESS

    for skill in skills:

        canonical, status = canonicalize_skill(skill)

        if canonical is None:
            continue

        # Remove duplicates while preserving order
        if canonical not in seen:
            normalized_skills.append(canonical)
            seen.add(canonical)

        if status == NORMALIZATION_PARTIAL:
            overall_status = NORMALIZATION_PARTIAL

    return normalized_skills, overall_status


if __name__ == "__main__":

    print("Testing Individual Skills\n")

    test_cases = [
        "Python",
        "python",
        "Python3",
        "python programming",
        "React",
        "React.js",
        "reactjs",
        "ML",
        "Machine Learning",
        "AI",
        "Docker",
        "UnknownSkill",
        "",
        None,
    ]

    for test in test_cases:

        canonical, status = canonicalize_skill(test)

        print(
            f"{repr(test):<25} -> "
            f"{str(canonical):<25} ({status})"
        )

    print("\n---------------------------------------")
    print("Testing Skill List\n")

    sample = [
        "Python",
        "python",
        "Python3",
        "React",
        "React.js",
        "ML",
        "Machine Learning",
        "Docker",
        "Docker",
        "UnknownSkill",
        None,
        ""
    ]

    skills, status = canonicalize_skill_list(sample)

    print("Normalized Skills:")
    print(skills)

    print("\nOverall Status:")
    print(status)