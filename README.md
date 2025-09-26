# PROJECT README: Tax Co-Pilot

<!-- Version: 1.0 -->
<!-- This document is the canonical source of truth for the Tax Co-Pilot application. -->
<!-- It serves as a guide for human developers and a foundational context for AI assistants. -->

## 1. System Overview and Core Purpose

The Tax Co-Pilot is a secure, scalable, and production-ready web application designed to provide AI-assisted tax analysis. It implements a Retrieval-Augmented Generation (RAG) pipeline to answer user questions based on a curated knowledge base of tax documents.

The architecture is a multi-layered, asynchronous API built with FastAPI, following modern software engineering best practices.

## 2. Core Architectural Principles

All development, whether human or AI-driven, MUST adhere to these principles:

1.  **Separation of Concerns:** The application is strictly divided into layers (API, Services, Repositories), each with a single, clear responsibility.
2.  **Decoupled Indexing:** The process of creating the knowledge base (indexing) is completely decoupled from the API server. The API server is a lightweight "Reader" and does not contain heavy ML dependencies for indexing.
3.  **Configuration-Driven:** Application behavior is controlled by explicit configuration (`config.yml`, `.env`), not hardcoded values. This allows for flexibility across different environments.
4.  **Dependency Injection:** Components are loosely coupled using FastAPI's dependency injection system, making the application highly testable and maintainable.
5.  **Environmental Realism:** All technical choices are validated against the target production environment: **Oracle Cloud Infrastructure (OCI), Oracle Linux 10 (`aarch64`)**.

## 3. Service Architecture & Data Flow

The system is composed of a well-defined set of layers that handle a request's lifecycle.

```
+----------------+   +----------------------+   +---------------------+   +-----------------+   +------------------+
|   User via UI  |-->|  API Layer (api/)    |-->| Service Layer (svc/) |-->| Repo Layer (repo/)|-->| PostgreSQL DB    |
| (Sends Request)|   | (Validates & Routes) |   | (Orchestrates Logic)|   | (Executes Query)  |   | (Stores Vectors) |
+----------------+   +----------------------+   +---------------------+   +-----------------+   +------------------+
                                                        |
                                                        | (Calls External AI)
                                                        v
                                                 +------------------+
                                                 |   Generative AI  |
                                                 | (Gemini/DeepSeek)|
                                                 +------------------+
```

-   **`app/api/` (The Front Door):** Handles incoming HTTP requests, validates data against schemas, and enforces security. It knows nothing about business logic.
-   **`app/services/` (The Brain):** Orchestrates the entire RAG process. It uses the `EmbeddingService` to vectorize the query, the `KnowledgeRepository` to find relevant context, and the `ResponseHandler` to build the final prompt and call the external LLM.
-   **`app/repositories/` (The Hands):** The only layer that communicates directly with the database. It encapsulates all SQLAlchemy and SQL logic.
-   **`app/core/` (The Central Nervous System):** Manages application-wide concerns like configuration loading and database connection lifecycle.
-   **`app/models/` (The Blueprint):** Defines the database schema using SQLAlchemy ORM models.
-   **`app/schemas/` (The Contract):** Defines the API data contracts using Pydantic models.

## 4. How to Run the Application Locally

### Prerequisites
- Python 3.11+
- A running PostgreSQL instance with the `pgvector` extension.

### Setup
1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies from `pyproject.toml`:**
    ```bash
    pip install -e ".[dev]"
    ```
4.  **Configure your environment:**
    - Create a `.env` file in the project root.
    - Add your database URL and AI provider API keys:
      ```env
      DATABASE_URL="postgresql+psycopg://user:pass@host:port/db"
      GEMINI_API_KEY="your_gemini_key"
      STATIC_API_KEY="dev-key"
      ```
5.  **Run the development server:**
    - The server runs on a non-standard port to avoid conflicts on shared hosts.
    ```bash
    uvicorn app.main:app --reload --port 8002
    ```
6.  **Access the API:**
    - The application will be available at `http://127.0.0.1:8002`.
    - Interactive API documentation is at `http://127.0.0.1:8002/docs`.

## 5. What to Expect from the Output (Current State)

The application is architecturally complete but is currently operating with a **mocked RAG pipeline**.

-   **Retrieval:** The database search for context (`find_similar_documents`) will execute, but since the database is empty, it will return no results.
-   **Generation:** The `ResponseHandler` will construct a prompt *without* any retrieved context and send the raw user question to the configured LLM (e.g., Gemini).
-   **Response:** You will receive a valid, live response from the LLM, but it will not be grounded in any specific project knowledge yet. The `sources` array in the JSON response will be empty.

## 6. What to Do Next (The Path Forward)

The immediate next step is to prove that this application can run in its target production environment.

-   **Next Task:** Perform a "smoke test" deployment. This involves:
    1.  Copying the application source code to the OCI VM.
    2.  Setting up the Python environment on the Oracle Linux 10 (`aarch64`) host.
    3.  Configuring the application to connect to the production PostgreSQL instance.
    4.  Running the application as a `systemd` service.
    5.  Verifying that it can be accessed and that the `/health` endpoint reports a successful database connection.

This will de-risk all environmental and architectural assumptions before we proceed with building the final ingestion pipeline.
