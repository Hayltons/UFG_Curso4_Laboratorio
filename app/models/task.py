"""Modelos Pydantic para tarefas."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

TaskStatus = Literal["pendente", "em_andamento", "concluida"]
TaskPriority = Literal["baixa", "media", "alta"]


class TaskCreate(BaseModel):
    """Dados necessários para criar uma tarefa."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2_000)
    status: TaskStatus = "pendente"
    priority: TaskPriority = "media"

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Remove espaços e rejeita títulos vazios."""
        title = value.strip()
        if not title:
            raise ValueError("O título não pode estar vazio.")
        return title


class TaskUpdate(BaseModel):
    """Dados permitidos para atualizar uma tarefa."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2_000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        """Remove espaços e rejeita títulos vazios quando informados."""
        if value is None:
            return None

        title = value.strip()
        if not title:
            raise ValueError("O título não pode estar vazio.")
        return title

    @model_validator(mode="after")
    def validate_update_data(self) -> "TaskUpdate":
        """Exige pelo menos um campo para atualização."""
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualização.")
        return self


class TaskOut(BaseModel):
    """Representação pública de uma tarefa."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
