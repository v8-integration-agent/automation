## Feature: Cadastro de Usuário  
```gherkin
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar minha conta
  Para poder acessar os serviços do banco

  Scenario: Cadastro bem-sucedido com todos os campos preenchidos
    Given o usuário está na página de cadastro
    When o usuário preenche os campos obrigatórios com dados válidos
    And clica em "Criar conta"
    Then o sistema exibe a mensagem "Cadastro concluído com sucesso"
    And o usuário passa a poder fazer login

  Scenario: Tentativa de cadastro com campo obrigatório em branco
    Given o usuário está na página de cadastro
    When o usuário deixa o campo "Nome" em branco e preenche os demais campos
    And clica em "Criar conta"
    Then o sistema exibe a mensagem de erro "O campo Nome é obrigatório"

  Scenario: Cadastro com telefone inválido
    Given o usuário está na página de cadastro
    When o usuário insere "1234" no campo telefone
    And preenche os demais campos
    And clica em "Criar conta"
    Then o sistema exibe a mensagem de erro "Telefone inválido"

  Scenario: Cadastro com CEP inválido
    Given o usuário está na página de cadastro
    When o usuário insere "ABCDE" no campo CEP
    And preenche os demais campos
    And clica em "Criar conta"
    Then o sistema exibe a mensagem de erro "CEP inválido"

  Scenario: Cadastro com e‑mail inválido
    Given o usuário está na página de cadastro
    When o usuário insere "usuario@exemplo" no campo e‑mail
    And preenche os demais campos
    And clica em "Criar conta"
    Then o sistema exibe a mensagem de erro "E‑mail inválido"
```

## Feature: Login  
```gherkin
Feature: Login
  Como usuário registrado
  Quero entrar no ParaBank
  Para visualizar minha conta

  Scenario: Login com credenciais válidas
    Given o usuário está na página de login
    When o usuário insere "usuario123" no campo usuário
    And insere "senhaSegura" no campo senha
    And clica em "Entrar"
    Then o sistema redireciona para a página inicial da conta

  Scenario: Login com senha incorreta
    Given o usuário está na página de login
    When o usuário insere "usuario123" no campo usuário
    And insere "senhaErrada" no campo senha
    And clica em "Entrar"
    Then o sistema exibe a mensagem "Credenciais inválidas"

  Scenario: Login com usuário inexistente
    Given o usuário está na página de login
    When o usuário insere "naoExiste" no campo usuário
    And insere "senhaQualquer" no campo senha
    And clica em "Entrar"
    Then o sistema exibe a mensagem "Credenciais inválidas"
```

## Feature: Acesso à Conta – Saldo e Extrato  
```gherkin
Feature: Acesso à Conta – Saldo e Extrato
  Como cliente autenticado
  Quero ver meu saldo e histórico
  Para acompanhar minhas finanças

  Scenario: Saldo atualizado após transferência
    Given o usuário está na página inicial da conta
    When o usuário realiza uma transferência de R$ 200,00
    Then o saldo exibido na página inicial reflete a dedução de R$ 200,00

  Scenario: Extrato lista transações recentes em ordem cronológica
    Given o usuário está na página de extrato
    When o usuário visualiza as transações
    Then as transações são listadas do mais recente ao mais antigo
```

## Feature: Transferência de Fundos  
```gherkin
Feature: Transferência de Fundos
  Como cliente autenticado
  Quero transferir dinheiro entre minhas contas
  Para movimentar meus recursos

  Scenario: Transferência bem-sucedida entre contas
    Given o usuário está na tela de transferência
    When o usuário seleciona conta de origem "Corrente 123"
    And seleciona conta de destino "Poupança 456"
    And insere o valor R$ 150,00
    And confirma a transferência
    Then R$ 150,00 é debitado da conta de origem
    And R$ 150,00 é creditado na conta de destino
    And a transação aparece no histórico de ambas as contas

  Scenario: Transferência bloqueada por saldo insuficiente
    Given o usuário tem saldo de R$ 50,00 na conta de origem
    When o usuário tenta transferir R$ 100,00
    And confirma a transferência
    Then o sistema exibe a mensagem "Saldo insuficiente para esta transferência"

  Scenario: Transferência bloqueada por valor superior ao saldo disponível
    Given o usuário tem saldo de R$ 300,00
    When o usuário tenta transferir R$ 500,00
    And confirma a transferência
    Then o sistema exibe a mensagem "Valor excede saldo disponível"
```

## Feature: Solicitação de Empréstimo  
```gherkin
Feature: Solicitação de Empréstimo
  Como cliente autenticado
  Quero solicitar um empréstimo
  Para financiar meus projetos

  Scenario: Empréstimo aprovado
    Given o usuário tem renda anual de R$ 80.000,00
    And o valor solicitado é R$ 20.000,00
    When o usuário envia a solicitação
    Then o sistema retorna o status "Aprovado"
    And exibe a mensagem "Seu empréstimo foi aprovado"

  Scenario: Empréstimo negado por renda insuficiente
    Given o usuário tem renda anual de R$ 30.000,00
    And o valor solicitado é R$ 40.000,00
    When o usuário envia a solicitação
    Then o sistema retorna o status "Negado"
    And exibe a mensagem "Empréstimo negado – renda insuficiente"
```

## Feature: Pagamento de Contas  
```gherkin
Feature: Pagamento de Contas
  Como cliente autenticado
  Quero registrar pagamentos de contas
  Para manter meus compromissos em dia

  Scenario: Registro de pagamento imediato
    Given o usuário está na tela de pagamento de contas
    When o usuário preenche: beneficiário "Eletrônica S.A.", 
      endereço "Rua A, 100", cidade "São Paulo", estado "SP", cep "01234-567", telefone "1199999999", 
      conta de destino "Conta 789", valor R$ 150,00, data "01/12/2025"
    And confirma o pagamento
    Then a transação aparece no histórico de pagamentos
    And o saldo da conta é debitado em R$ 150,00

  Scenario: Pagamento futuro agendado
    Given o usuário está na tela de pagamento de contas
    When o usuário agenda um pagamento de R$ 200,00 para a data "15/12/2025"
    And confirma a agenda
    Then o sistema exibe a mensagem "Pagamento agendado para 15/12/2025"
    And o pagamento é incluído no histórico com status "Agendado"
```

## Feature: Navegação e Usabilidade  
```gherkin
Feature: Navegação e Usabilidade
  Como usuário do ParaBank
  Quero navegar pelo sistema sem erros
  Para ter uma experiência consistente

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega por todas as páginas do aplicativo
    Then nenhuma página apresenta erro de carregamento
    And todas as rotas são válidas

  Scenario: Mensagens de erro exibidas de forma clara
    When uma ação inválida é realizada
    Then o sistema exibe uma mensagem de erro objetiva e específica

  Scenario: Links e menus consistentes em todas as páginas
    Given o usuário está em qualquer página do site
    Then os menus principais estão presentes e apontam para as mesmas seções
```

> **Obs.:** Cada cenário pode ser dividido em *Background* para autenticação ou configuração comum, se necessário. Esses exemplos cobrem os principais pontos de aceitação descritos no documento e servem como base para a criação de testes automatizados usando BDD.