```gherkin
# Feature: Cadastro de Usuário
# ---------------------------------
Feature: Cadastro de Usuário

  Scenario: Cadastros completos são aceitos
    Given o usuário está na página de cadastro
    When ele preenche todos os campos obrigatórios com dados válidos
    And clica no botão “Registrar”
    Then o sistema exibe a mensagem “Cadastro concluído com sucesso”
    And o usuário aparece autenticado na página de login

  Scenario Outline: Dados inválidos bloqueiam o cadastro
    Given o usuário está na página de cadastro
    When ele preenche os campos obrigatórios com "<campo>" inválido
    And clica em “Registrar”
    Then o sistema exibe a mensagem de erro correspondente ao "<campo>"
    And nenhum dado é salvo no banco

    Examples:
      | campo      |
      | telefone   |
      | CEP        |
      | email      |

  Scenario: Campos obrigatórios não preenchidos impedem o cadastro
    Given o usuário está na página de cadastro
    When ele deixa o campo “Nome” em branco
    And clica em “Registrar”
    Then o sistema exibe a mensagem “Nome é obrigatório”

# Feature: Login
# ---------------------------------
Feature: Login

  Scenario: Usuário com credenciais válidas entra no sistema
    Given o usuário possui conta registrada
    And está na página de login
    When ele digita seu e‑mail e senha corretos
    And clica em “Entrar”
    Then o sistema redireciona para a página inicial da conta
    And mostra o saldo atual do usuário

  Scenario: Credenciais inválidas retornam erro
    Given o usuário está na página de login
    When ele digita um e‑mail não registrado
    And uma senha incorreta
    And clica em “Entrar”
    Then o sistema exibe a mensagem “Credenciais inválidas”

  Scenario: Usuário recém‑registrado pode fazer login imediatamente
    Given o usuário acabou de se registrar com sucesso
    When ele tenta fazer login com as mesmas credenciais
    Then o sistema aceita e redireciona para a página inicial

# Feature: Acesso à Conta – Saldo e Extrato
# ---------------------------------
Feature: Acesso à Conta – Saldo e Extrato

  Scenario: Saldo reflete operações recentes
    Given o usuário está logado na sua conta
    When ele realiza um depósito de R$ 500,00
    And volta à página inicial
    Then o saldo exibido é atualizado com o novo valor

  Scenario: Extrato lista transações em ordem cronológica
    Given o usuário tem pelo menos três transações registradas
    When ele acessa a aba “Extrato”
    Then a lista mostra as transações mais recentes no topo
    And cada item exibe data, descrição e valor

# Feature: Transferência de Fundos
# ---------------------------------
Feature: Transferência de Fundos

  Scenario: Transferência dentro do saldo disponível
    Given o usuário tem saldo de R$ 1.000,00 na conta A
    And a conta B possui saldo de R$ 200,00
    When ele transfere R$ 300,00 da conta A para a conta B
    And confirma a operação
    Then R$ 300,00 é debitado da conta A
    And R$ 300,00 é creditado na conta B
    And ambas as contas mostram a transação no histórico

  Scenario: Transferência acima do saldo não é permitida
    Given o usuário tem saldo de R$ 150,00 na conta A
    When ele tenta transferir R$ 200,00 da conta A para a conta B
    And confirma a operação
    Then o sistema exibe a mensagem “Saldo insuficiente”
    And nenhum débito ocorre

  Scenario: Transferência para a própria conta é bloqueada
    Given o usuário tem saldo de R$ 400,00
    When ele seleciona a própria conta como destino
    And tenta transferir R$ 100,00
    Then o sistema exibe a mensagem “Conta de destino deve ser diferente da origem”

# Feature: Solicitação de Empréstimo
# ---------------------------------
Feature: Solicitação de Empréstimo

  Scenario: Empréstimo aprovado quando renda atende limite
    Given o usuário possui renda anual de R$ 120.000,00
    When ele solicita empréstimo de R$ 20.000,00
    And confirma a requisição
    Then o sistema retorna “Aprovado”
    And o valor fica disponível na conta do usuário

  Scenario: Empréstimo negado por renda insuficiente
    Given o usuário possui renda anual de R$ 30.000,00
    When ele solicita empréstimo de R$ 50.000,00
    And confirma a requisição
    Then o sistema retorna “Negado”

  Scenario: Solicitação sem preencher campos obrigatórios falha
    Given o usuário abre a tela de solicitação
    When ele deixa o campo “Valor do empréstimo” em branco
    And tenta submeter
    Then o sistema exibe a mensagem “Valor é obrigatório”

# Feature: Pagamento de Contas
# ---------------------------------
Feature: Pagamento de Contas

  Scenario: Pagamento normal é registrado
    Given o usuário está na página de pagamento
    When ele preenche: beneficiário “Pedro”, endereço “Rua X, 123”, cidade “São Paulo”, estado “SP”, CEP “01000-000”, telefone “(11) 99999-9999”, conta de destino “123456”, valor R$ 150,00, data “2025-10-01”
    And confirma o pagamento
    Then o sistema exibe “Pagamento agendado com sucesso”
    And a transação aparece no histórico da conta

  Scenario: Pagamento futuro respeita data de agendamento
    Given o usuário agenda pagamento para “2025-12-01”
    When ele visualiza a lista de transações
    Then a transação está marcada como “Agendado”
    And não é debitada antes da data de vencimento

  Scenario: Falta de dados obrigatórios impede o pagamento
    Given o usuário abre a tela de pagamento
    When ele deixa o campo “Telefone” em branco
    And tenta enviar
    Then o sistema exibe a mensagem “Telefone é obrigatório”

# Feature: Navegação e Usabilidade
# ---------------------------------
Feature: Navegação e Usabilidade

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega entre todas as seções do aplicativo
    Then nenhuma página apresenta erros de carregamento nem exceções

  Scenario: Mensagens de erro são claras e objetivas
    When o usuário tenta acessar recurso sem permissão
    Then o sistema exibe “Acesso negado” em vez de “Erro inesperado”

  Scenario: Menu de navegação está consistente em todas as páginas
    Given o usuário está em qualquer página
    When ele observa o menu superior
    Then os links “Home”, “Transferência”, “Extrato”, “Empréstimo”, “Pagamentos” são sempre visíveis e corretos
```