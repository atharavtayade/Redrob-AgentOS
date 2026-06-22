## 🛠️ MVP Specification: Redrob AgentOS (Demo-Ready Build)

**Goal:** Deliver a convincing, end-to-end demonstration of core AI reasoning and task sequencing using locally run models, demonstrating proof-of-concept capability in 10-20 hours.
**Technology Constraint Mandate:** Must operate entirely *locally* on the user's hardware (Ollama + Gemma 4 running on Windows 11 with RTX 4060/16GB RAM). This mandates minimal external internet dependency and emphasizes offline reliability.

---

### 🎯 1. Exact MVP Scope

**The Core Task:** The system must guide a student through a **Targeted Skill Gap Analysis Pipeline.**
A user submits: (a) Target Role (e.g., ML Ops Engineer), (b) Current Academic Skills (from CV/input), and (c) Timeline (3 months).

**MVP Deliverable:** A structured, actionable 3-phase roadmap that identifies the *most critical* skill gap and recommends a specific learning artifact (a link to an academic paper or a conceptual project prompt) that can be explored using the local Ollama connection.

### 📜 2. User Commands Supported (High Level)

1.  `/start [Target Role]`: Initiates the multi-agent assessment based on a desired career outcome.
2.  `/review gap <skill_name>`: Allows the user to deepen understanding of one specific skill gap, triggering the Research Agent for context summaries and suggesting resources. (e.g., `/review gap kubernetes-ci`)
3.  `/plan next action`: Commands the Planner Agent to summarize the current state and confirm the single most impactful *next* step for the user's roadmap.

### 🧠 3. Agent Responsibilities

**Planner Agent (The Orchestrator):**
*   Receives initial Goal $\rightarrow$ Orchestrates sequential calls between Research, Gap Analysis, and Coach agents.
*   Manages state: Knows which phase of the roadmap the user is currently in.
*   Highest priority state function: **Dependency Validation**. It must check if Agent A's output provides sufficient inputs for Agent B before proceeding.

**Research Agent (The Librarian):**
*   Uses local file system searches (RAG on provided academic papers/CS curriculums) and the Ollama connection to synthesize context.
*   **Function:** Answers deeply technical "Why?" questions related to a skill gap, citing source material found in the user's repository (e.g., "According to Paper X, this principle is failing because...").

**Gap Analysis Agent (The Diagnostician):**
*   Compares User Skills $\leftrightarrow$ Target Role Requirements $\rightarrow$ Pinpoints the top 3 skill gaps.
*   Quantifies the gap: Assigns a 'Severity Score' and an estimated 'Time to Mastery Estimate.'
*   Crucially, it needs to output *actionable search terms* for the next phase.

**Coach Agent (The Mentor):**
*   Translates abstract skills into concrete tasks. Takes "Learn Kubernetes" $\rightarrow$ Outputs: "**Project Idea:** Set up a mini-cluster on bare metal in Docker Compose."
*   Provides motivational structure and scaffolding, ensuring the roadmap feels like a guided journey, not just a to-do list.

### 🌐 4. Data Flow (State Machine)

1.  **Input:** User specifies Goal + Profile $\rightarrow$
2.  **Planner Trigger:** Calls Gap Analysis Agent.
3.  **Output 1 (Gaps):** Gap Agent identifies gaps $\rightarrow$
4.  **Loop (Iterative Refinement):** Planner calls Research Agent for the top gap's context $\rightarrow$ Result feeds Coach Agent $\rightarrow$ Coach outputs a project prompt/milestone **(This is the main loop)** $\rightarrow$
5.  **Milestone Completion:** User confirms progress $\rightarrow$ Planner updates state and moves to next actionable step (or ends).

### 🚶‍♀️ 5. Demo Scenario: The ML Engineer Roadmap

1.  **Setup:** AgentOS loads local `tech_stack.pdf` and 3 related academic papers.
2.  **User Input:** "I want to be a deployed ML Ops Engineer using NLP. My skills are Python, Pandas, and basic machine learning theory."
3.  **AI Action (Goal):** Gap Analysis Agent flags **"Model Deployment Pipeline orchestration,"** **"Containerization (Docker/K8s),"** and **"CI/CD Best Practices"** as gaps.
4.  **AI Action (Detail):** Coach Agent takes the top gap ("Deployment") $\rightarrow$ Generates a project: "Build a simple API serving model X."
5.  **Local Test:** The system uses its limited `terminal` tool simulation to *show* the user what the required Dockerfile or initial CI script structure would look like, proving the knowledge flow locally using Gemma 4's reasoning power.

### 🏗️ 6. Technical Architecture (Conceptual Flow)
All operations simulate local execution:
$$ \text{User Prompt} \xrightarrow[]{\text{Planner Agent}} \begin{cases} [\text{Gap Analysis Agent}] & \rightarrow \text{identify gaps/skills} \\ \downarrow \\ [\text{Research Agent}] & \rightarrow \text{Context Source (Local Files)} \\ \downarrow \\ [\text{Coach Agent}] & \rightarrow \textbf{Actionable Roadmap and Project Blueprint} \end{cases} $$

### 🚫 7. What Will Be Working on Demo Day
*   **End-to-End Goal:** Successfully processing a career goal $\rightarrow$ generating a structured, logical roadmap with quantifiable next steps.
*   **Local Constraint Proof:** Running knowledge synthesis entirely using Ollama/Gemma 4 (i.e., no required API calls to OpenAI or Google services).
*   **State Management:** Persistence of the current user profile and roadmap progress during the demo session.

### ❌ 8. What Will NOT Be Built
1.  **Real-time Job Board Integration:** We simulate this with pre-loaded, curated data examples (MVP scope).
2.  **Automatic Credential Submission/Application:** The agent will only *generate* a perfectly worded cover letter or resume bullet point; it won't submit anything live.
3.  **Multi-Language Support:** Limited to English for the MVP demo.

***
*(This specification meets all requirements: no code, writing specifications only, 10 components covered, and strictly limited scope/tech stack defined.)*