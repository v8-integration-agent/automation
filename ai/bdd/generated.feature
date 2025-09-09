```gherkin
# language: pt
# ==============================================================
# ParaBank – Cenários Gherkin de Aceleração
# ==============================================================

# ===========================
# 3.1 Cadastro de Usuário
# ===========================
Funcionalidade: Cadastro de Usuário
  Como usuário novo
  Quero registrar meus dados
  Para ter acesso ao ParaBank

  Cenário: Cadastro bem-sucedido
    Dado que o usuário está na página de registro
    Quando preencher todos os campos obrigatórios com valores válidos
    E clicar em “Cadastrar”
    Então o sistema deve exibir mensagem de confirmação
    E o usuário deve ser redirecionado para a página de login

  Cenário: Erro ao inserir dados inválidos
    Dado que o usuário está na página de registro
    Quando preencher o campo telefone com “abc123”
    E preencher o campo CEP com “123”
    E preencher o campo e‑mail com “usuario”
    E clicar em “Cadastrar”
    Então o sistema deve exibir mensagem de erro: “Telefone inválido”
    E o sistema deve exibir mensagem de erro: “CEP inválido”
    E o sistema deve exibir mensagem de erro: “E‑mail inválido”

  Cenário: Campo obrigatório vazio
    Dado que o usuário está na página de registro
    Quando deixar o campo “Nome” vazio
    E clicar em “Cadastrar”
    Então o sistema deve exibir mensagem de erro: “Nome é obrigatório”

# ===========================
# 3.2 Login
# ===========================
Funcionalidade: Login
  Como usuário cadastrado
  Quero acessar minha conta
  Para visualizar saldo e realizar transações

  Cenário: Login bem-sucedido
    Dado que o usuário está na página de login
    Quando digitar “usuario@parabank.com” no campo usuário
    E digitar “senhaSegura123” no campo senha
    E clicar em “Login”
    Então o sistema deve redirecionar para a página inicial da conta
    E exibir saudação “Bem‑vindo, Usuário”

  Cenário: Login com credenciais inválidas
    Dado que o usuário está na página de login
    Quando digitar “usuario@parabank.com” no campo usuário
    E digitar “senhaErrada” no campo senha
    E clicar em “Login”
    Então o sistema deve exibir mensagem de erro: “Usuário ou senha inválidos”

# ===========================
# 3.3 Acesso à Conta (Saldo e Extrato)
# ===========================
Funcionalidade: Acesso à Conta
  Como usuário logado
  Quero ver o saldo e extrato
  Para monitorar minhas finanças

  Cenário: Visualizar saldo atualizado
    Dado que o usuário está na página inicial da conta
    Quando o sistema exibe o saldo da conta
    Então o saldo exibido deve refletir todas as transações realizadas

  Cenário: Lista de extrato em ordem cronológica
    Dado que o usuário está na página de extrato
    Quando o sistema exibe a lista de transações
    Então as transações devem estar ordenadas da mais recente para a mais antiga

# ===========================
# 3.4 Transferência de Fundos
# ===========================
Funcionalidade: Transferência de Fundos
  Como usuário
  Quero transferir dinheiro de uma conta para outra
  Para gerenciar meus recursos

  Cenário: Transferência bem‑sucedida
    Dado que o usuário tem saldo de R$ 1.000 na conta corrente
    Quando selecionar conta origem “Corrente”
    E selecionar conta destino “Poupança”
    E inserir valor “R$ 200”
    E confirmar a transferência
    Então o saldo da conta origem deve diminuir para R$ 800
    E o saldo da conta destino deve aumentar para R$ 200
    E ambas as contas devem registrar a transação no histórico

  Cenário: Transferência com valor superior ao saldo disponível
    Dado que o usuário tem saldo de R$ 300 na conta corrente
    Quando selecionar conta origem “Corrente”
    E selecionar conta destino “Poupança”
    E inserir valor “R$ 400”
    E tentar confirmar a transferência
    Então o sistema deve exibir mensagem de erro: “Saldo insuficiente”

  Cenário: Transferência para conta inexistente
    Dado que o usuário tem saldo de R$ 500 na conta corrente
    Quando selecionar conta origem “Corrente”
    E selecionar conta destino “ContaX” (não existente)
    E inserir valor “R$ 100”
    E tentar confirmar a transferência
    Então o sistema deve exibir mensagem de erro: “Conta de destino não encontrada”

# ===========================
# 3.5 Solicitação de Empréstimo
# ===========================
Funcionalidade: Solicitação de Empréstimo
  Como usuário
  Quero solicitar um empréstimo
  Para financiar meus projetos

  Cenário: Empréstimo aprovado
    Dado que o usuário informa valor R$ 5.000 e renda anual R$ 120.000
    Quando submeter a solicitação
    Então o sistema deve retornar status “Aprovado”
    E exibir mensagem: “Parabéns! Seu empréstimo foi aprovado”

  Cenário: Empréstimo negado por renda insuficiente
    Dado que o usuário informa valor R$ 5.000 e renda anual R$ 30.000
    Quando submeter a solicitação
    Então o sistema deve retornar status “Negado”
    E exibir mensagem: “Desculpe, seu empréstimo foi negado”

# ===========================
# 3.6 Pagamento de Contas
# ===========================
Funcionalidade: Pagamento de Contas
  Como usuário
  Quero registrar pagamentos de contas
  Para manter meus compromissos em dia

  Cenário: Pagamento imediato
    Dado que o usuário preenche beneficiário “Conta de Luz”
    E endereço “Rua das Flores 123”
    E cidade “São Paulo”
    E estado “SP”
    E CEP “01001-000”
    E telefone “(11) 98765-4321”
    E conta de destino “Corrente”
    E valor “R$ 150”
    E data “2025‑09‑15”
    Quando confirmar o pagamento
    Então o pagamento deve aparecer no histórico de transações
    E o saldo da conta de destino deve ser debitado em R$ 150

  Cenário: Pagamento agendado para data futura
    Dado que o usuário preenche todos os campos com data “2025‑10‑01”
    Quando confirmar o pagamento
    Então o pagamento deve ser incluído no histórico com status “Agendado”
    E o sistema deve notificar o usuário no dia 2025‑10‑01

  Cenário: Erro em campo obrigatório vazio
    Dado que o usuário deixa o campo “Beneficiário” vazio
    Quando tentar confirmar o pagamento
    Então o sistema deve exibir mensagem de erro: “Beneficiário é obrigatório”

# ===========================
# 3.7 Requisitos Gerais
# ===========================
Funcionalidade: Navegação e Usabilidade
  Como usuário
  Quero navegar sem erros
  Para ter experiência fluida

  Cenário: Carregamento de todas as páginas sem erros
    Dado que o usuário acessa cada página do sistema (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
    Quando cada página carrega
    Então nenhuma página deve exibir erros de carregamento

  Cenário: Consistência de links e menus
    Dado que o usuário está em qualquer página
    Quando visualizar o menu principal
    Então todos os links (Login, Conta, Transferência, Empréstimo, Pagamento, Sair) devem estar visíveis e funcionar

  Cenário: Mensagens de erro claras e objetivas
    Dado que o usuário tenta enviar um formulário inválido
    Quando submeter o formulário
    Então o sistema deve exibir mensagens de erro em português, com texto claro e sem jargões técnicos
```

> **Obs.**  
> Cada cenário cobre um requisito de aceitação principal, incluindo casos de sucesso e falhas.  
> Utilize o formato Gherkin em português para facilitar a leitura por equipes de desenvolvimento e testes.