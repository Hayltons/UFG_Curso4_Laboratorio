"""Repositório em memória para tarefas."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.task import TaskCreate, TaskOut, TaskUpdate


class TaskRepository:
    """Armazena tarefas em memória durante a execução da aplicação."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, TaskOut] = {}

    def create(self, task_data: TaskCreate) -> TaskOut:
        """Cria e armazena uma nova tarefa."""
        now = self._utc_now()
        task = TaskOut(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **task_data.model_dump(),
        )
        self._tasks[task.id] = task
        return task

    def list(self) -> list[TaskOut]:
        """Retorna todas as tarefas cadastradas."""
        return list(self._tasks.values())

    def get_by_id(self, task_id: UUID) -> TaskOut | None:
        """Retorna uma tarefa pelo identificador, se existir."""
        return self._tasks.get(task_id)

    def update(self, task_id: UUID, task_data: TaskUpdate) -> TaskOut | None:
        """Atualiza os campos informados de uma tarefa existente."""
        task = self.get_by_id(task_id)
        if task is None:
            return None

        updated_task = task.model_copy(
            update={
                **task_data.model_dump(exclude_unset=True),
                "updated_at": self._utc_now(),
            }
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: UUID) -> bool:
        """Exclui uma tarefa e informa se ela existia."""
        return self._tasks.pop(task_id, None) is not None

    @staticmethod
    def _utc_now() -> datetime:
        """Retorna o horário atual em UTC."""
        return datetime.now(timezone.utc)
