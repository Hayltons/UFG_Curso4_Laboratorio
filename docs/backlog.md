# Backlog Mínimo — Micro-API de Tarefas

## Release 1 — Core

- [ ] **RF-01 — Endpoint de saúde**
  - Disponibilizar `GET /health`.
  - Critérios de aceite:
    - Retorna HTTP `200` quando a aplicação está disponível.
    - Retorna `status` com valor `ok`.
    - Retorna `timestamp` no padrão ISO 8601, em UTC.

- [ ] **RF-02 — Criar tarefa**
  - Disponibilizar endpoint para cadastrar tarefa com título, descrição opcional, status e prioridade.
  - Critérios de aceite:
    - Gera identificador único para cada tarefa criada.
    - Rejeita título vazio ou composto apenas por espaços.
    - Define e retorna datas de criação e atualização em UTC.
    - Retorna HTTP `201` para cadastro válido.

- [ ] **RF-03 — Consultar e listar tarefas**
  - Disponibilizar consulta por identificador e listagem de tarefas.
  - Critérios de aceite:
    - Consulta por identificador retorna HTTP `200` e os dados da tarefa.
    - Identificador inexistente retorna HTTP `404`.
    - A listagem retorna tarefas cadastradas em JSON.
    - A listagem suporta paginação por limite e deslocamento.

- [ ] **RF-04 — Atualizar e concluir tarefa**
  - Permitir atualizar título, descrição, status e prioridade, incluindo a conclusão da tarefa.
  - Critérios de aceite:
    - Atualização válida retorna HTTP `200` e renova a data de atualização.
    - É possível alterar o status para `concluida`.
    - Tarefas concluídas permanecem disponíveis para consulta.
    - Atualização de identificador inexistente retorna HTTP `404`.

- [ ] **RF-05 — Excluir tarefa**
  - Permitir excluir uma tarefa pelo identificador.
  - Critérios de aceite:
    - Exclusão válida retorna HTTP `204`.
    - A tarefa excluída não é retornada por consulta ou listagem.
    - Exclusão de identificador inexistente retorna HTTP `404`.

- [ ] **RT-01 — Modelos e validação de dados**
  - Definir contratos de entrada e saída para tarefas e saúde.
  - Critérios de aceite:
    - Status aceitos: `pendente`, `em_andamento` e `concluida`.
    - Prioridades aceitas: `baixa`, `media` e `alta`.
    - Dados inválidos retornam HTTP `422` com descrição do erro.

- [ ] **RT-02 — Armazenamento em memória**
  - Implementar repositório temporário desacoplado da camada HTTP.
  - Critérios de aceite:
    - Operações CRUD utilizam o repositório definido.
    - A API funciona sem banco de dados externo.
    - A perda de dados após reinicialização está documentada.

## Release 2 — Qualidade

- [ ] **RF-06 — Filtrar tarefas**
  - Permitir filtrar a listagem por status e prioridade.
  - Critérios de aceite:
    - A listagem aceita filtros opcionais de status e prioridade.
    - O retorno contém somente tarefas compatíveis com todos os filtros informados.
    - Valores de filtro inválidos retornam HTTP `422`.

- [ ] **RT-03 — Testes automatizados**
  - Cobrir os fluxos principais da API com testes automatizados.
  - Critérios de aceite:
    - Existem testes para saúde e operações CRUD.
    - Existem testes para validação, recurso inexistente e filtros.
    - A suíte de testes é executada com sucesso em ambiente local.

- [ ] **RT-04 — Tratamento de erros e logs**
  - Padronizar respostas de erro e registrar falhas internas.
  - Critérios de aceite:
    - Erros de validação, recurso inexistente e conflito usam códigos HTTP adequados.
    - Falhas não tratadas retornam HTTP `500` sem expor dados sensíveis.
    - Falhas não tratadas são registradas para diagnóstico técnico.

- [ ] **RT-05 — Documentação técnica da API**
  - Manter documentação de uso e contrato da API atualizados.
  - Critérios de aceite:
    - A especificação OpenAPI lista todos os endpoints implementados.
    - A documentação interativa está acessível em `/docs`.
    - O repositório contém instruções para instalação, execução e testes locais.

## Release 3 — Entrega final

- [ ] **RT-06 — Revisão de prontidão para entrega**
  - Validar a versão candidata à entrega contra o escopo do MVP.
  - Critérios de aceite:
    - Todos os itens previstos para as Releases 1 e 2 estão concluídos.
    - A suíte de testes é executada com sucesso.
    - Não há erros de formatação, importação ou inicialização da aplicação.

- [ ] **RT-07 — Empacotamento e configuração de execução**
  - Consolidar os artefatos necessários para executar a API no ambiente interno.
  - Critérios de aceite:
    - As dependências estão declaradas em arquivo versionado.
    - A aplicação pode ser iniciada por comando documentado.
    - O endpoint `/health` e a documentação `/docs` estão acessíveis após a inicialização.

- [ ] **RT-08 — Documentação de entrega**
  - Registrar escopo, limitações e procedimento de validação da entrega.
  - Critérios de aceite:
    - O documento de escopo do MVP está disponível e atualizado.
    - O backlog reflete o estado final dos itens entregues.
    - As limitações conhecidas, incluindo persistência em memória e ausência de autenticação, estão registradas.
