## Feature: Cadastro de Usuário
```gherkin
@cadastro
Scenario: Usuário cadastra-se com sucesso
  Given que eu estou na tela de cadastro
  When preencho todos os campos obrigatórios com dados válidos
  And clico em "Cadastrar"
  Then devo ver uma mensagem de confirmação "Cadastro concluído com sucesso"
  And devo conseguir fazer login com as credenciais recém‑criadas

@cadastro
Scenario Outline: Usuário tenta se cadastrar com campo obrigatório em branco
  Given que eu estou na tela de cadastro
  When deixo o campo "<campo>" em branco
  And preencho os demais campos com dados válidos
  And clico em "Cadastrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo           | mensagem                                 |
    | Nome            | "O nome é obrigatório"                   |
    | Email           | "O email é obrigatório"                  |
    | Senha           | "A senha é obrigatória"                  |
    | Confirmação Senha | "A confirmação de senha é obrigatória" |

@cadastro
Scenario Outline: Usuário tenta se cadastrar com dados inválidos
  Given que eu estou na tela de cadastro
  When preencho o campo "<campo>" com "<valor>"
  And preencho os demais campos com dados válidos
  And clico em "Cadastrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo    | valor           | mensagem                                |
    | Email    | "usuario.com"   | "Formato de email inválido"             |
    | Telefone | "123"           | "Formato de telefone inválido"          |
    | CEP      | "abcde"         | "Formato de CEP inválido"               |
```

---

## Feature: Login
```gherkin
@login
Scenario: Usuário faz login com credenciais válidas
  Given que eu tenho uma conta válida
  When eu entro na tela de login
  And preencho o campo "Email" com "usuario@exemplo.com"
  And preencho o campo "Senha" com "SenhaSegura123"
  And clico em "Entrar"
  Then devo ser redirecionado para a página inicial da conta
  And devo ver o saldo atualizado

@login
Scenario Outline: Usuário tenta fazer login com credenciais inválidas
  Given que eu tenho uma conta válida
  When eu entro na tela de login
  And preencho o campo "Email" com "<email>"
  And preencho o campo "Senha" com "<senha>"
  And clico em "Entrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | email                | senha          | mensagem                              |
    | "invalido@exemplo.com" | "senhaErrada" | "Credenciais inválidas. Tente novamente." |
    | ""                    | "SenhaSegura123" | "O email é obrigatório."              |
    | "usuario@exemplo.com" | ""              | "A senha é obrigatória."              |
```

---

## Feature: Acesso à Conta – Saldo e Extrato
```gherkin
@saldo
Scenario: Exibição do saldo após operação financeira
  Given que o usuário está autenticado
  And possui saldo inicial de R$ 1.000,00
  When realizo uma transferência de R$ 200,00
  Then o saldo exibido deve ser R$ 800,00

@extrato
Scenario: O extrato lista transações recentes em ordem cronológica
  Given que o usuário está autenticado
  And já realizou as seguintes transações:
    | Data        | Descrição          | Valor  |
    | 01/10/2023 | Depósito           | +R$500 |
    | 02/10/2023 | Transferência      | -R$200 |
  When acesso a página de extrato
  Then devo ver a lista de transações ordenada por data mais recente para mais antiga
```

---

## Feature: Transferência de Fundos
```gherkin
@transferencia
Scenario: Usuário transfere fundos entre contas
  Given que o usuário possui a conta origem com saldo R$ 1.000,00
  And possui a conta destino
  When seleciono a conta origem
  And seleciono a conta destino
  And informo o valor de R$ 300,00
  And confirmo a transferência
  Then o saldo da conta origem deve ser R$ 700,00
  And o saldo da conta destino deve ser R$ 300,00
  And a transação deve aparecer no histórico de ambas as contas

@transferencia
Scenario: Usuário não pode transferir valor superior ao saldo disponível
  Given que o usuário possui a conta origem com saldo R$ 100,00
  When tento transferir R$ 200,00
  Then devo ver a mensagem de erro "Transferência não pode exceder o saldo disponível"

@transferencia
Scenario Outline: Usuário tenta transferir com dados incompletos
  Given que o usuário possui conta origem com saldo R$ 500,00
  When informo o valor "<valor>" e deixo "<campo>" vazio
  And confirmo a transferência
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo          | valor  | mensagem                                |
    | Conta Destino  | 100    | "A conta de destino é obrigatória"     |
    | Valor          | ""     | "O valor da transferência é obrigatório"|
```

---

## Feature: Solicitação de Empréstimo
```gherkin
@emprestimo
Scenario: Usuário solicita empréstimo e recebe aprovação
  Given que o usuário possui renda anual de R$ 80.000,00
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo R$ 20.000,00
  And confirmo a solicitação
  Then o sistema deve retornar o status "Aprovado"
  And devo ver a mensagem "Empréstimo aprovado em até 3 dias úteis"

@emprestimo
Scenario: Usuário solicita empréstimo e é negado
  Given que o usuário possui renda anual de R$ 30.000,00
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo R$ 20.000,00
  And confirmo a solicitação
  Then o sistema deve retornar o status "Negado"
  And devo ver a mensagem "Empréstimo negado por insuficiência de renda"

@emprestimo
Scenario Outline: Usuário fornece dados inválidos na solicitação de empréstimo
  Given que o usuário tem renda anual de "<renda>"
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo "<valor>"
  And confirmo a solicitação
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | renda    | valor | mensagem                                   |
    | 80.000   | "-500"| "O valor do empréstimo deve ser positivo" |
    | 80.000   | "0"   | "O valor do empréstimo deve ser maior que zero" |
```

---

## Feature: Pagamento de Contas
```gherkin
@pagamento
Scenario: Usuário registra pagamento de conta
  Given que o usuário está autenticado
  When acesso a página de pagamento de contas
  And preencho:
    | Beneficiário | Endereço | Cidade | Estado | CEP   | Telefone     | Conta | Valor | Data   |
    | "Eletricidade" | "Av. X" | "SP"   | "SP"   | "12345-678" | "(11) 98765-4321" | "123456" | 200 | 15/11/2023 |
  And confirmo o pagamento
  Then devo ver a mensagem "Pagamento confirmado"
  And o pagamento deve aparecer no histórico de transações na data correta

@pagamento
Scenario: Pagamento futuro respeita data de agendamento
  Given que o usuário está autenticado
  When registro pagamento agendado para 01/12/2023
  And confirmo
  Then a data de vencimento exibida deve ser 01/12/2023
  And o pagamento só deve aparecer no extrato após 01/12/2023

@pagamento
Scenario Outline: Usuário tenta registrar pagamento com campo inválido
  Given que o usuário está autenticado
  When preencho o campo "<campo>" com "<valor>"
  And confirmo o pagamento
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo        | valor          | mensagem                                |
    | CEP          | "abcde"        | "Formato de CEP inválido"               |
    | Telefone     | "123"          | "Formato de telefone inválido"          |
    | Valor        | "-100"         | "Valor do pagamento deve ser positivo" |
```

---

## Feature: Requisitos Gerais de Navegação e Usabilidade
```gherkin
@navegacao
Scenario: Todas as páginas carregam sem erros de navegação
  Given que estou autenticado
  When navego entre todas as páginas do aplicativo
  Then cada página deve carregar com sucesso e sem mensagens de erro

@mensagens
Scenario: Mensagens de erro são claras e objetivas
  Given que eu realizo uma ação inválida
  When a aplicação exibe um erro
  Then a mensagem deve conter a razão do erro e instruções de correção

@menus
Scenario: Links e menus são consistentes em todas as páginas
  Given que estou em qualquer página do aplicativo
  When verifico os itens de navegação no cabeçalho
  Then eles devem ser os mesmos que na página inicial
```

---

> **Observação**: Cada cenário pode ser ampliado com `Scenario Outline` e `Examples` para cobrir variáveis de entrada. Os cenários acima cobrem os requisitos de aceitação descritos no documento, garantindo que o ParaBank ofereça funcionalidades completas, robustas e de fácil uso.