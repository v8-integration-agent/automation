## 📜 **Features em Gherkin – Sistema ParaBank**  
*(As cenários foram escritos em português e seguem a estrutura **Given‑When‑Then**.)*  

---  

### 1️⃣ **Cadastro de Usuário**  
*Arquivo: `CadastroUsuario.feature`*

```gherkin
Feature: Cadastro de Usuário
  Como um visitante do ParaBank
  Quero criar uma nova conta
  Para que eu possa usar os serviços do banco

  Background:
    Dado que eu estou na página de cadastro

  # 1.1. Cadastro bem‑sucedido
  Scenario: Usuário cria conta com dados válidos
    Quando preencho todos os campos obrigatórios com dados válidos
    E clico no botão "Cadastrar"
    Then devo ver a mensagem "Cadastro concluído com sucesso"
    And devo ser redirecionado para a página de login

  # 1.2. Validação de telefone
  Scenario Outline: Telefone inválido impede cadastro
    When preencho o campo "Telefone" com "<telefone>"
    And preencho os demais campos obrigatórios com dados válidos
    And clico no botão "Cadastrar"
    Then devo ver a mensagem de erro "Telefone inválido"
    
    Examples:
      | telefone        |
      | 123            |
      | (11) 9876-543   |
      | +55 11 9876-5432 |
  
  # 1.3. Validação de CEP
  Scenario Outline: CEP inválido impede cadastro
    When preencho o campo "CEP" com "<cep>"
    And preencho os demais campos obrigatórios com dados válidos
    And clico no botão "Cadastrar"
    Then devo ver a mensagem de erro "CEP inválido"
    
    Examples:
      | cep    |
      | 1234   |
      | abcde  |
      | 123456789 |
  
  # 1.4. Validação de e‑mail
  Scenario Outline: E‑mail inválido impede cadastro
    When preencho o campo "E‑mail" com "<email>"
    And preencho os demais campos obrigatórios com dados válidos
    And clico no botão "Cadastrar"
    Then devo ver a mensagem de erro "E‑mail inválido"
    
    Examples:
      | email            |
      | user@          |
      | user.com       |
      | @domain.com    |
```

---

### 2️⃣ **Login**  
*Arquivo: `Login.feature`*

```gherkin
Feature: Login
  Como usuário registrado
  Quero acessar minha conta
  Para que eu possa consultar saldo e fazer transações

  Background:
    Dado que eu já possuo uma conta cadastrada com e‑mail "<email>" e senha "<senha>"

  Scenario: Usuário faz login com credenciais válidas
    When entro na página de login
    And preencho o campo "E‑mail" com "<email>"
    And preencho o campo "Senha" com "<senha>"
    And clico no botão "Entrar"
    Then devo ser redirecionado para a página inicial da conta
    And devo ver a mensagem "Bem‑vindo, <nome>"

  Scenario Outline: Login falha com credenciais inválidas
    When entro na página de login
    And preencho o campo "E‑mail" com "<email>"
    And preencho o campo "Senha" com "<senha>"
    And clico no botão "Entrar"
    Then devo ver a mensagem de erro "<mensagem>"
    
    Examples:
      | email                | senha      | mensagem                         |
      | wrong@example.com    | qualquer   | Usuário ou senha incorretos      |
      | valid@example.com    | errada     | Usuário ou senha incorretos      |
      |                     | senha123   | E‑mail é obrigatório             |
```

---

### 3️⃣ **Acesso à Conta (Saldo e Extrato)**  
*Arquivo: `AcessoConta.feature`*

```gherkin
Feature: Acesso à Conta
  Como usuário autenticado
  Quero visualizar saldo e extrato
  Para acompanhar minhas finanças

  Background:
    Dado que eu estou logado com e‑mail "<email>" e senha "<senha>"
    E minha conta possui saldo inicial de <saldo_inicial>

  Scenario: Visualizar saldo após operação
    When realizo a transferência de <valor> para a conta "<conta_destino>"
    And volto à página inicial da conta
    Then devo ver o saldo atualizado: "<saldo_final>"

  Scenario: Extrato lista transações em ordem cronológica
    When volto à página "Extrato"
    Then devo ver a lista de transações ordenada de mais recente a mais antiga
    And cada transação deve exibir data, descrição e valor
```

---

### 4️⃣ **Transferência de Fundos**  
*Arquivo: `TransferenciaFundos.feature`*

```gherkin
Feature: Transferência de Fundos
  Como usuário autenticado
  Quero transferir dinheiro entre contas
  Para movimentar recursos de forma segura

  Background:
    Dado que eu estou logado com e‑mail "<email>" e senha "<senha>"
    E minha conta tem saldo de <saldo_inicial>

  Scenario: Transferência bem‑sucedida
    When realizo a transferência de <valor> para a conta "<conta_destino>"
    Then o valor deve ser debitado da minha conta
    And o valor deve ser creditado na conta "<conta_destino>"
    And a transação deve aparecer no histórico das duas contas

  Scenario Outline: Transferência proibida por saldo insuficiente
    When realizo a transferência de "<valor>" para a conta "<conta_destino>"
    Then devo ver a mensagem de erro "Saldo insuficiente para transferência"
    
    Examples:
      | valor   | conta_destino |
      | 1000    | 987654        |
      | 50000   | 123456        |
```

---

### 5️⃣ **Solicitação de Empréstimo**  
*Arquivo: `SolicitacaoEmprestimo.feature`*

```gherkin
Feature: Solicitação de Empréstimo
  Como usuário autenticado
  Quero solicitar um empréstimo
  Para obter recursos adicionais

  Background:
    Dado que eu estou logado com e‑mail "<email>" e senha "<senha>"

  Scenario Outline: Empréstimo aprovado
    When informo o valor do empréstimo "<valor_emprestimo>" e renda anual "<renda_anual>"
    And confirmo a solicitação
    Then devo ver a mensagem "Empréstimo Aprovado"
    
    Examples:
      | valor_emprestimo | renda_anual |
      | 2000             | 50000       |
      | 10000            | 120000      |

  Scenario Outline: Empréstimo negado
    When informo o valor do empréstimo "<valor_emprestimo>" e renda anual "<renda_anual>"
    And confirmo a solicitação
    Then devo ver a mensagem "Empréstimo Negado"
    
    Examples:
      | valor_emprestimo | renda_anual |
      | 50000            | 30000       |
      | 100000           | 40000       |
```

---

### 6️⃣ **Pagamento de Contas**  
*Arquivo: `PagamentoContas.feature`*

```gherkin
Feature: Pagamento de Contas
  Como usuário autenticado
  Quero pagar contas com agendamento
  Para garantir pagamentos dentro do prazo

  Background:
    Dado que eu estou logado com e‑mail "<email>" e senha "<senha>"
    E minha conta tem saldo de <saldo_inicial>

  Scenario: Pagamento de conta futuro
    When registro o pagamento com:
      | Beneficiário | Endereço | Cidade | Estado | CEP   | Telefone   | Conta Destino | Valor | Data de Pagamento |
      | Energia      | Rua X    | São Paulo | SP  | 01234-567 | +55 11 9999-9999 | 123456        | 150   | 2025-10-15 |
    And confirmo o pagamento
    Then devo ver a mensagem "Pagamento agendado com sucesso"
    And o pagamento deve aparecer no histórico de transações na data futura

  Scenario: Pagamento imediato
    When registro o pagamento com:
      | Beneficiário | Endereço | Cidade | Estado | CEP   | Telefone   | Conta Destino | Valor | Data de Pagamento |
      | Água          | Rua Y    | Rio de Janeiro | RJ  | 98765-432 | +55 21 8888-8888 | 654321        | 80    | 2025-08-01 |
    And confirmo o pagamento
    Then o saldo da conta deve ser debitado em <valor>
    And o pagamento deve aparecer no histórico de transações imediatamente
```

---

### 7️⃣ **Requisitos Gerais de Navegação e Usabilidade**  
*Arquivo: `RequisitosGerais.feature`*

```gherkin
Feature: Navegação e Usabilidade
  Como usuário do ParaBank
  Quero que a aplicação seja fácil de usar e sem erros
  Para garantir uma experiência agradável

  Scenario: Todas as páginas carregam sem erros
    When navego por todas as rotas principais (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
    Then cada página deve carregar sem erros de console e sem redirecionamentos inesperados

  Scenario: Mensagens de erro são claras e objetivas
    When realizo uma ação inválida (ex.: telefone sem dígito)
    Then a mensagem de erro deve ser exibida em destaque e explicar claramente o problema

  Scenario: Links e menus são consistentes
    When verifico o menu principal em todas as páginas
    Then todos os itens de menu (Home, Contas, Transferir, Empréstimos, Pagamentos, Logout) devem estar presentes e funcionando
```

---

> **Observações**  
> - Os valores (`<valor>`, `<saldo_inicial>`, etc.) são placeholders que podem ser substituídos por dados reais nos testes automatizados.  
> - Para cenários de aprovação/negação de empréstimo, a lógica de aprovação pode ser baseada em regras de negócio (ex.: renda > 4× valor).  
> - As mensagens de erro e sucesso devem ser exatamente as exibidas pelo sistema para garantir a correspondência durante a execução.  

Assim, esses cenários cobrem **todos** os critérios de aceitação listados no documento, proporcionando uma base robusta para testes automatizados e manuais.