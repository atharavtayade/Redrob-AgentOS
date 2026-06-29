import re

def parse_candidate(candidate: dict) -> dict:
    """
    Converts raw candidate dictionaries into a standardized format.

    Args:
        candidate: A dictionary with raw candidate data, potentially including 'name' and 'skills'.

    Returns:
        A cleaned and standardized candidate dictionary with 'name' and 'skills' (list of lowercase strings).
    """
    parsed_candidate = {}

    # 1. Validate and normalize name
    name = candidate.get('name', '')
    if isinstance(name, str) and name.strip():
        parsed_candidate['name'] = name.strip().title()
    else:
        parsed_candidate['name'] = ''

    # 2. Validate, normalize, remove duplicates, and remove empty values for skills
    raw_skills = candidate.get('skills', [])
    if not isinstance(raw_skills, list):
        raw_skills = []

    normalized_skills_set = set()
    for skill in raw_skills:
        if isinstance(skill, str) and skill.strip():
            normalized_skills_set.add(skill.strip().lower())

    # Sort skills for deterministic output
    parsed_candidate['skills'] = sorted(list(normalized_skills_set))

    return parsed_candidate
