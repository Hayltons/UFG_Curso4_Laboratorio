"""Testes unitários para o componente de sugestão de prioridade."""

import pytest

from app.services.priority_advisor import PriorityAdvisor


@pytest.fixture
def local_advisor(monkeypatch: pytest.MonkeyPatch) -> PriorityAdvisor:
    """Fornece um advisor sem acesso a chave de API."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    return PriorityAdvisor()


def test_suggest_returns_high_priority_for_urgent_incident(
    local_advisor: PriorityAdvisor,
) -> None:
    """Classifica incidentes urgentes como prioridade alta."""
    priority = local_advisor.suggest(
        title="Incidente em produção",
        description="Serviço indisponível para a equipe.",
    )

    assert priority == "alta"


def test_suggest_returns_low_priority_for_documentation_task(
    local_advisor: PriorityAdvisor,
) -> None:
    """Classifica tarefas de documentação como prioridade baixa."""
    priority = local_advisor.suggest(
        title="Atualizar documentação",
        description="Revisar exemplos do guia interno.",
    )

    assert priority == "baixa"


def test_suggest_returns_medium_priority_without_matching_keywords(
    local_advisor: PriorityAdvisor,
) -> None:
    """Usa prioridade média quando nenhuma regra se aplica."""
    priority = local_advisor.suggest(
        title="Criar endpoint de tarefas",
        description="Adicionar operação de consulta.",
    )

    assert priority == "media"


def test_suggest_does_not_call_llm_without_api_key(
    local_advisor: PriorityAdvisor,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mantém a heurística local quando não há chave configurada."""
    def fail_if_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("A chamada externa não deveria ser executada.")

    monkeypatch.setattr(local_advisor, "_suggest_with_llm", fail_if_called)

    priority = local_advisor.suggest(
        title="Atualizar documentação",
        description=None,
    )

    assert priority == "baixa"


def test_suggest_uses_local_fallback_when_llm_call_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mantém a sugestão local quando a chamada externa falha."""
    advisor = PriorityAdvisor(api_key="test-api-key")

    def raise_timeout(*args: object, **kwargs: object) -> None:
        raise TimeoutError("Tempo limite excedido")

    monkeypatch.setattr(advisor, "_suggest_with_llm", raise_timeout)

    priority = advisor.suggest(
        title="Falha de segurança",
        description="Investigar o erro imediatamente.",
    )

    assert priority == "alta"


def test_suggest_uses_local_fallback_for_invalid_llm_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Usa a heurística local quando a LLM não retorna uma prioridade válida."""
    advisor = PriorityAdvisor(api_key="test-api-key")
    monkeypatch.setattr(advisor, "_suggest_with_llm", lambda *args: None)

    priority = advisor.suggest(
        title="Atualizar documentação",
        description=None,
    )

    assert priority == "baixa"
