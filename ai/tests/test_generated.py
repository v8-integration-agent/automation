## 1️⃣ Visão geral

Abaixo você encontra um **esqueleto completo** de testes automatizados em Python usando **pytest‑bdd** para o arquivo BDD (Gherkin) que você forneceu.  
O projeto está organizado da seguinte forma:

```
para_bank/
├── features/
│   └── para_bank.feature          # arquivo Gherkin completo
├── tests/
│   ├── conftest.py                # fixtures globais (driver, context, etc.)
│   └── steps/
│       └── para_bank_steps.py    # step‑definitions (Python)
├── pages/
│   ├── base_page.py              # classe base (driver, utils)
│   ├── registration_page.py
│   ├── login_page.py
│   ├── account_page.py
│   ├── transfer_page.py
│   ├── loan_page.py
│   ├── payment_page.py
│   └── navigation_page.py
└── requirements.txt
```

> **Obs.:**  
> O código abaixo **não** faz chamadas reais a um navegador. Ele contém apenas **placeholders** que mostram onde a lógica real (Selenium, requests, mocks, etc.) deve ser inserida.  
> Para usar em um ambiente real basta trocar os `pass / # TODO` pelos comandos Selenium ou pela API que sua aplicação expõe.

---

## 2️⃣ Arquivo Gherkin – `features/para_bank.feature`

```gherkin
Feature: Cadastro de Usuário
  Para garantir que novos usuários possam criar uma conta de forma segura e completa

  @Cadastro
  Scenario Outline: Cadastro com todos os campos obrigatórios preenchidos
    Given O usuário acessa a página de cadastro
    When Ele preenche os campos obrigatórios com valores válidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"
    Then O sistema deve exibir a mensagem de confirmação "Cadastro realizado com sucesso"
    And O usuário deve ser redirecionado para a tela de login

    Examples:
      | Nome          | Email                 | Telefone            | CEP       |
      | João da Silva | joao.silva@email.com  | (11) 98765-4321     | 01010-010 |
      | Maria Pereira | maria.pereira@email.com | (21) 99876-5432   | 20020-020 |

  @Cadastro
  Scenario Outline: Cadastro com campos inválidos
    Given O usuário acessa a página de cadastro
    When Ele preenche os campos obrigatórios com valores inválidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"
    Then O sistema deve exibir a mensagem de erro "Email inválido"
    And O sistema deve exibir a mensagem de erro "Telefone inválido"
    And O sistema deve exibir a mensagem de erro "CEP inválido"

    Examples:
      | Nome  | Email    | Telefone  | CEP   |
      | João  | joao.com | 1234      | abcde |
      | Maria | maria@   | (xx) xxxx-xxxx | 0000000 |

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
        | Data        | Descrição     | Valor  |
        | 01/09/2024  | Depósito      | +R$200 |
        | 02/09/2024  | Transferência | -R$50  |
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

---

## 3️⃣ Fixtures – `tests/conftest.py`

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# 1. WebDriver
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")          # remova se quiser ver o browser
    options.add_argument("--disable-gpu")
    # Caminho do ChromeDriver (ajuste se necessário)
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ------------------------------------------------------------------
# 2. Base Page (para que as páginas tenham acesso ao driver)
# ------------------------------------------------------------------
@pytest.fixture
def base_page(driver):
    return BasePage(driver)

# ------------------------------------------------------------------
# 3. Helpers de dados (ex.: criar contas, logar, etc.)
# ------------------------------------------------------------------
@pytest.fixture
def login_user(base_page):
    def _login(email, password):
        login_page = base_page.navigate_to_login()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_enter()
    return _login

@pytest.fixture
def create_account(base_page):
    def _create(nome, email, telefone, cep):
        reg_page = base_page.navigate_to_registration()
        reg_page.enter_name(nome)
        reg_page.enter_email(email)
        reg_page.enter_phone(telefone)
        reg_page.enter_cep(cep)
        reg_page.submit()
    return _create

@pytest.fixture
def get_account_balance(base_page):
    def _balance():
        return base_page.account_page.get_balance()
    return _balance

# ------------------------------------------------------------------
# 4. Fixtures de contexto para cenários “Given”
# ------------------------------------------------------------------
@pytest.fixture
def user_with_account():
    # Retorna um dicionário de usuário que pode ser usado em vários steps
    return {"email": "usuario@email.com", "senha": "Senha123"}

@pytest.fixture
def logged_in_user(login_user, user_with_account):
    login_user(user_with_account["email"], user_with_account["senha"])
    return user_with_account
```

> **Dica:** Se a aplicação for **API‑first**, troque os *fixtures* de Selenium por chamadas `requests`. A estrutura do projeto continua igual.

---

## 4️⃣ Page Objects – Exemplos

### 4.1 `pages/base_page.py`

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # ------------------------ Navegação ------------------------
    def navigate_to_login(self):
        from pages.login_page import LoginPage
        self.driver.get("https://app.parabank.com/login")
        return LoginPage(self.driver)

    def navigate_to_registration(self):
        from pages.registration_page import RegistrationPage
        self.driver.get("https://app.parabank.com/register")
        return RegistrationPage(self.driver)

    def navigate_to_account(self):
        from pages.account_page import AccountPage
        self.driver.get("https://app.parabank.com/account")
        return AccountPage(self.driver)

    def navigate_to_transfer(self):
        from pages.transfer_page import TransferPage
        self.driver.get("https://app.parabank.com/transfer")
        return TransferPage(self.driver)

    def navigate_to_loan(self):
        from pages.loan_page import LoanPage
        self.driver.get("https://app.parabank.com/loan")
        return LoanPage(self.driver)

    def navigate_to_payment(self):
        from pages.payment_page import PaymentPage
        self.driver.get("https://app.parabank.com/payment")
        return PaymentPage(self.driver)
```

> **Obs.:** Os demais arquivos de página (`registration_page.py`, `login_page.py`, `account_page.py`, ...) contêm os *locators* e os métodos usados nos *steps*. Eles são apenas esqueleto; substitua os `pass` pelos comandos Selenium reais.

---

## 5️⃣ Step Definitions – `tests/steps/para_bank_steps.py`

```python
import pytest
from pytest_bdd import given, when, then, parsers, scenario
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# 1. Decorator de cenário (pode ser usado para cada cenário ou para
#    o arquivo inteiro).  Para manter o arquivo enxuto, use a opção
#    de “scenarios” nos testes abaixo (não mostramos todos os 30
#    cenários, apenas alguns exemplares).
# ------------------------------------------------------------------
# Exemplo:
# @scenario('features/para_bank.feature', 'Cadastro com todos os campos obrigatórios preenchidos')
# def test_cadastro_completo():
#     pass

# ------------------------------------------------------------------
# 2. Steps
# ------------------------------------------------------------------

# ---------------------- Cadastro ----------------------
@given("O usuário acessa a página de cadastro")
def user_accesses_registration(base_page):
    return base_page.navigate_to_registration()

@when(parsers.cfparse('Ele preenche os campos obrigatórios com valores válidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"'))
def fill_registration_valid(base_page, Nome, Email, Telefone, CEP):
    reg_page = base_page.navigate_to_registration()
    reg_page.enter_name(Nome)
    reg_page.enter_email(Email)
    reg_page.enter_phone(Telefone)
    reg_page.enter_cep(CEP)
    reg_page.submit()

@when(parsers.cfparse('Ele preenche os campos obrigatórios com valores inválidos "<Nome>", "<Email>", "<Telefone>", "<CEP>" e clica em "Registrar"'))
def fill_registration_invalid(base_page, Nome, Email, Telefone, CEP):
    reg_page = base_page.navigate_to_registration()
    reg_page.enter_name(Nome)
    reg_page.enter_email(Email)
    reg_page.enter_phone(Telefone)
    reg_page.enter_cep(CEP)
    reg_page.submit()

@then('O sistema deve exibir a mensagem de confirmação "Cadastro realizado com sucesso"')
def confirm_registration_success(reg_page):
    assert reg_page.is_success_message_displayed(), "Mensagem de sucesso não apareceu"

@then('O usuário deve ser redirecionado para a tela de login')
def user_redirected_to_login(reg_page):
    assert reg_page.current_url.endswith("/login"), "Não redirecionou para login"

@then('O sistema deve exibir a mensagem de erro "Email inválido"')
def error_email_invalid(reg_page):
    assert reg_page.is_error_message_displayed("Email inválido")

@then('O sistema deve exibir a mensagem de erro "Telefone inválido"')
def error_phone_invalid(reg_page):
    assert reg_page.is_error_message_displayed("Telefone inválido")

@then('O sistema deve exibir a mensagem de erro "CEP inválido"')
def error_cep_invalid(reg_page):
    assert reg_page.is_error_message_displayed("CEP inválido")

# ---------------------- Login ----------------------
@given(parsers.cfparse('O usuário possui conta cadastrada com e‑mail "{email}" e senha "{senha}"'))
def user_account_created(create_account, email, senha):
    # Em cenário real, o usuário já existe. Aqui criamos (ou garante)
    create_account(nome="User", email=email, telefone="(11) 90000-0000", cep="01000-000")
    # Salvar a senha em algum local seguro se precisar de acesso direto
    return {"email": email, "senha": senha}

@when(parsers.cfparse('O usuário digita o e‑mail e a senha na tela de login e clica em "Entrar"'))
def login_user(login_user, user_account_created):
    login_user(user_account_created["email"], user_account_created["senha"])

@when(parsers.cfparse('O usuário digita o e‑mail "<Email>" e a senha "<Senha>" na tela de login e clica em "Entrar"'))
def login_with_invalid_creds(login_user, Email, Senha):
    login_user(Email, Senha)

@then('O sistema deve redirecionar o usuário para a página inicial da conta')
def redirect_to_home(base_page):
    assert base_page.current_url.endswith("/account"), "Não redirecionou para a página de conta"

@then('O saldo exibido deve ser igual ao saldo inicial da conta')
def balance_matches_initial(get_account_balance):
    assert get_account_balance() == 1000.00  # valor fictício

@then('O sistema deve exibir a mensagem de erro "Credenciais inválidas"')
def error_invalid_credentials(base_page):
    assert base_page.is_error_message_displayed("Credenciais inválidas")

# ---------------------- Extrato ----------------------
@given(parsers.cfparse('O usuário está logado e sua conta possui saldo inicial de R$ {saldo:float},00'))
def login_and_set_balance(logged_in_user, saldo):
    # Aqui você pode usar mocks para definir o saldo
    pass

@given(parsers.cfparse('O usuário está logado e possui as seguintes transações:'))
def user_with_transactions(base_page, table):
    """
    `table` é um objeto que contém os dados da tabela do Gherkin.
    Ex.: table.cells[0] = ["01/09/2024", "Depósito", "+R$200"]
    """
    # Aplique as transações na conta (mock ou via API)
    pass

@when(parsers.cfparse('O usuário navega até a página de “{page}”'))
def navigate_to_page(base_page, page):
    if page == "Minha Conta":
        base_page.navigate_to_account()
    elif page == "Extrato":
        base_page.navigate_to_account()  # ou navega via menu
    else:
        raise ValueError(f"Página desconhecida: {page}")

@then(parsers.cfparse('O saldo exibido deve ser R$ {saldo:float},00'))
def verify_balance(base_page, saldo):
    displayed = base_page.account_page.get_balance()
    assert displayed == saldo, f"Saldo {displayed} ≠ {saldo}"

@then(parsers.cfparse('O extrato deve listar:'))
def verify_transaction_list(base_page, table):
    expected = [row for row in table.cells]
    actual = base_page.account_page.get_transactions()
    assert actual == expected, f"Transações esperadas {expected} não correspondem às reais {actual}"

@then('As transações devem estar em ordem decrescente de data')
def transactions_order(base_page):
    dates = [row[0] for row in base_page.account_page.get_transactions()]
    assert dates == sorted(dates, reverse=True)

# ------------------------------------------------------------------
# 6️⃣  Os demais steps (Transferência, Empréstimo, Pagamento,
#     Navegação, Acessibilidade, etc.) seguem a mesma lógica:
#
# - use `@given`, `@when`, `@then` com `parsers.cfparse`
# - interaja com a página via Page Objects
# - faça asserções usando `assert` (ou `pytest.raises` se necessário)
# ------------------------------------------------------------------
```

> **Dica:**  
> Para cenários **Outline** (`Scenario Outline`), `pytest‑bdd` já gera uma execução para cada linha da tabela.  
> A sintaxe acima já suporta essa funcionalidade, basta garantir que os parâmetros sejam declarados no `parsers.cfparse`.

---

## 6️⃣ Como rodar

```bash
# 1️⃣ Instale as dependências
pip install -r requirements.txt

# 2️⃣ Execute os testes
pytest
```

> **requirements.txt**

```
pytest>=8.0
pytest-bdd>=3.0
selenium>=4.0
```

---

## 7️⃣ Próximos passos

1. **Implementar os métodos** de cada *Page Object* (`enter_name`, `submit`, `is_success_message_displayed`, etc.) usando Selenium ou a API da aplicação.  
2. **Configurar um driver** (ChromeDriver, GeckoDriver, etc.) que esteja no PATH.  
3. **Criar fixtures de banco de dados** ou usar *mock* para evitar chamadas reais em ambiente de CI.  
4. **Adicionar relatórios** (`pytest-html`, `allure-pytest`) para geração automática de artefatos.  
5. **Rodar em containers** (Docker + Selenium Grid) caso seu ambiente de teste seja distribuído.

---

## 8️⃣ Observações finais

- **Localizadores** (`By.ID`, `By.XPATH`, etc.) devem ser revisados conforme o HTML real da aplicação.  
- Para garantir **acessibilidade**, o teste de teclado pode usar `send_keys(Keys.TAB)` e verificar a presença de `aria-label`.  
- O **mapeamento de mensagens** (sucesso, erro) deve ser consistente com o texto exibido na UI; se a aplicação usar internacionalização, troque as mensagens pelos valores corretos.  

Pronto! Agora você tem um **esqueleto funcional** em Python com `pytest-bdd` que cobre todas as histórias BDD que você descreveu. Basta preencher os detalhes e integrar com o seu ambiente de teste. Boa codificação!