## Gherkin – ParaBank Acceptance Scenarios  
*(All scenarios are written in Portuguese, using the standard Gherkin syntax.)*

```gherkin
Feature: Cadastro de Usuário
  Como um novo usuário
  Eu quero registrar-me no ParaBank
  Para que eu possa acessar as funcionalidades bancárias

  Scenario: Cadastro bem-sucedido
    Given o usuário preenche todos os campos obrigatórios com valores válidos
    When o usuário envia o formulário de cadastro
    Then a página exibe a mensagem "Cadastro concluído com sucesso"
    And o usuário pode fazer login com as credenciais recém‑criada

  Scenario Outline: Cadastro com campo obrigatório vazio
    Given o usuário preenche todos os campos obrigatórios, exceto o "<campo>"
    When o usuário envia o formulário de cadastro
    Then a página exibe a mensagem de erro "O campo '<campo>' é obrigatório"
    Examples:
      | campo       |
      | Nome        |
      | Email       |
      | Telefone    |
      | CEP         |
      | Senha       |
      | Confirmação |

  Scenario Outline: Cadastro com dados inválidos
    Given o usuário preenche o campo "<campo>" com "<valor_invalido>"
    When o usuário envia o formulário de cadastro
    Then a página exibe a mensagem de erro "<mensagem>"
    Examples:
      | campo   | valor_invalido          | mensagem                                     |
      | Email   | usuario@          | "Formato de e‑mail inválido"                 |
      | Telefone| 123ABC            | "Telefone deve conter apenas números"        |
      | CEP     | 12.345-678        | "CEP inválido. Use apenas dígitos"           |

---

Feature: Login
  Como um usuário cadastrado
  Eu quero entrar no sistema
  Para que eu possa acessar minha conta

  Scenario: Login com credenciais válidas
    Given o usuário está na página de login
    When o usuário insere um e‑mail e senha válidos
    And clica no botão "Entrar"
    Then o sistema redireciona para a página inicial da conta
    And exibe a mensagem "Bem‑vindo, <Nome>"

  Scenario Outline: Login com credenciais inválidas
    Given o usuário está na página de login
    When o usuário insere "<campo>" "<valor>"
    And clica no botão "Entrar"
    Then o sistema exibe a mensagem "<mensagem>"
    Examples:
      | campo   | valor              | mensagem                                |
      | e‑mail  | usuario@exemplo.com| "Credenciais inválidas"                 |
      | senha   | senhaErrada        | "Credenciais inválidas"                 |
      | ambos   | errado@example.com| "Credenciais inválidas"                 |

---

Feature: Acesso à Conta – Saldo e Extrato
  Como usuário autenticado
  Eu quero ver saldo e extrato
  Para ter controle das minhas finanças

  Scenario: Exibição de saldo atualizado após operação
    Given o usuário possui saldo inicial de R$ 1.000,00
    And realizou um depósito de R$ 500,00
    When o usuário acessa a página de saldo
    Then o saldo exibido é R$ 1.500,00

  Scenario: Listagem de transações recentes no extrato
    Given o usuário realizou três transações nas últimas 24h
    When o usuário abre o extrato
    Then as transações aparecem em ordem cronológica, da mais recente à mais antiga

---

Feature: Transferência de Fundos
  Como usuário autenticado
  Eu quero transferir dinheiro para outra conta
  Para pagar ou dividir despesas

  Scenario: Transferência bem‑sucedida
    Given o usuário tem saldo de R$ 2.000,00 na conta A
    And selecionou a conta B como destino
    When o usuário envia R$ 300,00 para a conta B
    Then a conta A é debitada em R$ 300,00
    And a conta B é creditada em R$ 300,00
    And ambas as contas registram a transação no histórico

  Scenario Outline: Transferência com valor superior ao saldo
    Given o usuário tem saldo de R$ <saldo> na conta A
    And selecionou a conta B como destino
    When o usuário tenta enviar R$ <valor> para a conta B
    Then o sistema exibe a mensagem "Saldo insuficiente"
    Examples:
      | saldo | valor |
      | 500   | 600   |
      | 100   | 150   |

  Scenario: Transferência para conta inexistente
    Given o usuário selecionou a conta "999999" como destino
    When o usuário tenta enviar R$ 200,00 para a conta
    Then o sistema exibe a mensagem "Conta de destino não encontrada"

---

Feature: Solicitação de Empréstimo
  Como usuário autenticado
  Eu quero solicitar um empréstimo
  Para financiar meus projetos

  Scenario: Empréstimo aprovado
    Given o usuário informa valor R$ 20.000,00 e renda anual R$ 120.000,00
    When o usuário envia a solicitação
    Then o sistema exibe a mensagem "Empréstimo aprovado"

  Scenario: Empréstimo negado por renda insuficiente
    Given o usuário informa valor R$ 20.000,00 e renda anual R$ 30.000,00
    When o usuário envia a solicitação
    Then o sistema exibe a mensagem "Empréstimo negado – renda insuficiente"

---

Feature: Pagamento de Contas
  Como usuário autenticado
  Eu quero pagar contas recorrentes ou pontuais
  Para manter meus débitos em dia

  Scenario: Pagamento pontual imediato
    Given o usuário preenche beneficiário "João Silva"
    And endereço "Rua Exemplo, 123"
    And cidade "São Paulo"
    And estado "SP"
    And CEP "01001-000"
    And telefone "11987654321"
    And conta de destino "123456"
    And valor R$ 150,00
    And data de pagamento "Hoje"
    When o usuário confirma o pagamento
    Then o sistema registra a transação no histórico
    And exibe a mensagem "Pagamento efetuado com sucesso"

  Scenario: Pagamento agendado para data futura
    Given o usuário define data de pagamento "2025‑12‑01"
    When o usuário confirma o pagamento
    Then o sistema exibe a mensagem "Pagamento agendado para 01/12/2025"
    And a transação aparece no histórico com status "Agendado"

---

Feature: Navegação e Usabilidade
  Como usuário
  Eu quero navegar pelo sistema sem erros
  Para ter uma experiência consistente

  Scenario: Carregamento sem erros de navegação
    Given o usuário navega por todas as páginas do aplicativo
    Then todas as páginas carregam sem mensagens de erro

  Scenario: Consistência de links e menus
    Given o usuário acessa qualquer página
    When ele verifica o cabeçalho
    Then todos os menus e links estão presentes e funcionam
    And o link "Minha Conta" leva ao painel correto

  Scenario: Exibição clara de mensagens de erro
    Given o usuário tenta executar uma operação inválida
    When a operação falha
    Then o sistema exibe uma mensagem de erro concisa e informativa
```

> **Dicas de implementação**  
> - Use **Scenario Outline** para testar múltiplas combinações de dados inválidos.  
> - Garanta que a mensagem de erro exibida no sistema corresponda exatamente ao texto esperado nos testes.  
> - Para os testes de transferência, crie contas de teste com saldos conhecidos para garantir previsibilidade.  
> - No cenário de pagamento, utilize datas dinâmicas (hoje, futuro) para validar a lógica de agendamento.  

Esses cenários cobrem todos os requisitos de aceitação listados no documento e servem como base sólida para testes automatizados BDD.