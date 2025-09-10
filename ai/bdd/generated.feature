```gherkin
# --------------------------------------
# Feature: Cadastro de Usuário
# --------------------------------------
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar uma conta no sistema
  Para que eu possa usar os serviços bancários

  Background:
    Dado que o usuário está na página de cadastro

  Scenario: Cadastro bem‑sucesso
    Quando preencho todos os campos obrigatórios com valores válidos
    E envio o formulário
    Then devo ver a mensagem “Cadastro concluído com sucesso”
    And a opção de login deve estar habilitada

  Scenario Outline: Validação de campos obrigatórios vazios
    When deixo o campo "<campo>" em branco
    And envio o formulário
    Then vejo a mensagem de erro “<mensagem>”

    Examples:
      | campo              | mensagem                            |
      | Nome               | Nome é obrigatório                   |
      | Sobrenome          | Sobrenome é obrigatório              |
      | Telefone           | Telefone é obrigatório               |
      | CEP                | CEP é obrigatório                    |
      | Email              | Email é obrigatório                  |
      | Senha              | Senha é obrigatória                  |
      | Confirmação Senha  | Confirmação da senha é obrigatória  |

  Scenario Outline: Validação de formatos inválidos
    When insiro "<valor>" no campo "<campo>"
    And envio o formulário
    Then vejo a mensagem de erro “<mensagem>”

    Examples:
      | campo    | valor           | mensagem                      |
      | Telefone | 123             | Telefone inválido             |
      | CEP      | 12               | CEP inválido                  |
      | Email    | usuario@       | Email inválido                |

  Scenario: Tentar cadastrar com e‑mail já existente
    When uso o e‑mail “exemplo@parabank.com” já cadastrado
    And envio o formulário
    Then vejo a mensagem de erro “E‑mail já cadastrado”

# --------------------------------------
# Feature: Login
# --------------------------------------
Feature: Login
  Como usuário cadastrado
  Quero fazer login no ParaBank
  Para acessar minha conta

  Background:
    Dado que o usuário está na página de login

  Scenario: Login com credenciais válidas
    When insero e‑mail “usuario@parabank.com” e senha “senhaSegura”
    And clico em “Login”
    Then o sistema deve redirecionar para a página inicial da conta
    And exibir “Bem‑vindo, usuário”

  Scenario Outline: Login com credenciais inválidas
    When insero e‑mail “<email>” e senha “<senha>”
    And clico em “Login”
    Then vejo a mensagem de erro “<mensagem>”

    Examples:
      | email               | senha        | mensagem                        |
      | usuário@parabank.com | wrongpass   | Credenciais inválidas           |
      | wrong@parabank.com   | senhaSegura | Credenciais inválidas           |
      | (vazio)              | senhaSegura | Email é obrigatório             |
      | usuário@parabank.com | (vazio)     | Senha é obrigatória             |

# --------------------------------------
# Feature: Acesso à Conta – Saldo e Extrato
# --------------------------------------
Feature: Acesso à Conta – Saldo e Extrato
  Como cliente autenticado
  Quero ver saldo atualizado e extrato
  Para controlar minhas finanças

  Background:
    Dado que o usuário está autenticado
    E a página inicial da conta está visível

  Scenario: Visualizar saldo atualizado
    Then a tela deve exibir o saldo atual “R$ 10.000,00”

  Scenario: Extrato listado em ordem cronológica
    When acesso a aba “Extrato”
    Then vejo a lista de transações em ordem decrescente (mais recente primeiro)
    And cada transação exibe data, descrição, valor e saldo

# --------------------------------------
# Feature: Transferência de Fundos
# --------------------------------------
Feature: Transferência de Fundos
  Como cliente autenticado
  Quero transferir dinheiro entre contas
  Para gerenciar meu patrimônio

  Background:
    Dado que o usuário tem saldo “R$ 10.000,00” na conta “Corrente”

  Scenario: Transferência bem‑sucesso
    When seleciono origem “Corrente”
    And destino “Poupança”
    And monto “R$ 1.000,00”
    And confirmo a transferência
    Then o saldo da conta “Corrente” deve ser “R$ 9.000,00”
    And o saldo da conta “Poupança” deve ser “R$ 1.000,00”
    And a transação aparece no histórico de ambas as contas

  Scenario: Transferência com valor superior ao saldo
    When seleciono origem “Corrente”
    And destino “Poupança”
    And monto “R$ 20.000,00”
    And confirmo a transferência
    Then vejo a mensagem de erro “Saldo insuficiente”

# --------------------------------------
# Feature: Solicitação de Empréstimo
# --------------------------------------
Feature: Solicitação de Empréstimo
  Como cliente autenticado
  Quero solicitar um empréstimo
  Para financiar projetos

  Background:
    Dado que o usuário está na aba “Empréstimo”

  Scenario: Empréstimo aprovado
    When informo valor “R$ 50.000,00”
    And renda anual “R$ 120.000,00”
    And envio a solicitação
    Then o sistema retorna “Empréstimo Aprovado”

  Scenario: Empréstimo negado por renda insuficiente
    When informo valor “R$ 100.000,00”
    And renda anual “R$ 50.000,00”
    And envio a solicitação
    Then o sistema retorna “Empréstimo Negado”

# --------------------------------------
# Feature: Pagamento de Contas
# --------------------------------------
Feature: Pagamento de Contas
  Como cliente autenticado
  Quero registrar pagamentos
  Para manter contas em dia

  Background:
    Dado que o usuário está na aba “Pagamentos”

  Scenario: Pagamento de conta futuro
    When preencho beneficiário “Energia”
    And endereço “Rua X, 123”
    And cidade “São Paulo”
    And estado “SP”
    And CEP “01000-000”
    And telefone “(11) 99999-8888”
    And conta de destino “Conta Energia”
    And valor “R$ 200,00”
    And data “2025-10-15”
    And confirmo o pagamento
    Then vejo a mensagem “Pagamento agendado com sucesso”
    And o pagamento aparece no histórico com status “Agendado”

  Scenario: Pagamento imediato
    When preencho os mesmos dados do cenário anterior
    And data “2025-09-12” (data atual)
    And confirmo o pagamento
    Then o saldo da conta deve ser debitado “R$ 200,00”
    And o histórico mostra a transação com status “Pago”

  Scenario Outline: Dados obrigatórios vazios
    When deixo o campo "<campo>" em branco
    And confirmo o pagamento
    Then vejo a mensagem de erro “<mensagem>”

    Examples:
      | campo           | mensagem                        |
      | Beneficiário    | Beneficiário é obrigatório      |
      | Endereço        | Endereço é obrigatório           |
      | Cidade          | Cidade é obrigatória            |
      | Estado          | Estado é obrigatório             |
      | CEP             | CEP é obrigatório                |
      | Telefone        | Telefone é obrigatório           |
      | Conta Destino   | Conta de destino é obrigatória  |
      | Valor           | Valor é obrigatório              |
      | Data            | Data é obrigatória              |

# --------------------------------------
# Feature: Navegação e Usabilidade
# --------------------------------------
Feature: Navegação e Usabilidade
  Como usuário do ParaBank
  Quero que a navegação seja consistente e livre de erros
  Para usar o sistema sem frustrações

  Scenario: Links e menus acessíveis em todas as páginas
    When navego pela aplicação
    Then todos os menus devem estar visíveis
    And cada link deve redirecionar corretamente

  Scenario: Mensagens de erro claras
    When realizo qualquer operação inválida
    Then as mensagens exibidas são curtas, claras e informativas

  Scenario: Carregamento de páginas sem erros
    When acesso cada página do sistema
    Then a página carrega dentro de 5 segundos
    And não há mensagens de erro de navegação

```

Esses cenários cobrem os critérios de aceite descritos: cadastro, login, visualização de saldo/extrato, transferências, empréstimos, pagamentos, e requisitos gerais de navegação e usabilidade. Cada cenário está estruturado em *Given‑When‑Then*, permitindo que as equipes de teste automatizem e validem as funcionalidades de forma consistente.