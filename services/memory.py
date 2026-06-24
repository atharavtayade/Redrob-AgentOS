import uuid
from datetime import datetime
# Assuming this path is relative to the execution environment root
from storage.storage_manager import load_json, save_json 
from typing import Any, Optional

class MemoryManager:
    """
    Manages the local-first knowledge base stored in memory.json.
    Handles structured facts, recurring goals, and ephemeral notes using a single JSON source.
    """

    def __init__(self, memory_file_path: str = "data/memory.json"):
        self.memory_file_path = memory_file_path
        self._initial_load()

    def _initial_load(self):
        """Loads the current state from disk into a mutable internal dictionary."""
        # Load all data, or initialize an empty structure if not found/readable
        self.memory_data = load_json(self.memory_file_path) or {
                    "structured_facts": {}, # For structured knowledge (old 'memory_data')
                    "goals": [],
                    "notes": [],
                    "career_insights": [] # New key for persistent career intelligence
                }

    def _save_state(self):
        """Saves the current internal state back to memory.json using storage_manager."""
        return save_json(self.memory_data, self.memory_file_path)


    # --- Structured Memory Functions (Facts/Knowledge Base) ---

    def list_structured_memories(self) -> str:
        """Returns all structured memory facts in a readable format."""
        facts = self.memory_data.get("structured_facts", {})
        if not facts:
            return "No structured memories are currently stored."
        
        output = ["--- Current Structured Knowledge Base ---"]
        for fact_id, fact in facts.items():
            output.append(f"\n💡 [ID: {fact_id}]: {fact['fact']} (Source: {fact.get('source_date', 'Unknown')})")
        return "\n".join(output)

    def get_structured_memory_entry(self, fact_id: str) -> Optional[dict]:
        """Retrieves a single memory fact by its unique ID."""
        return self.memory_data.get("structured_facts", {}).get(fact_id)


    # --- Goal Management Functions (The Agent's Focus) ---

    def remember_career_insight(self, insight: str) -> None:
        """
        Stores a career insight in the persistent memory for future career intelligence.
        Accepts a plain string and persists it with a timestamp.
        """
        if not insight or not isinstance(insight, str):
            return
        insights = self.memory_data.setdefault('career_insights', [])
        insights.append({
            "content": insight,
            "timestamp": datetime.now().isoformat()
        })
        self._save_state()
        print("[MemoryManager] Career insight remembered successfully.")

    def get_recent_career_insights(self, limit: int = 10) -> list:
        """
        Retrieves the N most recent career insights from persistent memory.
        Backward compatible with legacy plain-string entries and structured dict entries.
        """
        insights = self.memory_data.get("career_insights", [])
        if not insights:
            return []
        return insights[-limit:] if len(insights) >= limit else list(insights)

    def get_latest_goal(self) -> Optional[str]:
        """Returns the most recently set goal."""
        goals = self.memory_data.get("goals", [])
        if not goals:
            return None
        # Assuming the goals list is appended in time order, the last element is the latest.
        return goals[-1]['goal']

    def remember_goal(self, goal: str) -> None:
        """
        Stores a career goal with timestamp and unique ID for persistent memory tracking.

        Args:
            goal: The specific career goal string to store (e.g., "Become ML Engineer").

        Behavior:
            - Appends goal entry to memory_data["goals"] list
            - Includes id (UUID), content, and timestamp
            - Calls self._save_state() to persist changes
            - Backward compatible with existing code patterns
        """
        if not goal or not isinstance(goal, str):
            return

        new_goal_entry = {
            "id": str(uuid.uuid4()),
            "goal": goal.strip(),
            "timestamp": datetime.now().isoformat()
        }

        goals = self.memory_data.setdefault("goals", [])
        goals.append(new_goal_entry)

        self._save_state()
        print("[MemoryManager] Goal remembered successfully.")

    def force_sync_goals(self) -> bool:
        """Persists changes to goal memories."""
        self._save_state()
        return True


    # --- Note Management Functions (Ephemeral/General Notes) ---

    def remember_note(self, note: str) -> None:
        """
        Saves a general, unstructured note using UUID for tracking. 
        This is separate from the core structured 'facts'.
        """
        new_note = {
            "id": str(uuid.uuid3(uuid.NAMESPACE_DNS, note)),
            "content": note,
            "timestamp": datetime.now().isoformat()
        }
        self.memory_data.get("notes", []).append(new_note)
        self._save_state()
        print("[MemoryManager] Note remembered successfully.")

    def get_recent_notes(self, limit: int = 5) -> Optional[list]:
        """Retrieves the N most recent notes added since the last run."""
        notes = self.memory_data.get("notes", [])
        return notes[-limit:] if len(notes) >= limit else notes


    # --- Persistence Hook ---

    @staticmethod
    def save_all_state() -> bool:
        """Public static method to trigger a full persistence sync across all memory types."""
        print("\n[MemoryManager] Attempting full state saving...")
        return MemoryManager(memory_file_path="data/memory.json")._save_state()


    # --- Independent Test Section for services/memory.py ---

    @staticmethod
    def test_memory_manager():
        """Walkthrough function to test all methods."""
        print("\n" + "="*50)
        print("           STARTING MEMORY MANAGER TESTS")
        print("="*50)
        
        # 1. Setup (This section is for demonstration purposes and assumes storage_manager handles the file creation/deletion)
        # NOTE: In a real test suite, we would mock disk I/O to clean up without affecting system files.
        
        # Initialize Manager (which loads initial state from data/memory.json)
        manager = MemoryManager() 
        print(f"Initial Goals Loaded Count: {len(manager.memory_data.get('goals', []))}")
        
        # 2. Test Remember Goal
        print("\n--- Testing remember_goal ---")
        test_goal = "Goal to transition from Data Science to Product Management in FinTech."
        manager.remember_goal(test_goal)
        latest_goal = manager.get_latest_goal()
        assert latest_goal == test_goal, "Failed to set or retrieve the correct goal."
        
        # 3. Test Remember Notes
        print("\n--- Testing remember_note ---")
        manager.remember_note("Reminder: Need to check Python version compatibility with FastAPI.")
        manager.remember_note("Review documentation on cloud credentials flow.")
        recent = manager.get_recent_notes(limit=2)
        assert len(recent) == 2, "Failed to retrieve the correct number of recent notes."
        
        # 4. Test Structured Memory (Simulation - Requires a specific ID/Fact)
        print("\n--- Testing structured memories ---")
        dummy_id = str(uuid.uuid4())
        manager.memory_data['structured_facts'][dummy_id] = {'fact': 'Dummy fact for testing.', 'source_date': datetime.now().isoformat()}
        # In a real flow, we would now use add/update methods with this dummy ID.
        
        # 5. Final Persistence (Critical step)
        print("\n--- Testing final save ---")
        manager.force_sync_goals()
        print("Memory Manager tests complete and state saved.")

if __name__ == "__main__":
    MemoryManager.test_memory_manager()