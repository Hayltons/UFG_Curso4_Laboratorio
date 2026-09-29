"""Testes unitários para o serviço de tarefas."""

from uuid import uuid4

from app.models.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from tests.fakes import FakePriorityAdvisor


def test_create_task_persists_task_data(task_service: TaskService) -> None:
    """Cria uma tarefa com os dados informados."""
    created_task = task_service.create_task(
        TaskCreate(
            title="Preparar apresentação",
            description="Organizar os slides da reunião.",
            priority="alta",
        )
    )

    assert created_task.id is not None
    assert created_task.title == "Preparar apresentação"
    assert created_task.description == "Organizar os slides da reunião."
    assert created_task.priority == "alta"
    assert created_task.created_at == created_task.updated_at


def test_list_tasks_returns_all_created_tasks(task_service: TaskService) -> None:
    """Lista todas as tarefas cadastradas no repositório."""
    first_task = task_service.create_task(TaskCreate(title="Primeira tarefa"))
    second_task = task_service.create_task(TaskCreate(title="Segunda tarefa"))

    tasks = task_service.list_tasks()

    assert [task.id for task in tasks] == [first_task.id, second_task.id]


def test_update_task_changes_only_provided_fields(task_service: TaskService) -> None:
    """Atualiza os campos informados e preserva os demais."""
    created_task = task_service.create_task(
        TaskCreate(
            title="Revisar documentação",
            description="Versão inicial.",
            priority="baixa",
        )
    )

    updated_task = task_service.update_task(
        created_task.id,
        TaskUpdate(priority="alta", status="em_andamento"),
    )

    assert updated_task is not None
    assert updated_task.title == "Revisar documentação"
    assert updated_task.description == "Versão inicial."
    assert updated_task.priority == "alta"
    assert updated_task.status == "em_andamento"
    assert updated_task.updated_at >= created_task.updated_at


def test_delete_task_removes_task_from_repository(task_service: TaskService) -> None:
    """Exclui uma tarefa e impede nova consulta."""
    created_task = task_service.create_task(TaskCreate(title="Tarefa temporária"))

    was_deleted = task_service.delete_task(created_task.id)

    assert was_deleted is True
    assert task_service.get_task_by_id(created_task.id) is None


def test_nonexistent_task_returns_absent_values(task_service: TaskService) -> None:
    """Retorna valores de ausência para um identificador inexistente."""
    nonexistent_id = uuid4()

    assert task_service.get_task_by_id(nonexistent_id) is None
    assert task_service.update_task(nonexistent_id, TaskUpdate(title="Novo título")) is None
    assert task_service.delete_task(nonexistent_id) is False


def test_create_task_uses_suggested_priority_when_requested(
    task_service: TaskService,
    priority_advisor: FakePriorityAdvisor,
) -> None:
    """Aplica a prioridade retornada pelo advisor quando solicitado."""
    priority_advisor.priority = "alta"

    created_task = task_service.create_task(
        TaskCreate(
            title="Corrigir incidente",
            description="Falha identificada em produção.",
            priority="baixa",
        ),
        use_suggested_priority=True,
    )

    assert created_task.priority == "alta"
    assert priority_advisor.calls == [
        ("Corrigir incidente", "Falha identificada em produção.")
    ]
