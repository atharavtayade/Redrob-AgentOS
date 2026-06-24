import json
import os
import sys

# Ensure the project root is on sys.path so that `services.planner` resolves as
# a package and its relative imports (from .ollama_client, .memory, .skill_gap)
# work correctly when this test is executed directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# The existing ollama_client prints unicode symbols (e.g. "❌") that the default
# Windows cp1252 console cannot encode. Reconfigure stdout to UTF-8 so those
# prints do not crash the run. This is test-side setup only; no existing files
# are modified.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from services.planner import PlannerAgent


def main():
    target_role = "AI Engineer"
    current_skills = [
        "Python",
        "Pandas",
        "NumPy",
        "Machine Learning",
    ]

    print("=" * 60)
    print("           SKILL GAP DETECTOR TEST")
    print("=" * 60)
    print(f"Target Role    : {target_role}")
    print(f"Current Skills : {current_skills}")
    print("-" * 60)

    planner = PlannerAgent()
    report = planner.generate_skill_gap_report(target_role, current_skills)

    # --- Print full JSON output ---
    print("\n--- Full JSON Output ---")
    print(json.dumps(report, indent=2))

    # --- Verify execution ---
    print("\n--- Verification ---")
    assert isinstance(report, dict), "Report must be a dict."

    expected_keys = {
        "target_role",
        "current_skills",
        "missing_skills",
        "recommended_learning_order",
    }
    assert set(report.keys()) == expected_keys, (
        f"Unexpected keys. Got: {set(report.keys())}"
    )

    assert report["target_role"] == target_role, "target_role mismatch."
    assert isinstance(report["current_skills"], list), "current_skills must be a list."
    assert report["current_skills"] == current_skills, "current_skills mismatch."
    assert isinstance(report["missing_skills"], list), "missing_skills must be a list."
    assert isinstance(report["recommended_learning_order"], list), (
        "recommended_learning_order must be a list."
    )

    # None of the current skills should appear in missing_skills (case-insensitive)
    current_lower = {s.lower() for s in current_skills}
    leaked = [s for s in report["missing_skills"] if s.lower() in current_lower]
    assert not leaked, f"Current skills leaked into missing_skills: {leaked}"

    # recommended_learning_order should be a subset of missing_skills (case-insensitive)
    missing_lower = {s.lower() for s in report["missing_skills"]}
    order_leak = [s for s in report["recommended_learning_order"] if s.lower() not in missing_lower]
    assert not order_leak, (
        f"recommended_learning_order contains skills not in missing_skills: {order_leak}"
    )

    print("[OK] Report structure valid.")
    print(f"[OK] target_role           = {report['target_role']}")
    print(f"[OK] current_skills count  = {len(report['current_skills'])}")
    print(f"[OK] missing_skills count  = {len(report['missing_skills'])}")
    print(f"[OK] learning_order count  = {len(report['recommended_learning_order'])}")
    print("[OK] No current skills leaked into missing_skills.")
    print("[OK] recommended_learning_order is a subset of missing_skills.")
    print("\nTEST PASSED.")


if __name__ == "__main__":
    main()
