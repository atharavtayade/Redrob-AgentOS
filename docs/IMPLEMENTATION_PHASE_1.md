# 🚀 Redrob AgentOS: Implementation Phase 1 Blueprint

**Role:** Lead Software Engineer
**Goal:** Create a perfect, actionable blueprint for coding execution (Day 1 focus).
**Constraint:** Zero architecture documents. Write only technical requirements.

---

## 1. Final Project File Tree Structure

The project will be tightly organized to enforce separation of concerns:

```plaintext
E:\Projects\Redrob-AgentOS/
├── __init__.py               # Main package marker
├── main.py                   # The entry point and orchestration layer (Streamlit interface loader)
├── requirements.txt          # Minimal Python dependencies for Phase 1 setup.
│
├── storage/                  # Persistence Layer: Abstraction for loading/saving structured data.
│   ├── __init__.py
│   └── storage_manager.py    # Handles file I/O, JSON serialization/deserialization, and schema validation checks.
│
├── models/                   # Data Definition Layer: Implements Pydantic schemas to ensure type safety across the system.
│   ├── __init__.py
│   ├── user_profile_schema.py # Defines structure for user data (The "Who").
│   └── memory_schema.py      # Defines structure for stored knowledge/skills (The "What").
│
└── services/                 # Business Logic Layer: Contains stateless, testable components.
    ├── __init__.py
    ├── ollama_client.py      # Wrapper class handling all API calls to Ollama.
    ├── planner.py            # Module responsible for structured task decomposition (the 'brain').
    └── analyzer.py           # Module containing specific intelligence functions (Gap Analysis, Recs).
```

## 2. Python Files to Build First (Phase 1 Focus)
These files establish the foundations required *before* any complex logic can be built:

1.  `requirements.txt`: Establishes dependencies (e.g., `pydantic`, `streamlit`, `requests`).
2.  `storage/storage_manager.py`: Must be implemented and tested first, as nearly every other file depends on it for data access.
3.  `models/user_profile_schema.py`: Defining the data contract for user identity.
4.  `models/memory_scope.py`: Defining the data contract for persistent knowledge.
5.  `services/ollama_client.py`: Establishing connectivity to Ollama.

## 3. `requirements.txt` Contents (Minimal Dependencies)
We must keep this small and controlled.
```text
pydantic>=2.0 # Used in 'models/' for structured data validation.
streamlit>=1.0 # Required for the UI frontend/driver.
requests>=2.31 # General HTTP client for communicating with Ollama API.
python-dotenv # For safely loading required environment variables (e.g., model names).
```

## 4. JSON Schemas Definition (Data Contracts)

### A. `user_profile.json` Schema
(Schema definition stored in `models/user_schema.py`)
*   **Purpose:** Stable, identity-defining source of truth.
*   **Fields:**
    *   `name: str` (Required)
    *   `current_role: str` (e.g., Junior Engineer)
    *   `target_domain: str` (The desired career field/industry)
    *   `core_skills: list[str]` (Key skills the user currently possesses, e.g., ["Python", "AWS Basics"])
    *   `years_experience: float`

### B. `memory.json` Schema
(Schema definition stored in `models/memory_schema.py`)
*   **Purpose:** Captures reusable knowledge and temporary state (RAG context).
*   **Structure:** Dictionary where keys are named categories, and values are lists of facts.
*   **Example Data Structure:**
    ```json
    {
        "career_insights": [
            {"id": "c1", "fact": "Product Management requires familiarity with Agile sprints.", "source_date": "2026-01-15"}
        ],
        "technical_standards": [
            {"id": "t1", "fact": "The standard Python packaging library is Poetry.", "source_date": "2025-05-01"}
        ]
    }
    ```

## 5. Ollama API Integration Strategy (Abstraction Layer)
The `services/ollama_client.py` must act as a black box wrapper around the direct REST calls to the local Ollama instance (`http://localhost:11434`).

*   **Function Signature:** All complex user-facing calls are unified under one method, e.g., `LLMClient.generate(system_prompt: str, context: dict, user_query: str) -> str`.
*   **System Prompt Control:** The integration strategy must mandate that the system prompt is *always* constructed by combining two pieces of data before sending to Ollama:
    1.  The hard-coded instructions for the Agent (e.g., "You are a helpful Product Manager...").
    2.  The retrieved, formatted context from `memory_schema.json`/`user_profile.json`.
*   **Model Pinning:** All calls must use the pinned model name defined in the environment variables (`GEMMA4:latest`).

## 6. Streamlit Page Layout (Desired User Experience)
The UI should be clean, linear, and professional—like a single interactive whiteboarding tool.

1.  **Header:** Project Name/Branding ("Redrob AgentOS").
2.  **Input (Top):** Large text input area for the user's ambiguous Goal/Intent.
3.  **Controls:** A simple "Analyze & Plan" button.
4.  **Main Output Area (Scrollable Timeline):** This is the core display, visualizing the state machine flow:
    *   **A.** **Initial Context Display:** Shows what data was loaded (`Profile Loaded`, `Memory Retrieved`).
    *   **B.** **The Plan:** Displays the structured sequence of steps detected by the Agent.
    *   **C.** **Execution Log:** Detailed, step-by-step breakdown showing Input $\rightarrow$ Tool Called $\rightarrow$ Output Received $\rightarrow$ Next Thought (Narrative representation).
    *   **D.** **Final Deliverable:** The polished 90-day roadmap/report.

## 🧠 7. Build Order for Day 1 (The Atomic Steps)

This sequence minimizes dependencies and builds confidence layer by layer.

1.  **Setup Environment:** Write `requirements.txt` and project folder structure (`write_file`).
2.  **Data Contracts:** Implement the models using Pydantic (`models/*.py`). Test saving/loading placeholder data via `storage_manager.py`.
3.  **API Proxy:** Implement `ollama_client.py`. Write a simple helper function to confirm text generation from Ollama is working with placeholders (e.g., "Hello World").
4.  **Service Skeleton:** Build basic stubs for `planner.py` and `analyzer.py` that accept structured input (Profile, Memory) and return abstractly parsed results, relying on the LLM client only at the very final step.
5.  **Orchestration Test:** Implement a barebones `main.py` stub that initializes the services but does *not* run the full loop yet. Its sole purpose is to successfully launch the Streamlit shell and display static UI headers.

---
**Conclusion:** By following this precise, step-by-step blueprint, we guarantee demonstrable progress every day. We avoid building complex features until the core data flow (Plan $\rightarrow$ Execute $\rightarrow$ Store) is 100% stable.