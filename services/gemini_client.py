import os
from google.generativeai import GeminiClient
from google.generativeai import GenerationConfig
from google.generativeai.types import SafetySetting

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_TIMEOUT = 30
GEMINI_SAFETY_SETTINGS = [
    SafetySetting(category="BLOCK_HARASSMENT", severity="BLOCK_ONLY_HIGH"),
    SafetySetting(category="BLOCK_TOXICITY", severity="BLOCK_ONLY_HIGH"),
    SafetySetting(category="BLOCK_INSULTS", severity="BLOCK_ONLY_HIGH"),
    SafetySetting(category="BLOCK_NUDITY", severity="BLOCK_ONLY_HIGH")
]

class GeminiClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = GeminiClient(api_key=GEMINI_API_KEY)
        self.config = GenerationConfig(model=GEMINI_MODEL, temperature=0.7, top_p=0.9,
                                       max_output_tokens=2048, safety_settings=GEMINI_SAFETY_SETTINGS)

    def generate(self, prompt):
        try:
            response = self.client.generate_content(prompt=prompt, generation_config=self.config)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, messages):
        try:
            response = self.client.generate_content(history=messages, generation_config=self.config)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"