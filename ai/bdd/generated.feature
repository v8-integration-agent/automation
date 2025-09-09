**Feature: Cadastro de Usuário**

```gherkin
Scenario: Usuário cadastra conta com todos os campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche os campos: nome="Ana Silva", email="ana.silva@example.com", telefone="(11) 98765‑4321", CEP="01234‑567", endereço="Rua A, 123"
  And clica em “Cadastrar”
  Then o sistema exibe a mensagem de confirmação “Cadastro concluído com sucesso”
  And o usuário pode fazer login com as credenciais recém‑criadas

Scenario Outline: Usuário tenta cadastrar conta com campo inválido
  Given o usuário acessa a página de cadastro
  When ele preenche os campos: nome="<nome>", email="<email>", telefone="<telefone>", CEP="<cep>", endereço="Rua A, 123"
  And clica em “Cadastrar”
  Then o sistema exibe a mensagem de erro "<mensagem_erro>"
  And a conta não é criada

  Examples:
    | nome | email               | telefone | cep      | mensagem_erro                                 |
    |      | ana.silva@ex.com    | (11)9876 | 01234-567| "Nome é obrigatório"                          |
    | Ana  | anasilvaexample.com | (11)9876 | 01234-567| "Email inválido"                              |
    | Ana  | ana.silva@ex.com    | 111111   | 01234-567| "Telefone inválido"                           |
    | Ana  | ana.silva@ex.com    | (11)98765-4321 | 0123-567 | "CEP inválido"                                 |
```

---

**Feature: Login**

```gherkin
Scenario: Usuário faz login com credenciais válidas
  Given o usuário está na página de login
  When ele insere o email "<email>" e a senha "<senha>"
  And clica em “Login”
  Then o usuário é redirecionado para a página inicial da conta
  And o banner de boas‑vindas exibe “Bem‑vindo, <nome>”

  Examples:
    | email              | senha    | nome  |
    | ana.silva@example.com | 123456 | Ana   |

Scenario: Usuário tenta login com credenciais inválidas
  Given o usuário está na página de login
  When ele insere o email "<email>" e a senha "<senha>"
  And clica em “Login”
  Then o sistema exibe a mensagem de erro “Credenciais inválidas”
  And permanece na página de login
```

---

**Feature: Acesso à aplicação bancária (Saldo e Extrato)**

```gherkin
Scenario: Usuário visualiza saldo atualizado após operação
  Given o usuário está autenticado
  When ele realiza a operação de “Transferência” de R$100,00
  And volta à tela principal
  Then o saldo exibido deve ser “R$<saldo_atualizado>”

Scenario: Usuário visualiza extrato em ordem cronológica
  Given o usuário está autenticado
  When ele acessa a aba “Extrato”
  Then o extrato lista as transações recentes em ordem decrescente de data
  And cada linha exibe data, descrição, valor e saldo final
```

---

**Feature: Transferência de Fundos**

```gherkin
Scenario: Usuário transfere fundos entre contas válidas
  Given o usuário está autenticado
  And a conta “Corrente” tem saldo de R$500,00
  When ele seleciona a origem “Corrente”, destino “Poupança” e valor “R$200,00”
  And confirma a transferência
  Then o saldo da conta “Corrente” é de R$300,00
  And o saldo da conta “Poupança” é de R$200,00
  And a transação aparece no histórico de ambas as contas

Scenario Outline: Transferência não permitida por saldo insuficiente
  Given o usuário está autenticado
  And a conta “Corrente” tem saldo de R$<saldo>
  When ele tenta transferir R$<valor> da “Corrente” para “Poupança”
  Then o sistema exibe a mensagem de erro “Saldo insuficiente para esta transferência”
  And a conta não é debitada

  Examples:
    | saldo | valor |
    | 300   | 400   |
    | 100   | 101   |
```

---

**Feature: Solicitação de Empréstimo**

```gherkin
Scenario: Usuário solicita empréstimo e recebe aprovação
  Given o usuário está autenticado
  When ele insere valor do empréstimo “R$10.000,00” e renda anual “R$80.000,00”
  And submete a solicitação
  Then o sistema exibe “Status: Aprovado”

Scenario: Usuário solicita empréstimo e recebe negação
  Given o usuário está autenticado
  When ele insere valor do empréstimo “R$50.000,00” e renda anual “R$30.000,00”
  And submete a solicitação
  Then o sistema exibe “Status: Negado”
```

---

**Feature: Pagamento de Contas**

```gherkin
Scenario: Usuário registra pagamento de conta com dados completos
  Given o usuário está autenticado
  When ele preenche: beneficiário="Empresa XYZ", endereço="Av. B, 200", cidade="São Paulo", estado="SP", CEP="01000‑000", telefone="(11) 91234‑5678", conta="1234-5", valor="R$250,00", data="2025‑10‑01"
  And confirma o pagamento
  Then o sistema registra “Pagamento confirmado”
  And o pagamento aparece no histórico de transações
  And a conta de destino é debitada do valor correspondente

Scenario: Pagamento futuro respeita data de agendamento
  Given o usuário está autenticado
  When ele agenda pagamento de R$150,00 para “2025‑12‑15”
  And confirma
  Then o sistema exibe “Pagamento agendado para 15/12/2025”
  And o pagamento só aparece no histórico após a data agendada
```

---

**Feature: Requisitos Gerais de Navegação e Usabilidade**

```gherkin
Scenario: Todas as páginas carregam sem erros de navegação
  Given o usuário está autenticado
  When ele navega entre todas as páginas principais: “Conta”, “Transferência”, “Extrato”, “Empréstimo”, “Pagamento”
  Then cada página carrega sem erros ou mensagens de “404”

Scenario: Mensagens de erro são claras e objetivas
  Given o usuário tenta cadastrar conta com telefone inválido
  When ele submete o formulário
  Then a mensagem exibida deve ser “Telefone inválido. Use o formato (xx) xxxxx‑xxxx”

Scenario: Menus e links são consistentes em todas as páginas
  Given o usuário está em qualquer página do ParaBank
  When ele verifica o menu de navegação
  Then ele encontra os mesmos itens: “Conta”, “Transferência”, “Extrato”, “Empréstimo”, “Pagamento”, “Sair”
  And os links redirecionam para as páginas corretas
```