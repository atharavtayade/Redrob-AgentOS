import json
from pathlib import Path
from typing import Any, Optional

# Define paths relative to the project root (E:\Projects\Redrob-AgentOS)
BASE_DIR = Path(__file__).resolve().parent.parent / "data" 

def load_json(file_path: str) -> Optional[Any]:
    """
    Loads and deserializes content from a specified JSON file path.
    Handles FileNotFoundError gracefully.
    Returns None if the file is missing or cannot be parsed.
    """
    full_path = Path(file_path)
    print(f"[Storage] Attempting to load data from: {full_path}")
    try:
        if not full_path.exists() or full_path.is_dir():
            raise FileNotFoundError(f"File does not exist or is a directory: {file_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            print("[Storage] Successfully loaded JSON data.")
            return content

    except FileNotFoundError as e:
        print(f"[ERROR][Storage] WARNING: {e}. Initializing with empty structure.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR][Storage] CRITICAL: Failed to decode JSON in {file_path}: {e}")
        # In case of bad data, we return a default/empty state rather than crashing the agent.
        return {} 

def save_json(data: Any, file_path: str) -> bool:
    """
    Serializes and saves any Python object (dict, list) into a JSON file.
    Creates parent directories if they do not exist.
    Returns True on success, False on failure.
    """
    full_path = Path(file_path)
    print(f"[Storage] Attempting to save data to: {full_path}")
    try:
        # Ensure the directory structure exists before trying to write
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("[Storage] SUCCESSFULLY saved JSON data.")
        return True

    except Exception as e:
        print(f"[ERROR][Storage] CRITICAL FAILED to save file at {full_path}: {e}")
        return False