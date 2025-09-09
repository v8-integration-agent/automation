```gherkin
# Feature: ParaBank – Cadastro e Autenticação
# ------------------------------------------------

Scenario: Registro de um novo usuário com campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche todos os campos obrigatórios corretamente
  And clica em “Registrar”
  Then ele deve ver uma mensagem de confirmação “Cadastro concluído”
  And o usuário deve ser redirecionado para a tela de login

Scenario Outline: Registro de um usuário com campos inválidos
  Given o usuário acessa a página de cadastro
  When ele preenche os campos obrigatórios com os seguintes valores: <campo> = "<valor>"
  And clica em “Registrar”
  Then o sistema exibe a mensagem de erro “<mensagem>”

  Examples:
    | campo   | valor           | mensagem                                  |
    | Telefone| "12345"         | "Telefone inválido"                       |
    | CEP     | "abcde"         | "CEP inválido"                            |
    | Email   | "usuario@"      | "Email inválido"                          |

Scenario: Usuário já cadastrado tenta registrar novamente
  Given o usuário já existe no banco de dados
  When ele tenta cadastrar-se com o mesmo e‑mail
  Then o sistema exibe a mensagem “E‑mail já cadastrado”

# Feature: ParaBank – Login
# ------------------------------------------------

Scenario: Login com credenciais válidas
  Given o usuário está na tela de login
  When ele insere “usuario@exemplo.com” e “senhaCorreta”
  And clica em “Entrar”
  Then ele é redirecionado para a página inicial da conta
  And a tela exibe “Bem‑vindo, <nome do usuário>”

Scenario: Login com credenciais inválidas
  Given o usuário está na tela de login
  When ele insere “usuario@exemplo.com” e “senhaErrada”
  And clica em “Entrar”
  Then o sistema exibe a mensagem “Usuário ou senha inválidos”

# Feature: ParaBank – Consulta de Saldo e Extrato
# ------------------------------------------------

Scenario: Visualização do saldo atualizado
  Given o usuário está logado na conta
  When ele navega até a tela “Saldo”
  Then a página exibe o valor “Saldo atual: R$ <saldo>”

Scenario: Visualização do extrato em ordem cronológica
  Given o usuário tem transações recentes no extrato
  When ele navega até a tela “Extrato”
  Then o extrato lista as transações em ordem decrescente de data
  And cada linha contém “Data, Descrição, Valor, Saldo”

# Feature: ParaBank – Transferência de Fundos
# ------------------------------------------------

Scenario: Transferência de fundos bem-sucedida
  Given o usuário está logado e possui saldo de R$ 1.000,00 na conta A
  When ele seleciona conta de origem “A” e conta de destino “B”
  And insere o valor “R$ 200,00”
  And confirma a transferência
  Then R$ 200,00 é debitado da conta A
  And R$ 200,00 é creditado na conta B
  And ambas as contas registram a transação no histórico

Scenario: Transferência com valor maior que o saldo disponível
  Given o usuário está logado e possui saldo de R$ 100,00 na conta A
  When ele tenta transferir R$ 200,00
  Then o sistema exibe a mensagem “Saldo insuficiente”

# Feature: ParaBank – Solicitação de Empréstimo
# ------------------------------------------------

Scenario: Empréstimo aprovado
  Given o usuário é logado
  When ele solicita R$ 10.000,00 de empréstimo com renda anual de R$ 120.000,00
  Then o sistema retorna “Solicitação Aprovada”
  And a mensagem é exibida claramente para o usuário

Scenario: Empréstimo negado por renda insuficiente
  Given o usuário é logado
  When ele solicita R$ 50.000,00 de empréstimo com renda anual de R$ 30.000,00
  Then o sistema retorna “Solicitação Negada”
  And a mensagem indica “Renda anual insuficiente”

# Feature: ParaBank – Pagamento de Contas
# ------------------------------------------------

Scenario: Registro de pagamento futuro
  Given o usuário está logado
  When ele registra um pagamento para “Conta X” com data “2025‑10‑15”
  And clica em “Confirmar”
  Then o pagamento é incluído no histórico de transações
  And o sistema exibe “Pagamento agendado para 15 de outubro de 2025”

Scenario: Pagamento imediato respeita data de agendamento
  Given o usuário registra um pagamento com data “2025‑10‑15” e confirma
  When a data atual é 2025‑10‑16
  Then o pagamento não é executado imediatamente
  And o sistema informa “Pagamento agendado para 15 de outubro”

# Feature: ParaBank – Navegação e Usabilidade
# ------------------------------------------------

Scenario: Carregamento correto de todas as páginas
  Given o usuário navega por todas as páginas principais (Login, Cadastro, Saldo, Extrato, Transferência, Empréstimo, Pagamento)
  When ele não encontra erros de carregamento
  Then todas as páginas carregam sem mensagens de erro

Scenario: Mensagens de erro claras e objetivas
  Given o usuário tenta executar uma ação inválida em qualquer módulo
  When o sistema responde
  Then a mensagem de erro é exibida em destaque
  And descreve exatamente o problema (ex.: “O campo telefone deve conter 10 dígitos”)

Scenario: Consistência de links e menus
  Given o usuário acessa qualquer página
  When ele verifica os links de navegação e menus
  Then os mesmos itens (Login, Cadastro, Saldo, Extrato, Transferência, Empréstimo, Pagamento, Logout) aparecem em todas as páginas
  And cada link funciona corretamente
```