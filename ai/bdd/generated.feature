```gherkin
# Feature: Cadastro de Usuário
# @cadastro
Feature: Registro de novos usuários no ParaBank
  Como usuário que ainda não possui conta,
  Eu quero me cadastrar no sistema,
  Para que eu possa usar os serviços bancários.

  Scenario: Cadastro bem‑sucedido com todos os campos preenchidos
    Given o usuário acessa a página de cadastro
    When preenche os campos obrigatórios com dados válidos
      | Campo            | Valor             |
      | Nome             | João da Silva     |
      | Email            | joao@email.com    |
      | Telefone         | (11) 98765-4321   |
      | CEP              | 12345-678          |
      | Endereço         | Rua A, 123        |
      | Cidade           | São Paulo         |
      | Estado           | SP                |
      | Senha            | P@ssw0rd!         |
      | Confirmação Senha| P@ssw0rd!         |
    When clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Cadastro concluído com sucesso”
    And o usuário deve ser redirecionado para a tela de login

  Scenario: Cadastro falha quando campos obrigatórios estão vazios
    Given o usuário acessa a página de cadastro
    When deixa os campos obrigatórios em branco
    Then o sistema deve exibir mensagem de erro “Este campo é obrigatório” para cada campo vazio
    And nenhuma conta deve ser criada

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a página de cadastro
    When preenche os campos obrigatórios com os valores abaixo
      | Campo    | Valor |
      | <Campo>  | <Valor> |
    And preenche os demais campos com dados válidos
    When clica em “Cadastrar”
    Then o sistema exibe a mensagem de erro “<MensagemErro>”

    Examples:
      | Campo      | Valor               | MensagemErro                      |
      | Telefone   | 1234                | Telefone inválido                |
      | CEP        | ABCDE               | CEP inválido                     |
      | Email      | joao[at]email.com   | Email inválido                   |

# Feature: Login
# @login
Feature: Acesso ao sistema
  Como usuário registrado,
  Eu quero fazer login com credenciais válidas,
  Para que eu possa acessar minha conta.

  Scenario: Login bem‑sucedido com credenciais válidas
    Given o usuário está na página de login
    When preenche “Email” com “joao@email.com”
    And preenche “Senha” com “P@ssw0rd!”
    And clica em “Entrar”
    Then o usuário deve ser redirecionado para a página inicial da conta
    And o saldo inicial deve ser exibido

  Scenario: Login falha com credenciais inválidas
    Given o usuário está na página de login
    When preenche “Email” com “joao@email.com”
    And preenche “Senha” com “errada123”
    And clica em “Entrar”
    Then o sistema exibe a mensagem de erro “Credenciais inválidas”

# Feature: Acesso à aplicação bancária (Saldo e Extrato)
# @saldo @extrato
Feature: Visualização de saldo e extrato
  Como cliente logado,
  Eu quero ver meu saldo atualizado e extrato recente,
  Para que eu possa monitorar minhas transações.

  Scenario: Saldo atualizado após depósito
    Given o usuário já fez um depósito de R$ 100,00
    When acessa a página inicial
    Then o saldo exibido deve refletir o depósito

  Scenario: Extrato lista transações em ordem cronológica
    Given o usuário tem as seguintes transações:
      | Data       | Descrição           | Valor      |
      | 01/10/2024 | Saldo Inicial       | R$ 1.000  |
      | 02/10/2024 | Depósito            | R$ 100    |
      | 03/10/2024 | Transferência       | -R$ 50    |
    When acessa a aba “Extrato”
    Then o extrato deve listar as transações da mais recente à mais antiga

# Feature: Transferência de Fundos
# @transferencia
Feature: Transferir dinheiro entre contas
  Como usuário,
  Eu quero transferir fundos de uma conta para outra,
  Para que eu possa mover recursos entre minhas contas.

  Scenario: Transferência bem‑sucedida
    Given o usuário tem saldo de R$ 500,00 em Conta A
    And existe a Conta B
    When seleciona Conta A como origem
    And seleciona Conta B como destino
    And entra o valor R$ 200,00
    And confirma a transferência
    Then o saldo de Conta A deve ser R$ 300,00
    And o saldo de Conta B deve ser R$ 200,00
    And a transação aparece no histórico de ambas as contas

  Scenario Outline: Transferência falha quando valor excede saldo
    Given o usuário tem saldo de R$ <Saldo> em Conta A
    When tenta transferir R$ <Transferir> de Conta A para Conta B
    Then o sistema exibe a mensagem “Saldo insuficiente”
    And a transferência não é realizada

    Examples:
      | Saldo | Transferir |
      | 150   | 200        |
      | 100   | 150        |

# Feature: Solicitação de Empréstimo
# @emprestimo
Feature: Pedir um empréstimo
  Como cliente,
  Eu quero solicitar um empréstimo,
  Para que eu possa obter recursos adicionais.

  Scenario: Empréstimo aprovado
    Given o usuário informa valor R$ 10.000 e renda anual R$ 80.000
    When envia a solicitação de empréstimo
    Then o sistema deve exibir “Solicitação Aprovada”

  Scenario: Empréstimo negado
    Given o usuário informa valor R$ 50.000 e renda anual R$ 30.000
    When envia a solicitação de empréstimo
    Then o sistema deve exibir “Solicitação Negada”

# Feature: Pagamento de Contas
# @pagamento
Feature: Registrar pagamento de contas
  Como cliente,
  Eu quero registrar um pagamento de conta,
  Para que eu possa acompanhar meus débitos.

  Scenario: Pagamento imediato
    Given o usuário informa:
      | Beneficiário | Endereço         | Cidade    | Estado | CEP     | Telefone     | Conta Destino | Valor | Data        |
      | Luz          | Av. Central, 10  | Rio       | RJ     | 10000-000 | (21) 1234-5678 | 987654321 | R$ 80 | 05/10/2024 |
    When confirma o pagamento
    Then o sistema deve registrar a transação no histórico
    And exibir mensagem “Pagamento realizado com sucesso”

  Scenario: Pagamento agendado futuro
    Given o usuário informa data de pagamento “12/10/2024”
    When confirma o pagamento
    Then o sistema deve marcar a transação como “Agendada”
    And a data de vencimento deve ser exibida no extrato

# Feature: Navegação e Usabilidade
# @usabilidade
Feature: Navegação consistente e mensagens claras
  Como usuário,
  Eu quero que todas as páginas carreguem corretamente e que as mensagens de erro sejam claras,
  Para que eu tenha uma experiência de uso fluída.

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega por todas as funcionalidades do sistema
    Then nenhuma página deve apresentar erros de carregamento ou links quebrados

  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta enviar um formulário com dados inválidos
    When submete o formulário
    Then cada campo com erro exibe uma mensagem explicativa em linguagem simples

  Scenario: Menus e links são consistentes em todas as páginas
    Given o usuário navega entre diferentes seções do aplicativo
    When verifica a presença de menus e links
    Then os mesmos itens de menu devem estar disponíveis em todas as páginas
```