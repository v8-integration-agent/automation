```gherkin
# Feature: Cadastro de Usuário
# O cadastro deve validar campos obrigatórios e formatos específicos.

Scenario: Cadastro bem‑sucedido
  Given o usuário está na página de cadastro
  When preenche os campos obrigatórios com dados válidos
  And confirma o cadastro
  Then exibe a mensagem de confirmação “Cadastro concluído com sucesso”
  And habilita o acesso ao login

Scenario: Tentativa de cadastro com campo obrigatório em branco
  Given o usuário está na página de cadastro
  When deixa o campo “Nome” em branco
  And preenche os demais campos obrigatórios
  And confirma o cadastro
  Then exibe a mensagem de erro “Nome é obrigatório”

Scenario: Cadastro com telefone inválido
  Given o usuário está na página de cadastro
  When preenche “Telefone” com “12345”
  And preenche os demais campos obrigatórios
  And confirma o cadastro
  Then exibe a mensagem de erro “Telefone inválido”

Scenario: Cadastro com CEP inválido
  Given o usuário está na página de cadastro
  When preenche “CEP” com “ABCDE”
  And preenche os demais campos obrigatórios
  And confirma o cadastro
  Then exibe a mensagem de erro “CEP inválido”

Scenario: Cadastro com e‑mail inválido
  Given o usuário está na página de cadastro
  When preenche “E‑mail” com “usuario@@example.com”
  And preenche os demais campos obrigatórios
  And confirma o cadastro
  Then exibe a mensagem de erro “Endereço de e‑mail inválido”

# Feature: Login
# O sistema deve autenticar credenciais válidas e rejeitar inválidas.

Scenario: Login bem‑sucedido
  Given o usuário tem credenciais válidas
  When abre a página de login
  And insere “usuario@exemplo.com” no campo de e‑mail
  And insere “SenhaSegura123” no campo de senha
  And clica em “Entrar”
  Then redireciona para a página inicial da conta
  And exibe o nome do usuário no cabeçalho

Scenario: Login com credenciais inválidas
  Given o usuário tem credenciais inválidas
  When abre a página de login
  And insere “usuario@exemplo.com” no campo de e‑mail
  And insere “SenhaIncorreta” no campo de senha
  And clica em “Entrar”
  Then exibe a mensagem de erro “Credenciais inválidas”

# Feature: Acesso à conta (Saldo e Extrato)
# O saldo deve ser atualizado e o extrato em ordem cronológica.

Scenario: Exibição de saldo atualizado após depósito
  Given o usuário tem saldo de R$ 1.000,00
  And realizou um depósito de R$ 500,00
  When acessa a página da conta
  Then o saldo exibido é “R$ 1.500,00”

Scenario: Listagem de extrato em ordem cronológica
  Given o usuário tem as seguintes transações:
    | Data       | Tipo      | Valor |
    | 2024‑01‑01 | Depósito  | 200   |
    | 2024‑01‑10 | Saque     | 50    |
    | 2024‑01‑15 | Transferência | 100 |
  When acessa a página de extrato
  Then o extrato lista as transações em ordem crescente de data

# Feature: Transferência de Fundos
# O sistema deve validar saldo e registrar transação.

Scenario: Transferência bem‑sucedida
  Given o usuário possui R$ 1.000,00 na conta origem
  When seleciona a conta origem “Conta A”
  And seleciona a conta destino “Conta B”
  And insere o valor “200,00”
  And confirma a transferência
  Then debita R$ 200,00 da Conta A
  And credita R$ 200,00 na Conta B
  And registra a transação no extrato de ambas as contas

Scenario: Transferência com valor superior ao saldo
  Given o usuário possui R$ 100,00 na conta origem
  When tenta transferir “200,00”
  Then exibe a mensagem de erro “Saldo insuficiente”

Scenario: Transferência sem informar valor
  Given o usuário possui saldo suficiente
  When seleciona contas de origem e destino
  And deixa o campo “Valor” em branco
  And tenta confirmar a transferência
  Then exibe a mensagem de erro “O campo Valor é obrigatório”

# Feature: Solicitação de Empréstimo
# O sistema retorna status aprovado ou negado baseado na renda.

Scenario: Empréstimo aprovado
  Given o usuário possui renda anual de R$ 80.000,00
  When solicita empréstimo de R$ 10.000,00
  And confirma a solicitação
  Then exibe a mensagem “Empréstimo aprovado”
  And registra a solicitação no histórico

Scenario: Empréstimo negado por renda insuficiente
  Given o usuário possui renda anual de R$ 20.000,00
  When solicita empréstimo de R$ 10.000,00
  And confirma a solicitação
  Then exibe a mensagem “Empréstimo negado”

# Feature: Pagamento de Contas
# O pagamento deve ser registrado e respeitar data de agendamento.

Scenario: Pagamento imediato bem‑sucedido
  Given o usuário possui saldo de R$ 1.000,00
  When registra pagamento com:
    | Beneficiário | Endereço | Cidade | Estado | CEP | Telefone | Conta | Valor | Data   |
    | João Silva   | Rua X    | SP     | SP     | 12345-678 | (11) 91234‑5678 | Conta C | 300 | 2024‑02‑01 |
  And confirma o pagamento
  Then débita R$ 300,00 da conta
  And registra a transação no extrato

Scenario: Pagamento agendado para data futura
  Given o usuário possui saldo suficiente
  When registra pagamento com data “2024‑12‑25”
  And confirma o pagamento
  Then exibe a mensagem “Pagamento agendado para 2024‑12‑25”
  And não debita o saldo imediatamente
  And registra a transação no histórico de pagamentos agendados

Scenario: Pagamento com telefone inválido
  Given o usuário possui saldo suficiente
  When registra pagamento com telefone “123”
  And confirma o pagamento
  Then exibe a mensagem de erro “Telefone inválido”

# Feature: Requisitos Gerais de Navegação e Usabilidade
# As páginas devem carregar corretamente e os menus devem ser consistentes.

Scenario: Todas as páginas carregam sem erros de navegação
  Given o usuário está autenticado
  When navega por todas as páginas disponíveis (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
  Then nenhuma página apresenta erro de carregamento

Scenario: Mensagens de erro claras e objetivas
  Given o usuário tenta uma operação inválida (ex.: transferência sem valor)
  When confirma a operação
  Then a mensagem exibida contém apenas informação necessária para correção

Scenario: Menus e links consistentes em todas as páginas
  Given o usuário navega entre as páginas
  When inspeciona os menus de navegação
  Then todos os links aparecem em todas as páginas
  And a estrutura de navegação permanece a mesma
```