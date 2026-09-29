# Task Prioritization API

Micro-API REST para gestão interna de tarefas, construída com FastAPI. O MVP permite criar, consultar, atualizar e excluir tarefas, com uma camada de sugestão de prioridade que funciona localmente e pode consultar uma LLM de forma opcional.

## Recursos

- CRUD de tarefas versionado em `/api/v1/tasks`.
- Validação de entradas com Pydantic v2.
- Datas em UTC e identificadores UUID gerados pelo serviço.
- Sugestão local de prioridade (`baixa`, `media` ou `alta`) com fallback seguro.
- Documentação OpenAPI em `/docs`.
- Testes unitários e de rotas com Pytest.

## Requisitos

- Python 3.11 ou superior.
- `pip`.

## Instalação e execução

No PowerShell, a partir da raiz do repositório:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse a documentação interativa em <http://127.0.0.1:8000/docs>. O endpoint de disponibilidade é `GET /health`.

## Uso da API

| Método | Rota | Resultado |
| --- | --- | --- |
| `POST` | `/api/v1/tasks` | Cria uma tarefa (`201`) |
| `GET` | `/api/v1/tasks` | Lista tarefas (`200`) |
| `GET` | `/api/v1/tasks/{task_id}` | Consulta uma tarefa (`200` ou `404`) |
| `PUT` | `/api/v1/tasks/{task_id}` | Atualiza os campos enviados (`200` ou `404`) |
| `DELETE` | `/api/v1/tasks/{task_id}` | Exclui uma tarefa (`204` ou `404`) |

Exemplo de criação:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/tasks `
  -H "Content-Type: application/json" `
  -d '{"title":"Preparar demonstração","description":"Revisar o fluxo principal.","priority":"alta"}'
```

`title` é obrigatório. Os status aceitos são `pendente`, `em_andamento` e `concluida`; as prioridades aceitas são `baixa`, `media` e `alta`. A prioridade padrão é `media`.

## Testes

Execute toda a suíte:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Para executar uma camada específica, use, por exemplo:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_task_routes.py
```

Os testes isolam o repositório em memória e não exigem rede ou chave de API.

## Arquitetura

```text
Cliente HTTP → Rotas FastAPI → TaskService → TaskRepository → Memória
                                   └──────→ PriorityAdvisor
```

- `app/api/`: rotas e códigos HTTP.
- `app/services/`: regras de negócio e sugestão de prioridade.
- `app/repositories/`: armazenamento em memória.
- `app/models/`: contratos Pydantic de entrada e saída.

Veja o diagrama detalhado em [docs/arquitetura-componentes.md](docs/arquitetura-componentes.md).

## Priorização assistida por IA

`PriorityAdvisor` classifica tarefas localmente por palavras-chave. Termos como `incidente`, `urgente` e `produção` sugerem prioridade alta; `documentação` e `refatoração` sugerem baixa; os demais casos usam média.

Sem `OPENAI_API_KEY`, não há chamada externa nem custo de API. Com a chave configurada, o advisor pode consultar a Responses API, usando `OPENAI_MODEL` quando definido (o padrão atual é `gpt-4.1-mini`), timeout de três segundos e `store: false`. Falhas de rede, timeout ou respostas inválidas retornam à heurística local. Consulte a [documentação oficial da Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

```powershell
$env:OPENAI_API_KEY = "sua-chave"
$env:OPENAI_MODEL = "gpt-4.1-mini" # opcional
```

Não versione chaves. Atualmente, as rotas CRUD mantêm a prioridade recebida na requisição; a aplicação automática da sugestão está disponível na camada `TaskService` por meio de `use_suggested_priority=True` e ainda não possui parâmetro ou endpoint HTTP dedicado.

## Limitações do MVP

- O repositório é em memória; dados são perdidos ao reiniciar o processo.
- Não há autenticação, autorização, auditoria ou isolamento por equipe.
- Listagem ainda não possui filtros nem paginação.
- Não há banco de dados, migrações, backup ou execução multi-instância.
- A sugestão por LLM não fornece justificativa e não é exposta diretamente pela API.

## Próximos passos

1. Adicionar filtros, paginação e regras formais de transição de status.
2. Expor uma opção ou endpoint para aplicar a prioridade sugerida.
3. Substituir a persistência em memória por banco de dados com migrações.
4. Adicionar autenticação, logs estruturados, métricas e tratamento padronizado de erros.
5. Configurar linting, formatação, integração contínua e testes de integração com banco de dados.
