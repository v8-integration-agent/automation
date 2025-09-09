**Feature: Cadastro de Usuário**

```gherkin
Scenario: Cadastro bem‑sucesso com todos os campos obrigatórios preenchidos
  Given o usuário está na página de cadastro
  When ele preenche os campos: nome, CPF, telefone, CEP, email, senha e confirma a senha
  And clica em “Registrar”
  Then o sistema deve exibir a mensagem “Cadastro efetuado com sucesso”
  And o usuário deve ser redirecionado à página de login

Scenario: Tentativa de cadastro com campo telefone inválido
  Given o usuário está na página de cadastro
  When ele preenche todos os campos, mas insere um telefone com caracteres inválidos
  And clica em “Registrar”
  Then o sistema deve exibir “Telefone inválido – use o formato (xx) xxxx‑xxxx”

Scenario: Tentativa de cadastro com e‑mail duplicado
  Given um usuário já cadastrado com e‑mail “exemplo@teste.com”
  And o usuário está na página de cadastro
  When ele preenche todos os campos, usando o mesmo e‑mail
  And clica em “Registrar”
  Then o sistema deve exibir “E‑mail já cadastrado. Por favor, use outro endereço”

Scenario: Campos obrigatórios em branco
  Given o usuário está na página de cadastro
  When ele clica em “Registrar” sem preencher nenhum campo
  Then o sistema deve exibir “Todos os campos são obrigatórios”
```

---

**Feature: Login**

```gherkin
Scenario: Login bem‑sucesso com credenciais válidas
  Given o usuário já está cadastrado
  And está na página de login
  When ele digita seu e‑mail e senha corretos
  And clica em “Entrar”
  Then o sistema deve redirecionar para a página inicial da conta

Scenario: Login com senha incorreta
  Given o usuário já está cadastrado
  And está na página de login
  When ele digita seu e‑mail e uma senha inválida
  And clica em “Entrar”
  Then o sistema deve exibir “Credenciais inválidas. Tente novamente”

Scenario: Login com e‑mail não cadastrado
  Given o usuário não está cadastrado
  And está na página de login
  When ele digita um e‑mail desconhecido e uma senha válida
  And clica em “Entrar”
  Then o sistema deve exibir “Credenciais inválidas. Tente novamente”
```

---

**Feature: Visualização de Saldo e Extrato**

```gherkin
Scenario: Exibição do saldo atualizado após depósito
  Given o usuário está logado
  And sua conta tem saldo de R$ 1.000,00
  When ele realiza um depósito de R$ 200,00
  Then o saldo exibido na página inicial deve ser R$ 1.200,00

Scenario: Listagem do extrato em ordem cronológica
  Given o usuário tem três transações recentes
    | Data       | Descrição | Valor  |
    | 2025-08-01 | Depósito  | +1000 |
    | 2025-08-03 | Transferência | -200 |
    | 2025-08-05 | Pagamento  | -50  |
  When o usuário acessa a aba “Extrato”
  Then as transações devem aparecer listadas do mais recente ao mais antigo
```

---

**Feature: Transferência de Fundos**

```gherkin
Scenario: Transferência bem‑sucesso entre duas contas
  Given o usuário está logado na conta A com saldo R$ 500,00
  And a conta B está cadastrada
  When ele seleciona conta A como origem, conta B como destino e digita R$ 150,00
  And confirma a transferência
  Then conta A deve ter saldo R$ 350,00
  And conta B deve ter saldo R$ 150,00
  And ambas as contas devem registrar a transação no histórico

Scenario: Tentativa de transferência excedendo saldo disponível
  Given o usuário tem saldo R$ 100,00
  When ele tenta transferir R$ 200,00
  Then o sistema deve exibir “Transferência não permitida – saldo insuficiente”

Scenario: Transferência para conta inexistente
  Given o usuário tenta transferir para a conta “123456789”
  When ele confirma a operação
  Then o sistema deve exibir “Conta destino não encontrada”
```

---

**Feature: Solicitação de Empréstimo**

```gherkin
Scenario: Empréstimo aprovado
  Given o usuário tem renda anual de R$ 100.000,00
  And solicita um empréstimo de R$ 10.000,00
  When a solicitação é processada
  Then o sistema deve exibir “Empréstimo aprovado”

Scenario: Empréstimo negado por renda insuficiente
  Given o usuário tem renda anual de R$ 20.000,00
  And solicita um empréstimo de R$ 25.000,00
  When a solicitação é processada
  Then o sistema deve exibir “Empréstimo negado – renda insuficiente”

Scenario: Validação de campo “valor do empréstimo” vazio
  Given o usuário está na tela de solicitação de empréstimo
  When ele deixa o campo “valor” em branco e clica em “Enviar”
  Then o sistema deve exibir “O valor do empréstimo é obrigatório”
```

---

**Feature: Pagamento de Contas**

```gherkin
Scenario: Pagamento de conta futuro
  Given o usuário selecionou um pagamento para o dia 15/09/2025
  And informou beneficiário, endereço, cidade, estado, CEP, telefone, conta destino, valor e data
  When ele confirma o pagamento
  Then o pagamento deve aparecer no histórico de transações com status “Agendado”
  And não deve ser debitado imediatamente

Scenario: Pagamento de conta com data no passado
  Given o usuário tenta agendar um pagamento para 01/01/2023
  When ele confirma a operação
  Then o sistema deve exibir “A data deve ser futura”

Scenario: Pagamento sem informar telefone
  Given o usuário deixa o campo telefone em branco
  When ele confirma o pagamento
  Then o sistema deve exibir “Telefone do beneficiário é obrigatório”
```

---

**Feature: Navegação e Usabilidade**

```gherkin
Scenario: Todas as páginas carregam sem erros
  Given o usuário navega por todas as páginas do sistema (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
  Then nenhuma página deve apresentar erro de carregamento (404, 500 ou erro de script)

Scenario: Consistência de menus e links
  Given o usuário acessa qualquer página
  When ele verifica os menus de navegação
  Then todos os menus e links devem ser os mesmos em todas as páginas

Scenario: Mensagens de erro claras
  Given o usuário faz um cadastro com e‑mail inválido
  When ele tenta salvar
  Then a mensagem de erro exibida deve indicar exatamente o problema (“Formato de e‑mail inválido”) e sugerir correção
```

---