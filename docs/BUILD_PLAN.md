***# Redrob AgentOS - Minimum Viable Product (MVP) Build Plan***

***Disclaimer:** This plan assumes foundational infrastructure is in place (e.g., core Python environment, git repository initialized). The estimated build time is scoped for a single, proficient engineer and targets a 10–20 hour completion window.*

## 💡 Project Goal
To create a functional internal agentOS prototype demonstrating the core loop: User Intent $\rightarrow$ Planning $\rightarrow$ Execution (Tools/Skills) $\rightarrow$ Output. The MVP should prove end-to-end task completion capability without solving all known bugs or integrating every niche tool.

---

## 1. Folder Structure Required for MVP
The repository structure must be clean, separating core logic from dynamic assets and knowledge bases.

```markdown
Redrob-AgentOS/
├── .venv/                      # Virtual environment
├── redrob_agentos/             # Core package directory (Python module)
│   ├── __init__.py
│   └── core/                   # Main Agent Logic & Orchestration
│       ├── agent.py            # The primary agent loop orchestrator
│       ├── planner.py          # Responsible for task breakdown and tool selection
│       └── executor.py         # Runs external commands, file patches, etc. (Terminal wrapper)
├── skills/                     # Directory for reusable procedures (Skills directory)
│   ├── __init__.py
│   └── builtin_skills/        # Simple, pre-packaged initial skill definitions (.md or .yaml)
├── data/                       # Persistent or simulated operational data store
│   └── knowledge_base.sqlite  # Initial local database for structured state (e.g., inventory, user profiles)
├── tests/                      # Unit and integration tests
│   ├── test_agent_loop.py     # Core agent loop testing
│   └── test_tools.py          # Testing individual tool wrappers
├── requirements.txt           # Project dependencies (PyPI packages)
└── README.md                   # Quick start guide & project overview
```

## 2. Python Files Required
*   `redrob_agentos/core/agent.py`: The main function that receives user input, invokes the planner, and manages the execution loop until completion or failure.
*   `redrob_agentos/core/planner.py`: Logic dedicated to interpreting natural language requests into structured plans (e.g., a series of steps: `[STEP_1: Read file X]`, `[STEP_2: Call API Y]`).
*   `redrob_agentos/core/executor.py`: A wrapper class handling the physical execution of tools, managing standard I/O streams, and logging tool calls for auditing.
*   `skills/builtin_skills/__init__.py`/`.md`: Placeholder files defining 2-3 core skills (e.g., `file-read`, `web-search`).

## 3. Responsibilities of Each File
| File Path | Responsibility | Notes |
| :--- | :--- | :--- |
| `agent.py` | **Orchestration/Lifecyle:** Controls the agent's state machine (Input $\rightarrow$ Plan $\rightarrow$ Execute $\rightarrow$ Output). This is the entry point for the agent. | Must handle retries and complex failure paths gracefully. |
| `planner.py` | **Reasoning/Decomposition:** Takes user input, determines feasibility, generates a step-by-step action plan (tool calls, system interactions), and predicts potential errors/ambiguities. | Should be the most "intelligent" module, possibly using an internal LLM call (or placeholder). |
| `executor.py` | **Action/Execution:** Acts as the reliable interface to the operating environment (terminal, file system, external APIs). It sanitizes inputs and captures outputs for logging. | Must ensure robust error handling for non-zero exits from shell commands. |
| `data/knowledge_base.sqlite` | **State Storage:** Stores persistent data that agents interact with over multiple sessions or tasks (e.g., user defined credentials, project constants). | Simple SQLite schema is sufficient for MVP. |

## 4. Data Storage Format
The primary storage format will be **SQLite**.

*   **Location:** `data/knowledge_base.sqlite`
*   **Structure:** Tabular records are preferred (e.g., Key-Value pairs, or structured JSON blobs for complex entities).
*   **Reasoning:** Using SQL provides ACID guarantees and is simple to integrate into Python environment wrappers without requiring external services for the MVP scope.

## 5. Ollama Integration Approach
The agent should treat Ollama as a **predictable backend model provider**, not just an endpoint.

1.  **Standardization:** All LLM interactions (for planning or reasoning) must be abstracted behind a `LLMClient` interface that currently calls the Ollama API (`ollama run <model>`).
2.  **Context Inclusion:** The agent's prompt/context for any task must include instructions on how to handle tool output, error codes, and data references from `data/knowledge_base.sqlite`.
3.  **Model Choice (MVP):** Use a single, known model (e.g., Llama 3) via Ollama for consistency during the build phase.

## 6. User Interaction Flow
1.  **Input:** User provides an ambiguous or complex goal via text prompt.
2.  **Planning Stage (Planner):** Agent captures state, consults `knowledge_base.sqlite`, and outputs a structured plan (internal representation: JSON array of steps).
3.  **Execution Stage (Executor/Tools):** The agent iterates through the planned steps. For each step, it calls the appropriate tool (`read_file()`, `terminal()`, etc.).
4.  **Feedback Loop:** Tool output is captured and fed back into the *Planner* (or a dedicated state-updater) for re-evaluation until the required outcome is achieved or a terminal error occurs.
5.  **Output:** Final synthesized answer presented to the user, summarizing successful steps and any remaining ambiguities.

## 7. Demo Workflow
A highly controlled, simple end-to-end task: **"Find all Python files over 100 lines in the `redrob_agentos/` directory, summarize their purpose, and tell me which file is the primary orchestrator."**

*   **Steps:** $\rightarrow$ Tool Search (`search_files`) $\rightarrow$ Loop Read ($\times N$) $\rightarrow$ Summary Generation (Planner/LLM) $\rightarrow$ Final Report.
*   **Expected Success State:** A polished summary identifying `agent.py` as the main orchestrator module.

## 8. Exact Implementation Order
1.  **Phase 1: Foundation (20% of time)**
    *   Setup Folder Structure & Basic Dependencies (`requirements.txt`).
    *   Implement robust File I/O and CLI Wrapper (`executor.py` using `terminal` calls). Focus on error handling first.
    *   Wire up Ollama Client Interface into `agent.py`.
2.  **Phase 2: Core Logic (60% of time)**
    *   Develop the Planning Module (`planner.py`) to output structured plans from text prompts.
    *   Implement the State Loop in `agent.py`: Looping plan steps, calling executor, and passing results back for re-planning.
    *   Integrate basic state management with SQLite (Read/Write functions).
3.  **Phase 3: Polish & Testing (20% of time)**
    *   Build the Demo Workflow end-to-end in a dedicated test environment.
    *   Create stubbed skills and initial README/Usage guide.
    *   Refactor plans into clean, separated functional units.

## 9. Estimated Build Time Per Component
| Component | Effort Estimate (Hours) | Key Dependencies / Risks |
| :--- | :--- | :--- |
| **Setup/Structure** | 1 hr | Low risk; involves file system setup and tooling wrapper basics. |
| **`executor.py` & Tooling** | 3–4 hrs | Medium risk: Shell command quoting, I/O stream management complexity. Must be rock solid before proceeding. |
| **SQLite State Mgmt.** | 2–3 hrs | Low to Medium risk; schema design is critical but localized. |
| **`planner.py`** | 4–6 hrs | High risk: This module requires accurate LLM prompt engineering and complex parsing of structured output from the model. |
| **`agent.py` Loop/Orchestration** | 3–4 hrs | Medium to High risk; managing the state machine, failure modes, and retries is non-trivial. |
| **Documentation & Testing** | 2 hr | Low complexity; focused effort on writing thorough tests for existing logic. |

## 10. Definition of Done (MVP Complete)
The project is "Done" when:
1.  A single run from the `agent.py` entry point successfully completes the **Demo Workflow** (Section 7).
2.  All major components (`agent.py`, `planner.py`, `executor.py`) are passing their unit tests in the `tests/` directory.
3.  The successful run generates a useful summary report that accurately reflects the user's original intent and the steps taken to achieve it, without any manual intervention (no needed debugging or code modification *after* the initial successful test).

---