"""Dublês de teste compartilhados."""

from app.models.task import TaskPriority


class FakePriorityAdvisor:
    """Advisor previsível para testes isolados."""

    def __init__(self, priority: TaskPriority = "media") -> None:
        self.priority = priority
        self.calls: list[tuple[str, str | None]] = []

    def suggest(self, *, title: str, description: str | None) -> TaskPriority:
        """Registra a chamada e retorna a prioridade configurada."""
        self.calls.append((title, description))
        return self.priority
