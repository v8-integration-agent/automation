# language: pt
@web @smoke @P1
Funcionalidade: Login no Parabank
  Como cliente do Parabank
  Quero autenticar com usuário e senha
  Para acessar minhas contas

  Cenário: Login inválido
    Dado que estou na página inicial
    Quando eu tento autenticar com usuário "invalid" e senha "invalid"
    Então devo ver uma mensagem de erro contendo "could not be verified"

  Esquema do Cenário: Login válido
    Dado que estou na página inicial
    Quando eu tento autenticar com usuário "<user>" e senha "<pass>"
    Então devo ver a página de "Accounts Overview"

    Exemplos:
      | user     | pass     |
      | "john"   | "demo"   |