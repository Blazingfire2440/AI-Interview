# Real-time SAR Interview Assistant

A real-time, end-to-end system for Search and Rescue operations that suggests context-aware follow-up questions and extracts actionable clues during interviews with missing persons' contacts.

![frontpage.png](docs/frontpage.png)

## Vision

In Search and Rescue (SAR) operations, time pressure and inexperience can lead to missed opportunities during interviews with a missing person's friends and family. This system leverages large language models (LLMs), agentic design patterns, and integration with the IntelliSAR platform to assist interviewers in surfacing more complete and relevant information. It compiles key insights into a structured clue log, ready for human review, refinement, and dissemination to the rest of the team.

**Ultimate Goal:** Accelerate clue discovery and reduce the likelihood of critical information being overlooked in time-sensitive SAR missions.

## Docker Compose Installation

For docker compose, copy .env.example to .env and fill in all the required environment variables. Then expose expose nginx's port 80 and bring up the system:

```bash
docker compose up
```

## Development Installation

### 1. Environment Setup

Copy the .env.example to .env in both `frontend/` and `backend/`, fill in the required environment variables.

### 2. Backend Setup

Run these commands to install dependencies and setup the database:

```bash
cd backend
uv sync
uv run alembic upgrade head
```

### 2. Frontend Setup

```bash
cd frontend
pnpm install
```

### 5. Pre-Commit Hook Setup

In the root of the repo run:

```bash
pre-commit install
```

## Run for Development

### Start Backend Server

```bash
cd backend
uv run ./src/main.py
```

### Start Frontend Development Server

```bash
cd frontend
pnpm dev
```

The frontend will be available at `https://localhost:5173` and the backend WebRTC server runs on the configured port.

### Mock Authentication (development only)

To skip OIDC and be logged in automatically as a stable test user (`Mock Test User`, sub `mock-auth|test-user`):

- Backend `backend/.env`: `ENVIRONMENT=development` and `MOCK_AUTH=true` (OIDC variables become optional and OIDC discovery is skipped).
- Frontend `frontend/.env`: `VITE_MOCK_AUTH=true`, then run `pnpm dev`.

Limits: the backend refuses to start if `MOCK_AUTH=true` without `ENVIRONMENT=development` (`ENVIRONMENT` defaults to `production`); the frontend flag only works in `pnpm dev`, not in production builds. The mock token is only accepted by the backend when mock auth is enabled; with it disabled, normal OIDC is unchanged. The mock user is stored in the normal users table like any OIDC user.

## Other Tasks

### Structurizr

See an interactive diagram of the architecture:

```
docker run -it --rm -p 8080:8080 -v docs:/usr/local/structurizr structurizr/lite
```

### LLM Eval Tests

To run the LLM eval tests, in the `backend/` dir run:

```
uv run deepeval test run -m "llm"  .\src\interview_helper\ai_analysis\eval
```

### Create Alembic Migration

To autogenerate a migration with alembic, in the `backend/` dir run:

```
uv run alembic revision --autogenerate -m "<message>"
```
