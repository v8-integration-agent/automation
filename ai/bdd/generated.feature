## Gherkin – ParaBank (Português)

```gherkin
# ===========================================================
#  Feature: Cadastro de Usuário
# ===========================================================
Feature: Cadastro de Usuário

  Scenario: Cadastro com sucesso quando todos os campos obrigatórios são preenchidos corretamente
    Given o usuário acessa a página de cadastro
    When ele preenche o nome completo, data de nascimento, CPF, telefone válido, CEP válido, email válido e senha
    And ele confirma a senha
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de confirmação "Cadastro realizado com sucesso"
    And o usuário deve ser direcionado para a página de login

  Scenario Outline: Cadastro falha quando campo obrigatório está vazio
    Given o usuário acessa a página de cadastro
    When ele deixa o campo "<campo>" em branco
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de erro "<mensagem>"
    And o cadastro não é criado

    Examples:
      | campo          | mensagem                           |
      | Nome           | "Nome completo é obrigatório."     |
      | Data de Nasc.  | "Data de nascimento é obrigatória."|
      | CPF            | "CPF é obrigatório."               |
      | Telefone       | "Telefone é obrigatório."          |
      | CEP            | "CEP é obrigatório."               |
      | Email          | "Email é obrigatório."             |
      | Senha          | "Senha é obrigatória."             |

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a página de cadastro
    When ele preenche o campo "<campo>" com "<valor_invalido>"
    And preenche os demais campos corretamente
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de erro "<mensagem_erro>"
    And o cadastro não é criado

    Examples:
      | campo    | valor_invalido        | mensagem_erro                                 |
      | Telefone | "123abc"              | "Formato de telefone inválido."               |
      | CEP      | "abc123"              | "Formato de CEP inválido."                    |
      | Email    | "usuario@exemplo"     | "Formato de email inválido."                  |

# ===========================================================
#  Feature: Login
# ===========================================================
Feature: Login

  Scenario: Login bem-sucedido com credenciais válidas
    Given o usuário está na página de login
    When ele digita email "usuario@exemplo.com" e senha "SenhaSegura1!"
    And ele clica em "Entrar"
    Then o sistema redireciona o usuário para a página inicial da conta
    And a mensagem "Seja bem‑vindo, usuário!" é exibida

  Scenario: Login falha com credenciais inválidas
    Given o usuário está na página de login
    When ele digita email "usuario@exemplo.com" e senha "SenhaErrada"
    And ele clica em "Entrar"
    Then o sistema exibe a mensagem de erro "Credenciais inválidas. Tente novamente."

# ===========================================================
#  Feature: Acesso à Conta (Saldo e Extrato)
# ===========================================================
Feature: Acesso à Conta

  Scenario: Ver saldo atualizado após uma transferência
    Given o usuário está logado e na página inicial da conta
    And a conta possui saldo R$ 5.000,00
    When ele realiza uma transferência de R$ 1.000,00
    Then o saldo exibido é R$ 4.000,00

  Scenario: Extrato lista transações em ordem cronológica
    Given o usuário está na página de extrato
    When existem transações registradas em ordem crescente de data
    Then o extrato exibe as transações do mais antigo para o mais recente

# ===========================================================
#  Feature: Transferência de Fundos
# ===========================================================
Feature: Transferência de Fundos

  Scenario: Transferência bem‑sucedida entre contas
    Given o usuário seleciona a conta de origem "Conta A" com saldo R$ 2.000,00
    And escolhe a conta de destino "Conta B"
    And insere o valor R$ 500,00
    When ele confirma a transferência
    Then o saldo da Conta A é debitado para R$ 1.500,00
    And o saldo da Conta B é creditado com R$ 500,00
    And a transação aparece no histórico de ambas as contas

  Scenario: Transferência falha quando valor excede saldo disponível
    Given o usuário seleciona a conta de origem com saldo R$ 300,00
    And escolhe a conta de destino
    And insere o valor R$ 500,00
    When ele confirma a transferência
    Then o sistema exibe a mensagem de erro "Saldo insuficiente para transferência."
    And os saldos das contas permanecem inalterados

  Scenario: Transferência falha quando valor informado é negativo
    Given o usuário seleciona a conta de origem
    And escolhe a conta de destino
    And insere o valor "-100,00"
    When ele confirma a transferência
    Then o sistema exibe a mensagem de erro "O valor da transferência deve ser positivo."

# ===========================================================
#  Feature: Solicitação de Empréstimo
# ===========================================================
Feature: Solicitação de Empréstimo

  Scenario: Empréstimo aprovado quando renda anual atende critério
    Given o usuário preenche o valor do empréstimo de R$ 10.000,00
    And a renda anual informada é R$ 80.000,00
    When ele envia a solicitação
    Then o sistema exibe o status "Aprovado" em destaque
    And a mensagem "Seu empréstimo foi aprovado. Detalhes na sua conta." aparece

  Scenario: Empréstimo negado quando renda anual não atende critério
    Given o usuário preenche o valor do empréstimo de R$ 10.000,00
    And a renda anual informada é R$ 20.000,00
    When ele envia a solicitação
    Then o sistema exibe o status "Negado"
    And a mensagem "Infelizmente, seu empréstimo foi negado por não atender os requisitos de renda." aparece

  Scenario: Solicitação de empréstimo falha com dados incompletos
    Given o usuário deixa o campo "Valor" vazio
    When ele envia a solicitação
    Then o sistema exibe a mensagem de erro "Valor do empréstimo é obrigatório."

# ===========================================================
#  Feature: Pagamento de Contas
# ===========================================================
Feature: Pagamento de Contas

  Scenario: Pagamento de conta criado com sucesso
    Given o usuário acessa a tela de pagamento
    And preenche beneficiário "Conta de Luz", endereço "Rua X, 123", cidade "São Paulo", estado "SP", CEP "01001-000", telefone "(11) 98765-4321", conta de destino "Conta C", valor R$ 200,00 e data de hoje
    When ele confirma o pagamento
    Then o sistema exibe a mensagem de confirmação "Pagamento agendado com sucesso"
    And o pagamento aparece no histórico de transações

  Scenario: Pagamento de conta agendado para data futura
    Given o usuário preenche a data de pagamento como "2025-12-31"
    When ele confirma o pagamento
    Then o sistema confirma que o pagamento será processado em 31/12/2025

  Scenario: Pagamento falha quando data está no passado
    Given o usuário preenche a data de pagamento como "2020-01-01"
    When ele confirma o pagamento
    Then o sistema exibe a mensagem de erro "Data de pagamento não pode ser no passado."

# ===========================================================
#  Feature: Navegação e Usabilidade Geral
# ===========================================================
Feature: Navegação e Usabilidade

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega por todas as páginas (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
    When cada página é carregada
    Then nenhuma mensagem de erro de carregamento é exibida

  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta realizar uma ação inválida (ex.: cadastro sem email)
    When a página de cadastro é exibida
    Then as mensagens de erro são específicas e instruem sobre o que deve ser corrigido

  Scenario: Menu de navegação é consistente em todas as páginas
    Given o usuário está em qualquer página do ParaBank
    When ele visualiza o cabeçalho e o rodapé
    Then os links "Home", "Transferências", "Empréstimos", "Pagamentos", "Extrato" aparecem em todas as páginas com o mesmo estilo

  Scenario: Links funcionam corretamente
    Given o usuário clica no link "Extrato" no cabeçalho
    When o sistema redireciona
    Then a página de extrato é exibida sem erros
```

> **Notas:**
> * Os cenários acima cobrem os requisitos de aceite fornecidos, incluindo verificações positivas e negativas, validações de campos, mensagens de erro e consistência de navegação.
> * Use os placeholders (`<campo>`, `<valor_invalido>`, `<mensagem>`) em cenários *Outline* para gerar múltiplos testes de forma concisa.
> * Os textos das mensagens são exemplos e podem ser ajustados de acordo com o sistema real.