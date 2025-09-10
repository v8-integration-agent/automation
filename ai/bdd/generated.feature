**Feature: Cadastro de Usuário**

```gherkin
Feature: Registro de novos clientes

  Scenario: Cadastro bem-sucedido com dados válidos
    Given o usuário acessa a página de cadastro
    When ele preenche todos os campos obrigatórios com dados válidos
    And clica em “Registrar”
    Then o sistema exibe a mensagem “Cadastro concluído com sucesso”
    And o usuário pode logar com as credenciais cadastradas

  Scenario Outline: Cadastro falha ao enviar dados inválidos
    Given o usuário acessa a página de cadastro
    When ele preenche o campo "<campo>" com "<valor_invalido>"
    And clica em “Registrar”
    Then o sistema exibe a mensagem de erro “<mensagem_erro>”

    Examples:
      | campo      | valor_invalido | mensagem_erro                 |
      | Telefone   | 123abc         | Telefone inválido             |
      | CEP        | 999999         | CEP inválido                  |
      | Email      | usuario@      | Email inválido                |

  Scenario: Cadastro falha quando campos obrigatórios estão vazios
    Given o usuário acessa a página de cadastro
    When ele deixa os campos “Nome”, “CPF” e “Senha” vazios
    And clica em “Registrar”
    Then o sistema exibe as mensagens “Campo obrigatório” para cada campo vazio
```

---

**Feature: Login**

```gherkin
Feature: Autenticação de usuários

  Scenario: Login bem-sucedido com credenciais válidas
    Given o usuário possui cadastro ativo
    When ele entra com e‑mail “usuario@parabank.com” e senha “senhaSegura123”
    And clica em “Login”
    Then o sistema redireciona para a página inicial da conta
    And exibe o nome do usuário “Usuário Teste”

  Scenario: Login falha com credenciais inválidas
    Given o usuário possui cadastro ativo
    When ele entra com e‑mail “usuario@parabank.com” e senha “senhaErrada”
    And clica em “Login”
    Then o sistema exibe a mensagem de erro “Credenciais inválidas”
```

---

**Feature: Visualização de Saldo e Extrato**

```gherkin
Feature: Acesso ao saldo e ao extrato da conta

  Scenario: Exibição correta do saldo após uma operação
    Given o usuário está logado
    When ele realiza um depósito de R$ 500,00
    Then o saldo exibido na página inicial deve ser atualizado para “R$ 500,00”

  Scenario: Lista de transações em ordem cronológica
    Given o usuário está logado
    When ele acessa a aba “Extrato”
    Then o extrato deve listar as transações mais recentes primeiro
    And cada linha contém data, descrição e valor
```

---

**Feature: Transferência de Fundos**

```gherkin
Feature: Transferência entre contas

  Scenario: Transferência válida entre duas contas
    Given o usuário está logado e possui saldo de R$ 1.000,00 na conta A
    When ele seleciona a conta de origem “Conta A”
    And seleciona a conta de destino “Conta B”
    And insere o valor “R$ 200,00”
    And confirma a transferência
    Then a conta A deve refletir saldo de “R$ 800,00”
    And a conta B deve refletir saldo de “R$ 200,00”
    And ambas as contas devem registrar a transação no histórico

  Scenario: Transferência rejeitada por saldo insuficiente
    Given o usuário está logado e possui saldo de R$ 100,00 na conta A
    When ele tenta transferir “R$ 150,00” para a conta B
    And confirma a transferência
    Then o sistema exibe a mensagem “Saldo insuficiente para esta transferência”

  Scenario Outline: Validação dos campos de transferência
    Given o usuário está logado
    When ele insere "<valor>" no campo de valor
    And tenta confirmar a transferência
    Then o sistema exibe a mensagem "<mensagem>"

    Examples:
      | valor        | mensagem                                 |
      | (campo vazio)| Valor da transferência é obrigatório     |
      | -100,00      | Valor inválido: deve ser positivo         |
```

---

**Feature: Solicitação de Empréstimo**

```gherkin
Feature: Pedido de crédito

  Scenario: Empréstimo aprovado com renda adequada
    Given o usuário possui cadastro ativo
    When ele acessa a aba “Solicitar Empréstimo”
    And insere o valor “R$ 10.000,00”
    And informa renda anual “R$ 70.000,00”
    And confirma a solicitação
    Then o sistema retorna o status “Aprovado”
    And exibe mensagem “Empréstimo aprovado. Parabéns!”

  Scenario: Empréstimo negado por renda insuficiente
    Given o usuário possui cadastro ativo
    When ele acessa a aba “Solicitar Empréstimo”
    And insere o valor “R$ 10.000,00”
    And informa renda anual “R$ 20.000,00”
    And confirma a solicitação
    Then o sistema retorna o status “Negado”
    And exibe mensagem “Empréstimo negado devido à renda insuficiente”
```

---

**Feature: Pagamento de Contas**

```gherkin
Feature: Registro e agendamento de pagamentos

  Scenario: Pagamento imediato com todos os dados
    Given o usuário está logado
    When ele acessa a aba “Pagar Conta”
    And preenche:
      | Beneficiário | Empresa X |
      | Endereço     | Rua Y, 100|
      | Cidade       | São Paulo |
      | Estado       | SP        |
      | CEP          | 12345-678 |
      | Telefone     | 1199999999|
      | Conta Destino| 12345678  |
      | Valor        | R$ 250,00 |
      | Data         | Hoje      |
    And confirma o pagamento
    Then o pagamento aparece no histórico de transações
    And o saldo da conta diminui em R$ 250,00

  Scenario: Agendamento de pagamento futuro
    Given o usuário está logado
    When ele acessa a aba “Pagar Conta”
    And preenche os campos com data “01/12/2025”
    And confirma o pagamento
    Then o sistema exibe “Pagamento agendado para 01/12/2025”
    And o pagamento aparece no histórico com status “Agendado”
```

---

**Feature: Navegação e Usabilidade**

```gherkin
Feature: Navegação consistente e mensagens claras

  Scenario: Todas as páginas carregam sem erros
    Given o usuário está logado
    When ele navega por todas as seções (Conta, Transferências, Empréstimos, Pagamentos)
    Then cada página deve carregar com sucesso sem mensagens de erro

  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta inserir dados inválidos em qualquer formulário
    When ele clica em “Enviar”
    Then o sistema exibe uma mensagem de erro específica e compreensível

  Scenario: Menu e links são consistentes em todas as páginas
    Given o usuário está em qualquer página
    When ele verifica a barra de navegação
    Then todos os links (Conta, Transferências, Empréstimos, Pagamentos, Logout) são visíveis e levam às páginas corretas
```

---

Esses cenários cobrem os critérios de aceite especificados no documento, garantindo que cada funcionalidade seja testada quanto à integridade dos dados, comportamento do sistema, exibição de informações e experiência do usuário.