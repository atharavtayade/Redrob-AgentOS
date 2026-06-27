import re


def _normalize_skills(text):
    """Normalize skills to lowercase."""
    if not text:
        return set()
    parts = re.split(r'[,;\s]+', text.lower().strip())
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
    # Extract and normalize job description keywords
    job_keywords = _extract_keywords(job_description)

    results = []

    for candidate in candidates:
        name = candidate.get('name', '') or ''
        candidate_skills = _normalize_skills(candidate.get('skills', ''))

        # Compute matched skills (intersection of candidate skills and job keywords)
        matched_skills = candidate_skills & job_keywords

        total_job_keywords = max(len(job_keywords), 1)  # Avoid division by zero
        score = int((len(matched_skills) / total_job_keywords) * 100 if job_keywords else 0)

        results.append({
            'name': name,
            'score': min(score, 100),  # Clamp to max 100
            'matched_skills': matched_skills,
        })

    # Sort by descending score (then by name for determinism when scores are equal)
    results.sort(key=lambda x: (-x['score'], x['name']))

    return results
