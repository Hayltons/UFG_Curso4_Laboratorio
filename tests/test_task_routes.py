"""Testes de integração das rotas de tarefas."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.task_routes import get_task_service
from app.main import app
from app.services.task_service import TaskService


@pytest.fixture
def client(task_service: TaskService) -> Generator[TestClient, None, None]:
    """Fornece a aplicação real com serviço isolado por teste."""
    app.dependency_overrides[get_task_service] = lambda: task_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_task_service, None)


def create_task(client: TestClient, title: str = "Tarefa de teste") -> dict[str, object]:
    """Cria uma tarefa e retorna sua representação JSON."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": title, "priority": "media"},
    )

    assert response.status_code == 201
    return response.json()


def test_application_exposes_health_and_task_routes(client: TestClient) -> None:
    """Expõe saúde e a listagem de tarefas na aplicação principal."""
    assert client.get("/health").status_code == 200
    assert client.get("/api/v1/tasks").status_code == 200


def test_create_task_returns_201(client: TestClient) -> None:
    """Cria uma tarefa e retorna HTTP 201."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Preparar demonstração", "priority": "alta"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Preparar demonstração"
    assert response.json()["priority"] == "alta"


def test_list_tasks_returns_200_with_created_tasks(client: TestClient) -> None:
    """Lista as tarefas cadastradas e retorna HTTP 200."""
    created_task = create_task(client)

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [created_task["id"]]


def test_update_task_returns_200(client: TestClient) -> None:
    """Atualiza uma tarefa existente e retorna HTTP 200."""
    created_task = create_task(client)

    response = client.put(
        f"/api/v1/tasks/{created_task['id']}",
        json={"status": "concluida", "priority": "alta"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "concluida"
    assert response.json()["priority"] == "alta"


def test_delete_task_returns_204_and_then_404(client: TestClient) -> None:
    """Exclui uma tarefa e confirma que ela deixa de ser consultável."""
    created_task = create_task(client)
    task_url = f"/api/v1/tasks/{created_task['id']}"

    response = client.delete(task_url)

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(task_url).status_code == 404


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PUT", {"title": "Novo título"}),
        ("DELETE", None),
    ],
)
def test_nonexistent_task_operations_return_404(
    client: TestClient,
    method: str,
    payload: dict[str, str] | None,
) -> None:
    """Retorna HTTP 404 para operações em uma tarefa inexistente."""
    response = client.request(
        method,
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa não encontrada."


def test_task_routes_return_422_for_invalid_payloads(client: TestClient) -> None:
    """Rejeita dados inválidos de criação e atualização."""
    invalid_title = client.post("/api/v1/tasks", json={"title": "   "})
    invalid_priority = client.post(
        "/api/v1/tasks",
        json={"title": "Tarefa", "priority": "urgente"},
    )
    created_task = create_task(client)
    empty_update = client.put(f"/api/v1/tasks/{created_task['id']}", json={})

    assert invalid_title.status_code == 422
    assert invalid_priority.status_code == 422
    assert empty_update.status_code == 422
