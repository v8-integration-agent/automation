```gherkin
# Feature: Cadastro de Usuário
Feature: Cadastro de Usuário
  Para garantir que apenas dados válidos sejam aceitos, o sistema deve validar
  todos os campos obrigatórios e apresentar mensagens de erro claras.

  Scenario: Cadastro bem‑sucedido
    Given o usuário abre a página de cadastro
    When ele preenche todos os campos obrigatórios com valores válidos
    And clica em “Cadastrar”
    Then o sistema exibe a mensagem “Cadastro concluído com sucesso”
    And o usuário pode realizar login com as credenciais recém‑criado

  Scenario Outline: Cadastro com campo obrigatório em branco
    Given o usuário abre a página de cadastro
    When ele deixa o campo "<campo>" em branco e preenche os demais com dados válidos
    And clica em “Cadastrar”
    Then o sistema exibe a mensagem “Campo <campo> é obrigatório”

    Examples:
      | campo          |
      | Nome           |
      | Email          |
      | Senha          |
      | CEP            |
      | Telefone       |

  Scenario Outline: Cadastro com dados inválidos
    Given o usuário abre a página de cadastro
    When ele preenche o campo "<campo>" com valor "<valor_invalido>" e os demais com dados válidos
    And clica em “Cadastrar”
    Then o sistema exibe a mensagem “<mensagem_erro>”

    Examples:
      | campo   | valor_invalido      | mensagem_erro                                  |
      | Email   | usuario@          | Email inválido                                 |
      | CEP     | 123                 | CEP inválido                                   |
      | Telefone| 12abc               | Telefone inválido                              |

# Feature: Login
Feature: Login
  O sistema deve permitir o acesso apenas com credenciais válidas.

  Scenario: Login com credenciais válidas
    Given o usuário está na página de login
    When ele insere email e senha válidos
    And clica em “Entrar”
    Then o sistema redireciona para a página inicial da conta

  Scenario: Login com credenciais inválidas
    Given o usuário está na página de login
    When ele insere email ou senha inválidos
    And clica em “Entrar”
    Then o sistema exibe a mensagem “Credenciais inválidas”

# Feature: Acesso à Conta (Saldo e Extrato)
Feature: Acesso à Conta
  O usuário deve visualizar saldo atualizado e extrato ordenado cronologicamente.

  Scenario: Exibição de saldo atualizado
    Given o usuário está na página inicial da conta
    When ele acessa a seção “Saldo”
    Then o sistema exibe o saldo correto e atualizado

  Scenario: Lista de extrato em ordem cronológica
    Given o usuário está na página “Extrato”
    When ele visualiza as transações
    Then as transações são listadas em ordem decrescente de data (mais recente primeiro)

# Feature: Transferência de Fundos
Feature: Transferência de Fundos
  O sistema deve gerenciar transferências entre contas, evitando saldo insuficiente.

  Scenario: Transferência bem‑sucedida
    Given o usuário está na página de transferências
    When ele seleciona “Conta A” como origem
    And seleciona “Conta B” como destino
    And insere valor “100.00” (≤ saldo disponível)
    And confirma a transferência
    Then o valor “100.00” é debitado da Conta A
    And o valor “100.00” é creditado na Conta B
    And a transação é registrada nos históricos de ambas as contas

  Scenario: Transferência com saldo insuficiente
    Given o usuário está na página de transferências
    When ele tenta transferir “2000.00” (excede o saldo)
    And confirma a transferência
    Then o sistema exibe a mensagem “Saldo insuficiente”

  Scenario Outline: Transferência com valor inválido
    Given o usuário na página de transferências
    When ele insere valor "<valor>"
    And confirma
    Then o sistema exibe a mensagem “<mensagem>”

    Examples:
      | valor          | mensagem                   |
      | 0              | Valor mínimo é 0,01        |
      | -50.00         | Valor negativo não permitido|

# Feature: Solicitação de Empréstimo
Feature: Solicitação de Empréstimo
  O usuário pode solicitar empréstimo e receber feedback de aprovação ou negação.

  Scenario: Empréstimo aprovado
    Given o usuário está na página de empréstimo
    When ele insere valor “5000” e renda anual “60000”
    And envia a solicitação
    Then o sistema exibe “Aprovado”

  Scenario: Empréstimo negado
    Given o usuário está na página de empréstimo
    When ele insere valor “20000” e renda anual “30000”
    And envia a solicitação
    Then o sistema exibe “Negado”

# Feature: Pagamento de Contas
Feature: Pagamento de Contas
  O usuário deve registrar pagamentos com dados completos e respeitar a data agendada.

  Scenario: Pagamento futuro agendado
    Given o usuário está na página de pagamento de contas
    When ele preenche beneficiário, endereço, cidade, estado, CEP, telefone, conta de destino, valor “150.00” e data “2025-12-31”
    And confirma
    Then o sistema registra o pagamento
    And o pagamento aparece no histórico de transações com data “2025-12-31”

  Scenario Outline: Pagamento com campo obrigatório em branco
    Given o usuário na página de pagamento
    When ele deixa o campo "<campo>" em branco e preenche os demais
    And confirma
    Then o sistema exibe “Campo <campo> é obrigatório”

    Examples:
      | campo           |
      | Beneficiário    |
      | Endereço        |
      | Cidade          |
      | Estado          |
      | CEP             |
      | Telefone        |
      | Conta de destino|
      | Valor           |
      | Data            |

# Feature: Requisitos Gerais de Navegação e Usabilidade
Feature: Navegação e Usabilidade
  Garantir que todas as páginas carreguem sem erros e que mensagens de erro sejam claras.

  Scenario: Todas as páginas carregam corretamente
    Given o usuário navega por todas as páginas do sistema
    When ele acessa cada uma
    Then nenhuma página apresenta erro de carregamento

  Scenario: Mensagens de erro claras e objetivas
    Given o usuário tenta uma operação inválida (ex.: transferir com saldo insuficiente)
    When a ação falha
    Then a mensagem exibida é clara, objetiva e localizada próximo ao campo afetado

  Scenario: Consistência de menus e links
    Given o usuário está em qualquer página
    When ele verifica a barra de navegação
    Then todos os links (Home, Conta, Transferência, Empréstimo, Pagamento) estão presentes e levam à página correta
```