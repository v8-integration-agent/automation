**Feature: Cadastro de Usuário**  
```gherkin
Scenario: Usuário cadastra conta com todos os campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche todos os campos obrigatórios com dados válidos
  And clica no botão “Registrar”
  Then o sistema deve criar a conta
  And exibir a mensagem “Cadastro concluído com sucesso”
  And o usuário deve estar habilitado a fazer login

Scenario Outline: Validação de campos obrigatórios e inválidos no cadastro
  Given o usuário acessa a página de cadastro
  When ele preenche os campos obrigatórios com os seguintes dados:
    | campo  | valor |
    | <campo> | <valor> |
  And clica no botão “Registrar”
  Then o sistema deve exibir a mensagem de erro “<mensagem>”

  Examples:
    | campo     | valor      | mensagem                                     |
    | telefone  | 1234       | O telefone informado é inválido              |
    | CEP       | ABCDE      | O CEP informado é inválido                   |
    | email     | usuario@   | O e‑mail informado é inválido                |
    | nome      |            | O campo nome é obrigatório                    |
```

---

**Feature: Login**  
```gherkin
Scenario: Usuário faz login com credenciais válidas
  Given o usuário tem uma conta cadastrada
  When ele acessa a página de login
  And digita o e‑mail “usuario@exemplo.com”
  And digita a senha “SenhaSegura123”
  And clica em “Entrar”
  Then o sistema deve redirecionar para a página inicial da conta
  And exibir o nome do usuário no cabeçalho

Scenario Outline: Login falha com credenciais inválidas
  Given o usuário tem uma conta cadastrada
  When ele acessa a página de login
  And digita o e‑mail “<email>”
  And digita a senha “<senha>”
  And clica em “Entrar”
  Then o sistema deve exibir a mensagem de erro “<mensagem>”

  Examples:
    | email                | senha             | mensagem                       |
    | usuario@exemplo.com  | senhaErrada       | Credenciais inválidas          |
    | desconhecido@ex.com  | SenhaSegura123    | Credenciais inválidas          |
```

---

**Feature: Acesso à Conta – Saldo e Extrato**  
```gherkin
Scenario: O saldo exibido está atualizado após uma operação de débito
  Given o usuário está autenticado
  And possui saldo de R$ 1.000,00 na conta principal
  When ele faz um depósito de R$ 200,00
  Then o saldo exibido deve ser R$ 1.200,00

Scenario: O extrato lista transações em ordem cronológica
  Given o usuário está autenticado
  And possui as seguintes transações:
    | data       | descrição   | valor  |
    | 2024-08-01 | Saldo Inicial | 1.000,00 |
    | 2024-08-05 | Transferência | 200,00 |
  When ele acessa a página “Extrato”
  Then a lista deve exibir as transações em ordem crescente de data
  And a última transação deve ser “Transferência” de R$ 200,00
```

---

**Feature: Transferência de Fundos**  
```gherkin
Scenario: Usuário transfere fundos entre contas existentes
  Given o usuário está autenticado
  And possui saldo de R$ 1.500,00 na conta A
  And tem a conta B com saldo de R$ 300,00
  When ele seleciona a conta A como origem
  And seleciona a conta B como destino
  And digita o valor “500,00”
  And confirma a transferência
  Then o saldo da conta A deve ser R$ 1.000,00
  And o saldo da conta B deve ser R$ 800,00
  And a transação deve aparecer no histórico de ambas as contas

Scenario Outline: Transferência não permitida quando o valor excede o saldo
  Given o usuário está autenticado
  And possui saldo de R$ <saldo> na conta origem
  When ele tenta transferir R$ <valor> para outra conta
  Then o sistema deve exibir a mensagem “Saldo insuficiente para transferências”

  Examples:
    | saldo  | valor  |
    | 300,00 | 400,00 |
    | 100,00 | 101,00 |
```

---

**Feature: Solicitação de Empréstimo**  
```gherkin
Scenario: Usuário solicita empréstimo aprovado
  Given o usuário está autenticado
  And seu salário anual é R$ 80.000,00
  When ele solicita um empréstimo de R$ 10.000,00
  And confirma a solicitação
  Then o sistema deve exibir o status “Aprovado”
  And o valor deve estar disponível na conta após aprovação

Scenario: Usuário solicita empréstimo negado
  Given o usuário está autenticado
  And seu salário anual é R$ 30.000,00
  When ele solicita um empréstimo de R$ 50.000,00
  And confirma a solicitação
  Then o sistema deve exibir o status “Negado”
  And nenhuma mudança de saldo deve ocorrer
```

---

**Feature: Pagamento de Contas**  
```gherkin
Scenario: Pagamento de conta registrado com sucesso
  Given o usuário está autenticado
  When ele registra um pagamento com:
    | beneficiário | endereço         | cidade  | estado | CEP     | telefone | conta_destino | valor  | data        |
    | Energia      | Av. Paulista 100 | São Paulo | SP     | 01310-000 | 11 98765-4321 | 123456 | 50,00 | 2024-08-20 |
  And confirma o pagamento
  Then o pagamento deve aparecer no histórico de transações
  And o saldo da conta origem deve ser debitado em R$ 50,00

Scenario: Pagamento futuro deve respeitar a data de agendamento
  Given o usuário está autenticado
  When ele agenda um pagamento de R$ 100,00 para a data 2024-09-15
  And confirma a agenda
  Then o pagamento não deve aparecer no extrato até 2024‑09‑15
  And o sistema deve exibir a data prevista no histórico de pagamentos
```

---

**Feature: Navegação e Usabilidade Geral**  
```gherkin
Scenario: Todas as páginas carregam sem erros de navegação
  Given o usuário está autenticado
  When ele navega para cada página do menu principal
  Then nenhuma página deve exibir mensagens de erro ou links quebrados

Scenario: Mensagens de erro são claras e objetivas
  Given o usuário está na página de login
  When ele clica em “Entrar” sem preencher os campos
  Then o sistema deve exibir a mensagem “Todos os campos são obrigatórios”

Scenario: Consistência de links e menus em todas as páginas
  Given o usuário está autenticado
  When ele acessa qualquer página do sistema
  Then o cabeçalho deve conter os mesmos links de “Home”, “Conta”, “Transferências”, “Pagamentos”, “Empréstimos” e “Sair”
```

--- 

Esses cenários cobrem os critérios de aceitação descritos no documento, fornecendo cobertura tanto para fluxos positivos quanto para casos de erro e limites de negócio. Eles podem ser diretamente usados por ferramentas BDD como Cucumber, SpecFlow ou Behave.