# Escopo do MVP — Micro-API de Tarefas

## 1. Objetivo

Disponibilizar uma micro-API REST para que a equipe interna registre, consulte, atualize e acompanhe tarefas de trabalho em um repositório único. O MVP deve fornecer uma base simples e confiável para a gestão operacional de tarefas, sem automações avançadas de priorização, colaboração ou integrações externas.

## 2. Público e contexto de uso

- Usuários: membros da equipe interna autorizados a consumir a API.
- Consumidores: aplicações internas, scripts de automação e ferramentas administrativas.
- Unidade gerenciada: tarefa individual vinculada ao contexto operacional da equipe.

## 3. Requisitos funcionais

### RF-01 — Verificação de disponibilidade

A API deve disponibilizar um endpoint de saúde para informar se o serviço está disponível e retornar o horário da verificação em UTC.

### RF-02 — Cadastro de tarefas

A API deve permitir criar uma tarefa com, no mínimo:

- identificador único gerado pelo serviço;
- título obrigatório;
- descrição opcional;
- status;
- prioridade;
- data de criação e data de atualização geradas pelo serviço.

### RF-03 — Consulta de tarefas

A API deve permitir:

- consultar uma tarefa pelo identificador;
- listar tarefas cadastradas;
- filtrar a listagem por status e prioridade;
- paginar a listagem para limitar o volume retornado.

### RF-04 — Atualização de tarefas

A API deve permitir atualizar título, descrição, status e prioridade de uma tarefa existente. A data de atualização deve ser renovada a cada alteração bem-sucedida.

### RF-05 — Encerramento de tarefas

A API deve permitir marcar uma tarefa como concluída. Tarefas concluídas devem permanecer consultáveis.

### RF-06 — Exclusão de tarefas

A API deve permitir excluir uma tarefa pelo identificador. Após a exclusão, a tarefa não deve ser retornada em consultas ou listagens.

### RF-07 — Validação e erros

A API deve validar os dados de entrada e retornar respostas HTTP coerentes:

- `400` ou `422` para dados inválidos;
- `404` para tarefa inexistente;
- `409` para conflito de estado, quando aplicável;
- `500` para falhas internas não tratadas.

### RF-08 — Contrato da API

A API deve expor documentação interativa baseada em OpenAPI, contendo endpoints, parâmetros, modelos de dados e respostas esperadas.

## 4. Regras de negócio

- O título da tarefa é obrigatório e não pode ser composto apenas por espaços.
- Os status permitidos são `pendente`, `em_andamento` e `concluida`.
- As prioridades permitidas são `baixa`, `media` e `alta`.
- Uma tarefa concluída pode ser reaberta mediante atualização de status para `pendente` ou `em_andamento`.
- Identificadores de tarefas são imutáveis e não podem ser reutilizados.
- Datas devem ser registradas e retornadas no padrão ISO 8601, em UTC.

## 5. Requisitos não funcionais

### RNF-01 — Arquitetura e interface

- A solução deve ser implementada como API HTTP REST em Python, utilizando FastAPI.
- As respostas devem utilizar JSON e codificação UTF-8.
- A API deve versionar os endpoints sob o prefixo `/api/v1`.

### RNF-02 — Persistência

- No MVP, os dados podem permanecer em memória durante a execução do serviço.
- A perda dos dados após reinicialização é aceita para esta etapa.
- A camada de armazenamento deve ser isolada da camada HTTP para viabilizar persistência durável em evolução futura.

### RNF-03 — Segurança

- O acesso é restrito ao ambiente interno da equipe.
- O MVP deve registrar a necessidade de autenticação para a próxima versão, mas não exige mecanismo de autenticação ou autorização nesta entrega.
- Dados sensíveis não devem ser incluídos em mensagens de erro ou logs de aplicação.

### RNF-04 — Qualidade e manutenção

- O código deve incluir validação de modelos de entrada e saída.
- Os fluxos de saúde, cadastro, consulta, atualização, conclusão, exclusão e erros principais devem possuir testes automatizados.
- A aplicação deve ter instruções de execução local e dependências declaradas no repositório.

### RNF-05 — Observabilidade mínima

- A aplicação deve registrar erros não tratados com informações suficientes para diagnóstico técnico.
- O endpoint de saúde deve poder ser usado por verificações automatizadas de disponibilidade.

## 6. Fora de escopo

Os itens abaixo não fazem parte do MVP:

- autenticação, autorização por perfil e isolamento de dados por usuário ou equipe;
- banco de dados persistente, migrações, backup e recuperação de dados;
- atribuição de responsáveis, comentários, anexos, etiquetas, subtarefas e dependências entre tarefas;
- notificações por e-mail, chat, push ou lembretes de prazo;
- interface web, aplicativo móvel ou painel administrativo;
- integração com ferramentas externas, como Jira, Trello, GitHub, Slack ou Microsoft Teams;
- cálculo automático de prioridade, recomendações ou integração com provedores de IA;
- relatórios, indicadores, auditoria detalhada e métricas de produtividade;
- suporte a múltiplas organizações, internacionalização ou configuração avançada por cliente;
- garantias de alta disponibilidade, escalabilidade horizontal ou acordos formais de nível de serviço.

## 7. Critérios de aceite do MVP

O MVP será considerado aceito quando:

1. o endpoint de saúde responder com sucesso e informar horário em UTC;
2. for possível executar operações de criar, consultar, listar, atualizar, concluir e excluir tarefas pela documentação OpenAPI;
3. entradas inválidas e tarefas inexistentes retornarem os códigos HTTP previstos;
4. a listagem suportar filtro por status e prioridade, além de paginação;
5. os testes automatizados dos fluxos principais forem executados com sucesso;
6. as instruções de execução local permitirem iniciar a API e acessar sua documentação.
