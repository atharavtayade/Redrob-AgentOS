import json
import re
from typing import Optional

try:
    from .ollama_client import OllamaClient
except ImportError:
    print("Warning: ollama_client not found. Using a mock object.")
    class MockOllamaClient:
        def generate(self, prompt: str, system_context: Optional[str] = None) -> Optional[str]:
            return '{"required_skills": [], "learning_order": []}'
    OllamaClient = MockOllamaClient


def _normalize_skill(skill: str) -> str:
    """Normalizes a skill string for case-insensitive comparison."""
    return (skill or "").strip().lower()


def _extract_json(text: str) -> Optional[dict]:
    """
    Extracts and parses the first JSON object from an LLM response.
    Strips markdown fences and tolerates surrounding prose.
    """
    if not text:
        return None
    cleaned = text.strip()
    # Strip markdown code fences if present
    fence_match = re.search(r"```(?:json)?\s*(.*?)```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    # Try direct parse first
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        pass
    # Fallback: locate the first {...} block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def _coerce_skill_list(value) -> list:
    """Coerces a possibly-messy LLM value into a clean list of skill strings."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r"[\n,;|]", value)
        return [p.strip(" -\t0123456789.") for p in parts if p.strip(" -\t0123456789.")]
    if isinstance(value, list):
        out = []
        for item in value:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    out.append(cleaned)
            elif isinstance(item, dict):
                name = item.get("name") or item.get("skill")
                if isinstance(name, str) and name.strip():
                    out.append(name.strip())
                else:
                    for v in item.values():
                        if isinstance(v, str) and v.strip():
                            out.append(v.strip())
                            break
        return out
    return []


def analyze_skill_gap(target_role: str, current_skills: list) -> dict:
    """
    Analyzes the skill gap between a user's current skills and the requirements
    of a target role using a local Ollama model.

    Args:
        target_role: The role the user is targeting (e.g., "AI Engineer").
        current_skills: A list of skills the user already possesses.

    Returns:
        A dict with keys: target_role, current_skills, missing_skills,
        recommended_learning_order.
    """
    # Defensively normalize inputs
    if not isinstance(target_role, str) or not target_role.strip():
        target_role = "Unknown Role"
    if not isinstance(current_skills, list):
        current_skills = []
    current_skills = [str(s).strip() for s in current_skills if str(s).strip()]

    current_set = {_normalize_skill(s) for s in current_skills}

    client = OllamaClient()

    system_context = (
        "You are a career intelligence engine specializing in skill taxonomy. "
        "Respond ONLY with a single valid JSON object, no prose, no markdown."
    )

    prompt = (
        f"Target Role: {target_role}\n"
        f"User's Current Skills: {', '.join(current_skills) if current_skills else 'None'}\n\n"
        "Identify the complete set of skills required for this target role, then "
        "determine a sensible learning order (foundational skills first, advanced last) "
        "for someone acquiring them.\n\n"
        "Respond with EXACTLY this JSON schema and nothing else:\n"
        "{\n"
        '  "required_skills": ["skill1", "skill2"],\n'
        '  "learning_order": ["foundational_skill", "next_skill"]\n'
        "}"
    )

    print("--- Sending skill-gap analysis request to Ollama ---")
    response = client.generate(prompt=prompt, system_context=system_context)

    parsed = _extract_json(response) if response else None

    required_skills = []
    learning_order = []
    if parsed:
        required_skills = _coerce_skill_list(parsed.get("required_skills"))
        learning_order = _coerce_skill_list(parsed.get("learning_order"))
    else:
        print("[SkillGap] Could not parse LLM response; returning empty gap analysis.")

    # Missing skills = required skills not already in current skills (case-insensitive)
    missing_skills = []
    seen = set()
    for skill in required_skills:
        norm = _normalize_skill(skill)
        if not norm or norm in current_set or norm in seen:
            continue
        seen.add(norm)
        missing_skills.append(skill)

    # Recommended learning order: filter the LLM's learning order to only missing
    # skills (preserving order), then append any missing skills not covered.
    missing_norms = {_normalize_skill(s) for s in missing_skills}
    recommended_learning_order = []
    ordered_seen = set()
    for skill in learning_order:
        norm = _normalize_skill(skill)
        if norm in missing_norms and norm not in ordered_seen:
            ordered_seen.add(norm)
            recommended_learning_order.append(skill)
    for skill in missing_skills:
        norm = _normalize_skill(skill)
        if norm not in ordered_seen:
            ordered_seen.add(norm)
            recommended_learning_order.append(skill)

    return {
        "target_role": target_role,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "recommended_learning_order": recommended_learning_order,
    }


if __name__ == "__main__":
    report = analyze_skill_gap("AI Engineer", ["Python", "Pandas", "Git"])
    print(json.dumps(report, indent=2))
