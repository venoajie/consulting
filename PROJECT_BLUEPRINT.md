
<!-- FILENAME: PROJECT_BLUEPRINT_V1.1.md -->
```markdown
# PROJECT BLUEPRINT: Tax Co-Pilot

- **version**: 1.1
- **status**: IN_PROGRESS
- **goal**: "Create a secure, scalable, and production-ready RAG-based web application to provide AI-assisted tax analysis."

---
## 1. Core Architectural Principles

- **version**: 1.0
- **status**: PENDING_BOOTSTRAP
- **goal**: "Create a secure, scalable, and production-ready RAG-based web application to provide AI-assisted tax analysis."

---
## 1. Core Architectural Principles

This project is governed by six non-negotiable principles:

1.  **The Principle of the Canonical Blueprint:** This document is the single source of truth for the project's state, architecture, and plan. It is the input and output of every major interaction.
2.  **The Principle of Stateful Orchestration:** Development is managed via a stateful command loop. The AI Program Manager (`core/pmo-1-sre`) analyzes this blueprint and issues a precise "Next Command" for the developer to execute.
3.  **The Principle of "Investigate then Act":** All analysis and recommendations must be grounded in verifiable evidence, gathered through active investigation of project artifacts.
4.  **The Principle of Critical Partnership:** The AI partner is obligated to challenge flawed premises or requests that conflict with established principles, explaining the risks and proposing superior alternatives.
5.  **The Principle of Structured Contracts:** All outputs must adhere to a strict contract, separating `Analysis & Plan` from `Generated Artifacts`. Data contracts will be defined in a machine-readable format (`docs/system_contracts.yml`).
6.  **The Principle of Environmental Realism:** All technical choices must be validated against the target production environment: **Oracle Cloud Infrastructure (OCI), Oracle Linux 10 (`aarch64`)**.

---
## 2. Persona & Interaction Model

-   **AI Persona:** `core/pmo-1-sre` (Program Manager & Site Reliability Engineer). This persona orchestrates the project.
-   **Interaction Model (The Command Loop):**
    1.  **Developer:** Executes the precise shell command provided in the "Next Command" section.
    2.  **AI Orchestrator:** Receives the developer's report, updates this blueprint to reflect the new state, provides analysis for the next task, and issues the next command.

---
## 3. Architectural Decisions Record (ADR)

-   **ADR-001: Framework Choice:** **FastAPI over Django.** Justification: FastAPI's native asynchronous support, performance, and Pydantic-based data validation are perfectly suited for an I/O-bound, API-first application.
-   **ADR-002: Ingestion Pipeline:** **"Keep It Simple" Function (for MVP).** Justification: A single OCI Function provides the fastest path to a working ingestion pipeline for our initial, simple document formats, deferring the complexity of a Queue/Worker model.
-   **ADR-003: Deployment Model:** **Direct Deployment (Systemd/Gunicorn).** Justification: Avoids the unnecessary complexity of Docker networking for a single-VM deployment, simplifying debugging and management for the MVP.
-   **ADR-004: Authentication:** **Static API Key (for MVP).** Justification: Delivers a secure-enough solution for a private beta without the significant upfront effort of integrating a full identity provider, allowing focus on core AI features.

---
## 4. Environment & Deployment Constraints

-   **Cloud Provider:** Oracle Cloud Infrastructure (OCI)
-   **Host System:** Oracle Linux 10 (`aarch64`)
-   **Key Risks & Mitigations:**
    -   **ARM (`aarch64`) Dependency Risk:** High probability of Python packages requiring source compilation. **Mitigation:** All dependencies will be vetted, and an early integration test will be performed on the target VM to identify build failures immediately.
    -   **OCI Service Compatibility:** OCI Agent plugins may be unsupported on ARM. **Mitigation:** We will prefer the OCI Python SDK over platform-specific plugins for all integrations.

---
## 5. Service Architecture & Data Flow

The system consists of two primary workflows:

1.  **Asynchronous Ingestion Pipeline:** `File Upload (OCI Object Storage) -> OCI Event -> OCI Function (Parse, Embed) -> Write to PostgreSQL`.
2.  **Synchronous RAG API:** `User Request -> FastAPI API -> Embed Query -> Query PostgreSQL -> Build Prompt -> Call LLM -> Stream Response`.

---
## 6. Data & State Contracts

The canonical source for all data contracts (API request/response models, database schemas) will be a machine-readable file: `docs/system_contracts.yml`. This file will be used to programmatically generate runtime validation schemas and documentation.

---
## 7. Governance & Testing Protocols

### RAG Pipeline Integrity

1.  **Health & Robustness:** The CI pipeline **MUST** include a "Sanity Check" step after any knowledge ingestion to verify that the number of indexed documents is above a reasonable threshold, preventing silent data exclusion.
2.  **Effectiveness:** We **MUST** create a "Golden Set" of evaluation questions in `tests/rag_evaluation_set.yml`. An automated script (`scripts/evaluate_rag.py`) will run against this set as a CI quality gate to prevent regressions in answer relevance.
3.  **Efficiency:** Indexing time and query latency **SHOULD** be monitored to track performance over time.

---
## 8. Known Failure Modes & Recovery Strategies

-   **Failure Mode:** "Poison Pill" document in the ingestion pipeline causes the OCI Function to repeatedly fail.
    -   **Likely Cause:** A malformed or corrupted file (PDF, DOCX) that the parsing library cannot handle.
    -   **Recovery:** 1. Check OCI Function logs to identify the failing object name. 2. Manually move the problematic object from the 'inbox' bucket to a 'quarantine' bucket. 3. The pipeline will automatically resume processing the next files. 4. Analyze the quarantined file offline.

-   **Failure Mode:** RAG API returns irrelevant context, or answers are nonsensical.
    -   **Likely Cause:** 1. Mismatch between the embedding model used for ingestion and the one used at query time. 2. Low-quality source documents. 3. A regression in the "Golden Set" evaluation has gone unnoticed.
    -   **Recovery:** 1. Immediately run the `scripts/evaluate_rag.py` script to get a baseline metric. 2. Verify the embedding model name in the application configuration matches the model used during ingestion. 3. Review the source documents related to the failing queries.

---
## 9. Project Plan & Dependency Chain

### Phase 1: Foundation & Infrastructure
-   **Objective:** Prepare the cloud and local environments for development.
-   **Specialist:** Developer (guided by `core/pmo-1-sre`)
-   **Status:** **PENDING**
-   **Inputs:** N/A
-   **Output:** A working local development environment and provisioned cloud resources.

### Phase 2: Asynchronous Ingestion Pipeline
-   **Objective:** Build the automated pipeline for populating the vector database.
-   **Specialist:** Developer (guided by `core/pmo-1-sre`)
-   **Status:** BLOCKED (depends on Phase 1)

### Phase 3: Core RAG API
-   **Objective:** Build the user-facing API for asking questions.
-   **Specialist:** Developer (guided by `core/pmo-1-sre`)
-   **Status:** BLOCKED (depends on Phase 2)

### Phase 4: Integration, Security & Deployment
-   **Objective:** Secure the API and deploy the full application to OCI.
-   **Specialist:** Developer (guided by `core/pmo-1-sre`)
-   **Status:** BLOCKED (depends on Phase 3)
---
## 9. Project Plan & Dependency Chain

### Phase 1: Foundation & Infrastructure
- **Objective:** Prepare the cloud and local environments for development.
- **Specialist:** Developer (guided by `core/pmo-1-sre`)
- **Status:** **IN_PROGRESS**
- **Inputs:** N/A
- **Output:** A working local development environment and provisioned cloud resources.

### Phase 2: Core project directory and file structure according to the principle of Separation of Concerns.
*   `app/`: **The Application Core.**
    *   **Why:** This directory is the heart of your installable Python package. All application-specific logic lives here, cleanly separating it from project-level files like `pyproject.toml` or `docs/`.

*   `app/main.py`: **The Entrypoint.**
    *   **Why:** This file will initialize the FastAPI application instance. It's the single, clear starting point where you will mount your API routers. It should contain minimal logic beyond assembly.

*   `app/api/`: **The Web Layer (The Front Door).**
    *   **Why:** This directory will contain your FastAPI routers and endpoint definitions. Its sole responsibility is to handle HTTP requests, validate incoming data using schemas, and return HTTP responses. It **should not** contain any business logic. This prevents your business logic from being tightly coupled to the web framework.

*   `app/services/`: **The Business Logic Layer (The Brain).**
    *   **Why:** This is the most important directory. It contains the core business logic of your application—the "how" things get done. The entire RAG process (embedding queries, building prompts, calling the LLM) will live here. The API layer will simply call functions or methods from this layer. This makes your logic highly testable and reusable.

*   `app/schemas/`: **The Data Contracts.**
    *   **Why:** This directory will contain all your Pydantic models. These models define the explicit shape of your API data, database objects, and internal data structures. This enforces data integrity at the boundaries of your system and provides automatic validation, directly addressing the need for the strong contracts seen in your other projects.

*   `app/repositories/`: **The Data Access Layer.**
    *   **Why:** This directory will abstract all direct interactions with the PostgreSQL database. It will contain functions like `find_similar_chunks(...)` that encapsulate the SQL or ORM queries. Your `services` will call these functions. This isolation means if you ever wanted to change how you access data, you would only need to change it in one place.

*   `app/core/`: **The Central Nervous System.**
    *   **Why:** This is for project-wide concerns like configuration loading (`config.py`), logging setup, and database session management. Placing these here prevents circular dependencies and provides a single source for essential configurations.

*   `tests/`: **The Safety Net.**
    *   **Why:** A dedicated directory for all your tests. The structure inside `tests/` should mirror the structure of `app/` (e.g., `tests/services/test_rag.py`). This makes it easy to find tests and encourages a culture of testing.

*   `scripts/`: **The Toolbox.**
    *   **Why:** For operational or one-off scripts that are part of the project but not the core application, such as our `evaluate_rag.py` or a script to perform a manual data backfill.

*   `docs/`: **The Constitution Hall.**
    *   **Why:** As mandated by our blueprint, this is where the canonical, version-controlled sources of truth for our project will live, starting with `system_contracts.yml`.
