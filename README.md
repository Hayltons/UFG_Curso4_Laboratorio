# Task Prioritization API

Micro-API para gestão de tarefas com priorização assistida por IA. O objetivo é ajudar equipes e pessoas a organizar o trabalho, combinando dados objetivos — como prazo, impacto e esforço — com sugestões de prioridade geradas por inteligência artificial.

## Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pytest

## Executando localmente

1. Crie e ative o ambiente virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Inicie a API:

   ```powershell
   uvicorn app.main:app --reload
   ```

4. Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Roadmap de releases

### v0.1 — Fundação

- Estrutura inicial da API FastAPI
- Endpoints CRUD de tarefas
- Validação de dados e documentação automática
- Testes básicos

### v0.2 — Priorização assistida

- Campos de impacto, urgência e esforço
- Cálculo de prioridade baseado em regras
- Endpoint de recomendação de prioridade

### v0.3 — Integração com IA

- Integração com provedor de IA configurável
- Sugestões de prioridade com justificativa
- Proteções para falhas e limites de uso

### v1.0 — Produto inicial

- Persistência de dados
- Autenticação e isolamento por usuário
- Observabilidade, testes de integração e documentação de implantação
