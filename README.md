# Task Prioritization API

Micro-API REST para gestão interna de tarefas, desenvolvida com FastAPI. O MVP oferece CRUD de tarefas e uma camada de sugestão de prioridade com heurística local e integração opcional com LLM.

## Recursos

- CRUD versionado sob `/api/v1/tasks`.
- Validação de entrada e saída com Pydantic v2.
- UUIDs e timestamps ISO 8601 em UTC gerados pelo serviço.
- Documentação OpenAPI em `/docs`.
- Sugestão de prioridade local com fallback seguro para falhas externas.
- 26 testes automatizados de serviço, advisor e rotas.

## Requisitos

- Python **3.11** (versão usada e validada neste projeto).
- `pip` associado ao Python 3.11.
- Opcional: GNU Make para os atalhos do `Makefile`. No Windows, ele não vem instalado por padrão; use os comandos Python equivalentes abaixo caso não o possua.

## Quickstart em máquina limpa

Clone o repositório e entre na pasta do projeto:

```powershell
git clone <repository-url>
cd UFG_Curso4_Laboratorio
```

Crie o ambiente virtual, instale as dependências, valide a suíte e inicie a API:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

Resultado esperado: os 26 testes devem passar e a API deve responder em <http://127.0.0.1:8000>.

Verifique a aplicação em outro terminal:

```powershell
curl.exe http://127.0.0.1:8000/health
```

```json
{"status":"ok","timestamp":"2026-01-01T00:00:00Z"}
```

A documentação interativa está disponível em <http://127.0.0.1:8000/docs>.

## Atalhos do Makefile

Em ambientes com `make`, os comandos equivalentes são:

```bash
make install
make test
make run
```

É possível selecionar outro interpretador ou porta:

```bash
make PYTHON=python3.11 test
make PORT=8001 run
```

## Uso da API

| Método | Rota | Resultado |
| --- | --- | --- |
| `POST` | `/api/v1/tasks` | Cria uma tarefa (`201`) |
| `GET` | `/api/v1/tasks` | Lista tarefas (`200`) |
| `GET` | `/api/v1/tasks/{task_id}` | Consulta uma tarefa (`200` ou `404`) |
| `PUT` | `/api/v1/tasks/{task_id}` | Atualiza os campos enviados (`200`, `404` ou `422`) |
| `DELETE` | `/api/v1/tasks/{task_id}` | Exclui uma tarefa (`204` ou `404`) |

### Criar uma tarefa

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/tasks `
  -H "Content-Type: application/json" `
  -d '{"title":"Preparar demonstracao","description":"Revisar o fluxo principal.","priority":"alta"}'
```

Resposta resumida (`201`):

```json
{
  "id": "<task-id>",
  "title": "Preparar demonstracao",
  "status": "pendente",
  "priority": "alta"
}
```

### Listar e consultar

```powershell
curl.exe http://127.0.0.1:8000/api/v1/tasks
curl.exe http://127.0.0.1:8000/api/v1/tasks/<task-id>
```

### Atualizar e excluir

```powershell
curl.exe -X PUT http://127.0.0.1:8000/api/v1/tasks/<task-id> `
  -H "Content-Type: application/json" `
  -d '{"status":"concluida"}'

curl.exe -X DELETE http://127.0.0.1:8000/api/v1/tasks/<task-id>
```

`title` é obrigatório. Os status aceitos são `pendente`, `em_andamento` e `concluida`; as prioridades aceitas são `baixa`, `media` e `alta`. O padrão de ambos é `pendente` e `media`, respectivamente. Um UUID inválido ou corpo inválido retorna `422`; uma tarefa inexistente retorna `404`.

## Testes

Execute a suíte completa:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Para executar uma camada específica:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_task_routes.py
```

Os testes substituem as dependências de persistência e prioridade por fixtures isoladas. Não exigem rede, chave de API nem modificam o estado em memória da API em execução.

## Arquitetura

```text
Cliente HTTP → Rotas FastAPI → TaskService → TaskRepository → Memória
                                   └──────→ PriorityAdvisor
```

- `app/main.py` cria a aplicação e registra o router.
- `app/api/` traduz HTTP para chamadas de serviço e define códigos de resposta.
- `app/services/` coordena regras de negócio e a sugestão de prioridade.
- `app/repositories/` implementa o armazenamento atual em memória.
- `app/models/` concentra os contratos Pydantic.

O router monta um único `TaskService` com um único `TaskRepository` em memória para o processo atual. Logo, as tarefas sobrevivem a múltiplas requisições no mesmo processo, mas são perdidas quando ele é reiniciado. Veja o diagrama detalhado em [docs/arquitetura-componentes.md](docs/arquitetura-componentes.md).

## Configuração de ambiente

O arquivo [.env.example](.env.example) documenta as variáveis reconhecidas:

```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

O projeto **não carrega arquivos `.env` automaticamente**. Copiar `.env.example` para `.env` serve apenas como referência local; para usar a integração, exporte as variáveis no processo que inicia a API:

```powershell
$env:OPENAI_API_KEY = "sua-chave-real"
$env:OPENAI_MODEL = "gpt-4.1-mini" # opcional
python -m uvicorn app.main:app --reload
```

Nunca versione chaves reais. `.env` e `.env.*` permanecem ignorados, enquanto `.env.example` é versionável.

## Priorização assistida por IA

### Estado atual da integração

As rotas HTTP CRUD **não acionam a LLM** e mantêm a prioridade recebida na requisição. A sugestão automática existe na camada `TaskService` e só é aplicada quando o consumidor chama `create_task(..., use_suggested_priority=True)`. Não há, por enquanto, parâmetro ou endpoint HTTP dedicado para solicitar a sugestão.

| Configuração | Comportamento |
| --- | --- |
| Sem `OPENAI_API_KEY` | Usa apenas heurística local; não há chamada externa nem custo de API. |
| Com `OPENAI_API_KEY` e sugestão solicitada | Envia título e descrição à Responses API para classificar a prioridade. |
| Falha de rede, timeout ou resposta inválida | Retorna à heurística local, sem interromper a criação da tarefa. |

A heurística local sugere `alta` para termos como `incidente`, `urgente` e `produção`; `baixa` para `documentação` e `refatoração`; e `media` nos demais casos. A integração externa usa `OPENAI_MODEL` ou o padrão `gpt-4.1-mini`, limita a chamada a três segundos e solicita `store: false`.

`store: false` reduz a retenção de respostas pela API, mas não elimina o envio do título e da descrição ao provedor nem os custos de uma chamada com chave configurada. Avalie os dados enviados, configure alertas de gasto e consulte a [documentação oficial da Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

Os testes usam `FakePriorityAdvisor` e `monkeypatch` para validar sugestões e fallback sem chave ou acesso de rede.

## Limitações do MVP

- O repositório é em memória; não há banco de dados, migrações, backup ou execução multi-instância.
- Não há autenticação, autorização, auditoria ou isolamento por equipe.
- A listagem ainda não possui filtros nem paginação.
- Não há regras formais de transição de status ou resposta `409` para conflitos de estado.
- A LLM não fornece justificativa e não é acessível diretamente por HTTP.

## Desenvolvimento e contribuição

Consulte [AGENTS.md](AGENTS.md) para convenções de estrutura, estilo, testes e commits. Use commits Conventional Commits, por exemplo: `feat(api): add task routes` ou `test(api): expand task route coverage`.

## Próximos passos

1. Adicionar filtros, paginação e regras formais de transição de status.
2. Expor uma opção ou endpoint para aplicar a prioridade sugerida.
3. Substituir a persistência em memória por banco de dados com migrações.
4. Adicionar autenticação, logs estruturados, métricas e tratamento padronizado de erros.
5. Configurar linting, formatação, integração contínua e testes de integração com banco de dados.
