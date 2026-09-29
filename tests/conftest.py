"""Fixtures compartilhadas pela suíte de testes."""

import pytest

from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from tests.fakes import FakePriorityAdvisor


@pytest.fixture
def priority_advisor() -> FakePriorityAdvisor:
    """Fornece um advisor falso sem chamadas externas."""
    return FakePriorityAdvisor()


@pytest.fixture
def task_service(priority_advisor: FakePriorityAdvisor) -> TaskService:
    """Fornece um serviço com repositório isolado."""
    return TaskService(
        repository=TaskRepository(),
        priority_advisor=priority_advisor,
    )
