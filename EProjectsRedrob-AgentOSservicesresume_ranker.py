import re


def _normalize_skills(text):
    """Normalize skills to lowercase."""
    if not text:
        return set()
    parts = re.split(r'[,\;\s]+', text.lower().strip())
    return {p for p in parts if p}


def _extract_keywords(text):
    """Extract keywords from the job description."""
    if not text:
        return set()
    words = re.findall(r'[a-z]+', text.lower())
    return {w.strip('.') for w in words if len(w) > 2}


def rank_candidates(job_description, candidates):
    """Rank candidates based on job description.

    Args:
        job_description: The job posting text to extract keywords from.
        candidates: List of candidate dictionaries with 'skills' and 'name' keys.

    Returns:
        Sorted list (descending by score) of dicts containing:
          - name: Candidate's full name or empty string if unavailable
          - score: Match percentage (integer, clamped to 100)
          - matched_skills: List of skills that match job keywords
    """

