# 💡 Redrob AgentOS: Final MVP Scope Definition

**Role:** Senior AI Solutions Architect
**Project Target:** Hackathon Winning Prototype (Max Impact, Min Hours)
**Architecture Constraint:** Local-First Agents using Ollama + Gemma 4

***Disclaimer: This document defines the optimal scope for a focused 30–40 hour hackathon effort. Strict adherence to these boundaries is mandatory to ensure completion with demonstrable working functionality.***

## ✅ 1. Features We MUST Build (Core Intelligence Loop)
These features are non-negotiable minimums required to prove the agent's capability and establish the core technical pillars.
1.  **Goal Ingestion & Planning:** Accepts a complex user goal (e.g., "I want to transition from X role to Y field"). The Agent must break this down into 3-5 discrete, actionable steps.
2.  **Profile Loading (`USER_PROFILE`):** Successfully loads the core profile data (Experience, Skills, Interests) as verifiable JSON/SQLite content and uses it in decision-making.
3.  **Context Retrieval (RAG Mini):** Run a targeted search over the local database/profile to pull out specific supporting facts relevant to the current plan step (e.g., "You have experience with Python," or "Your profile lists Agile methodology").
4.  **Roadmap Generation:** The final output must be a multi-stage, actionable 30/60/90 day timeline structured as markdown text by the Agent.

## ✨ 2. Features We SHOULD Build (Polish & Differentiators)
If time permits after achieving the MUST build goals, these elements provide significantly higher hackathon impact and "wow" factor.
1.  **Skill Gap Analysis:** Compare desired skills (from Goal/Industry data) against stored skills (from Profile). Output a clear gap report.
2.  **Certification Recommendations:** Suggest 3-5 highly relevant certifications based on the identified skill gaps.
3.  **Minimal Memory Persistence:** Implement saving the final `Roadmap` and `SkillGapReport` back to the user's persistent memory store.

## ❌ 3. Features We MUST NOT Build (Hard Scope Limits)
These are scope creep items that will burn time and must be strictly avoided.
1.  **Real-time Chat / Conversation History:** We treat input as a single, definitive job request, not an interactive dialogue.
2.  **External API Integration:** No connections to LinkedIn, GitHub, remote APIs, or email services (keep it 100% local).
3.  **Multi-user Support:** The agent operates on one user profile per session.
4.  **Dynamic Skill Learning Loop:** We use pre-defined models/skills; we are not building a continuous self-improvement loop that trains the model.

## ⚙️ 4. Agent Architecture: State Machine Approach
The agent must run as a deterministic state machine, managed by `main.py`.
*   **Input $\rightarrow$ Planner:** User intent enters the system. The **Planner Module** (LLM call) receives the input and mandatory context (`Profile`, `Memory`) and outputs a structured plan (e.g., JSON: `[{"step": "Analyze skills", "tool": "Analyzer", "input": ...}, {"step": "Generate roadmap", "tool": "Synthesize", "input": ...}]`).
*   **Execution $\rightarrow$ Executor:** The **Executor Module** iterates through the plan, executes the designated tool/service call, and captures a verbose result.
*   **Feedback Loop:** The output of each tool execution is passed back to the Planner (or an internal refinement module) for validation or modification before proceeding to the next step, mimicking iterative reasoning.

## <0xF0><0x9F><0x97><0x84>️ 5. RAG Architecture: Local Vector Indexing Simulation
We will simulate a functional Retrieval Augmented Generation (RAG) pattern using local JSON storage indexes, avoiding the complexity of setting up a true vector database like Chroma or Pinecone.
*   **Source Chunking:** All stored `User Profiles` and historical `Knowledge Base` facts are treated as "chunks."
*   **Retrieval Mechanism:** When planning, the Agent uses optimized search queries (via `storage_manager`) to retrieve the top 3 most relevant fact chunks based on keywords from the current step's input.
*   **Context Injection:** These retrieved facts are then packaged and injected *directly* into the prompt sent to Gemma 4/Ollama as "System Context."

## 🧠 6. Memory Architecture: Dual Persistence Model
We separate memory into two functional, distinct mechanisms for clarity and future scale.
1.  **Profile Memory (Long-Term Identity):** Stored in `user_profile.json`. Contains the immutable facts about the user. *Frequency:* High priority; read at every step.
2.  **Working Memory (Short-Term Context/Knowledge Base):** Stored in `knowledge_base.json` (or SQLite placeholder). Represents captured knowledge from external sources or completed runs that must inform future planning. *Function:* Acts as the immediate shared factsheet for the current session and subsequent sessions.

## 💻 7. Streamlit UI Pages
Limiting complexity to a single-page application greatly minimizes deployment time.
1.  **`Page 1: The Core Engine (The Main View)`:** Single input box for the goal, a prominent "Run Agent" button, and structured output panels that dynamically populate:
    *   Plan Flow Diagram (Step 1 $\rightarrow$ Step 2...).
    *   Current State Context Snapshot.
    *   Final Roadmap/Report.

## 🎬 8. Demo Workflow & Judge Script
**Narrative:** "Goal-Oriented, Single Run." The demo should feel like a narrative revelation, not just code execution.
1.  **Judge Start:** User inputs ambiguous goal: *“I want to get into Product Management because I find the blend of user empathy and technical strategy fascinating.”*
2.  **Agent Output (Visible):** The agent displays its initial Plan/Thought Process ("Analyzing skills gap $\rightarrow$ Consulting target role requirements $\rightarrow$ Generating path...").
3.  **Technical Proof Point:** The plan reveals that the 'Planner' module successfully retrieved context that indicated: "User has strong Python background but needs market knowledge." (Proves RAG).
4.  **Conclusion:** The agent outputs a polished, highly structured 90-day roadmap, directly addressing the skill gap identified by comparing Profile vs. Goal.

## 🎯 9. Final Project Boundaries & Deliverables
*   **Scope Inclusions:** Core Agent Loop, Local File I/O (JSON), Ollama API proxy, Single-user state machine, and the output of a structured Roadmap report.
*   **Deliverable State:** A working Streamlit application launched by `main.py` that can accept user input and generate the roadmap artifact *without* manual intervention after clicking 'Run'.

***Optimize for Impact Checklist:***
*   $\square$ **Local/Offline Capable:** (Yes, Ollama + Local JSON)
*   $\square$ **Demonstrates Intelligence:** (Yes, Plan $\rightarrow$ Search Context $\rightarrow$ Generate Output)
*   $\square$ **Time Constraint Adherence:** (Yes, Limited to 30-40 hours by strict scope control)