# Repository Guidelines

## Project Structure & Module Organization

- `app/main.py` creates the FastAPI application, registers routers, and exposes `GET /health`.
- `app/api/` contains HTTP routes. Keep request parsing and HTTP status handling here.
- `app/services/` contains business orchestration (`TaskService`) and priority suggestion logic (`PriorityAdvisor`).
- `app/repositories/` contains persistence implementations; the current `TaskRepository` is in memory.
- `app/models/` contains Pydantic request and response models.
- `tests/` mirrors the core layers. Shared fixtures live in `tests/conftest.py`; reusable fakes belong in `tests/fakes.py`.
- `docs/` holds scope, backlog, architecture, and review material. `prompts/` stores the exercise prompts.

## Build, Test, and Development Commands

Use Python 3.11+ and PowerShell on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`. Run the full test suite before submitting changes:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run a focused test file when iterating, for example: `python -m pytest -q tests/test_task_routes.py`.

## Coding Style & Naming Conventions

Use Python type hints, four-space indentation, and short Portuguese docstrings. Use `snake_case` for functions, variables, and modules; `PascalCase` for classes; and descriptive test names such as `test_delete_task_returns_204_and_then_404`.

Keep responsibilities separated: routes call services, services coordinate business rules, and repositories manage storage. Use dependency injection or protocols for boundaries that need isolation in tests. No formatter or linter is configured; keep imports grouped and code consistent with adjacent modules.

## Testing Guidelines

Use Pytest and FastAPI `TestClient`. Every behavior change should include focused coverage for success and failure paths. Override `get_task_service` in route tests to prevent shared in-memory state. Mock external priority calls with `monkeypatch`; tests must not require `OPENAI_API_KEY` or network access.

## Commit & Pull Request Guidelines

Follow the Conventional Commit format used in the history: `feat(api): add task routes`, `feat(service): add task service`, or `docs: add core API review`. Keep each commit focused on one concern.

For pull requests, describe the behavior changed, list executed tests, link the relevant issue when available, and include request/response examples for API-contract changes. Never commit API keys; configure `OPENAI_API_KEY` only through the environment.
