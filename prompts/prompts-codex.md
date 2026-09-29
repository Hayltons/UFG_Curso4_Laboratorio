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

# Cap04 - Prompt 1 - Testes do service
Contexto: Tenho TaskService com CRUD de tarefas.
Objetivo: Gerar suite Pytest cobrindo criacao, listagem, atualizacao, exclusao e caso de erro por ID inexistente.
Estilo: Testes claros, nomes descritivos e fixtures simples.
Resposta: Codigo completo de tests/test_task_service.py. Pode criar o arquivo de código gerado

# Cap04 - Prompt 2 - Testes do PriorityAdvisor
Contexto: PriorityAdvisor possui heuristica local e fallback quando chamada externa falha.
Objetivo: Gerar testes para os tres niveis de prioridade e para fallback.
Estilo: Usar monkeypatch quando necessario.
Resposta: Codigo de tests/test_priority_advisor.py. Pode criar o arquivo de código gerado

# Cap04 - Prompt 3 - Testes de API
Contexto: API FastAPI com endpoints CRUD de /tasks.
Objetivo: Criar testes de rota com TestClient para status 201, 200, 204 e 404.
Estilo: Isolar dependencia de repositorio para evitar estado global entre testes.
Resposta: Codigo de tests/test_task_routes.py.Pode criar o arquivo de código gerado

# Cap04 - Prompt 4 - Refatoracao DRY/SRP
Analise os arquivos app/services/task_service.py e app/repositories/task_repository.py.
Objetivo: Sugerir refatoracao com foco em DRY e SRP sem mudar comportamento externo.
Resposta: 1) lista de mudancas propostas 2) patch sugerido por arquivo.

# Cap04 - Prompt 5 - README final tecnico
Contexto: MVP de micro-API de tarefas com prioridade assistida por IA.
Objetivo: Gerar README completo com instalacao, execucao, testes, arquitetura, uso da IA, limitacoes e proximos passos.
Estilo: Markdown profissional e objetivo.
Resposta: README inteiro. Pode alterar o arquivo existente

# Cap04 - Prompt EXTRA - Rodar testes neste ponto
Ok. agora que temos bastantes testes podemos executá-los para verificar se está tudo correto. Avalie

# Cap04 - Prompt EXTRA - Commits
Contexto: foram criados vários arquivos de teste, também o AGENTS.md e atualização do README.md, além do prompts\prompts-codex.md e do app\main.py em função de refatorações.
Objetivo: Suger
ir mensagens de commit no padrão Conventional Commits para cada arquivo incluído ou alterado.
Resposta: criar as linhas de commit e fazer o commit.

# Cap05 - Prompt EXTRA - Rodar a API
Eu gostaria de ver a API funcionando. Rode a API e mostre alguns casos de cliente criando e listando tasks

# Cap05 - Prompt EXTRA - Testar endpoints sem cobertura de teste
Verifique e informe se há endpoints não testados e amplie a cobertura de testes se necessário. Pergunte antes fazer alteração nos arquivos de teste, se for preciso.

# Cap05 - Prompt EXTRA - Commits
Contexto: Foi aumentada a cobertura de testes em tests\test_task_routes.py
Objetivo: Sugerir mensagens de commit no padrão Conventional Commits.
Resposta: criar as linhas de commit e fazer o commit.


# Cap05 - Prompt 1 - Makefile
Contexto: Projeto FastAPI com comandos de instalar dependencias, executar API e rodar testes.
Objetivo: Gerar Makefile com targets install, run e test.
Estilo: Simples e portavel.
Resposta: Conteudo completo de Makefile e crie o arquivo.

# Cap05 - Prompt 2 - .env.example
Contexto: O projeto usa integracao opcional de LLM.
Objetivo: Criar arquivo .env.example com variaveis necessarias e valores placeholder seguros.
Estilo: Minimalista.
Resposta: Crie o arquivo e salve-o. Além disso, verifique se as regras do arquivo .gitignore permitem que o arquivo .env.example fique visível e seja incluído em commits mas mantendo as regras de ignorar os demais arquivos .env ouo sensíveis.

# Cap05 - Prompt 3 - Revisao de README
Analise meu README e responda:
1) O que falta para ser reproduzivel em maquina limpa?
2) Quais secoes estao fracas para onboarding tecnico?
3) Como melhorar a secao de uso da IA?
Resposta em checklist objetivo.

# Cap05 - Prompt EXTRA - Commits
Contexto: foram feitas alterações no projeto incluindo o Makefile, .env.example, alterado o .gitignore e README. Se houver mais algo inclua.
Objetivo: Sugerir mensagens de commit no padrão Conventional Commits para cada arquivo alterado.
Resposta: criar as linhas de commit e fazer o commit.