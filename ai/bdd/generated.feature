## Feature: Cadastro de Usuário  

```gherkin
Feature: Cadastro de Usuário
  Para que novos clientes possam utilizar o ParaBank, o sistema deve permitir a criação de contas com todos os campos obrigatórios preenchidos e validar os dados de entrada.

  Scenario: Cadastro bem‑sucedido com dados válidos
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com “Ana Silva”
    And preenche "Email" com “ana.silva@example.com”
    And preenche "Telefone" com “(11) 91234-5678”
    And preenche "CEP" com “01001-000”
    And preenche "Senha" com “Password123”
    And confirma a senha com “Password123”
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Cadastro concluído com sucesso.”
    And o usuário deve ser redirecionado para a tela de login

  Scenario Outline: Cadastro falha com campos obrigatórios vazios
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com "<nome>"
    And preenche "Email" com "<email>"
    And preenche "Telefone" com "<telefone>"
    And preenche "CEP" com "<cep>"
    And preenche "Senha" com "<senha>"
    And confirma a senha com "<confirmação>"
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “<mensagem>”

    Examples:
      | nome | email                | telefone | cep       | senha      | confirmação | mensagem                                  |
      |      | ana.silva@example.com | (11) 91234-5678 | 01001-000 | Password123 | Password123 | Nome é obrigatório                         |
      | Ana  |                       | (11) 91234-5678 | 01001-000 | Password123 | Password123 | Email é obrigatório                        |
      | Ana  | ana.silva@example.com |           | 01001-000 | Password123 | Password123 | Telefone é obrigatório                     |
      | Ana  | ana.silva@example.com | (11) 91234-5678 |           | Password123 | Password123 | CEP é obrigatório                          |
      | Ana  | ana.silva@example.com | (11) 91234-5678 | 01001-000 |            |            | Senha e confirmação são obrigatórias      |

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com “Ana Silva”
    And preenche "Email" com "<email>"
    And preenche "Telefone" com "<telefone>"
    And preenche "CEP" com "<cep>"
    And preenche "Senha" com “Password123”
    And confirma a senha com “Password123”
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “<mensagem>”

    Examples:
      | email                   | telefone       | cep       | mensagem                                   |
      | ana.silvaexample.com    | (11) 91234-5678 | 01001-000 | Email inválido                             |
      | ana.silva@example.com   | 912345678       | 01001-000 | Telefone inválido                          |
      | ana.silva@example.com   | (11) 91234-5678 | 01         | CEP inválido                               |
```

---

## Feature: Login

```gherkin
Feature: Login
  O sistema deve permitir que usuários autenticados acessem sua conta, exibindo erro para credenciais inválidas.

  Scenario: Login bem‑sucedido
    Given o usuário está na página de login
    When ele insere “Username” com “anasilva”
    And insere “Password” com “Password123”
    And clica em “Entrar”
    Then o sistema deve redirecionar para a página inicial da conta
    And exibir “Bem‑vindo, Ana Silva”

  Scenario Outline: Login falha com credenciais inválidas
    Given o usuário está na página de login
    When ele insere “Username” com "<usuario>"
    And insere “Password” com "<senha>"
    And clica em “Entrar”
    Then o sistema deve exibir a mensagem “<mensagem>”

    Examples:
      | usuario   | senha          | mensagem                            |
      | anasilva  | wrongPassword  | Credenciais inválidas. Tente novamente |
      | wrongUser | Password123    | Credenciais inválidas. Tente novamente |
```

---

## Feature: Acesso à aplicação bancária (Saldo e Extrato)

```gherkin
Feature: Saldo e Extrato
  O cliente deve ter acesso a saldo atualizado e histórico de transações.

  Background:
    Dado o usuário está autenticado e na página inicial

  Scenario: Visualização de saldo após depósito
    When ele faz um depósito de R$ 1.000,00
    Then o saldo deve ser R$ 1.000,00

  Scenario: Extrato listado em ordem cronológica
    When ele visualiza o extrato
    Then o extrato deve mostrar as transações em ordem decrescente de data
    And a transação mais recente deve aparecer primeiro
```

---

## Feature: Transferência de Fundos

```gherkin
Feature: Transferência de Fundos
  O sistema deve permitir transferir dinheiro entre contas com validação de saldo e registro de histórico.

  Background:
    Dado o usuário está autenticado e na página de transferência
    E a conta “Conta Corrente” possui saldo de R$ 5.000,00
    E a conta “Conta Poupança” possui saldo de R$ 2.000,00

  Scenario: Transferência bem‑sucedida
    When ele seleciona conta de origem “Conta Corrente”
    And seleciona conta de destino “Conta Poupança”
    And digita valor “R$ 500,00”
    And confirma a transferência
    Then a conta “Conta Corrente” deve mostrar saldo de R$ 4.500,00
    And a conta “Conta Poupança” deve mostrar saldo de R$ 2.500,00
    And ambas as contas devem registrar a transação no histórico

  Scenario Outline: Transferência bloqueada por saldo insuficiente
    When ele seleciona conta de origem "<conta_origem>"
    And seleciona conta de destino "<conta_destino>"
    And digita valor "<valor>"
    And confirma a transferência
    Then o sistema deve exibir a mensagem “Saldo insuficiente para transferir R$ <valor>”

    Examples:
      | conta_origem   | conta_destino | valor     |
      | Conta Corrente | Conta Poupança | R$ 5.500,00 |

  Scenario: Transferência para conta inexistente
    When ele seleciona conta de origem “Conta Corrente”
    And seleciona conta de destino “Conta Não Existente”
    And digita valor “R$ 100,00”
    And confirma a transferência
    Then o sistema deve exibir a mensagem “Conta de destino não encontrada”
```

---

## Feature: Solicitação de Empréstimo

```gherkin
Feature: Solicitação de Empréstimo
  O cliente pode solicitar um empréstimo informando valor e renda anual, recebendo aprovação ou negação.

  Background:
    Dado o usuário está autenticado e na página de empréstimos

  Scenario: Empréstimo aprovado
    When ele insere valor “R$ 10.000,00”
    And insere renda anual “R$ 120.000,00”
    And clica em “Solicitar”
    Then o sistema deve exibir a mensagem “Empréstimo aprovado”
    And o valor deve aparecer no extrato como crédito

  Scenario: Empréstimo negado por renda insuficiente
    When ele insere valor “R$ 50.000,00”
    And insere renda anual “R$ 30.000,00”
    And clica em “Solicitar”
    Then o sistema deve exibir a mensagem “Empréstimo negado – renda insuficiente”
```

---

## Feature: Pagamento de Contas

```gherkin
Feature: Pagamento de Contas
  O cliente pode registrar pagamentos, incluindo dados completos do beneficiário e data de agendamento.

  Background:
    Dado o usuário está autenticado e na página de pagamentos
    And a conta “Conta Corrente” possui saldo de R$ 3.000,00

  Scenario: Pagamento confirmado imediatamente
    When ele preenche "Beneficiário" com “Pedro”
    And preenche "Endereço" com “Rua das Flores”
    And preenche "Cidade" com “São Paulo”
    And preenche "Estado" com “SP”
    And preenche "CEP" com “01001-000”
    And preenche "Telefone" com “(11) 99876-5432”
    And preenche "Conta de destino" com “Conta Poupança”
    And preenche "Valor" com “R$ 300,00”
    And preenche "Data" com “Hoje”
    And clica em “Confirmar”
    Then o saldo da conta “Conta Corrente” deve diminuir em R$ 300,00
    And a transação deve aparecer no histórico

  Scenario Outline: Pagamento futuro agendado
    When ele preenche "Beneficiário" com “Maria”
    And preenche "Endereço" com “Av. Central”
    And preenche "Cidade" com “Rio de Janeiro”
    And preenche "Estado" com “RJ”
    And preenche "CEP" com “20001-000”
    And preenche "Telefone" com “(21) 98765-4321”
    And preenche "Conta de destino" com “Conta Poupança”
    And preenche "Valor" com “<valor>”
    And preenche "Data" com “<data>”
    And clica em “Confirmar”
    Then a transação deve aparecer no histórico com data agendada “<data>”
    And o saldo não deve ser debitado imediatamente

    Examples:
      | valor     | data      |
      | R$ 200,00 | 2025-10-15|
      | R$ 150,00 | 2025-12-01|
```

---

## Feature: Requisitos Gerais de Navegação e Usabilidade

```gherkin
Feature: Navegação e Usabilidade
  Todas as páginas devem carregar sem erro, exibir mensagens claras e manter links consistentes.

  Scenario: Carregamento de todas as páginas sem erro
    Given o usuário navega para “/home”
    Then a página deve carregar sem mensagens de erro
    And o cabeçalho deve exibir “ParaBank”

    When ele clica no link “Transferências”
    Then a página de transferências deve carregar sem erro

    When ele clica no link “Empréstimos”
    Then a página de empréstimos deve carregar sem erro

    When ele clica no link “Pagamentos”
    Then a página de pagamentos deve carregar sem erro

  Scenario: Mensagens de erro claras e objetivas
    When ele tenta salvar o cadastro com campos vazios
    Then o sistema deve exibir a mensagem “Nome é obrigatório”

    When ele tenta transferir R$ 1.000,00 de uma conta com saldo R$ 500,00
    Then o sistema deve exibir a mensagem “Saldo insuficiente para transferir R$ 1.000,00”

  Scenario: Consistência de links e menus
    Given o usuário está na página inicial
    Then o menu principal deve conter os links: “Conta”, “Transferências”, “Empréstimos”, “Pagamentos”

    When o usuário navega para “Conta”
    Then o menu principal ainda deve conter os mesmos links

    When o usuário navega para “Transferências”
    Then o menu principal ainda deve conter os mesmos links
```

---

Esses cenários cobrem todos os requisitos de aceite especificados, incluindo situações de sucesso e falha, validações de campos, controle de saldo, histórico de transações, aprovação/negação de empréstimos e consistência da navegação. Você pode adaptá‑los ao seu framework de teste BDD (Cucumber, SpecFlow, Behave, etc.) e expandi‑los com cenários de borda, performance ou acessibilidade conforme a necessidade.