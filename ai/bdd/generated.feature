**Cenários BDD – ParaBank (Formato Gherkin – Português)**  

```gherkin
#====================================================================#
# 1 – Cadastro de Usuário
#====================================================================#
Feature: Cadastro de Usuário
  Para garantir que novos clientes possam abrir conta
  Como usuário
  Quero registrar meus dados obrigatórios

  Scenario Outline: Cadastro bem‑sucedido
    Given o usuário está na página de cadastro
    When preenche os campos obrigatórios com
      | campo              | valor             |
      | nome               | <nome>            |
      | email              | <email>           |
      | telefone           | <telefone>        |
      | CEP                | <cep>             |
      | endereço           | <endereço>        |
      | cidade             | <cidade>          |
      | estado             | <estado>          |
      | senha              | <senha>           |
      | confirmaçãoSenha  | <senha>           |
    And clica no botão “Cadastrar”
    Then o sistema exibe a mensagem “Registro concluído”
    And o usuário pode efetuar login

    Examples:
      | nome            | email                     | telefone          | cep     | endereço          | cidade   | estado | senha      |
      | João Silva      | joao.silva@example.com    | 9999999999        | 12345678| Rua A, 123        | São Paulo| SP     | senha123   |

  Scenario Outline: Campos obrigatórios ausentes
    Given o usuário está na página de cadastro
    When preenche apenas os campos obrigatórios com
      | campo              | valor |
      | nome               | <nome> |
      | email              | <email> |
      | telefone           | <telefone> |
      | CEP                | <cep> |
      | senha              | <senha> |
      | confirmaçãoSenha  | <senha> |
    And clica no botão “Cadastrar”
    Then o sistema exibe a mensagem “O campo <campo> é obrigatório”

    Examples:
      | campo      | nome          | email                     | telefone          | cep     | senha      |
      | endereço   | João Silva    | joao.silva@example.com    | 9999999999        | 12345678| senha123   |
      | cidade     | João Silva    | joao.silva@example.com    | 9999999999        | 12345678| senha123   |

  Scenario Outline: Validação de dados inválidos
    Given o usuário está na página de cadastro
    When preenche os campos obrigatórios com
      | campo              | valor |
      | nome               | <nome> |
      | email              | <email> |
      | telefone           | <telefone> |
      | CEP                | <cep> |
      | endereço           | <endereço> |
      | cidade             | <cidade> |
      | estado             | <estado> |
      | senha              | <senha> |
      | confirmaçãoSenha  | <senha> |
    And clica no botão “Cadastrar”
    Then o sistema exibe a mensagem “<mensagem>”

    Examples:
      | email                 | mensagem                                 |
      | invalido@exemplo      | Email inválido                          |
      | usuario@exemplo.com   | Email inválido                          |
      |                       | Email obrigatório                       |
      | usuario@exemplo.com   | Email inválido (sem domínio)           |

      | telefone  | mensagem                        |
      | 1234      | Telefone inválido (menos de 10 dígitos) |
      | abcdefghij| Telefone inválido (não numérico) |

      | cep       | mensagem                        |
      | 123       | CEP inválido (menos de 8 dígitos) |
      | abc12345  | CEP inválido (não numérico)      |

#====================================================================#
# 2 – Login
#====================================================================#
Feature: Login
  Para que usuários autenticados acessem sua conta
  Como usuário
  Quero efetuar login com credenciais válidas

  Scenario: Login bem‑sucedido
    Given o usuário está na página de login
    When digita o usuário “<usuario>” e a senha “<senha>”
    And clica em “Entrar”
    Then o sistema redireciona para a página inicial da conta

    Examples:
      | usuario      | senha      |
      | joao.silva   | senha123   |

  Scenario Outline: Login com credenciais inválidas
    Given o usuário está na página de login
    When digita o usuário “<usuario>” e a senha “<senha>”
    And clica em “Entrar”
    Then o sistema exibe a mensagem “Credenciais inválidas”

    Examples:
      | usuario      | senha      |
      | joao.silva   | wrongpass  |
      | unknown      | senha123   |
      |             | senha123   |

#====================================================================#
# 3 – Acesso à Conta (Saldo e Extrato)
#====================================================================#
Feature: Acesso à Conta
  Para que o usuário verifique saldo e histórico
  Como cliente
  Quero visualizar saldo atualizado e extrato

  Scenario: Exibição de saldo após operação
    Given o usuário está logado
    And tem saldo inicial de $1000
    When realiza uma transferência de $200 para conta X
    Then o saldo exibido deve ser $800

  Scenario: Exibição do extrato em ordem cronológica
    Given o usuário está logado
    When visualiza o extrato
    Then as transações devem aparecer em ordem cronológica, mais recente no topo

#====================================================================#
# 4 – Transferência de Fundos
#====================================================================#
Feature: Transferência de Fundos
  Para que o cliente movimente recursos entre contas
  Como usuário
  Quero transferir um valor de uma conta para outra

  Scenario: Transferência com saldo suficiente
    Given o usuário tem saldo de $500 na conta origem
    And possui conta destino com número “1234”
    When solicita transferência de $200 para conta “1234”
    And confirma a transação
    Then o valor de $200 deve ser debitado da origem
    And o valor de $200 deve ser creditado na conta destino
    And ambas as contas registram a transação no histórico

  Scenario Outline: Transferência com saldo insuficiente
    Given o usuário tem saldo de $<saldo> na conta origem
    And possui conta destino com número “1234”
    When tenta transferir $<valor> para conta “1234”
    And confirma a transação
    Then o sistema exibe a mensagem “Saldo insuficiente”

    Examples:
      | saldo | valor |
      | 100   | 200   |
      | 50    | 75    |

#====================================================================#
# 5 – Solicitação de Empréstimo
#====================================================================#
Feature: Solicitação de Empréstimo
  Para que o cliente possa solicitar crédito
  Como usuário
  Quero informar valor e renda anual para receber aprovação

  Scenario Outline: Aprovação de empréstimo
    Given o usuário está logado
    When solicita empréstimo de $<valor> com renda anual $<renda>
    Then o sistema retorna “Aprovado”

    Examples:
      | valor | renda |
      | 5000  | 70000 |
      | 10000 | 120000|

  Scenario Outline: Negação de empréstimo
    Given o usuário está logado
    When solicita empréstimo de $<valor> com renda anual $<renda>
    Then o sistema retorna “Negado”

    Examples:
      | valor | renda |
      | 20000 | 40000 |
      | 15000 | 30000 |

#====================================================================#
# 6 – Pagamento de Contas
#====================================================================#
Feature: Pagamento de Contas
  Para que o cliente registre pagamentos recorrentes ou únicos
  Como usuário
  Quero cadastrar um pagamento com todos os dados obrigatórios

  Scenario Outline: Pagamento único
    Given o usuário está na tela de “Novo Pagamento”
    When preenche:
      | beneficiário | <beneficiario> |
      | endereço     | <endereço>     |
      | cidade       | <cidade>       |
      | estado       | <estado>       |
      | CEP          | <cep>          |
      | telefone     | <telefone>     |
      | contaDestino | <conta>        |
      | valor        | <valor>        |
      | data         | <data>         |
    And confirma
    Then o pagamento aparece no histórico com valor “$<valor>”
    And a data de pagamento é “<data>”

    Examples:
      | beneficiario | endereço         | cidade   | estado | cep      | telefone      | conta | valor | data       |
      | Conta de Luz  | Av. Paulista, 100| São Paulo| SP     | 01001000 | 11999999999   | 5678  | 120   | 2025-12-01 |

  Scenario: Pagamento futuro respeitando data agendada
    Given o usuário agenda pagamento para data “<data>”
    When a data atual é “<hoje>”
    Then o sistema não processa o pagamento até “<data>”

    Examples:
      | data       | hoje       |
      | 2025-12-15 | 2025-12-10 |

#====================================================================#
# 7 – Requisitos Gerais de Navegação e Usabilidade
#====================================================================#
Feature: Navegação e Usabilidade
  Para assegurar experiência consistente e sem erros

  Scenario: Carregamento de todas as páginas
    Given o usuário navega para cada página do sistema
    When a página carrega
    Then não há mensagens de erro de navegação

  Scenario: Consistência de menus e links
    Given o usuário verifica o menu principal
    Then todos os links estão presentes em todas as páginas
    And cada link redireciona corretamente

  Scenario: Clareza nas mensagens de erro
    Given o usuário faz uma ação inválida
    When o sistema gera mensagem de erro
    Then a mensagem é exibida em vermelho
    And o texto descreve claramente o problema
```

**Observações**  
- Cada `Scenario Outline` permite testar múltiplos valores de entrada com a mesma lógica.  
- As mensagens de erro e confirmações foram modeladas de forma genérica; podem ser ajustadas ao texto exato da aplicação.  
- Para testes de agendamento de pagamentos futuros, a comparação entre `data` e `hoje` deve ser implementada em código de teste (ou em um step definition que manipule datas).  
- Os cenários de transferência e empréstimo incluem tanto casos positivos quanto negativos, garantindo cobertura de fluxo e regras de negócio.