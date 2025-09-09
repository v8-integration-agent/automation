## Feature: Cadastro de Usuário

```gherkin
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar meus dados
  Para poder fazer login e usar os serviços

  Scenario Outline: Cadastro com dados válidos
    Given o usuário está na página de cadastro
    When ele preenche os campos obrigatórios com
      | nome | email | senha | telefone | cep  |
      | <nome> | <email> | <senha> | <telefone> | <cep> |
    And ele clica em “Cadastrar”
    Then a mensagem “Cadastro concluído com sucesso” deve ser exibida
    And o usuário deve ser redirecionado para a página de login

    Examples:
      | nome            | email                 | senha | telefone     | cep     |
      | João Silva      | joao.silva@email.com  | Pass1! | (11) 98765‑4321 | 01234‑567 |
      | Maria Souza     | maria@email.com       | Pass2! | (21) 99876‑5432 | 22345‑678 |

  Scenario Outline: Cadastro com campo obrigatório vazio
    Given o usuário está na página de cadastro
    When ele deixa o campo "<campo>" vazio e preenche os demais com valores válidos
    And ele clica em “Cadastrar”
    Then a mensagem “O campo <campo> é obrigatório” deve ser exibida

    Examples:
      | campo   |
      | nome    |
      | email   |
      | senha   |
      | telefone|
      | cep     |

  Scenario Outline: Cadastro com dados inválidos
    Given o usuário está na página de cadastro
    When ele preenche os campos com valores inválidos
      | nome | email            | senha | telefone     | cep       |
      | <nome> | <email> | <senha> | <telefone> | <cep> |
    And ele clica em “Cadastrar”
    Then as mensagens de erro apropriadas devem aparecer:
      | mensagem                                    |
      | "<campo>" contém formato inválido           |

    Examples:
      | nome | email            | senha | telefone     | cep       | campo   |
      | João | joao@email       | Pass1! | (11) 98765‑4321 | 01234‑567 | email   |
      | Maria| maria@email.com | Pass2  | 12345          | 22345‑678 | telefone|
      | Ana  | ana@email.com   | Pass!  | (21) 99876‑5432 | 000000    | cep     |
```

---

## Feature: Login

```gherkin
Feature: Login
  Como cliente já registrado
  Quero entrar no sistema
  Para acessar minha conta

  Scenario Outline: Login com credenciais válidas
    Given o usuário está na página de login
    When ele insere:
      | email               | senha |
      | <email> | <senha> |
    And clica em “Entrar”
    Then ele deve ser redirecionado para a página inicial da conta
    And a mensagem “Bem‑vindo, <nome>” deve aparecer

    Examples:
      | email                 | senha  | nome   |
      | joao.silva@email.com  | Pass1! | João   |
      | maria@email.com       | Pass2! | Maria  |

  Scenario Outline: Login com credenciais inválidas
    Given o usuário está na página de login
    When ele insere:
      | email               | senha |
      | <email> | <senha> |
    And clica em “Entrar”
    Then a mensagem “E‑mail ou senha inválidos” deve ser exibida

    Examples:
      | email                  | senha  |
      | joao.silva@email.com   | Wrong1 |
      | unknown@email.com      | Pass1! |
      | joao.silva@email.com   | Pass2! |
```

---

## Feature: Acesso à Conta – Saldo e Extrato

```gherkin
Feature: Acesso à Conta
  Como cliente logado
  Quero visualizar saldo e extrato
  Para acompanhar minhas finanças

  Scenario: Ver saldo atual
    Given o usuário está na página inicial da conta
    Then a tela deve mostrar “Saldo: R$ <saldo>”

  Scenario: Visualizar extrato em ordem cronológica
    Given o usuário está na página de extrato
    Then a lista de transações deve aparecer em ordem decrescente (mais recente primeiro)
    And cada linha deve conter:
      | data | descrição | valor | saldo |

  Scenario Outline: Após transferência, saldo e extrato atualizados
    Given o usuário realizou uma transferência de R$ <valor> para conta <destino>
    When ele navega para a página inicial da conta
    Then o saldo deve refletir a dedução de R$ <valor>
    And na página de extrato a transação “Transferência para <destino>” deve aparecer

    Examples:
      | valor | destino |
      | 100.00 | 123456 |
      | 200.00 | 654321 |
```

---

## Feature: Transferência de Fundos

```gherkin
Feature: Transferência de Fundos
  Como cliente logado
  Quero transferir dinheiro entre minhas contas
  Para gerenciar meus recursos

  Scenario Outline: Transferência bem‑sucedida
    Given o usuário está na página de transferência
    When ele seleciona:
      | conta origem | conta destino | valor |
      | <origem>     | <destino>     | <valor> |
    And clica em “Confirmar”
    Then a mensagem “Transferência concluída” deve aparecer
    And a conta origem deve ter saldo reduzido em R$ <valor>
    And a conta destino deve ter saldo aumentado em R$ <valor>
    And ambas as contas devem registrar a transação no histórico

    Examples:
      | origem | destino | valor |
      | 111111 | 222222 | 50.00 |
      | 333333 | 444444 | 200.00 |

  Scenario: Transferência com valor superior ao saldo
    Given o usuário tem saldo de R$ 100.00 na conta 111111
    When ele tenta transferir R$ 150.00 para a conta 222222
    Then a mensagem “Saldo insuficiente” deve ser exibida
    And a transferência não é concluída

  Scenario: Campos obrigatórios vazios na transferência
    Given o usuário está na página de transferência
    When ele deixa o campo “Conta destino” vazio
    And clica em “Confirmar”
    Then a mensagem “Conta destino é obrigatória” deve aparecer
```

---

## Feature: Solicitação de Empréstimo

```gherkin
Feature: Solicitação de Empréstimo
  Como cliente interessado
  Quero solicitar um empréstimo
  Para obter crédito adicional

  Scenario Outline: Solicitação com dados válidos
    Given o usuário está na página de empréstimo
    When ele insere:
      | valor do empréstimo | renda anual |
      | <valor>             | <renda>     |
    And clica em “Solicitar”
    Then o sistema deve exibir “Empréstimo <status>”
    And <status> deve ser “Aprovado” ou “Negado” conforme regras internas

    Examples:
      | valor | renda | status |
      | 10000 | 30000 | Aprovado |
      | 20000 | 25000 | Negado   |

  Scenario: Dados incompletos na solicitação
    Given o usuário está na página de empréstimo
    When ele deixa o campo “Renda anual” vazio
    And clica em “Solicitar”
    Then a mensagem “Renda anual é obrigatória” deve aparecer
```

---

## Feature: Pagamento de Contas

```gherkin
Feature: Pagamento de Contas
  Como cliente
  Quero registrar pagamentos futuros
  Para controlar contas de serviços

  Scenario Outline: Pagamento imediato
    Given o usuário está na página de pagamento
    When ele preenche:
      | beneficiário | endereço | cidade | estado | cep    | telefone | conta destino | valor | data   |
      | <benef>      | <addr>   | <city> | <state>| <cep> | <tel>    | <conta>      | <val> | <data> |
    And clica em “Confirmar”
    Then a mensagem “Pagamento registrado” deve aparecer
    And a transação deve aparecer no histórico de pagamentos

    Examples:
      | benef   | addr             | city   | state | cep      | tel           | conta | val  | data       |
      | Luz     | Av. das Flores   | SP     | SP    | 01010‑010| (11) 99999‑9999| 123456| 120  | 2025‑09‑15 |
      | Água    | Rua Nova         | RJ     | RJ    | 22000‑000| (21) 88888‑8888| 654321| 80   | 2025‑10‑01 |

  Scenario: Pagamento futuro com data posterior à hoje
    Given o usuário está na página de pagamento
    When ele define a data de pagamento como 10 dias à frente
    And clica em “Confirmar”
    Then o sistema deve agendar o pagamento e mostrar “Pagamento agendado para <data>”

  Scenario: Erro ao deixar campos obrigatórios vazios
    Given o usuário está na página de pagamento
    When ele deixa o campo “Beneficiário” vazio
    And clica em “Confirmar”
    Then a mensagem “Beneficiário é obrigatório” deve aparecer
```

---

## Feature: Navegação e Usabilidade

```gherkin
Feature: Navegação e Usabilidade
  Como usuário
  Quero que o sistema seja intuitivo
  Para usar sem dificuldades

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega para todas as páginas principais
    Then nenhuma página deve apresentar erro 500 ou 404

  Scenario: Menus consistentes em todas as páginas
    Given o usuário está em qualquer página
    Then o menu de navegação deve conter os itens:
      | Conta | Transferir | Empréstimo | Pagamentos | Logout |

  Scenario: Mensagens de erro claras e objetivas
    When um campo inválido é detectado
    Then a mensagem de erro deve conter:
      | texto | ação recomendada |
      | "<campo> contém formato inválido" | Corrija e tente novamente |
```

---

### Observações

* Os cenários acima cobrem os **casos positivos** (cadastro, login, transferência, empréstimo, pagamento) e **casos negativos** (dados inválidos, saldo insuficiente, campos vazios).  
* Para testes automatizados, use *Scenario Outline* com *Examples* ou *Data Tables* para parametrizar valores.  
* Se preferir manter os passos em inglês, basta substituir as frases por seu equivalente em inglês; a estrutura permanece a mesma.  

Esses cenários podem ser importados em ferramentas de BDD como Cucumber, SpecFlow ou Behave e servem como base para a implementação das histórias de teste.