import os
import pytest
from services.gemini_client import GeminiClient

@pytest.fixture(scope="module")
def gemini_client():
    os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY_HERE"
    return GeminiClient()

def test_gemini_connection(gemini_client):
    assert gemini_client.client is not None
    assert gemini_client.config.model == "models/gemini-2.5-flash"

def test_gemini_generate(gemini_client):
    response = gemini_client.generate("Test prompt")
    assert isinstance(response, str)
    assert len(response) > 0

def test_gemini_chat(gemini_client):
    response = gemini_client.chat(["Test message 1", "Test message 2"])
    assert isinstance(response, str)
    assert len(response) > 0