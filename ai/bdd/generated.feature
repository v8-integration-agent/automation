```gherkin
# language: pt

Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar-me no sistema
  Para que eu possa usar os serviços bancários

  Scenario: Cadastro bem‑sucedido com dados válidos
    Given o usuário abre a página “Cadastro”
    When ele preenche todos os campos obrigatórios com valores válidos
    And ele clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Cadastro concluído com sucesso”
    And o usuário deve ser redirecionado para a tela de login

  Scenario: Cadastro falha por campos obrigatórios faltando
    Given o usuário abre a página “Cadastro”
    When ele deixa o campo “Nome” em branco
    And ele preenche os demais campos obrigatórios corretamente
    And ele clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Nome é obrigatório”
    And nenhum registro deve ser criado no banco de dados

  Scenario Outline: Cadastro falha por campos inválidos
    Given o usuário abre a página “Cadastro”
    When ele preenche o campo "<campo>" com "<valor>"
    And ele preenche os demais campos obrigatórios corretamente
    And ele clica em “Cadastrar”
    Then o sistema deve exibir a mensagem "<mensagem>"

    Examples:
      | campo   | valor          | mensagem                               |
      | Email   | usuario@      | Email inválido.                         |
      | Telefone| 12345          | Telefone inválido.                      |
      | CEP     | ABCDEFGH       | CEP inválido.                           |
      | Email   | usuario@gmail  | Email inválido.                         |
      | Telefone| (99) 9999-9999 | Telefone inválido.                      |

  Scenario: Cadastro falha por telefone no formato incorreto
    Given o usuário abre a página “Cadastro”
    When ele preenche o campo “Telefone” com “123abc”
    And preenche todos os demais campos corretamente
    And ele clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Telefone inválido”

Feature: Login
  Como usuário registrado
  Quero fazer login
  Para acessar minha conta

  Scenario: Login bem‑sucedido
    Given o usuário abre a página “Login”
    When ele preenche “Email” com “cliente@parabank.com”
    And ele preenche “Senha” com “SenhaSegura1”
    And ele clica em “Entrar”
    Then o sistema deve redirecionar para a “Dashboard da Conta”
    And deve exibir a mensagem “Bem‑vindo, Cliente”

  Scenario Outline: Login falha por credenciais inválidas
    Given o usuário abre a página “Login”
    When ele preenche “Email” com "<email>"
    And ele preenche “Senha” com "<senha>"
    And ele clica em “Entrar”
    Then o sistema deve exibir a mensagem "<mensagem>"

    Examples:
      | email               | senha            | mensagem                                 |
      | cliente@parabank.com | senhaErrada     | Credenciais inválidas.                   |
      | invalido@parabank.com | SenhaSegura1   | Credenciais inválidas.                   |
      | cliente@parabank.com |                 | Senha é obrigatória.                     |
      |                       | SenhaSegura1   | Email é obrigatório.                     |

  Scenario: Login falha por senha vazia
    Given o usuário abre a página “Login”
    When ele preenche “Email” com “cliente@parabank.com”
    And deixa o campo “Senha” em branco
    And ele clica em “Entrar”
    Then o sistema deve exibir a mensagem “Senha é obrigatória”

Feature: Acesso à Conta – Saldo e Extrato
  Como usuário autenticado
  Quero ver meu saldo atual e extrato
  Para acompanhar minhas finanças

  Scenario: Visualização de saldo atualizado após operação de crédito
    Given o usuário está logado e na sua “Dashboard”
    When o usuário efetua um depósito de R$ 500,00
    Then o saldo exibido deve ser “R$ 1.000,00” (exemplo)
    And a transação de depósito deve aparecer no extrato

  Scenario: Lista de transações no extrato em ordem cronológica
    Given o usuário está na página “Extrato”
    When o usuário tem três transações recentes
    Then as transações devem estar listadas da mais recente para a mais antiga
    And cada transação deve mostrar data, descrição, valor e saldo pós‑transação

Feature: Transferência de Fundos
  Como cliente
  Quero transferir dinheiro entre minhas contas
  Para gerenciar meu orçamento

  Scenario: Transferência bem‑sucedida entre duas contas
    Given o usuário está logado e na página “Transferir”
    When ele seleciona a conta de origem “Conta A”
    And seleciona a conta de destino “Conta B”
    And digita o valor “R$ 200,00”
    And confirma a transferência
    Then o saldo de “Conta A” deve reduzir em R$ 200,00
    And o saldo de “Conta B” deve aumentar em R$ 200,00
    And ambas as contas devem registrar a transação no histórico

  Scenario: Transferência falha por valor superior ao saldo
    Given o usuário está logado e na página “Transferir”
    When ele seleciona a conta de origem com saldo de R$ 100,00
    And seleciona a conta de destino “Conta C”
    And digita o valor “R$ 150,00”
    And tenta confirmar a transferência
    Then o sistema deve exibir a mensagem “Saldo insuficiente”
    And nenhuma transferência deve ocorrer

  Scenario: Transferência falha por campo obrigatório vazio
    Given o usuário está logado e na página “Transferir”
    When ele deixa o campo “Conta de Destino” em branco
    And digita o valor “R$ 50,00”
    And tenta confirmar a transferência
    Then o sistema deve exibir a mensagem “Conta de destino é obrigatória”

Feature: Solicitação de Empréstimo
  Como cliente
  Quero solicitar um empréstimo
  Para obter recursos adicionais

  Scenario Outline: Empréstimo aprovado com renda adequada
    Given o usuário está logado e na página “Solicitar Empréstimo”
    When ele informa “Valor do Empréstimo” como "<valor>"
    And ele informa “Renda Anual” como "<renda>"
    And ele confirma a solicitação
    Then o sistema deve retornar o status “Aprovado”
    And deve exibir a mensagem “Empréstimo aprovado. Valor: <valor>”

    Examples:
      | valor   | renda |
      | 10.000  | 80.000|
      | 5.000   | 30.000|

  Scenario Outline: Empréstimo negado por renda insuficiente
    Given o usuário está logado e na página “Solicitar Empréstimo”
    When ele informa “Valor do Empréstimo” como "<valor>"
    And ele informa “Renda Anual” como "<renda>"
    And ele confirma a solicitação
    Then o sistema deve retornar o status “Negado”
    And deve exibir a mensagem “Empréstimo negado. Renda insuficiente”

    Examples:
      | valor | renda |
      | 20.000| 20.000|
      | 15.000| 25.000|

Feature: Pagamento de Contas
  Como cliente
  Quero registrar um pagamento de conta
  Para manter minhas obrigações em dia

  Scenario: Pagamento de conta agendado para data futura
    Given o usuário está logado e na página “Pagar Conta”
    When ele informa “Beneficiário” como “Electricidade”
    And ele informa “Endereço” como “Rua X, 123”
    And ele informa “Cidade” como “São Paulo”
    And ele informa “Estado” como “SP”
    And ele informa “CEP” como “01001-000”
    And ele informa “Telefone” como “(11) 91234-5678”
    And ele informa “Conta de Destino” como “Conta B”
    And ele informa “Valor” como “R$ 150,00”
    And ele agenda a data de pagamento para “2025‑10‑01”
    And ele confirma o pagamento
    Then o pagamento deve aparecer no histórico de transações
    And o status deve ser “Agendado”
    And a data de pagamento futura deve ser respeitada

  Scenario: Pagamento de conta falha por data de pagamento inválida
    Given o usuário está logado e na página “Pagar Conta”
    When ele agenda a data de pagamento para “31/02/2025”
    And tenta confirmar o pagamento
    Then o sistema deve exibir a mensagem “Data inválida”

Feature: Requisitos Gerais de Navegação e Usabilidade
  Como usuário
  Quero navegar sem erros
  Para garantir experiência fluída

  Scenario: Todas as páginas carregam sem erros de navegação
    Given o usuário clica em cada link de menu (“Perfil”, “Contas”, “Transferências”, “Empréstimos”, “Contas a Pagar”)
    When cada página é carregada
    Then nenhuma página deve apresentar erros de carregamento

  Scenario: Mensagens de erro claras e objetivas
    Given o usuário tenta inserir “Email” como “abc”
    When ele submete o formulário
    Then o sistema deve exibir a mensagem “Formato de e‑mail inválido”

  Scenario: Menus e links consistentes em todas as páginas
    Given o usuário está na página “Dashboard”
    And está na página “Extrato”
    And está na página “Transferir”
    When ele verifica os links de navegação em cada página
    Then todos os links devem ser idênticos e apontar para os mesmos destinos

```