## Gherkin – ParaBank  
*(Português – todos os cenários foram escritos em Gherkin padrão 1.0)*  

```gherkin
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero me cadastrar preenchendo todos os campos obrigatórios
  Para poder usar o sistema

  Background:
    Dado que eu esteja na página “Criar Conta”

  Scenario: Cadastro completo e válido
    When eu preencho “Nome” com “Ana Silva”
    And eu preencho “CPF” com “123.456.789-00”
    And eu preencho “Telefone” com “(11) 91234-5678”
    And eu preencho “CEP” com “01001-000”
    And eu preencho “Email” com “ana.silva@example.com”
    And eu preencho “Senha” com “SenhaSegura123”
    And eu preencho “Confirmar Senha” com “SenhaSegura123”
    And eu clico em “Criar Conta”
    Then eu devo ver a mensagem “Cadastro concluído com sucesso!”
    And eu devo ser redirecionado para a tela de login

  Scenario Outline: Validação de campos inválidos
    When eu preencho “Telefone” com "<telefone>"
    And eu preencho “CEP” com "<cep>"
    And eu preencho “Email” com "<email>"
    And eu clico em “Criar Conta”
    Then eu devo ver a mensagem "<mensagem>"

    Examples:
      | telefone           | cep      | email                    | mensagem                                |
      | 1234               | 01001-000| ana.silva@example.com    | Telefone inválido, digite um telefone 11 dígitos |
      | (11) 91234-5678    | 01       | ana.silva@example.com    | CEP inválido, digite um CEP no formato 5-4 |
      | (11) 91234-5678    | 01001-000| ana.silvaexample.com     | E‑mail inválido, digite um e‑mail válido |

  Scenario: Tentativa de cadastro com campo obrigatório em branco
    When eu deixo o campo “Nome” vazio
    And eu preencho os demais campos corretamente
    And eu clico em “Criar Conta”
    Then eu devo ver a mensagem “Nome é obrigatório”

  Scenario: Cadastro com email já existente
    Given que “email.exemplo@example.com” já está cadastrado
    When eu preencho “Email” com “email.exemplo@example.com”
    And eu preencho todos os outros campos corretamente
    And eu clico em “Criar Conta”
    Then eu devo ver a mensagem “E‑mail já cadastrado”

--------------------------------------------------------------------

Feature: Login
  Como usuário registrado
  Quero fazer login com credenciais válidas
  Para acessar minha conta

  Background:
    Dado que o usuário “usuario1” esteja cadastrado com senha “Senha123”

  Scenario: Login bem‑sucedido
    When eu preencho “E‑mail” com “usuario1@example.com”
    And eu preencho “Senha” com “Senha123”
    And eu clico em “Entrar”
    Then eu devo ser redirecionado para a página inicial da conta
    And eu devo ver “Bem‑vindo, usuario1”

  Scenario: Login com senha incorreta
    When eu preencho “E‑mail” com “usuario1@example.com”
    And eu preencho “Senha” com “SenhaErrada”
    And eu clico em “Entrar”
    Then eu devo ver a mensagem “Credenciais inválidas. Por favor, tente novamente.”

  Scenario: Login com e‑mail inexistente
    When eu preencho “E‑mail” com “naoexiste@example.com”
    And eu preencho “Senha” com “Senha123”
    And eu clico em “Entrar”
    Then eu devo ver a mensagem “Credenciais inválidas. Por favor, tente novamente.”

--------------------------------------------------------------------

Feature: Acesso à Conta – Saldo e Extrato
  Como cliente logado
  Quero visualizar meu saldo atualizado
  E consultar o extrato em ordem cronológica

  Background:
    Dado que eu esteja logado no sistema
    E que a minha conta possua saldo R$ 1.000,00
    E que haja 3 transações recentes

  Scenario: Exibir saldo após operação
    When eu realizo uma transferência de R$ 200,00 para conta “123-45”
    Then o saldo exibido deve ser “R$ 800,00”

  Scenario Outline: Extrato em ordem cronológica
    When eu acesso “Extrato”
    Then eu devo ver a lista de transações:
      | Data       | Descrição          | Valor     |
      | <data1>    | Transferência para 123-45 | -R$ 200,00 |
      | <data2>    | Depósito            | +R$ 500,00 |
      | <data3>    | Pagamento de Luz    | -R$ 150,00 |

    Examples:
      | data1      | data2      | data3      |
      | 2025-08-01 | 2025-07-30 | 2025-07-25 |

--------------------------------------------------------------------

Feature: Transferência de Fundos
  Como cliente logado
  Quero transferir dinheiro de uma conta para outra
  Para gerenciar meus recursos

  Background:
    Dado que eu esteja logado no sistema
    E a minha conta tenha saldo R$ 1.000,00

  Scenario: Transferência válida entre contas
    When eu seleciono conta origem “Minha Conta”
    And eu seleciono conta destino “Conta 987‑65”
    And eu preencho “Valor” com “R$ 300,00”
    And eu confirmo a transferência
    Then o saldo da conta origem deve ser “R$ 700,00”
    And o saldo da conta destino deve ser “R$ 300,00”
    And a transação deve aparecer no histórico de ambas as contas

  Scenario Outline: Transferência com valor superior ao saldo
    When eu seleciono conta origem “Minha Conta”
    And eu seleciono conta destino “Conta 987‑65”
    And eu preencho “Valor” com "<valor>"
    And eu confirmo a transferência
    Then eu devo ver a mensagem "<mensagem>"

    Examples:
      | valor      | mensagem                                                |
      | R$ 1.200,00 | “Saldo insuficiente. Transferência não realizada.”     |
      | R$ 0,00      | “O valor deve ser maior que zero.”                     |

  Scenario: Transferência com campo em branco
    When eu deixo o campo “Valor” vazio
    And eu confirmo a transferência
    Then eu devo ver a mensagem “Campo valor é obrigatório”

--------------------------------------------------------------------

Feature: Solicitação de Empréstimo
  Como cliente logado
  Quero solicitar um empréstimo
  Para financiar projetos

  Background:
    Dado que eu esteja logado no sistema

  Scenario: Empréstimo aprovado
    When eu preencho “Valor” com “R$ 5.000,00”
    And eu preencho “Renda Anual” com “R$ 80.000,00”
    And eu envio a solicitação
    Then eu devo ver o status “Aprovado”
    And a mensagem “Parabéns! Seu empréstimo foi aprovado.” deve ser exibida

  Scenario: Empréstimo negado por renda insuficiente
    When eu preencho “Valor” com “R$ 5.000,00”
    And eu preencho “Renda Anual” com “R$ 20.000,00”
    And eu envio a solicitação
    Then eu devo ver o status “Negado”
    And a mensagem “Seu empréstimo foi negado. Renda insuficiente.” deve ser exibida

  Scenario: Empréstimo com campo em branco
    When eu deixo “Valor” vazio
    And eu preencho “Renda Anual” com “R$ 80.000,00”
    And eu envio a solicitação
    Then eu devo ver a mensagem “Campo valor é obrigatório”

--------------------------------------------------------------------

Feature: Pagamento de Contas
  Como cliente logado
  Quero registrar um pagamento
  Para manter contas em dia

  Background:
    Dado que eu esteja logado no sistema

  Scenario: Pagamento futuro agendado
    When eu preencho “Beneficiário” com “Concessionária X”
    And eu preencho “Endereço” com “Rua A, 123”
    And eu preencho “Cidade” com “São Paulo”
    And eu preencho “Estado” com “SP”
    And eu preencho “CEP” com “01001-000”
    And eu preencho “Telefone” com “(11) 98765-4321”
    And eu preencho “Conta de Destino” com “987‑65”
    And eu preencho “Valor” com “R$ 250,00”
    And eu preencho “Data” com “2025‑09‑30”
    And eu confirmo o pagamento
    Then o pagamento deve aparecer na lista de transações agendadas
    And a data do pagamento deve ser “30/09/2025”

  Scenario: Pagamento imediato
    When eu preencho “Beneficiário” com “Banco Y”
    And eu preencho “Conta de Destino” com “123‑45”
    And eu preencho “Valor” com “R$ 150,00”
    And eu confirmo o pagamento
    Then a transação deve aparecer imediatamente no histórico
    And o saldo da conta deve ser debitado em “R$ 150,00”

  Scenario Outline: Pagamento com dados inválidos
    When eu preencho “Telefone” com "<telefone>"
    And eu preencho “CEP” com "<cep>"
    And eu preencho “Data” com "<data>"
    And eu confirmo o pagamento
    Then eu devo ver a mensagem "<mensagem>"

    Examples:
      | telefone          | cep      | data       | mensagem                                 |
      | 1234              | 01001-000 | 2025‑09‑30 | Telefone inválido, digite no formato (xx) xxxxx‑xxxx |
      | (11) 98765-4321   | 01       | 2025‑09‑30 | CEP inválido, digite no formato 5‑4           |
      | (11) 98765-4321   | 01001-000 | 2020‑01‑01 | Data de pagamento não pode ser passada.      |

--------------------------------------------------------------------

Feature: Navegação e Usabilidade – Requisitos Gerais
  Como usuário
  Quero ter uma experiência consistente em todas as páginas

  Scenario: Carregamento sem erros
    When eu acesso qualquer página do sistema
    Then a página deve carregar em menos de 3 segundos
    And não deve aparecer nenhuma mensagem de erro de navegação

  Scenario: Consistência de links e menus
    When eu navego pelas seguintes páginas: “Conta”, “Extrato”, “Transferências”, “Empréstimos”, “Pagamentos”
    Then cada página deve exibir o menu de navegação com os mesmos itens
    And o link “Sair” deve estar presente em todas as páginas

  Scenario: Mensagens de erro claras
    When eu tento submeter um formulário incompleto
    Then cada campo em falta deve exibir uma mensagem de erro no formato “<Campo> é obrigatório”
    And a mensagem global deve indicar “Por favor, corrija os erros abaixo”

  Scenario: Acessibilidade
    When eu navego usando apenas o teclado
    Then todos os botões e campos devem receber foco em ordem lógica
    And as imagens devem ter textos alternativos adequados

```

> **Obs.:**  
> • Cada *Background* contém o estado pré‑condicional comum ao conjunto de cenários da feature.  
> • Os *Scenario Outline* permitem testar variações de entrada sem duplicação de código.  
> • Mensagens de erro foram padronizadas de acordo com as regras de negócio citadas.  
> • O tempo de carregamento (≤ 3 s) e a ausência de erros de navegação são verificações de usabilidade e desempenho.  

Esses cenários cobrem os requisitos de aceite apresentados, garantindo que a aplicação **ParaBank** atenda às funcionalidades de cadastro, login, saldo/extrato, transferência, empréstimo, pagamento de contas e requisitos gerais de navegação.