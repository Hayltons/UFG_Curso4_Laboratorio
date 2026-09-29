"""Regras de negócio para gerenciamento de tarefas."""

from typing import Protocol
from uuid import UUID

from app.models.task import TaskCreate, TaskOut, TaskPriority, TaskUpdate


class TaskRepositoryProtocol(Protocol):
    """Contrato de persistência usado pelo serviço."""

    def create(self, task_data: TaskCreate) -> TaskOut: ...

    def list(self) -> list[TaskOut]: ...

    def get_by_id(self, task_id: UUID) -> TaskOut | None: ...

    def update(self, task_id: UUID, task_data: TaskUpdate) -> TaskOut | None: ...

    def delete(self, task_id: UUID) -> bool: ...


class PriorityAdvisorProtocol(Protocol):
    """Contrato para sugestão de prioridade."""

    def suggest(self, *, title: str, description: str | None) -> TaskPriority: ...


class TaskService:
    """Coordena operações de tarefa e regras de prioridade."""

    def __init__(
        self,
        repository: TaskRepositoryProtocol,
        priority_advisor: PriorityAdvisorProtocol,
    ) -> None:
        self._repository = repository
        self._priority_advisor = priority_advisor

    def create_task(
        self,
        task_data: TaskCreate,
        *,
        use_suggested_priority: bool = False,
    ) -> TaskOut:
        """Cria uma tarefa, opcionalmente aplicando a prioridade sugerida."""
        if use_suggested_priority:
            task_data = self._apply_suggested_priority(task_data)

        return self._repository.create(task_data)

    def _apply_suggested_priority(self, task_data: TaskCreate) -> TaskCreate:
        """Retorna os dados com a prioridade sugerida."""
        return task_data.model_copy(
            update={"priority": self.suggest_priority(task_data)}
        )

    def list_tasks(self) -> list[TaskOut]:
        """Lista as tarefas cadastradas."""
        return self._repository.list()

    def get_task_by_id(self, task_id: UUID) -> TaskOut | None:
        """Obtém uma tarefa pelo identificador."""
        return self._repository.get_by_id(task_id)

    def update_task(self, task_id: UUID, task_data: TaskUpdate) -> TaskOut | None:
        """Atualiza os campos informados de uma tarefa."""
        return self._repository.update(task_id, task_data)

    def delete_task(self, task_id: UUID) -> bool:
        """Exclui uma tarefa pelo identificador."""
        return self._repository.delete(task_id)

    def suggest_priority(self, task_data: TaskCreate) -> TaskPriority:
        """Obtém uma sugestão de prioridade para uma nova tarefa."""
        return self._priority_advisor.suggest(
            title=task_data.title,
            description=task_data.description,
        )
