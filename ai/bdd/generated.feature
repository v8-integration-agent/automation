```gherkin
# Feature: Cadastro de Usuário
# ----------------------------------
Feature: Cadastro de usuário no ParaBank

  Scenario: Cadastro bem-sucedido com todos os campos obrigatórios preenchidos
    Given o usuário está na página de cadastro
    When ele preenche os campos:
      | nomeCompleto | email              | senha | telefone   | CEP   |
      | João Silva   | joao.silva@email.com | 123456 | 11987654321 | 12345000 |
    And clica em "Registrar"
    Then o sistema deve exibir a mensagem "Cadastro realizado com sucesso"
    And o usuário deve ser direcionado para a tela de login

  Scenario Outline: Cadastro falha quando campos obrigatórios estão vazios
    Given o usuário está na página de cadastro
    When ele preenche os campos:
      | nomeCompleto | email              | senha | telefone   | CEP   |
      | <nome>       | <email>            | <senha> | <telefone> | <cep> |
    And clica em "Registrar"
    Then o sistema deve exibir a mensagem "<mensagem>"
    And o usuário não pode continuar com o cadastro

    Examples:
      | nome | email | senha | telefone | cep | mensagem                          |
      |      | joao@email.com | 123456 | 11987654321 | 12345000 | O campo "Nome Completo" é obrigatório |
      | João |                 | 123456 | 11987654321 | 12345000 | O campo "E‑mail" é obrigatório |
      | João | joao@email.com  |        | 11987654321 | 12345000 | O campo "Senha" é obrigatório |
      | João | joao@email.com  | 123456 |           | 12345000 | O campo "Telefone" é obrigatório |
      | João | joao@email.com  | 123456 | 11987654321 |        | O campo "CEP" é obrigatório     |

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário está na página de cadastro
    When ele preenche os campos:
      | nomeCompleto | email              | senha | telefone   | CEP   |
      | João Silva   | <email>            | 123456 | <telefone> | <cep> |
    And clica em "Registrar"
    Then o sistema deve exibir a mensagem "<mensagem>"
    And o usuário não pode continuar com o cadastro

    Examples:
      | email                 | telefone      | cep      | mensagem                                     |
      | joao.silva@email      | 11987654321   | 12345000 | O e‑mail não possui um formato válido       |
      | joao.silva@email.com  | 1198765432    | 12345000 | O telefone não possui o formato válido      |
      | joao.silva@email.com  | 11987654321   | 12345    | O CEP não possui o formato válido           |

# Feature: Login
# ----------------------------------
Feature: Autenticação de usuário

  Scenario: Login bem-sucedido com credenciais válidas
    Given o usuário tem uma conta registrada com email "joao@email.com" e senha "123456"
    And o usuário está na página de login
    When ele insere o e‑mail "joao@email.com" e a senha "123456"
    And clica em "Entrar"
    Then o sistema deve redirecionar o usuário para a página inicial da conta
    And a mensagem de boas‑vindas deve conter o nome "João Silva"

  Scenario Outline: Login falha com credenciais inválidas
    Given o usuário tem uma conta registrada com email "joao@email.com" e senha "123456"
    And o usuário está na página de login
    When ele insere o e‑mail "<email>" e a senha "<senha>"
    And clica em "Entrar"
    Then o sistema deve exibir a mensagem "<mensagem>"
    And o usuário permanece na tela de login

    Examples:
      | email                  | senha   | mensagem                                 |
      | joao@email.com         | 654321  | Credenciais inválidas                    |
      | joao@exemplo.com       | 123456  | Credenciais inválidas                    |
      |                        | 123456  | O campo "E‑mail" é obrigatório           |
      | joao@email.com         |         | O campo "Senha" é obrigatório            |

# Feature: Acesso à Conta (Saldo e Extrato)
# ----------------------------------
Feature: Visualização de saldo e extrato

  Scenario: Exibição de saldo atualizado após operação
    Given o usuário está autenticado na sua conta
    And o saldo inicial é de R$ 5.000,00
    When o usuário realiza uma transferência de R$ 1.000,00 para outra conta
    Then o saldo exibido na página deve ser R$ 4.000,00

  Scenario: Lista de transações em ordem cronológica
    Given o usuário está autenticado e tem as seguintes transações:
      | data        | descrição        | valor      |
      | 2025-08-01 | Salário          | +R$ 3.000 |
      | 2025-08-02 | Compra supermercado | -R$ 200 |
      | 2025-08-03 | Transferência para Ana | -R$ 500 |
    When o usuário acessa a página de extrato
    Then o extrato deve listar as transações em ordem: 2025‑08‑03, 2025‑08‑02, 2025‑08‑01
    And cada linha deve exibir data, descrição e valor corretamente

# Feature: Transferência de Fundos
# ----------------------------------
Feature: Transferência entre contas

  Scenario: Transferência bem‑sucedida com saldo suficiente
    Given o usuário tem saldo disponível de R$ 3.000,00 em Conta A
    And o usuário tem Conta B com saldo R$ 0,00
    And está na tela de transferência
    When ele seleciona Conta A como origem
    And seleciona Conta B como destino
    And insere o valor R$ 500,00
    And confirma a transferência
    Then Conta A deve ter saldo R$ 2.500,00
    And Conta B deve ter saldo R$ 500,00
    And uma entrada de histórico deve aparecer em ambas as contas indicando a transação

  Scenario Outline: Transferência falha quando valor excede saldo
    Given o usuário tem saldo de R$ <saldo> na conta origem
    And está na tela de transferência
    When ele seleciona a conta origem
    And seleciona qualquer conta destino
    And insere o valor R$ <valor>
    And tenta confirmar a transferência
    Then o sistema exibe a mensagem "<mensagem>"
    And a transferência não é realizada

    Examples:
      | saldo  | valor | mensagem                                    |
      | 300,00 | 500,00 | Valor da transferência excede o saldo disponível |

  Scenario: Registro da transferência no histórico
    Given o usuário realizou uma transferência de R$ 250,00 de Conta X para Conta Y
    When ele acessa o histórico da Conta X
    Then deve ver uma entrada com descrição "Transferência para Conta Y" e valor "-R$ 250,00"
    And quando acessa o histórico da Conta Y
    Then deve ver uma entrada com descrição "Transferência de Conta X" e valor "+R$ 250,00"

# Feature: Solicitação de Empréstimo
# ----------------------------------
Feature: Pedido de empréstimo

  Scenario: Empréstimo aprovado
    Given o usuário tem renda anual de R$ 80.000,00
    And o valor solicitado é R$ 10.000,00
    When o usuário submete a solicitação
    Then o sistema retorna o status "Aprovado"
    And a mensagem "Seu empréstimo foi aprovado" deve ser exibida

  Scenario: Empréstimo negado devido a renda insuficiente
    Given o usuário tem renda anual de R$ 30.000,00
    And o valor solicitado é R$ 15.000,00
    When o usuário submete a solicitação
    Then o sistema retorna o status "Negado"
    And a mensagem "Seu empréstimo foi negado" deve ser exibida

  Scenario Outline: Mensagem de resultado da solicitação
    Given o usuário tem renda anual de R$ <renda> e solicita empréstimo de R$ <valor>
    When ele submete a solicitação
    Then o resultado exibido deve ser "<status>"
    And a mensagem de retorno deve conter "<mensagem>"

    Examples:
      | renda  | valor | status   | mensagem                                |
      | 120000 | 5000  | Aprovado | Seu empréstimo foi aprovado             |
      | 45000  | 20000 | Negado   | Seu empréstimo foi negado               |

# Feature: Pagamento de Contas
# ----------------------------------
Feature: Agendamento e registro de pagamentos

  Scenario: Pagamento imediato registrado no histórico
    Given o usuário preenche o pagamento com:
      | beneficiário | endereço   | cidade | estado | CEP       | telefone     | contaDestino | valor | data      |
      | Luz          | Rua X      | SP     | SP     | 12345000  | 1199999999   | 123456        | 200   | 2025-08-25|
    And confirma o pagamento
    Then o pagamento deve aparecer no histórico como "Pago" na data 2025‑08‑25
    And a conta de destino deve ter seu saldo alterado apropriadamente

  Scenario: Pagamento futuro deve respeitar data de agendamento
    Given o usuário agenda um pagamento para 2025‑09‑01
    When ele confirma a agenda
    Then o pagamento não deve aparecer no histórico imediatamente
    And quando a data atual for 2025‑09‑01
    Then o pagamento deve aparecer no histórico com status "Pago"

  Scenario Outline: Campos obrigatórios não preenchidos no pagamento
    Given o usuário tenta submeter um pagamento sem preencher o campo "<campo>"
    When ele clica em "Confirmar"
    Then o sistema exibe a mensagem "<mensagem>"
    And o pagamento não é processado

    Examples:
      | campo            | mensagem                        |
      | Beneficiário     | O campo "Beneficiário" é obrigatório |
      | Endereço         | O campo "Endereço" é obrigatório   |
      | Cidade           | O campo "Cidade" é obrigatório     |
      | Estado           | O campo "Estado" é obrigatório     |
      | CEP              | O campo "CEP" é obrigatório        |
      | Telefone         | O campo "Telefone" é obrigatório   |
      | ContaDestino     | O campo "Conta de Destino" é obrigatório |
      | Valor            | O campo "Valor" é obrigatório      |
      | Data             | O campo "Data" é obrigatório       |

# Feature: Navegação e Usabilidade
# ----------------------------------
Feature: Consistência e carregamento das páginas

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega por todas as páginas disponíveis
    When ele visita cada link
    Then cada página deve carregar em menos de 5 segundos
    And nenhuma mensagem de erro "404" ou "500" deve aparecer

  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta submeter um formulário inválido
    When o sistema processa a submissão
    Then todas as mensagens de erro exibidas devem ser:
      - curtas
      - em português
      - conter a palavra que indica o problema (ex.: "telefone", "email")

  Scenario: Menus e links são consistentes em todas as páginas
    Given o usuário abre a aplicação em qualquer página
    When ele observa os menus de navegação
    Then todos os itens de menu (Login, Conta, Transferência, Empréstimo, Pagamento, Sair) devem estar presentes e ativos
    And os links devem apontar para as rotas corretas

  Scenario: Redirecionamento automático após login
    Given o usuário faz login com credenciais válidas
    When a autenticação é concluída
    Then o usuário é automaticamente redirecionado para a página inicial da conta
    And a barra de navegação mostra a opção "Sair"

  Scenario: Exibição de saldo atual na página inicial
    Given o usuário está autenticado
    When ele acessa a página inicial da conta
    Then o saldo exibido na área de destaque deve corresponder ao saldo real da conta
```