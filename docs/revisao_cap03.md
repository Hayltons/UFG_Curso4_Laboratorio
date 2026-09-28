# Revisão do Core da API — Capítulo 03

## Pontos de acoplamento alto

- `task_routes.py` instancia `TaskRepository`, `PriorityAdvisor` e `TaskService`; a camada HTTP também faz a composição das dependências.
- `TaskService` depende de classes concretas, não de interfaces ou protocolos.
- `TaskRepository` persiste `TaskOut` (modelo de resposta da API), misturando persistência e contrato HTTP.
- `PriorityAdvisor` fixa URL, modelo padrão e transporte HTTP na mesma classe.

## Validações ausentes

- `app/main.py` não inclui o `router`; atualmente apenas `/health` fica exposto.
- Regras de transição de status e o caso de conflito `409` não estão implementados.
- `description` aceita texto apenas com espaços; datas em `TaskOut` não exigem explicitamente UTC.
- Não há validação de paginação, filtros por status/prioridade ou limite máximo de listagem.
- `timeout_seconds` do `PriorityAdvisor` aceita valores nulos, zero ou negativos.

## Testes prioritários para a próxima release

1. Testar que a aplicação inclui as rotas `/api/v1/tasks` e mantém `/health` disponível.
2. Testar ciclo HTTP completo: criar (`201`), consultar/listar (`200`), atualizar (`200`) e excluir (`204`).
3. Testar validações: título vazio/espaços, status/prioridade inválidos e corpo de atualização vazio (`422`).
4. Testar `404` para consulta, atualização e exclusão de UUID inexistente.
5. Testar `PriorityAdvisor` sem chave e com timeout/erro da LLM, garantindo fallback local.
