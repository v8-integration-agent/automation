**ParaBank – Cenários BDD em Gherkin (Português)**  

> Todos os cenários foram escritos seguindo o padrão BDD, utilizando os keywords `Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`.  
>  Para cenários que exigem variação de dados (ex.: diferentes tipos de erro) usei `Scenario Outline` com tabelas de exemplos.  

---

## 1️⃣ Cadastro de Usuário

```gherkin
Feature: Cadastro de Usuário

  Como cliente da ParaBank
  Quero criar uma conta
  Para poder acessar o sistema

  Scenario Outline: Cadastro com sucesso
    Given O usuário acessa a página de cadastro
    When Preenche os campos obrigatórios com
      | campo          | valor                |
      | Nome           | <nome>               |
      | Email          | <email>              |
      | Telefone       | <telefone>           |
      | CEP            | <cep>                |
      | Endereço       | <endereco>           |
      | Senha          | <senha>              |
      | Confirmação    | <senha>              |
    And Clica em "Cadastrar"
    Then O sistema exibe mensagem de sucesso
      | mensagem | "Cadastro realizado com sucesso." |
    And O usuário pode logar com o e‑mail <email> e senha <senha>

    Examples:
      | nome           | email                | telefone      | cep     | endereco        | senha   |
      | João Silva     | joao.silva@email.com | 11987654321   | 01001000| Av. Central, 10 | Pass123 |
      | Maria Costa    | maria.costa@email.com| 11912345678   | 02002000| Rua das Flores,5| Pass456 |

  Scenario Outline: Cadastro inválido – campos obrigatórios em branco
    Given O usuário acessa a página de cadastro
    When Preenche os campos com
      | campo          | valor |
      | Nome           | <nome>|
      | Email          | <email>|
      | Telefone       | <telefone>|
      | CEP            | <cep>|
      | Endereço       | <endereco>|
      | Senha          | <senha>|
      | Confirmação    | <confirmação>|
    And Clica em "Cadastrar"
    Then O sistema exibe mensagem de erro
      | campo | mensagem                                           |
      | Nome  | "Nome é obrigatório."                             |
      | Email | "E‑mail é obrigatório."                           |
      | Telefone | "Telefone é obrigatório."                     |
      | CEP | "CEP é obrigatório."                               |
      | Endereço | "Endereço é obrigatório."                         |
      | Senha | "Senha é obrigatória."                            |
      | Confirmação | "Confirmação de senha é obrigatória."      |

    Examples:
      | nome | email | telefone | cep | endereco | senha | confirma |
      |      |       |          |     |          |       |          |

  Scenario Outline: Cadastro inválido – dados com formato incorreto
    Given O usuário acessa a página de cadastro
    When Preenche os campos com
      | campo          | valor |
      | Nome           | João  |
      | Email          | <email>|
      | Telefone       | <telefone>|
      | CEP            | <cep>|
      | Endereço       | Rua A |
      | Senha          | Pass123|
      | Confirmação    | Pass123|
    And Clica em "Cadastrar"
    Then O sistema exibe mensagem de erro
      | campo | mensagem                                           |
      | Email | <mensagem_email>                                  |
      | Telefone | <mensagem_telefone>                            |
      | CEP | <mensagem_cep>                                    |

    Examples:
      | email            | telefone      | cep     | mensagem_email        | mensagem_telefone      | mensagem_cep        |
      | joao[dot]silva   | 1234          | 12345   | "E‑mail inválido."    | "Telefone inválido."   | "CEP inválido."    |
      | joao.silva@email | (12)3456789   | 01001-000 | "E‑mail inválido."  | "Telefone inválido."   | "CEP inválido."    |
```

---

## 2️⃣ Login

```gherkin
Feature: Login

  Como cliente cadastrado
  Quero entrar no sistema
  Para visualizar minha conta

  Scenario: Login bem‑sucedido
    Given O usuário está na página de login
    When Preenche os campos com
      | campo | valor            |
      | Email | joao.silva@email.com |
      | Senha | Pass123          |
    And Clica em "Entrar"
    Then O sistema redireciona para a página inicial da conta
    And Exibe mensagem de boas‑vindas
      | mensagem | "Bem-vindo, João Silva!" |

  Scenario Outline: Login falha – credenciais inválidas
    Given O usuário está na página de login
    When Preenche os campos com
      | campo | valor |
      | Email | <email> |
      | Senha | <senha> |
    And Clica em "Entrar"
    Then O sistema exibe mensagem de erro
      | mensagem | <mensagem> |

    Examples:
      | email                | senha   | mensagem                |
      | joao.silva@email.com | Wrong!  | "Senha inválida."       |
      | unknown@email.com    | Pass123 | "E‑mail não cadastrado."|

  Scenario: Login falha – campo em branco
    Given O usuário está na página de login
    When Preenche os campos com
      | campo | valor |
      | Email |        |
      | Senha |        |
    And Clica em "Entrar"
    Then O sistema exibe mensagem de erro
      | mensagem | "E‑mail e senha são obrigatórios." |
```

---

## 3️⃣ Acesso à aplicação bancária – Saldo e Extrato

```gherkin
Feature: Acesso à aplicação bancária

  Como cliente logado
  Quero visualizar saldo e extrato
  Para acompanhar meu dinheiro

  Scenario: Exibir saldo atualizado
    Given O usuário está na página inicial da conta
    When O usuário visualiza o saldo
    Then O sistema exibe saldo atual
      | saldo | R$ 1.250,00 |

  Scenario: Exibir extrato em ordem cronológica
    Given O usuário está na página do extrato
    When O usuário visualiza as transações
    Then O extrato lista as transações mais recentes primeiro
      | data        | descrição         | valor     |
      | 2025‑09‑29 | Transferência DE  | -R$ 200,00|
      | 2025‑09‑25 | Depósito          | +R$ 1.000,00|

  Scenario: Saldo reflete operação de transferência
    Given O usuário fez uma transferência de R$ 300,00
    And O usuário acessa a página inicial da conta
    Then O saldo deve refletir a dedução
      | saldo | R$ 950,00 |
```

---

## 4️⃣ Transferência de Fundos

```gherkin
Feature: Transferência de Fundos

  Como cliente logado
  Quero transferir dinheiro entre contas
  Para gerenciar meus recursos

  Scenario Outline: Transferência bem‑sucedida
    Given O usuário está na página de transferência
    When Seleciona conta origem "<conta_origem>"
    And Seleciona conta destino "<conta_destino>"
    And Preenche valor "<valor>"
    And Clica em "Transferir"
    Then O sistema exibe mensagem de sucesso
      | mensagem | "Transferência concluída com sucesso." |
    And O valor é debitado da conta origem
    And O valor é creditado na conta destino
    And A transação aparece no histórico de ambas as contas

    Examples:
      | conta_origem | conta_destino | valor |
      | 1001         | 2002          | 500   |
      | 1001         | 2003          | 250   |

  Scenario: Transferência falha – valor superior ao saldo
    Given O usuário está na página de transferência
    And O saldo da conta origem é R$ 400,00
    When Seleciona conta origem "1001"
    And Seleciona conta destino "2002"
    And Preenche valor "600"
    And Clica em "Transferir"
    Then O sistema exibe mensagem de erro
      | mensagem | "Saldo insuficiente para essa transferência." |

  Scenario: Transferência falha – valor negativo ou zero
    Given O usuário está na página de transferência
    When Seleciona conta origem "1001"
    And Seleciona conta destino "2002"
    And Preenche valor "-100"
    And Clica em "Transferir"
    Then O sistema exibe mensagem de erro
      | mensagem | "O valor da transferência deve ser positivo." |
```

---

## 5️⃣ Solicitação de Empréstimo

```gherkin
Feature: Solicitação de Empréstimo

  Como cliente logado
  Quero solicitar um empréstimo
  Para aumentar meu capital de trabalho

  Scenario Outline: Empréstimo aprovado
    Given O usuário está na página de solicitação de empréstimo
    When Preenche valor do empréstimo "<valor_emprestimo>"
    And Preenche renda anual "<renda_anual>"
    And Clica em "Solicitar"
    Then O sistema retorna status "<status>"
    And Exibe mensagem clara
      | mensagem | <mensagem> |

    Examples:
      | valor_emprestimo | renda_anual | status   | mensagem                                       |
      | 10000            | 40000       | Aprovado | "Parabéns! Seu empréstimo foi aprovado."        |
      | 50000            | 30000       | Negado   | "Desculpe, seu pedido foi negado."             |

  Scenario: Empréstimo com dados inválidos
    Given O usuário está na página de solicitação de empréstimo
    When Preenche valor do empréstimo "-5000"
    And Preenche renda anual "0"
    And Clica em "Solicitar"
    Then O sistema exibe mensagens de erro
      | campo          | mensagem                              |
      | valor do empréstimo | "Valor do empréstimo deve ser positivo." |
      | renda anual    | "Renda anual deve ser maior que zero."   |
```

---

## 6️⃣ Pagamento de Contas

```gherkin
Feature: Pagamento de Contas

  Como cliente logado
  Quero registrar pagamentos
  Para manter meus compromissos em dia

  Scenario Outline: Pagamento futuro agendado
    Given O usuário está na página de pagamento de contas
    When Preenche dados do pagamento com
      | beneficiário | endereço   | cidade  | estado | cep       | telefone    | conta destino | valor | data          |
      | <beneficiario>| <endereco> | <cidade>| <estado>| <cep>    | <telefone> | <conta>     | <valor> | <data>     |
    And Clica em "Confirmar"
    Then O sistema exibe mensagem de confirmação
      | mensagem | "Pagamento agendado com sucesso." |
    And O pagamento aparece no histórico
      | data          | beneficiário | valor   |
      | <data>        | <beneficiario>| +R$ <valor> |

    Examples:
      | beneficiario | endereco           | cidade | estado | cep       | telefone   | conta | valor | data        |
      | Água          | Av. das Águas, 5  | São Paulo | SP | 01001-000 | 11987654321 | 3001 | 150 | 2025‑10‑15 |

  Scenario: Pagamento imediato – valor negativo
    Given O usuário está na página de pagamento de contas
    When Preenche dados do pagamento com valor "-200"
    And Clica em "Confirmar"
    Then O sistema exibe mensagem de erro
      | mensagem | "O valor deve ser positivo." |

  Scenario: Pagamento com data passada
    Given O usuário está na página de pagamento de contas
    When Preenche dados do pagamento com data "2025‑01‑01"
    And Clica em "Confirmar"
    Then O sistema exibe mensagem de erro
      | mensagem | "Data de pagamento não pode ser anterior a hoje." |
```

---

## 7️⃣ Requisitos Gerais – Navegação e Usabilidade

```gherkin
Feature: Requisitos Gerais de Navegação e Usabilidade

  Como usuário do sistema
  Quero que a interface seja consistente
  Para navegar sem confusão

  Scenario: Todas as páginas carregam sem erros
    Given O usuário acessa cada página do sistema (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento, Extrato)
    Then Cada página deve carregar corretamente
      | página    | status |
      | Login     | 200 OK |
      | Cadastro  | 200 OK |
      | Conta     | 200 OK |
      | Transferência | 200 OK |
      | Empréstimo | 200 OK |
      | Pagamento | 200 OK |
      | Extrato   | 200 OK |

  Scenario: Mensagens de erro são claras
    Given O usuário tenta executar uma operação inválida
    When O sistema retorna erro
    Then O usuário deve ver
      | mensagem | "Erro: <descrição do erro>" |
      | contexto | "Por favor, verifique os dados." |

  Scenario: Links e menus são consistentes
    Given O usuário está em qualquer página
    Then Todos os menus de navegação (Topo, Lateral) contêm os mesmos itens
      | item          |
      | Conta         |
      | Transferências|
      | Empréstimos   |
      | Pagamentos    |
      | Extrato       |
      | Logout        |
```

---

### Observações

* Os cenários foram escritos com foco em **comportamento** – descrevendo *o que acontece* e *o que o usuário espera*, não em detalhes de implementação.  
* Para garantir cobertura, cada regra de negócio possui pelo menos um cenário **positiva** e um cenário **negativa** (erro).  
* Usei `Scenario Outline` nos casos onde o mesmo fluxo deve ser testado com diferentes valores.  
* Mensagens de erro e confirmações foram incluídas de forma a permitir validações automatizadas e garantir clareza para o usuário final.

Pronto! Se precisar de mais detalhes ou de cenários adicionais (por exemplo, testes de performance ou segurança), é só avisar.