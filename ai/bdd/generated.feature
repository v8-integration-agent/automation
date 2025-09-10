**ParaBank – Cenários BDD em Gherkin (português)**  

```gherkin
# tags: @Cadastro @Login @Transferência @Empréstimo @Pagamento @Navegação
Feature: Cadastro de Usuário
  Para garantir que novos usuários possam criar uma conta de forma segura e completa

  @Cadastro
  Scenario Outline: Cadastro com todos os campos obrigatórios preenchidos
    Given O usuário acessa a página de cadastro
    When Ele preenche os campos obrigatórios com valores válidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"
    Then O sistema deve exibir a mensagem de confirmação "Cadastro realizado com sucesso"
    And O usuário deve ser redirecionado para a tela de login

    Examples:
      | Nome          | Email                 | Telefone    | CEP       |
      | João da Silva | joao.silva@email.com  | (11) 98765-4321 | 01010-010 |
      | Maria Pereira| maria.pereira@email.com | (21) 99876-5432 | 20020-020 |

  @Cadastro
  Scenario Outline: Cadastro com campos inválidos
    Given O usuário acessa a página de cadastro
    When Ele preenche os campos obrigatórios com valores inválidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"
    Then O sistema deve exibir a mensagem de erro "Email inválido"
    And O sistema deve exibir a mensagem de erro "Telefone inválido"
    And O sistema deve exibir a mensagem de erro "CEP inválido"

    Examples:
      | Nome          | Email            | Telefone      | CEP         |
      | João          | joao.com         | 1234          | abcde       |
      | Maria         | maria@          | (xx) xxxx-xxxx | 0000000     |

  @Login
  Scenario: Login com credenciais válidas
    Given O usuário possui conta cadastrada com e‑mail "usuario@email.com" e senha "Senha123"
    When O usuário digita o e‑mail e a senha na tela de login e clica em "Entrar"
    Then O sistema deve redirecionar o usuário para a página inicial da conta
    And O saldo exibido deve ser igual ao saldo inicial da conta

  @Login
  Scenario Outline: Login com credenciais inválidas
    Given O usuário possui conta cadastrada com e‑mail "usuario@email.com" e senha "Senha123"
    When O usuário digita o e‑mail "<Email>" e a senha "<Senha>" na tela de login e clica em "Entrar"
    Then O sistema deve exibir a mensagem de erro "Credenciais inválidas"

    Examples:
      | Email                    | Senha      |
      | usuario@email.com        | senhaErrada|
      | usuarioErrado@email.com  | Senha123   |

Feature: Acesso à Conta – Saldo e Extrato
  Para que o usuário possa visualizar saldo e transações recentes

  @Extrato
  Scenario: Visualização do saldo atualizado
    Given O usuário está logado e sua conta possui saldo inicial de R$ 1.000,00
    When O usuário navega até a página de “Minha Conta”
    Then O saldo exibido deve ser R$ 1.000,00

  @Extrato
  Scenario: Lista de transações no extrato em ordem cronológica
    Given O usuário está logado e possui as seguintes transações:
      | Data        | Descrição           | Valor  |
      | 01/09/2024  | Depósito            | +R$200 |
      | 02/09/2024  | Transferência       | -R$50  |
    When O usuário navega até a página de “Extrato”
    Then O extrato deve listar:
      | 02/09/2024 | Transferência | -R$50 |
      | 01/09/2024 | Depósito      | +R$200 |
    And As transações devem estar em ordem decrescente de data

Feature: Transferência de Fundos
  Para que o usuário possa transferir dinheiro entre suas contas

  @Transferência
  Scenario: Transferência válida entre contas
    Given O usuário possui saldo R$ 500,00 na conta A
    And O usuário possui conta B com saldo R$ 300,00
    When O usuário faz a transferência de R$ 150,00 da conta A para a conta B
    Then O saldo da conta A deve ser R$ 350,00
    And O saldo da conta B deve ser R$ 450,00
    And O histórico da conta A deve conter a transação "Transferência para B" de -R$150,00
    And O histórico da conta B deve conter a transação "Transferência recebida de A" de +R$150,00

  @Transferência
  Scenario Outline: Transferência inválida por saldo insuficiente
    Given O usuário possui saldo R$ 100,00 na conta de origem
    When O usuário tenta transferir R$ <Valor> da conta de origem para a conta de destino
    Then O sistema deve exibir a mensagem de erro "Saldo insuficiente"
    And Nenhuma alteração deve ocorrer no saldo das contas

    Examples:
      | Valor |
      | 150   |
      | 200   |

Feature: Solicitação de Empréstimo
  Para que o usuário possa solicitar um crédito e receber um status

  @Empréstimo
  Scenario Outline: Solicitação de empréstimo com aprovação
    Given O usuário possui renda anual de R$ <Renda>
    When O usuário solicita um empréstimo de valor R$ <Valor>
    Then O sistema deve retornar o status "Aprovado"
    And O valor do empréstimo deve estar disponível na conta do usuário

    Examples:
      | Valor | Renda  |
      | 5000  | 120000 |
      | 10000 | 180000 |

  @Empréstimo
  Scenario Outline: Solicitação de empréstimo com negação
    Given O usuário possui renda anual de R$ <Renda>
    When O usuário solicita um empréstimo de valor R$ <Valor>
    Then O sistema deve retornar o status "Negado"

    Examples:
      | Valor | Renda  |
      | 20000 | 50000  |
      | 15000 | 80000  |

Feature: Pagamento de Contas
  Para que o usuário registre e agende pagamentos

  @Pagamento
  Scenario: Registro de pagamento imediato
    Given O usuário está logado
    When Ele registra o pagamento com:
      | Beneficiário | Endereço          | Cidade | Estado | CEP     | Telefone      | Conta Destino | Valor | Data    |
      | Luz          | Rua das Flores 1 | SP     | SP     | 12345-678 | (11) 91234-5678 | Conta123     | 150   | 01/09/2024 |
    Then O pagamento deve ser incluído no histórico de transações da conta do usuário
    And O sistema deve exibir a mensagem "Pagamento registrado com sucesso"

  @Pagamento
  Scenario: Agendamento de pagamento futuro
    Given O usuário está logado
    When Ele registra o pagamento com data de vencimento em 30 dias
    Then O pagamento deve aparecer no histórico com status "Agendado"
    And O sistema deve impedir que o usuário pague antes da data de vencimento

Feature: Requisitos Gerais – Navegação e Usabilidade
  Para garantir consistência e usabilidade em todo o site

  @Navegação
  Scenario: Todas as páginas carregam sem erros
    Given O usuário acessa cada página do site (Login, Cadastro, Minha Conta, Extrato, Transferência, Empréstimo, Pagamento)
    When Ele visualiza cada página
    Then Cada página deve carregar completamente sem mensagens de erro

  @Navegação
  Scenario: Consistência de menus e links
    Given O usuário navega pelos menus principais
    When Ele clica em cada link
    Then Cada link deve levar à página correta
    And Os menus devem permanecer visíveis em todas as páginas

  @Erro
  Scenario: Exibição de mensagens de erro claras
    Given O usuário tenta executar uma ação inválida (ex.: transferir valor superior ao saldo)
    When A ação é processada
    Then O sistema deve exibir uma mensagem de erro explicativa e específica
    And A mensagem deve estar em destaque (ex.: vermelho, negrito)

  @Acessibilidade
  Scenario: Navegação via teclado e leitores de tela
    Given O usuário utiliza um leitor de tela
    When Ele navega pelo site
    Then Todos os elementos interativos devem ter rótulos adequados e serem acessíveis via teclado

```

**Observações**  
- Os cenários “Scenario Outline” permitem testes de múltiplos valores de entrada em um único cenário.  
- Cada cenário pode ser enriquecido com *Background* se houver passos repetitivos (ex.: login prévio).  
- Para testes automatizados, as etapas de “When” e “Then” devem ser mapeadas para steps em sua camada de teste (Cucumber, SpecFlow, etc.).  
- Ajuste os exemplos de dados conforme o domínio real (ex.: CEP, formato de telefone).