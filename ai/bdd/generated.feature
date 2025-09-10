## Feature: Cadastro de Usuário

```gherkin
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar meus dados
  Para poder acessar a conta

  Scenario Outline: Cadastro com todos os campos obrigatórios preenchidos
    Dado o usuário esteja na página de cadastro
    Quando ele preencher o campo "<nome>" com "<valor_nome>"
      E preencher o campo "<sobrenome>" com "<valor_sobrenome>"
      E preencher o campo "<email>" com "<valor_email>"
      E preencher o campo "<telefone>" com "<valor_telefone>"
      E preencher o campo "<cep>" com "<valor_cep>"
      E preencher o campo "<endereco>" com "<valor_endereco>"
      E preencher o campo "<cidade>" com "<valor_cidade>"
      E selecionar "<estado>" no dropdown de estado
      E inserir a senha em "<senha>"
      E inserir a senha novamente em "<confirmar_senha>"
      E clicar no botão "Cadastrar"
    Então a mensagem de sucesso deve ser exibida
      E o usuário deve estar logado automaticamente

    Examples:
      | nome | sobrenome | valor_nome | valor_sobrenome | valor_email           | valor_telefone | valor_cep | valor_endereco | valor_cidade | estado | senha          | confirmar_senha |
      | João | Silva     | João       | Silva           | joao.silva@email.com | 5511999999999  | 01001-000 | Rua A          | São Paulo    | SP     | senhaSegura1  | senhaSegura1   |

  Scenario Outline: Cadastro com campo inválido
    Dado o usuário esteja na página de cadastro
    Quando ele preencher o campo "<campo>" com "<valor>"
      E preencher os demais campos com valores válidos
      E clicar no botão "Cadastrar"
    Então a mensagem de erro "<mensagem>" deve aparecer ao lado de "<campo>"

    Examples:
      | campo     | valor              | mensagem                          |
      | email     | usuario.com.br     | "Email inválido, por favor insira um email válido." |
      | telefone  | abcdefg            | "Telefone inválido, deve conter apenas números."   |
      | cep       | 123              | "CEP inválido, deve ter 8 dígitos no formato 00000-000." |
```

## Feature: Login

```gherkin
Feature: Login
  Como cliente já cadastrado
  Quero me autenticar no ParaBank
  Para acessar meu dashboard

  Scenario: Login bem-sucedido com credenciais válidas
    Dado o usuário esteja na página de login
    Quando ele digitar "<email>" no campo "Email"
      E digitar "<senha>" no campo "Senha"
      E clicar no botão "Entrar"
    Então o usuário deve ser redirecionado para a página inicial da conta
      E o cabeçalho deve conter "Olá, <nome>"

    Examples:
      | email                   | senha          | nome  |
      | joao.silva@email.com    | senhaSegura1   | João  |

  Scenario Outline: Login falhou com credenciais inválidas
    Dado o usuário esteja na página de login
    Quando ele digitar "<email>" no campo "Email"
      E digitar "<senha>" no campo "Senha"
      E clicar no botão "Entrar"
    Então a mensagem de erro "<mensagem>" deve aparecer

    Examples:
      | email                   | senha     | mensagem                                  |
      | joao.silva@email.com    | errada    | "Credenciais inválidas, tente novamente." |
      | invalido@email.com      | senhaSegura1 | "Usuário não encontrado."                |
```

## Feature: Acesso à Conta – Saldo e Extrato

```gherkin
Feature: Acesso à Conta – Saldo e Extrato
  Como cliente autenticado
  Quero ver meu saldo e extrato
  Para acompanhar minhas finanças

  Scenario: Visualizar saldo atualizado após operação de crédito
    Dado o usuário esteja na página inicial da conta
      E o saldo atual seja "<saldo_atual>"
    Quando o usuário receber um depósito de "<valor_deposito>"
    Então o saldo deve ser "<saldo_esperado>"
      E a transação de depósito deve aparecer no extrato

    Examples:
      | saldo_atual | valor_deposito | saldo_esperado |
      | 1.000,00     | 500,00          | 1.500,00        |

  Scenario: Extrato exibe transações em ordem cronológica
    Dado o usuário esteja na página de extrato
      E o extrato contenha as seguintes transações:
        | Data       | Descrição           | Valor   |
        | 01/05/2025 | Transferência       | -200,00 |
        | 02/05/2025 | Depósito            | +300,00 |
    Quando a página carregar
    Então as transações devem estar ordenadas do mais recente ao mais antigo
```

## Feature: Transferência de Fundos

```gherkin
Feature: Transferência de Fundos
  Como cliente autenticado
  Quero transferir valores entre minhas contas
  Para movimentar meu dinheiro

  Scenario: Transferência válida entre duas contas
    Dado o usuário esteja na página de transferência
      E a conta origem possua saldo "<saldo_orig>"
      E a conta destino exista
    Quando o usuário selecionar conta origem "<conta_origem>"
      E selecionar conta destino "<conta_destino>"
      E digitar valor "<valor>"
      E confirmar a transferência
    Then o saldo da conta origem deve ser "<saldo_final_origem>"
      E o saldo da conta destino deve ser "<saldo_final_destino>"
      E a transação deve aparecer no histórico de ambas as contas

    Examples:
      | saldo_orig | conta_origem | conta_destino | valor | saldo_final_origem | saldo_final_destino |
      | 1.000,00   | 123456-1     | 654321-9      | 200,00 | 800,00             | 200,00              |

  Scenario: Transferência falhou por saldo insuficiente
    Dado o usuário esteja na página de transferência
      E a conta origem possua saldo "<saldo_orig>"
    Quando o usuário selecionar conta origem "<conta_origem>"
      E digitar valor "<valor>"
      E confirmar a transferência
    Then a mensagem de erro "<mensagem>" deve ser exibida
      E o saldo da conta origem permanece inalterado

    Examples:
      | saldo_orig | conta_origem | valor | mensagem                          |
      | 100,00     | 123456-1     | 200,00 | "Saldo insuficiente para esta transferência." |
```

## Feature: Solicitação de Empréstimo

```gherkin
Feature: Solicitação de Empréstimo
  Como cliente autenticado
  Quero solicitar um empréstimo
  Para aumentar meu poder de compra

  Scenario Outline: Solicitação de empréstimo com aprovação ou negação
    Dado o usuário esteja na página de solicitação de empréstimo
    Quando ele informar valor "<valor_emprestimo>" e renda anual "<renda_anual>"
      E submeter a solicitação
    Então o sistema deve retornar status "<status>"
      E o usuário deve ver a mensagem "<mensagem>"

    Examples:
      | valor_emprestimo | renda_anual | status | mensagem                        |
      | 5.000,00         | 80.000,00   | Aprovado | "Seu empréstimo foi aprovado!"  |
      | 20.000,00        | 30.000,00   | Negado   | "Desculpe, não podemos aprovar seu empréstimo." |
```

## Feature: Pagamento de Contas

```gherkin
Feature: Pagamento de Contas
  Como cliente autenticado
  Quero registrar e agendar pagamentos de contas
  Para manter minhas contas em dia

  Scenario: Pagamento futuro agendado
    Dado o usuário esteja na página de pagamento de contas
    Quando ele preencher:
      | Campo          | Valor                    |
      | Beneficiário   | Conta de Energia        |
      | Endereço       | Rua X, 100              |
      | Cidade         | São Paulo               |
      | Estado         | SP                       |
      | CEP            | 01001-000                |
      | Telefone       | 5511999999999            |
      | Conta destino  | 123456-1                 |
      | Valor          | 150,00                   |
      | Data           | 15/06/2025 (futuro)      |
      Then o pagamento deve ser incluído no histórico de transações
        E a data de pagamento futura deve ser respeitada

  Scenario: Pagamento com data retroativa
    Dado o usuário esteja na página de pagamento de contas
    Quando ele definir a data de pagamento como "01/01/2025" (passado)
      E submeter o pagamento
    Then a mensagem de erro "Data de pagamento não pode ser passada." deve aparecer
```

## Feature: Requisitos Gerais de Navegação e Usabilidade

```gherkin
Feature: Navegação e Usabilidade
  Como cliente
  Quero que todas as páginas sejam navegáveis sem erros
  Para ter uma experiência de uso agradável

  Scenario: Carregamento correto de todas as páginas principais
    Dado o usuário esteja autenticado
    Quando ele acessar cada uma das páginas: Dashboard, Saldo, Extrato, Transferência, Empréstimo, Pagamento
    Então cada página deve carregar sem erros e exibir os componentes corretos

  Scenario: Consistência de menus e links
    Dado o usuário esteja em qualquer página
    Quando ele clicar no link "Contas" no menu
    Then ele deve ser redirecionado para a página de contas
      E o mesmo link deve funcionar em todas as outras páginas

  Scenario: Mensagens de erro claras e objetivas
    Dado o usuário esteja na página de login
    Quando ele tentar login com senha vazia
    Then a mensagem "Senha é obrigatória." deve ser exibida de forma destacada
```

Esses cenários cobrem todos os requisitos de aceite descritos no documento, incluindo fluxos positivos, negativos e de erro, além das validações de usabilidade e navegação.