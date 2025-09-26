```gherkin
# language: pt

############################################
# Cadastro de Usuário
############################################
Feature: Cadastro de Usuário

  @cadastro @valid
  Scenario: Cadastro com todos os campos obrigatórios preenchidos
    Given o usuário abre a página de cadastro
    When ele preenche "Nome" com "Maria Silva"
    And ele preenche "Telefone" com "(11) 91234-5678"
    And ele preenche "CEP" com "01001-000"
    And ele preenche "Email" com "maria.silva@email.com"
    And ele preenche "Senha" com "SenhaSegura123"
    And ele clica no botão "Cadastrar"
    Then o sistema deve exibir a mensagem "Cadastro concluído com sucesso"
    And o usuário deve ser redirecionado para a página de login

  @cadastro @invalid
  Scenario: Cadastro com telefone inválido
    Given o usuário abre a página de cadastro
    When ele preenche "Telefone" com "abc123"
    And ele preenche os demais campos obrigatórios corretamente
    And ele clica no botão "Cadastrar"
    Then o sistema deve exibir a mensagem "Telefone informado inválido"

  @cadastro @invalid
  Scenario: Cadastro com CEP inválido
    Given o usuário abre a página de cadastro
    When ele preenche "CEP" com "123"
    And ele preenche os demais campos obrigatórios corretamente
    And ele clica no botão "Cadastrar"
    Then o sistema deve exibir a mensagem "CEP informado inválido"

  @cadastro @invalid
  Scenario: Cadastro com email inválido
    Given o usuário abre a página de cadastro
    When ele preenche "Email" com "maria.silva"
    And ele preenche os demais campos obrigatórios corretamente
    And ele clica no botão "Cadastrar"
    Then o sistema deve exibir a mensagem "Email inválido"

  @cadastro @invalid
  Scenario: Cadastro sem preencher campos obrigatórios
    Given o usuário abre a página de cadastro
    When ele deixa os campos em branco
    And ele clica no botão "Cadastrar"
    Then o sistema deve exibir mensagens de erro para todos os campos obrigatórios

  @cadastro @success
  Scenario: Usuário pode fazer login após cadastro bem-sucedido
    Given o usuário possui conta registrada
    When ele abre a página de login
    And ele preenche "Email" com "maria.silva@email.com"
    And ele preenche "Senha" com "SenhaSegura123"
    And ele clica no botão "Entrar"
    Then o usuário deve ser redirecionado para a página inicial da conta


############################################
# Login
############################################
Feature: Login

  @login @valid
  Scenario: Login com credenciais válidas
    Given o usuário tem credenciais válidas
    When ele abre a página de login
    And ele preenche "Email" com "maria.silva@email.com"
    And ele preenche "Senha" com "SenhaSegura123"
    And ele clica no botão "Entrar"
    Then o usuário deve ser redirecionado para a página inicial da conta

  @login @invalid
  Scenario: Login com credenciais inválidas
    Given o usuário tem credenciais inválidas
    When ele abre a página de login
    And ele preenche "Email" com "maria.silva@email.com"
    And ele preenche "Senha" com "SenhaErrada"
    And ele clica no botão "Entrar"
    Then o sistema deve exibir a mensagem "Credenciais inválidas"


############################################
# Acesso à Conta (Saldo e Extrato)
############################################
Feature: Acesso à Conta

  @saldo @balance
  Scenario: Visualizar saldo atualizado após operação financeira
    Given o usuário está logado
    And a conta tem saldo inicial de R$ 1.000,00
    When o usuário realiza uma transferência de R$ 200,00 para outra conta
    Then o saldo da conta deve ser atualizado para R$ 800,00

  @extrato @chronology
  Scenario: Extrato lista transações recentes em ordem cronológica
    Given o usuário tem várias transações recentes
    When o usuário acessa a página de extrato
    Then as transações devem aparecer listadas do mais recente ao mais antigo


############################################
# Transferência de Fundos
############################################
Feature: Transferência de Fundos

  @transferencia @valid
  Scenario: Transferência de fundos válida
    Given a conta origem tem R$ 1.000,00
    And a conta destino tem R$ 200,00
    When o usuário seleciona a conta origem
    And seleciona a conta destino
    And entra o valor de R$ 300,00
    And confirma a transferência
    Then o valor de R$ 300,00 deve ser debitado da conta origem
    And o valor de R$ 300,00 deve ser creditado na conta destino
    And a transação deve aparecer no histórico de ambas as contas

  @transferencia @invalid
  Scenario: Transferência com valor superior ao saldo disponível
    Given a conta origem tem R$ 100,00
    When o usuário tenta transferir R$ 200,00
    Then o sistema deve exibir a mensagem "Saldo insuficiente para a transferência"


############################################
# Solicitação de Empréstimo
############################################
Feature: Solicitação de Empréstimo

  @emprestimo @approved
  Scenario: Empréstimo aprovado
    Given o usuário tem renda anual de R$ 120.000,00
    When ele solicita um empréstimo de R$ 50.000,00
    Then o sistema deve retornar o status "Aprovado"

  @emprestimo @denied
  Scenario: Empréstimo negado
    Given o usuário tem renda anual de R$ 20.000,00
    When ele solicita um empréstimo de R$ 50.000,00
    Then o sistema deve retornar o status "Negado"


############################################
# Pagamento de Contas
############################################
Feature: Pagamento de Contas

  @pagamento @record
  Scenario: Registro de pagamento
    Given o usuário entra na página de pagamento
    And ele preenche "Beneficiário" com "Pedro Santos"
    And ele preenche "Endereço" com "Rua A, 123"
    And ele preenche "Cidade" com "São Paulo"
    And ele preenche "Estado" com "SP"
    And ele preenche "CEP" com "01001-000"
    And ele preenche "Telefone" com "(11) 98765-4321"
    And ele preenche "Conta de Destino" com "123456"
    And ele preenche "Valor" com R$ 150,00
    And ele preenche "Data" com "2025-12-01"
    When ele confirma o pagamento
    Then o pagamento deve ser incluído no histórico de transações

  @pagamento @future
  Scenario: Pagamento futuro respeita a data de agendamento
    Given o usuário agenda um pagamento para "2025-12-01"
    When ele visualiza pagamentos futuros
    Then o pagamento deve aparecer com a data correta e não ser debitado até a data agendada


############################################
# Navegação e Usabilidade
############################################
Feature: Navegação e Usabilidade

  @navegacao @load
  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega entre todas as páginas do sistema
    Then cada página deve carregar corretamente sem mensagens de erro de navegação

  @mensagem @error
  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta fazer login com senha vazia
    When ele clica no botão "Entrar"
    Then o sistema deve exibir a mensagem "Senha não pode estar em branco"

  @menu @consistent
  Scenario: Links e menus são consistentes em todas as páginas
    Given o usuário abre a página inicial
    And ele abre a página de cadastro
    And ele abre a página de extrato
    Then em todas as páginas os mesmos itens de menu devem estar presentes e visíveis
```