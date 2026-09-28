# PROMPTS CAP01


# Prompt1- .gitignore

Contexto: Estou iniciando uma API Python com FastAPI em um repositório de produto.
Objetivo: Gere um arquivo .gitignore para Python, ambiente virtual, cache de testes e configurações locais do editor.
Estilo: Organize por seções com comentários.
Resposta: Forneça apenas o conteúdo do arquivo .gitignore e grave o arquivo.

# Prompt2 - README inicial

Contexto: MVP de micro-API para gestão de tarefas com priorização assistida por IA.

Objetivo: Escrever um README inicial com objetivo, stack, como rodar localmente e roadmap de releases.

Estilo: Markdown simples, direto e profissional.

Resposta: Forneça o README completo e salve o arquivo.

# Prompt3 - Endpoint de healthcheck

Contexto: Projeto em Python 3.11 com FastAPI.

Objetivo: Criar app/main.py com uma instancia FastAPI e endpoint GET /health retornando status ok e timestamp.

Estilo: Tipagem e codigo limpo.

Resposta: Forneca apenas o codigo de app/main.py.

# Prompt 4 - Revisão crítica

Analise o código gerado para app/main.py e responda:

1) Quais riscos técnicos existem?
2) O que pode quebrar em produção?
3) Quais testes mínimos devo criar agora?

Resposta curta em checklist.

# Prompt 5 - Mensagem de commit
Contexto: Adicionei estrutura inicial, README, .gitignore e endpoint /health. Veja também outras alterações que não estão aqui listadas

Objetivo: Gerar uma mensagem de commit no padrão Conventional Commits.

Resposta: Apenas uma linha de commit.

# ----------------------------------------------------------------------------

# PROMPTS CAP02

# Cap02 - Prompt 1 - Escopo MVP

Contexto: MVP de micro-API de tarefas para uso de equipe interna.
Objetivo: Gerar documento de escopo com objetivo, requisitos funcionais, nao funcionais e fora de escopo.
Estilo: Linguagem tecnica, direta, em Markdown.
Resposta: Forneca o conteudo completo de docs/escopo-mvp.md.

# Cap02 - Prompt 2 - Backlog por realeases

Contexto: O produto sera entregue em 3 releases: core, qualidade e entrega final.
Objetivo: Criar backlog minimo com IDs RF/RT e criterios de aceite.
Estilo: Checklist Markdown.
Resposta: Conteudo de docs/backlog.md.

# Cap02 - Prompt 3 - Arquitetura Mermaid

Contexto: FastAPI com camadas API, Service, Repository e componente PriorityAdvisor.
Objetivo: Gerar diagrama Mermaid de componentes e fluxo de dados.
Estilo: Simples, legível e versionável.
Resposta: Apenas bloco Mermaid.

# Cap02 - Prompt 4 - Conventional Commits
Contexto: Adicionei docs/escopo-mvp.md, docs/arquitetura.md e docs/backlog.md.
Objetivo: Sugerir 3 mensagens de commit no padrão Conventional Commits.
Resposta: Apenas as 3 linhas de commit.

# Cap02 - Prompt 5 - Revisão de Planejamento
Analise este escopo e backlog e responda:
1) O que esta grande demais para a release inicial?
2) O que esta faltando para testabilidade?
3) Quais 3 riscos tecnicos devo mitigar antes da implementacao?

Resposta em bullets curtos.

# Cap03 - Prompt 1 - Modelo Pydantic
Contexto: API de tarefas em FastAPI para uso interno de equipe.
Objetivo: Gerar modelos TaskCreate, TaskUpdate e TaskOut com tipagem e validações.
Estilo: Pydantic v2, codigo limpo e docstrings curtas.
Resposta: Apenas codigo de app/models/task.py.

# Cap03 - Prompt 2 - Repositório Inicial
Contexto: Preciso de persistencia inicial enxuta para viabilizar a primeira release.
Objetivo: Criar TaskRepository em memoria com create, list, get_by_id, update e delete.
Estilo: Python tipado, sem dependencias externas.
Resposta: Codigo completo de app/repositories/task_repository.py.

# Cap03 - Prompt 3 - Service com regra de prioridade
Contexto: A prioridade da tarefa pode ser sugerida automaticamente.
Objetivo: Criar TaskService que use TaskRepository e PriorityAdvisor.
Estilo: Separar regra de negocio da camada de API.
Resposta: Codigo de app/services/task_service.py. Pode criar o código

# Cap03 - Prompt 4 - PriorityAdvisor com fallback
Contexto: Quero rodar sem custo de API quando nao houver chave.
Objetivo: Implementar PriorityAdvisor com heuristica local e chamada opcional a LLM quando OPENAI_API_KEY existir.
Estilo: Falha segura, timeout e fallback obrigatorio.
Resposta: Codigo de app/services/priority_advisor.py.

# Cap03 - Prompt 4 EXTRA - complemento
Pode criar o arquivo app/services/priority_advisor.py com o código sugerido, mas verifique, também,e ajuste se for o caso,  se não há código repetido para o PriorityAdvisor no app\services\task_service.py, pois este último apenas utiliza o que foi definido no primeiro.

# Cap03 - Prompt 5 - Rotas CRUD
Contexto: FastAPI com TaskService pronto.
Objetivo: Criar rotas POST/GET/PUT/DELETE para tarefas com status HTTP corretos e tratamento de 404.
Estilo: Router separado em app/api/task_routes.py.
Resposta: Apenas o codigo do arquivo mas pode criar o arquivo

# Cap03 - Prompt 6 - Revisao tecnica
Revise os arquivos do core da API e responda:
1) Quais pontos de acoplamento estao altos?
2) Onde faltam validacoes?
3) Quais 5 testes devo priorizar na proxima release?
Resposta em checklist.

# Cap03 - Prompt Extra - Commits
Contexto: Adicionei app\api\task_routes.py, app\repositories\task_repository.py, app\services\priority_advisor.py, app\services\task_service.py e docs\revisao_cap03.md. Também inclui prompts em prompts\prompts-codex.md.
Objetivo: Sugerir mensagens de commit no padrão Conventional Commits para cada arquivo incluído ou alterado.
Resposta: criar as linhas de commit e fazer o commit.