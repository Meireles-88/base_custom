# Roadmap de Desenvolvimento: Sistema Segurança Integrada (SI)

**Visão Geral:** Construir um ecossistema de segurança pública multi-institucional, com uma arquitetura de contextos que separa a visão global (Lobby) do ambiente de trabalho focado (Painel Institucional).

---

### **FASE 1: Fundação e Estrutura de Dados (Concluída)**

* [x] **Estrutura de Modelos:** Definir a arquitetura do banco de dados com a separação entre `Instituicao`, `TipoInstituicao`, `Estado` e `Municipio`.
* [x] **Estrutura de Hierarquia Local:** Refatorar os modelos `Cargo`, `Patente` e `Funcao` para que pertençam a uma `Instituicao` específica, garantindo autonomia local.
* [x] **Estrutura de Templates Base:** Criar a arquitetura de templates com os contextos `_bases/lobby_base.html` e `_bases/institucional_base.html`.
* [x] **População de Dados Iniciais:** Implementar o comando `popular_localidades` para cadastrar todos os Estados e Municípios do Brasil.
* [x] **CRUD de Instituições (Nível SI):** Construir a interface para o Admin SI criar, listar e editar as instituições no sistema.
* [x] **CRUD de Hierarquia Local (Nível SI):** Construir a interface para o Admin SI (ou Institucional) "entrar" no painel de uma instituição e gerenciar seus `Cargos`, `Patentes` e `Funções` locais.

---

### **FASE 2: Gestão de Pessoas e Vínculos (Próximos Passos)**

* **Objetivo:** Dar vida ao gerenciamento de efetivo e implementar o fluxo de trabalho para que usuários possam se juntar às instituições.

* [ ] **Passo 2.1: Gerenciamento de Membros (Atribuição de Cargos):**
    * **O que faremos:** Implementar a funcionalidade no "Painel de Gerenciamento Institucional". O administrador poderá clicar em "Gerenciar Efetivo", ver a lista de membros e, ao clicar em um membro, abrir uma tela para atribuir a ele o `Cargo`, a `Patente` e as `Funções` que foram criadas para aquela instituição.

* [ ] **Passo 2.2: Implementar o Cadastro Público de Usuários:**
    * **O que faremos:** Criar uma página de registro (`/registro/`) acessível a todos, onde um novo agente possa criar sua própria conta pessoal no Sistema SI, com verificação de e-mail.

* [ ] **Passo 2.3: Implementar a Solicitação de Vínculo:**
    * **O que faremos:** Após o login, um usuário "sem vínculo" verá uma página com uma lista de todas as instituições cadastradas. Ele poderá buscar a sua e clicar em "Solicitar Vínculo".

* [ ] **Passo 2.4: Implementar a Aprovação de Vínculos:**
    * **O que faremos:** No painel do Administrador Institucional, criar uma nova seção "Solicitações Pendentes". Ele poderá ver a lista de usuários que pediram para entrar, visualizar seus perfis e clicar em "Aprovar" ou "Rejeitar".

---

### **FASE 3: Funcionalidades Avançadas e UX (Futuro)**

* **Objetivo:** Enriquecer a plataforma com ferramentas de inteligência, segurança e colaboração.
* [ ] **Implementar o Contexto Dinâmico na Interface:** Refatorar a `sidebar` e outros elementos para que mudem visualmente com base no contexto ativo (`instituicao_ativa`).
* [ ] **Módulo de Ocorrências:** Construir o núcleo operacional do sistema para registro e acompanhamento de ocorrências.
* [ ] **Dashboard Contextual:** Dar vida aos painéis do Admin Institucional e do Agente de Campo.
* [ ] **Controle de Acesso por Função (RBAC):** Integrar o sistema de Grupos e Permissões do Django às nossas `Funções`.
* [ ] **Log de Auditoria:** Implementar o módulo de auditoria para rastrear ações críticas.
* [ ] **Módulo de Câmeras:** Criar a funcionalidade para que instituições possam cadastrar e gerenciar seus equipamentos de vigilância.
* [ ] **Feed de Notícias e Comunicação:** Implementar o modelo `Publicacao` para criar o feed de notícias no "Lobby".