## Feature: Cadastro de Usuário

```gherkin
Feature: Cadastro de Usuário

  Scenario Outline: Cadastro com sucesso
    Given o usuário está na página de cadastro
    When preenche "<campo>" com "<valor>"
    And preenche os demais campos obrigatórios com valores válidos
    And clica em “Cadastrar”
    Then a mensagem de confirmação “Cadastro concluído!” deve ser exibida
    And o usuário pode fazer login com as credenciais recém‑criados

    Examples:
      | campo      | valor         |
      | Nome       | João Silva    |
      | Email      | joao@email.com|

  Scenario Outline: Cadastro falha por campo inválido
    Given o usuário está na página de cadastro
    When preenche "<campo>" com "<valor inválido>"
    And preenche os demais campos obrigatórios com valores válidos
    And clica em “Cadastrar”
    Then deve ser exibida a mensagem de erro "<mensagem>"

    Examples:
      | campo  | valor inválido | mensagem                        |
      | Email  | joaoemail.com  | “Email inválido. Digite um e‑mail válido.” |
      | Telefone | 123          | “Telefone inválido. Use apenas números.”   |
      | CEP    | abcde         | “CEP inválido. Digite apenas números.”     |
```

---

## Feature: Login

```gherkin
Feature: Login

  Scenario: Login bem‑sucedido
    Given existe um usuário cadastrado com e‑mail “maria@email.com” e senha “Segura123”
    When o usuário insere “maria@email.com” no campo de e‑mail
    And insere “Segura123” no campo de senha
    And clica em “Entrar”
    Then o usuário é redirecionado para a página inicial da conta
    And o banner “Bem‑vindo Maria!” é exibido

  Scenario: Login falha por credenciais inválidas
    Given existe um usuário cadastrado com e‑mail “maria@email.com”
    When o usuário insere “maria@email.com” no campo de e‑mail
    And insere “Errada456” no campo de senha
    And clica em “Entrar”
    Then a mensagem “Credenciais inválidas. Tente novamente.” é exibida
```

---

## Feature: Acesso à Conta (Saldo e Extrato)

```gherkin
Feature: Acesso à Conta

  Scenario: Visualização do saldo atualizado após depósito
    Given o usuário está logado e possui saldo de R$ 1.000,00
    When realiza um depósito de R$ 500,00
    Then o saldo exibido deve ser R$ 1.500,00

  Scenario: Extrato lista transações recentes em ordem cronológica
    Given o usuário está logado
    And possui as seguintes transações:
      | Data       | Tipo      | Valor  |
      | 2024-09-08 | Depósito  | 1.000  |
      | 2024-09-10 | Saque     | 200    |
    When acessa a página de extrato
    Then a lista de transações deve mostrar:
      | 1 | 2024-09-10 | Saque | -200 |
      | 2 | 2024-09-08 | Depósito | +1.000 |
```

---

## Feature: Transferência de Fundos

```gherkin
Feature: Transferência de Fundos

  Scenario: Transferência bem‑sucedida entre contas
    Given o usuário possui R$ 1.000,00 na conta A
    And a conta B possui R$ 500,00
    When o usuário seleciona conta A como origem
    And seleciona conta B como destino
    And define o valor R$ 300,00
    And confirma a transferência
    Then a conta A deve exibir saldo de R$ 700,00
    And a conta B deve exibir saldo de R$ 800,00
    And ambas as contas devem registrar a transação no histórico

  Scenario: Transferência falha por saldo insuficiente
    Given o usuário possui R$ 100,00 na conta A
    When tenta transferir R$ 200,00
    Then a mensagem “Saldo insuficiente” deve ser exibida
    And nenhuma conta é alterada
```

---

## Feature: Solicitação de Empréstimo

```gherkin
Feature: Solicitação de Empréstimo

  Scenario: Empréstimo aprovado
    Given o usuário tem renda anual de R$ 120.000,00
    When solicita empréstimo de R$ 50.000,00
    Then o sistema deve retornar “Aprovado”
    And o valor será adicionado ao saldo da conta

  Scenario: Empréstimo negado
    Given o usuário tem renda anual de R$ 20.000,00
    When solicita empréstimo de R$ 50.000,00
    Then o sistema deve retornar “Negado”
    And nenhum valor é creditado
```

---

## Feature: Pagamento de Contas

```gherkin
Feature: Pagamento de Contas

  Scenario: Pagamento imediato registrado no histórico
    Given o usuário possui saldo suficiente
    When registra pagamento com:
      | Beneficiário | Endereço      | Cidade | Estado | CEP  | Telefone | Conta Destino | Valor | Data       |
      | Luz Eletrônica | Rua A, 100 | São Paulo | SP | 01234-567 | 12345678 | 1234-5 | R$ 150,00 | 2024-09-10 |
    And confirma o pagamento
    Then a transação deve aparecer no histórico de pagamento
    And o saldo deve ser debitado em R$ 150,00

  Scenario: Pagamento futuro agendado
    Given o usuário possui saldo suficiente
    When registra pagamento com data futura “2024-12-01”
    And confirma o pagamento
    Then o pagamento é marcado como “Agendado”
    And não aparece no extrato até a data de vencimento
```

---

## Feature: Requisitos Gerais de Navegação e Usabilidade

```gherkin
Feature: Navegação e Usabilidade

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega entre as seções (Login, Cadastro, Extrato, Transferência, Empréstimo, Pagamento)
    When acessa cada página
    Then nenhuma página exibe erro de carregamento

  Scenario: Mensagens de erro são claras e objetivas
    When ocorre qualquer falha (ex.: campo obrigatório vazio)
    Then a mensagem exibida deve conter:
      | Contexto | Mensagem                |
      | Email   | “Campo email é obrigatório.” |

  Scenario: Links e menus são consistentes em todas as páginas
    Given o usuário está em qualquer página
    When verifica o menu principal
    Then todos os links (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento) estão presentes
    And ao clicar em cada link, a página correspondente é carregada corretamente
```

---

Esses cenários cobrem os requisitos de aceite apresentados, incluindo casos positivos e negativos, e asseguram que a aplicação `ParaBank` funcione conforme especificado para testes e estudos.