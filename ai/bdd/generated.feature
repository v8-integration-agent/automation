**Feature: Cadastro de Usuário (ParaBank)**  
*Como* usuário do ParaBank  
*Quero* criar uma conta  
*Para que* eu possa utilizar os serviços bancários.

```
Scenario: Cadastro de usuário com todos os campos obrigatórios preenchidos
  Given que eu estou na página de cadastro
  When eu preencho todos os campos obrigatórios com valores válidos
    | Campo        | Valor                   |
    | Nome         | João Silva              |
    | Endereço     | Rua A, 123              |
    | Cidade       | São Paulo               |
    | Estado       | SP                      |
    | CEP          | 01234-567                |
    | Telefone     | (11) 98765-4321          |
    | Email        | joao.silva@example.com  |
    | Senha        | SenhaSegura123!         |
  And eu clico em “Criar Conta”
  Then devo ver a mensagem de confirmação “Registro concluído com sucesso”
  And devo poder acessar a tela de login

Scenario: Cadastro de usuário com telefone inválido
  Given que eu estou na página de cadastro
  When eu preencho todos os campos obrigatórios
    | Campo        | Valor           |
    | Nome         | Maria Pereira   |
    | Endereço     | Av B, 456       |
    | Cidade       | Rio de Janeiro  |
    | Estado       | RJ              |
    | CEP          | 12345-678        |
    | Telefone     | 123abc          |
    | Email        | maria@exemplo.com |
    | Senha        | Senha1234!      |
  And eu clico em “Criar Conta”
  Then devo ver a mensagem de erro “Telefone inválido, por favor insira apenas números”

Scenario: Cadastro de usuário com CEP inválido
  Given que eu estou na página de cadastro
  When eu preencho todos os campos obrigatórios
    | Campo        | Valor            |
    | Nome         | Carlos Lima      |
    | Endereço     | Rua C, 789       |
    | Cidade       | Belo Horizonte   |
    | Estado       | MG              |
    | CEP          | ABCDEFG          |
    | Telefone     | (31) 99876-5432  |
    | Email        | carlos@exemplo.com|
    | Senha        | Senha123!        |
  And eu clico em “Criar Conta”
  Then devo ver a mensagem de erro “CEP inválido, insira 8 dígitos numéricos”

Scenario: Cadastro de usuário com e‑mail inválido
  Given que eu estou na página de cadastro
  When eu preencho todos os campos obrigatórios
    | Campo        | Valor              |
    | Nome         | Ana Oliveira      |
    | Endereço     | Praça D, 101      |
    | Cidade       | Curitiba          |
    | Estado       | PR                |
    | CEP          | 12345-678          |
    | Telefone     | (41) 98765-4321    |
    | Email        | ana-oliverasexemplo |
    | Senha        | Senha123!         |
  And eu clico em “Criar Conta”
  Then devo ver a mensagem de erro “E‑mail inválido, por favor insira um e‑mail válido”
```

---

**Feature: Login (ParaBank)**  
*Como* usuário registrado  
*Quero* entrar no sistema  
*Para que* eu possa visualizar minha conta.

```
Scenario: Login com credenciais válidas
  Given que eu estou na página de login
  When eu informo meu e‑mail “joao.silva@example.com” e senha “SenhaSegura123!”
  And eu clico em “Entrar”
  Then devo ser redirecionado para a página inicial da minha conta
  And devo ver o cabeçalho “Bem‑vindo, João”

Scenario: Login com credenciais inválidas – e‑mail não cadastrado
  Given que eu estou na página de login
  When eu informo o e‑mail “desconhecido@exemplo.com” e senha “senha”
  And eu clico em “Entrar”
  Then devo ver a mensagem de erro “E‑mail ou senha inválidos”

Scenario: Login com credenciais inválidas – senha incorreta
  Given que eu estou na página de login
  When eu informo o e‑mail “joao.silva@example.com” e senha “senhaErrada”
  And eu clico em “Entrar”
  Then devo ver a mensagem de erro “E‑mail ou senha inválidos”
```

---

**Feature: Exibição de Saldo e Extrato (ParaBank)**  
*Como* usuário logado  
*Quero* ver meu saldo atualizado  
*Para que* eu possa acompanhar minhas finanças.

```
Scenario: Exibição de saldo após operação de depósito
  Given que eu estou na página inicial da minha conta
  And meu saldo atual é R$ 1.000,00
  When eu realizo um depósito de R$ 500,00
  Then o saldo exibido deve ser R$ 1.500,00

Scenario: Lista do extrato em ordem cronológica
  Given que eu estou na página de extrato
  And existem as seguintes transações
    | Data       | Descrição         | Valor   |
    | 01/10/2024 | Saldo Inicial     | R$ 1.000,00 |
    | 02/10/2024 | Depósito          | R$ 500,00   |
    | 05/10/2024 | Transferência     | -R$ 200,00  |
  When eu carrego a página de extrato
  Then as transações devem ser exibidas em ordem do mais recente ao mais antigo
  And a primeira linha deve mostrar “05/10/2024 – Transferência – -R$ 200,00”
```

---

**Feature: Transferência de Fundos (ParaBank)**  
*Como* usuário logado  
*Quero* transferir dinheiro entre contas  
*Para que* eu possa movimentar meus recursos.

```
Scenario: Transferência válida entre contas
  Given que eu estou na página de transferência
  And minha conta de origem possui saldo R$ 1.000,00
  When eu seleciono “Conta A” como origem
  And eu seleciono “Conta B” como destino
  And eu informo o valor “200,00”
  And eu confirmo a transferência
  Then o saldo da conta de origem deve ser R$ 800,00
  And o saldo da conta de destino deve ser R$ 200,00
  And a transação deve aparecer no histórico da conta de origem
  And a transação deve aparecer no histórico da conta de destino

Scenario: Transferência com valor superior ao saldo disponível
  Given que eu estou na página de transferência
  And minha conta de origem possui saldo R$ 100,00
  When eu informo o valor “200,00”
  And eu confirmo a transferência
  Then devo ver a mensagem de erro “Saldo insuficiente para esta transferência”

Scenario: Transferência sem selecionar conta de destino
  Given que eu estou na página de transferência
  And minha conta de origem possui saldo R$ 500,00
  When eu seleciono “Conta A” como origem
  And eu deixo o campo “Conta de destino” vazio
  And eu informo o valor “50,00”
  And eu confirmo a transferência
  Then devo ver a mensagem de erro “Selecione uma conta de destino”
```

---

**Feature: Solicitação de Empréstimo (ParaBank)**  
*Como* usuário logado  
*Quero* solicitar um empréstimo  
*Para que* eu possa obter recursos adicionais.

```
Scenario: Solicitação de empréstimo aprovado
  Given que eu estou na página de solicitação de empréstimo
  And eu informo o valor “10.000,00” e renda anual “50.000,00”
  When eu envio a solicitação
  Then devo ver a mensagem “Empréstimo aprovado”
  And a mensagem deve indicar o prazo e a taxa de juros

Scenario: Solicitação de empréstimo negado
  Given que eu estou na página de solicitação de empréstimo
  And eu informo o valor “100.000,00” e renda anual “20.000,00”
  When eu envio a solicitação
  Then devo ver a mensagem “Empréstimo negado”
  And a mensagem deve indicar que a renda não atende ao requisito mínimo
```

---

**Feature: Pagamento de Contas (ParaBank)**  
*Como* usuário logado  
*Quero* cadastrar um pagamento programado  
*Para que* eu possa controlar despesas futuras.

```
Scenario: Cadastro de pagamento futuro com data futura
  Given que eu estou na página de pagamento de contas
  When eu informo
    | Beneficiário | Endereço   | Cidade      | Estado | CEP      | Telefone   | Conta de Destino | Valor | Data      |
    | Luz da Casa   | Rua E, 321 | Salvador    | BA     | 40010-000 | (71) 91234-5678 | Conta 1234   | 150,00 | 15/12/2024 |
  And eu confirmo o pagamento
  Then devo ver a mensagem “Pagamento agendado com sucesso”
  And o pagamento deve aparecer no histórico de transações com data “15/12/2024”

Scenario: Tentativa de cadastro de pagamento com data no passado
  Given que eu estou na página de pagamento de contas
  When eu informo a data “01/01/2023”
  And eu confirmo o pagamento
  Then devo ver a mensagem de erro “A data deve ser futura”

Scenario: Cadastro de pagamento sem informar telefone
  Given que eu estou na página de pagamento de contas
  When eu deixo o campo “Telefone” vazio
  And eu informo os demais dados
  And eu confirmo o pagamento
  Then devo ver a mensagem de erro “Telefone é obrigatório”
```

---

**Feature: Navegação e Usabilidade (ParaBank)**  
*Como* usuário  
*Quero* que a aplicação seja navegável sem erros  
*Para que* eu possa usar o sistema sem frustrações.

```
Scenario: Carregamento de todas as páginas sem erros
  Given que eu estou em cada página do sistema (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
  When eu navego para cada uma delas
  Then cada página deve carregar sem mensagens de erro de navegação

Scenario: Consistência de menus e links em todas as páginas
  Given que eu estou em qualquer página
  When eu verifico os menus e links de navegação
  Then todos os menus devem exibir as mesmas opções
  And os links “Sair”, “Conta”, “Transferências” devem estar presentes

Scenario: Mensagens de erro claras e objetivas
  Given que eu realizo uma ação inválida (ex.: login com senha incorreta)
  When a ação falha
  Then devo ver uma mensagem de erro que indique exatamente o problema (“E‑mail ou senha inválidos”) e como corrigi-lo
```

> **Obs.:** Cada cenário pode ser expandido com mais detalhes (pré‑condições, dados de teste, asserts) conforme a necessidade de automação. Os exemplos acima cobrem os principais critérios de aceite descritos no documento de requisitos.