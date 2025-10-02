```gherkin
# ======================================================================
# ParaBank – Cenários BDD em Gherkin (Português)
# ======================================================================

# 1. Feature: Cadastro de Usuário
Feature: Cadastro de Usuário
  Para que o sistema permita o registro de novos usuários
  o usuário deve preencher todos os campos obrigatórios
  e receber mensagens claras em caso de erro.

  @Cadastro
  Scenario Outline: Cadastro bem-sucedido
    Dado que o usuário acessa a tela de cadastro
    Quando ele preenche os campos obrigatórios com "<nome>", "<sobrenome>", "<email>", "<telefone>", "<cep>", "<senha>"
    E clica em “Cadastrar”
    Então a mensagem de sucesso "<mensagem_sucesso>" deve ser exibida
    E o usuário deve conseguir fazer login com "<email>" e "<senha>"

    Examples:
      | nome      | sobrenome | email                | telefone     | cep     | senha   | mensagem_sucesso                 |
      | João      | Silva     | joao.silva@email.com | (11)987654321| 01001000| senha123| "Cadastro realizado com sucesso!"|

  @Cadastro @Validacao
  Scenario Outline: Cadastro com campo obrigatório em branco
    Dado que o usuário acessa a tela de cadastro
    Quando ele deixa em branco o campo "<campo>"
    E clica em “Cadastrar”
    Então a mensagem de erro "<mensagem_erro>" deve ser exibida

    Examples:
      | campo        | mensagem_erro                                 |
      | nome         | "Nome é obrigatório"                          |
      | sobrenome    | "Sobrenome é obrigatório"                     |
      | email        | "Email é obrigatório"                         |
      | telefone     | "Telefone é obrigatório"                      |
      | cep          | "CEP é obrigatório"                           |
      | senha        | "Senha é obrigatória"                         |

  @Cadastro @Validacao
  Scenario Outline: Cadastro com dados inválidos
    Dado que o usuário acessa a tela de cadastro
    Quando ele preenche "<campo>" com o valor "<valor_invalido>"
    E clica em “Cadastrar”
    Então a mensagem de erro "<mensagem_erro>" deve ser exibida

    Examples:
      | campo      | valor_invalido           | mensagem_erro                                 |
      | telefone   | "abc123"                 | "Telefone inválido. Use apenas números."      |
      | cep        | "123"                    | "CEP inválido. Deve conter 8 dígitos."        |
      | email      | "usuario.com"            | "Email inválido. Use o formato nome@domínio." |

# 2. Feature: Login
Feature: Login
  Para que o usuário possa acessar sua conta
  o sistema deve validar credenciais e redirecionar para a página inicial.

  @Login
  Scenario Outline: Login bem-sucedido
    Dado que o usuário está na tela de login
    Quando ele digita "<email>" e "<senha>"
    E clica em “Entrar”
    Então o usuário é redirecionado para a página inicial da conta
    E a mensagem “Bem‑vindo, <nome>” é exibida

    Examples:
      | email                | senha   | nome     |
      | joao.silva@email.com | senha123| João     |

  @Login @Validacao
  Scenario Outline: Login com credenciais inválidas
    Dado que o usuário está na tela de login
    Quando ele digita "<email>" e "<senha>"
    E clica em “Entrar”
    Então a mensagem de erro "<mensagem_erro>" é exibida

    Examples:
      | email                | senha   | mensagem_erro                     |
      | joao.silva@email.com | wrong   | "Credenciais inválidas."          |
      | wrong@email.com      | senha123| "Credenciais inválidas."          |
      |                         |         | "Preencha email e senha."        |

# 3. Feature: Acesso à Conta – Saldo e Extrato
Feature: Acesso à Conta – Saldo e Extrato
  O sistema deve exibir saldo atualizado e extrato em ordem cronológica.

  @Conta @Saldo
  Scenario: Visualização do saldo após transação
    Dado que o usuário está na página inicial
    Quando ele faz uma transferência de R$ 500,00
    Então o saldo exibido deve ser "<saldo_atualizado>"
    E o extrato lista a transferência em ordem cronológica

    Examples:
      | saldo_atualizado |
      | R$ 2.500,00       |

  @Conta @Extrato
  Scenario: Exibição de extrato em ordem cronológica
    Dado que o usuário está na página de extrato
    Quando ele visualiza as transações recentes
    Então o extrato deve listar as transações do mais recente ao mais antigo

# 4. Feature: Transferência de Fundos
Feature: Transferência de Fundos
  O usuário deve transferir valores entre contas, respeitando saldo.

  @Transferencia @Sucesso
  Scenario: Transferência válida
    Dado que o usuário está na tela de transferência
    Quando ele seleciona conta de origem "<conta_orig>" e conta de destino "<conta_dest>" e valor de R$ <valor>
    E confirma a transferência
    Então o valor R$ <valor> deve ser debitado de "<conta_orig>"
    E creditado em "<conta_dest>"
    E a transação aparece no histórico de ambas as contas

    Examples:
      | conta_orig | conta_dest | valor |
      | 123456     | 654321     | 200   |

  @Transferencia @SaldoInsuficiente
  Scenario: Transferência com valor superior ao saldo
    Dado que o usuário está na tela de transferência
    Quando ele seleciona conta de origem "<conta_orig>" e conta de destino "<conta_dest>" e valor de R$ <valor>
    E tenta confirmar a transferência
    Então a mensagem de erro "<mensagem_erro>" é exibida
    E nenhum débito ou crédito ocorre

    Examples:
      | conta_orig | conta_dest | valor | mensagem_erro                     |
      | 123456     | 654321     | 10.000| "Saldo insuficiente para essa transferência."|

# 5. Feature: Solicitação de Empréstimo
Feature: Solicitação de Empréstimo
  O usuário solicita um empréstimo informando valor e renda anual.
  O sistema responde com aprovação ou negação.

  @Emprestimo @Aprovado
  Scenario: Solicitação de empréstimo aprovada
    Dado que o usuário está na tela de solicitação de empréstimo
    Quando ele preenche valor de R$ <valor> e renda anual de R$ <renda>
    E envia a solicitação
    Então a mensagem "<mensagem>" é exibida
    E o status do empréstimo é “Aprovado”

    Examples:
      | valor | renda  | mensagem                        |
      | 5.000 | 50.000 | "Empréstimo aprovado!"          |

  @Emprestimo @Negado
  Scenario: Solicitação de empréstimo negada
    Dado que o usuário está na tela de solicitação de empréstimo
    Quando ele preenche valor de R$ <valor> e renda anual de R$ <renda>
    E envia a solicitação
    Então a mensagem "<mensagem>" é exibida
    E o status do empréstimo é “Negado”

    Examples:
      | valor | renda  | mensagem                        |
      | 50.000| 10.000 | "Empréstimo negado: renda insuficiente." |

# 6. Feature: Pagamento de Contas
Feature: Pagamento de Contas
  O usuário registra pagamento de conta com todos os detalhes.

  @Pagamento @Sucesso
  Scenario: Pagamento de conta agendado
    Dado que o usuário está na tela de pagamento de contas
    Quando ele informa beneficiário "<beneficiario>", endereço "<endereco>", cidade "<cidade>", estado "<estado>", CEP "<cep>", telefone "<telefone>", conta de destino "<conta_dest>", valor de R$ <valor> e data "<data>"
    E confirma o pagamento
    Então a mensagem "<mensagem>" é exibida
    E o pagamento aparece no histórico de transações
    E o pagamento será executado na data "<data>"

    Examples:
      | beneficiario | endereco           | cidade | estado | cep      | telefone     | conta_dest | valor | data      | mensagem                          |
      | Maria        | Rua das Flores, 10 | SP     | SP     | 01001-000| (11)912345678| 123456     | 150   | 2025-11-01| "Pagamento agendado com sucesso!"|

  @Pagamento @Validacao
  Scenario Outline: Pagamento com campo obrigatório vazio
    Dado que o usuário está na tela de pagamento de contas
    Quando ele deixa em branco o campo "<campo>"
    E tenta confirmar o pagamento
    Então a mensagem de erro "<mensagem_erro>" é exibida

    Examples:
      | campo         | mensagem_erro                          |
      | beneficiario  | "Beneficiário é obrigatório"           |
      | endereco      | "Endereço é obrigatório"               |
      | cidade        | "Cidade é obrigatória"                 |
      | estado        | "Estado é obrigatório"                 |
      | cep           | "CEP é obrigatório"                    |
      | telefone      | "Telefone é obrigatório"               |
      | conta_dest    | "Conta de destino é obrigatória"       |
      | valor         | "Valor é obrigatório"                  |
      | data          | "Data de pagamento é obrigatória"      |

# 7. Feature: Requisitos Gerais de Navegação e Usabilidade
Feature: Requisitos Gerais de Navegação e Usabilidade
  As páginas devem carregar corretamente e menus/links devem ser consistentes.

  @Navegacao @Carregamento
  Scenario: Todas as páginas carregam sem erros
    Dado que o usuário navega para cada página do sistema
    Quando a página é carregada
    Então não há erros de navegação ou carregamento

  @Usabilidade @Consistencia
  Scenario: Menus e links são consistentes em todas as páginas
    Dado que o usuário acessa diferentes páginas (Login, Cadastro, Conta, Transferência, etc.)
    Quando ele observa os menus e links
    Então cada página exibe o mesmo menu principal e links correspondentes

  @Usabilidade @Mensagens
  Scenario: Mensagens de erro são claras e objetivas
    Dado que o usuário tenta realizar uma operação inválida
    Quando o sistema exibe a mensagem de erro
    Então a mensagem deve ser curta, direta e indicar a ação necessária para correção

```

> **Observação:**  
> - Use os tags (`@Cadastro`, `@Login`, etc.) para agrupar e filtrar cenários durante a execução do BDD.  
> - Os valores de exemplo podem ser ajustados conforme o ambiente de teste.  
> - Se necessário, crie `Scenario Outline` adicionais para cobrir mais variações de dados.