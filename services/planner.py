import os
from typing import Optional

# Assuming these classes exist in the project environment or are stubbed out/mocked for functionality demonstration
try:
    from .ollama_client import OllamaClient
except ImportError:
    print("Warning: ollama_client not found. Using a mock object.")
    class MockOllamaClient:
        def generate(self, prompt: str, system_context: Optional[str] = None) -> str:
            return "Mock LLM response based on the provided context and prompt."
    OllamaClient = MockOllamaClient

try:
    from .memory import MemoryManager
except ImportError:
    print("Warning: memory_manager not found. Using a mock object.")
    class MockMemoryManager:
        def get_latest_goal(self) -> Optional[str]:
            return "Analyze and formulate a precise career plan."
        def load_recent_notes(self) -> str:
            return "The user showed strong interest in AI/ML frameworks like PyTorch and TensorFlow, and expressed a desire for hands-on project experience over theoretical knowledge."
    MemoryManager = MockMemoryManager

class PlannerAgent:
    """
    Plans career trajectories based on user goals, memory context, and external LLM capabilities.
    """
    def __init__(self):
        # Initialize dependencies within the constructor
        self.ollama_client = OllamaClient()
        self.memory_manager = MemoryManager()

    def _build_context(self, goal: str) -> str:
        """
        Aggregates user goals and memory notes into a comprehensive context string 
        for the LLM model to use as system instructions.
        Returns the combined context string.
        """
        # Load necessary data sources
        latest_goal = self.memory_manager.get_latest_goal() or goal
        recent_notes = self.memory_manager.get_recent_notes()

        # Build the system instruction/context block
        combined_context = f"Primary Goal: {latest_goal}\n\nUser Context (Notes): {recent_notes}"
        return combined_context

    def generate_career_plan(self, goal: str) -> str:
        """
        Drives the planning process by gathering context and sending a request to Ollama.
        
        Args:
            goal: The specific career goal string for this run (e.g., "AI Engineer").

        Returns:
            A string containing the LLM's formatted response plan.
        """
        # 1. Build the system-wide context from memory and goals
        system_context = self._build_context(goal)

        # 2. Construct the full prompt for Ollama
        prompt = f"Using all provided context, generate a detailed, actionable career plan to achieve the goal: '{goal}'. The plan should be structured with phases (e.g., Phase I, II), specific skills to acquire, and recommended projects."

        # 3. Send the request to Ollama
        print(f"--- Sending request to Ollama using system context ---")
        response = self.ollama_client.generate(
            prompt=prompt,
            system_context=system_context
        )
        return response


if __name__ == "__main__":
    planner = PlannerAgent()
    print("--- Generating Career Plan for AI Engineer ---")
    result = planner.generate_career_plan("AI Engineer")
    print("\n===============================")
    print(result)