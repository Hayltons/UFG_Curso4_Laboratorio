"""Sugestão de prioridade com heurística local e LLM opcional."""

import json
import logging
import os
from typing import Final, cast
from urllib.request import Request, urlopen

from app.models.task import TaskPriority

LOGGER = logging.getLogger(__name__)

OPENAI_RESPONSES_URL: Final = "https://api.openai.com/v1/responses"
VALID_PRIORITIES: Final = frozenset({"baixa", "media", "alta"})


class PriorityAdvisor:
    """Sugere prioridades com fallback local seguro."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 3.0,
    ) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self._timeout_seconds = timeout_seconds

    def suggest(self, *, title: str, description: str | None) -> TaskPriority:
        """Retorna uma prioridade sugerida para a tarefa."""
        fallback_priority = self._suggest_locally(title, description)

        if not self._api_key:
            return fallback_priority

        try:
            return self._suggest_with_llm(title, description) or fallback_priority
        except Exception:
            LOGGER.warning(
                "Não foi possível obter sugestão de prioridade via LLM; "
                "usando heurística local.",
            )
            return fallback_priority

    def _suggest_locally(
        self,
        title: str,
        description: str | None,
    ) -> TaskPriority:
        """Aplica uma heurística local baseada em palavras-chave."""
        text = f"{title} {description or ''}".lower()

        high_priority_terms = {
            "urgente",
            "urgência",
            "critico",
            "crítico",
            "incidente",
            "indisponível",
            "indisponivel",
            "bloqueio",
            "bloqueada",
            "produção",
            "producao",
            "segurança",
            "seguranca",
            "vazamento",
            "falha",
        }
        low_priority_terms = {
            "documentação",
            "documentacao",
            "refatoração",
            "refatoracao",
            "melhoria",
            "pesquisa",
            "estudo",
        }

        if any(term in text for term in high_priority_terms):
            return "alta"

        if any(term in text for term in low_priority_terms):
            return "baixa"

        return "media"

    def _suggest_with_llm(
        self,
        title: str,
        description: str | None,
    ) -> TaskPriority | None:
        """Consulta a LLM e aceita apenas prioridades válidas."""
        prompt = (
            "Classifique a prioridade da tarefa abaixo. "
            "Responda somente com: baixa, media ou alta.\n\n"
            f"Título: {title}\n"
            f"Descrição: {description or 'Não informada'}"
        )
        payload = json.dumps(
            {
                "model": self._model,
                "input": prompt,
                "max_output_tokens": 10,
                "store": False,
            }
        ).encode("utf-8")
        request = Request(
            OPENAI_RESPONSES_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request, timeout=self._timeout_seconds) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        suggestion = self._extract_output_text(response_data).strip().lower()
        if suggestion in VALID_PRIORITIES:
            return cast(TaskPriority, suggestion)

        return None

    @staticmethod
    def _extract_output_text(response_data: object) -> str:
        """Extrai o texto da primeira mensagem retornada pela API."""
        if not isinstance(response_data, dict):
            return ""

        output = response_data.get("output", [])
        if not isinstance(output, list):
            return ""

        for item in output:
            if not isinstance(item, dict):
                continue

            content = item.get("content", [])
            if not isinstance(content, list):
                continue

            for part in content:
                if isinstance(part, dict) and part.get("type") == "output_text":
                    text = part.get("text", "")
                    if isinstance(text, str):
                        return text

        return ""
