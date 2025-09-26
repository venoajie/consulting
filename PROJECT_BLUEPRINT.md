
<!-- FILENAME: PROJECT_BLUEPRINT_V1.1.md -->
```markdown
# PROJECT BLUEPRINT: Tax Co-Pilot

- **version**: 1.1
- **status**: IN_PROGRESS
- **goal**: "Create a secure, scalable, and production-ready RAG-based web application to provide AI-assisted tax analysis."

---
## 1. Core Architectural Principles
... (sections 1-9 remain unchanged) ...

---
## 9. Project Plan & Dependency Chain

### Phase 1: Foundation & Infrastructure
- **Objective:** Prepare the cloud and local environments for development.
- **Specialist:** Developer (guided by `core/pmo-1-sre`)
- **Status:** **IN_PROGRESS**
- **Inputs:** N/A
- **Output:** A working local development environment and provisioned cloud resources.

---
## 10. Current Task Brief
- **Task ID:** P1-T1
- **Assigned To:** Developer
- **Status:** **COMPLETE**
- **Objective:** Set up the local Python development environment and create a minimal FastAPI application skeleton that can be run locally.

- **Task ID:** P1-T2
- **Assigned To:** Developer
- **Status:** **PENDING**
- **Objective:** Create the core project directory and file structure according to the principle of Separation of Concerns.
```

---
### Next Command
Execute the following commands to create the justified directory structure. After this, create a minimal "Hello World" FastAPI application in `app/main.py`.

```bash
# Create the core directories
mkdir -p app/api app/core app/services app/schemas app/repositories docs scripts tests

# Create initial empty Python package files
touch app/__init__.py app/api/__init__.py app/core/__init__.py app/services/__init__.py app/schemas/__init__.py app/repositories/__init__.py tests/__init__.py

# Create the main application file
touch app/main.py

# Create the canonical contracts file
touch docs/system_contracts.yml
```

After running this and creating the basic "Hello World" app in `app/main.py`, report back. You can test it with `uvicorn app.main:app --reload`.

---
## Critical Assessment
This is the justification for the structure created by the command above.

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
