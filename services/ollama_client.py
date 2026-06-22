import requests
from typing import Optional

class OllamaClient:
    """
    A robust client wrapper for communicating with a local Ollama instance.
    The model used is gemma4:latest as per the project requirements (Gemma 4/Ollama).
    """
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "gemma4:latest"):
        self.base_url = base_url
        self.model_name = model_name

    def _api_call(self, payload: dict) -> Optional[str]:
        """Generic wrapper for sending the API request and handling common network errors."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                f"{self.base_url}/api/generate", 
                json=payload, 
                headers=headers, 
                timeout=120 # Set a generous timeout for LLM responses
            )
            response.raise_for_status() # Raises an HTTPStatusError if the status is 4xx or 5xx
            return response.json().get('response') # Return value directly (string)
        except requests.exceptions.ConnectionError:
            print(f"[CRITICAL][Ollama] CONNECTION FAILED: Is Ollama running at {self.base_url}?")
            return None
        except requests.exceptions.Timeout:
            print("[CRITICAL][Ollama] TIMEOUT ERROR: The API call took too long to respond.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR][Ollama] HTTP Error during request: {e}. Status Code: {response.status_code}")
            return None

    def check_connection(self) -> bool:
        """
        Verifies both connectivity to the API endpoint (Liveness) 
        and existence/usability of the specified model.
        Returns True if operational, False otherwise.
        """
        print("\n--- Ollama Connectivity and Model Check ---")
        # We pass a minimal prompt just to test connectivity and capability.
        test_payload = {
            "model": self.model_name,
            "prompt": "Test query.", 
            "stream": False,
            "options": {"temperature": 0.2}
        }

        # Use _api_call to evaluate connectivity/availability.
        result = self._api_call(test_payload)
        
        if result:
            print(f"✅ SUCCESS: Ollama reported connection, and '{self.model_name}' appears available.")
            return True
        else:
            # Failure diagnostic printing with correct f-string usage.
            print("❌ FAILURE: Connection or model verification failed. Please ensure:")
            print("""   1. The 'ollama serve' process is running in the background.""")
            print(f"   2. You have explicitly run 'ollama pull {self.model_name}' and that it succeeded.")
            return False

    def generate(self, prompt: str, system_context: Optional[str] = None) -> Optional[str]:
        """
        Generates text content from the local Ollama LLM endpoint.
        Returns a cleaned plain string response or None on critical failure.
        """
        if not self.check_connection():
            return None # Early exit if connection fails

        full_system_prompt = f"You are an expert AI Solutions Architect and Lead Engineer focused on career intelligence. You must strictly follow all constraints provided in your System Context block. Respond only with the requested output."
        if system_context:
            full_system_prompt += "\n\n[CURRENT CONTEXT]: " + system_context + "\n\n"

        user_query = f"{full_system_prompt}\n\n--- USER GOAL ---\n{prompt}"

        payload = {
            "model": self.model_name,
            "prompt": user_query, 
            "stream": False,  
            "options": {"temperature": 0.2}
        }

        print(f"\n[Ollama] Executing planning request using {self.model_name}...")
        result = self._api_call(payload)

        if result is None:
            return None

        # Clean up common LLM wrapping artifacts (e.g., markdown fencing, extra spaces)
        cleaned_result = result.strip()
        if cleaned_result.startswith("```markdown") or cleaned_result.startswith("```"):
            try:
                content_part = cleaned_result[3:].split('\n')[:-1]
                return "\n".join(content_part)
            except Exception:
                # Fallback in case splitting fails unexpectedly
                return cleaned_result
        
        return cleaned_result
