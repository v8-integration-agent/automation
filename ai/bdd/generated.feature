```gherkin
# --------------- 1. Cadastro de Usuário ---------------
Feature: Cadastro de Usuário
  Como usuário do ParaBank
  Quero registrar um novo perfil
  Para poder utilizar os serviços bancários

  Background:
    Dado que estou na página de cadastro

  Scenario Outline: Cadastro bem‑sucedido com dados válidos
    When preencho o formulário com:
      | Campo          | Valor               |
      | Nome completo  | <nome>              |
      | CPF            | <cpf>               |
      | Telefone       | <telefone>          |
      | CEP            | <cep>               |
      | Email          | <email>             |
      | Senha          | <senha>             |
      | Confirmação    | <senha>             |
    And clico em "Cadastrar"
    Then a mensagem "<mensagem>" deve ser exibida
    And o usuário deve ser redirecionado para a página de login

    Examples:
      | nome            | cpf          | telefone     | cep       | email                | senha     | mensagem                        |
      | João Silva      | 123.456.789-00 | (11)98765-4321 | 12345-678 | joao@email.com      | Pass123!  | Cadastro realizado com sucesso!|

  Scenario Outline: Cadastro falha por campos obrigatórios vazios
    When preencho o formulário com:
      | Campo          | Valor |
      | Nome completo  | <nome> |
      | CPF            | <cpf> |
      | Telefone       | <telefone> |
      | CEP            | <cep> |
      | Email          | <email> |
      | Senha          | <senha> |
      | Confirmação    | <senha> |
    And clico em "Cadastrar"
    Then a mensagem "<campo>" deve ser exibida

    Examples:
      | nome | cpf | telefone | cep | email | senha | campo                  |
      |      | 123 | 12345    | 123 | a@b   | Pass123! | "Nome completo é obrigatório" |
      | João |     | 12345    | 123 | a@b   | Pass123! | "CPF é obrigatório" |
      | João | 123 |          | 123 | a@b   | Pass123! | "Telefone é obrigatório" |
      | João | 123 | 12345    |     | a@b   | Pass123! | "CEP é obrigatório" |
      | João | 123 | 12345    | 123 |       | Pass123! | "Email é obrigatório" |

  Scenario Outline: Cadastro falha por dados inválidos
    When preencho o formulário com:
      | Campo          | Valor |
      | Nome completo  | <nome> |
      | CPF            | <cpf> |
      | Telefone       | <telefone> |
      | CEP            | <cep> |
      | Email          | <email> |
      | Senha          | <senha> |
      | Confirmação    | <senha> |
    And clico em "Cadastrar"
    Then a mensagem "<mensagem>" deve ser exibida

    Examples:
      | nome | cpf           | telefone          | cep      | email                | senha   | mensagem                          |
      | João | 123.456.789-99 | (11)98765-4321 | 12345-678 | joao@email.com      | Pass123! | "CPF inválido" |
      | João | 123.456.789-00 | 12345-6789     | 12345-678 | joao@email.com      | Pass123! | "Telefone inválido" |
      | João | 123.456.789-00 | (11)98765-4321 | 12345-678 | joaoemail.com       | Pass123! | "Email inválido" |


# --------------- 2. Login ---------------
Feature: Login
  Como usuário já cadastrado
  Quero acessar minha conta
  Para visualizar saldo e fazer operações

  Background:
    Dado que estou na página de login

  Scenario: Login bem‑sucedido com credenciais válidas
    When insero "joao@email.com" no campo Email
    And insero "Pass123!" no campo Senha
    And clico em "Entrar"
    Then a página inicial da conta deve ser exibida
    And o nome "João Silva" deve aparecer na barra de navegação

  Scenario: Login falha com credenciais inválidas
    When insero "joao@email.com" no campo Email
    And insero "Err0r!" no campo Senha
    And clico em "Entrar"
    Then a mensagem "Usuário ou senha inválidos" deve ser exibida

# --------------- 3. Acesso a Saldo e Extrato ---------------
Feature: Acesso à conta (Saldo e Extrato)
  Como usuário logado
  Quero ver meu saldo atualizado
  E ver o extrato em ordem cronológica

  Background:
    Dado que estou na página inicial da conta

  Scenario: Visualizar saldo atualizado
    Then o saldo exibido deve ser igual ao valor real da conta

  Scenario: Extrato lista transações recentes em ordem cronológica
    When navego até a página de "Extrato"
    Then as transações devem estar listadas em ordem decrescente de data

# --------------- 4. Transferência de Fundos ---------------
Feature: Transferência de Fundos
  Como usuário logado
  Quero transferir valores entre contas
  Para movimentar meus recursos

  Background:
    Dado que estou na página de Transferência

  Scenario Outline: Transferência bem‑sucedida
    When seleciono a conta de origem "<origem>"
    And seleciono a conta de destino "<destino>"
    And informo o valor "<valor>"
    And confirmo a transferência
    Then o saldo da conta "<origem>" deve diminuir em "<valor>"
    And o saldo da conta "<destino>" deve aumentar em "<valor>"
    And a transação deve aparecer no histórico das duas contas

    Examples:
      | origem | destino | valor |
      | Conta A | Conta B | 100   |
      | Conta B | Conta C | 50    |

  Scenario: Transferência não permitida por saldo insuficiente
    When seleciono a conta de origem "Conta A"
    And seleciono a conta de destino "Conta B"
    And informo o valor "1000"
    And confirmo a transferência
    Then a mensagem "Saldo insuficiente" deve ser exibida

# --------------- 5. Solicitação de Empréstimo ---------------
Feature: Solicitação de Empréstimo
  Como usuário logado
  Quero solicitar um empréstimo
  Para financiar projetos

  Background:
    Dado que estou na página de Empréstimos

  Scenario Outline: Empréstimo aprovado
    When informo o valor do empréstimo "<valor>"
    And informo a renda anual "<renda>"
    And submeta a solicitação
    Then o status "<status>" deve ser exibido

    Examples:
      | valor | renda | status   |
      | 5000  | 80000 | "Aprovado"|
      | 12000 | 95000 | "Aprovado"|

  Scenario Outline: Empréstimo negado
    When informo o valor do empréstimo "<valor>"
    And informo a renda anual "<renda>"
    And submeta a solicitação
    Then o status "<status>" deve ser exibido

    Examples:
      | valor | renda | status   |
      | 20000 | 30000 | "Negado" |
      | 15000 | 40000 | "Negado" |

# --------------- 6. Pagamento de Contas ---------------
Feature: Pagamento de Contas
  Como usuário logado
  Quero registrar pagamentos
  Para manter meus compromissos em dia

  Background:
    Dado que estou na página de Pagamentos

  Scenario Outline: Pagamento futuro agendado
    When informo:
      | Beneficiário | Endereço  | Cidade   | Estado | CEP     | Telefone      | Conta destino | Valor | Data       |
      | <benef>      | Rua X, 1  | São Paulo| SP     | 01001-000 | (11)1111-2222 | Conta C        | <valor> | <data>     |
    And submeta o pagamento
    Then a mensagem "Pagamento agendado para <data>" deve ser exibida
    And o pagamento deve aparecer no histórico na data correta

    Examples:
      | benef         | valor | data       |
      | Conta de luz  | 150   | 2025-12-01 |
      | Internet      | 80    | 2025-12-03 |

  Scenario: Pagamento imediato
    When informo:
      | Beneficiário | Endereço  | Cidade   | Estado | CEP     | Telefone      | Conta destino | Valor | Data       |
      | Conta de água | Rua Y, 5 | Rio de Janeiro | RJ | 20001-000 | (21)3333-4444 | Conta D        | 90    | 2025-11-15 |
    And submeta o pagamento
    Then o pagamento deve aparecer imediatamente no histórico
    And o saldo da conta deve ser debitado em "<valor>"

# --------------- 7. Requisitos Gerais de Navegação e Usabilidade ---------------
Feature: Navegação e Usabilidade
  Como usuário
  Quero que a aplicação carregue sem erros
  E que todas as mensagens de erro sejam claras

  Scenario: Todas as páginas carregam corretamente
    When navego para cada página (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
    Then nenhuma página deve apresentar erro 500 ou erro de carregamento

  Scenario: Links e menus consistentes
    When verifico os menus de navegação
    Then todos os itens devem estar presentes em todas as páginas

  Scenario: Mensagens de erro claras
    When provoque um erro (por exemplo, login inválido)
    Then a mensagem exibida deve conter linguagem clara e instruções de correção

```