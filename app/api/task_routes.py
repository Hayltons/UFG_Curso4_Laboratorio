"""Rotas HTTP para gerenciamento de tarefas."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.models.task import TaskCreate, TaskOut, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

_task_service = TaskService(
    repository=TaskRepository(),
    priority_advisor=PriorityAdvisor(),
)


def get_task_service() -> TaskService:
    """Fornece a instância do serviço de tarefas."""
    return _task_service


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    service: TaskServiceDependency,
) -> TaskOut:
    """Cria uma nova tarefa."""
    return service.create_task(task_data)


@router.get("", response_model=list[TaskOut])
def list_tasks(service: TaskServiceDependency) -> list[TaskOut]:
    """Lista todas as tarefas."""
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: UUID,
    service: TaskServiceDependency,
) -> TaskOut:
    """Obtém uma tarefa pelo identificador."""
    task = service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    service: TaskServiceDependency,
) -> TaskOut:
    """Atualiza os campos informados de uma tarefa."""
    task = service.update_task(task_id, task_data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    service: TaskServiceDependency,
) -> Response:
    """Exclui uma tarefa pelo identificador."""
    if not service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
