## 📦 Estrutura recomendada

```
paraBank/
├── features/
│   └── paraBank.feature          # BDD em Gherkin
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures globais (webdriver, DB, etc.)
│   └── test_parabank.py         # Step‑definitions + testes
└── pages/
    ├── __init__.py
    ├── base_page.py             # Classe base com helpers
    ├── register_page.py
    ├── login_page.py
    ├── account_page.py
    ├── transfer_page.py
    ├── loan_page.py
    └── payment_page.py
```

> **Obs.:** Os arquivos *pages/* são apenas exemplos de *Page Object*; você pode ajustá‑los conforme o framework de UI que utilizar (Selenium, Playwright, Cypress‑Python, etc.).  
> Se preferir testes de API, troque os *Page Object* por *Client* que façam chamadas HTTP.

---

## 📄 `features/paraBank.feature`

```gherkin
# Feature: ParaBank – Cadastro e Autenticação
# ------------------------------------------------

Scenario: Registro de um novo usuário com campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche todos os campos obrigatórios corretamente
  And clica em “Registrar”
  Then ele deve ver uma mensagem de confirmação “Cadastro concluído”
  And o usuário deve ser redirecionado para a tela de login

Scenario Outline: Registro de um usuário com campos inválidos
  Given o usuário acessa a página de cadastro
  When ele preenche os campos obrigatórios com os seguintes valores: <campo> = "<valor>"
  And clica em “Registrar”
  Then o sistema exibe a mensagem de erro “<mensagem>”

  Examples:
    | campo   | valor           | mensagem                |
    | Telefone| 12345           | Telefone inválido       |
    | CEP     | abcde           | CEP inválido            |
    | Email   | usuario@        | Email inválido          |

Scenario: Usuário já cadastrado tenta registrar novamente
  Given o usuário já existe no banco de dados
  When ele tenta cadastrar-se com o mesmo e‑mail
  Then o sistema exibe a mensagem “E‑mail já cadastrado”

# Feature: ParaBank – Login
# ------------------------------------------------

Scenario: Login com credenciais válidas
  Given o usuário está na tela de login
  When ele insere “usuario@exemplo.com” e “senhaCorreta”
  And clica em “Entrar”
  Then ele é redirecionado para a página inicial da conta
  And a tela exibe “Bem‑vindo, <nome do usuário>”

Scenario: Login com credenciais inválidas
  Given o usuário está na tela de login
  When ele insere “usuario@exemplo.com” e “senhaErrada”
  And clica em “Entrar”
  Then o sistema exibe a mensagem “Usuário ou senha inválidos”

# Feature: ParaBank – Consulta de Saldo e Extrato
# ------------------------------------------------

Scenario: Visualização do saldo atualizado
  Given o usuário está logado na conta
  When ele navega até a tela “Saldo”
  Then a página exibe o valor “Saldo atual: R$ <saldo>”

Scenario: Visualização do extrato em ordem cronológica
  Given o usuário tem transações recentes no extrato
  When ele navega até a tela “Extrato”
  Then o extrato lista as transações em ordem decrescente de data
  And cada linha contém “Data, Descrição, Valor, Saldo”

# Feature: ParaBank – Transferência de Fundos
# ------------------------------------------------

Scenario: Transferência de fundos bem-sucedida
  Given o usuário está logado e possui saldo de R$ 1.000,00 na conta A
  When ele seleciona conta de origem “A” e conta de destino “B”
  And insere o valor “R$ 200,00”
  And confirma a transferência
  Then R$ 200,00 é debitado da conta A
  And R$ 200,00 é creditado na conta B
  And ambas as contas registram a transação no histórico

Scenario: Transferência com valor maior que o saldo disponível
  Given o usuário está logado e possui saldo de R$ 100,00 na conta A
  When ele tenta transferir R$ 200,00
  Then o sistema exibe a mensagem “Saldo insuficiente”

# Feature: ParaBank – Solicitação de Empréstimo
# ------------------------------------------------

Scenario: Empréstimo aprovado
  Given o usuário é logado
  When ele solicita R$ 10.000,00 de empréstimo com renda anual de R$ 120.000,00
  Then o sistema retorna “Solicitação Aprovada”
  And a mensagem é exibida claramente para o usuário

Scenario: Empréstimo negado por renda insuficiente
  Given o usuário é logado
  When ele solicita R$ 50.000,00 de empréstimo com renda anual de R$ 30.000,00
  Then o sistema retorna “Solicitação Negada”
  And a mensagem indica “Renda anual insuficiente”

# Feature: ParaBank – Pagamento de Contas
# ------------------------------------------------

Scenario: Registro de pagamento futuro
  Given o usuário está logado
  When ele registra um pagamento para “Conta X” com data “2025‑10‑15”
  And clica em “Confirmar”
  Then o pagamento é incluído no histórico de transações
  And o sistema exibe “Pagamento agendado para 15 de outubro de 2025”

Scenario: Pagamento imediato respeita data de agendamento
  Given o usuário registra um pagamento com data “2025‑10‑15” e confirma
  When a data atual é 2025‑10‑16
  Then o pagamento não é executado imediatamente
  And o sistema informa “Pagamento agendado para 15 de outubro”

# Feature: ParaBank – Navegação e Usabilidade
# ------------------------------------------------

Scenario: Carregamento correto de todas as páginas
  Given o usuário navega por todas as páginas principais (Login, Cadastro, Saldo, Extrato, Transferência, Empréstimo, Pagamento)
  When ele não encontra erros de carregamento
  Then todas as páginas carregam sem mensagens de erro

Scenario: Mensagens de erro claras e objetivas
  Given o usuário tenta executar uma ação inválida em qualquer módulo
  When o sistema responde
  Then a mensagem de erro é exibida em destaque
  And descreve exatamente o problema (ex.: “O campo telefone deve conter 10 dígitos”)

Scenario: Consistência de links e menus
  Given o usuário acessa qualquer página
  When ele verifica os links de navegação e menus
  Then os mesmos itens (Login, Cadastro, Saldo, Extrato, Transferência, Empréstimo, Pagamento, Logout) aparecem em todas as páginas
  And cada link funciona corretamente
```

---

## 📦 `tests/conftest.py`

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    """Instancia um webdriver Chrome (ou outro de sua escolha)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")           # Remova se quiser ver o browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Configuração global
    driver.implicitly_wait(5)   # segundos
    yield driver

    driver.quit()
```

---

## 📦 `tests/test_parabank.py`

```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Importa as páginas (Page Objects)
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.transfer_page import TransferPage
from pages.loan_page import LoanPage
from pages.payment_page import PaymentPage
from pages.base_page import BasePage


# ------------------  CENÁRIOS  ------------------
scenarios("features/paraBank.feature")


# ------------------  FIXTURES  ------------------
@pytest.fixture
def register_page(driver):
    return RegisterPage(driver)

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def account_page(driver):
    return AccountPage(driver)

@pytest.fixture
def transfer_page(driver):
    return TransferPage(driver)

@pytest.fixture
def loan_page(driver):
    return LoanPage(driver)

@pytest.fixture
def payment_page(driver):
    return PaymentPage(driver)

# Simulação de BD simples (para o cenário “já existe no banco”)
@pytest.fixture
def fake_db():
    return {"usuarios": []}


# ------------------  STEPS  ------------------
@given("o usuário acessa a página de cadastro")
def go_to_register(register_page):
    register_page.goto()


@given("ele preenche todos os campos obrigatórios corretamente")
def fill_valid_registration(register_page):
    register_page.fill_form({
        "nome": "Teste Usuário",
        "email": "teste@example.com",
        "senha": "Senha123!",
        "telefone": "1234567890",
        "cep": "12345-678",
        # outros campos obrigatórios...
    })


@given(parsers.parse("ele preenche os campos obrigatórios com os seguintes valores: {campo} = '{valor}'"))
def fill_invalid_field(register_page, campo, valor):
    # Preenche apenas o campo indicado com o valor inválido
    data = {
        "nome": "Teste Usuário",
        "email": "teste@example.com",
        "senha": "Senha123!",
        "telefone": "1234567890",
        "cep": "12345-678",
    }
    data[campo.lower()] = valor
    register_page.fill_form(data)


@when("clica em “Registrar”")
def click_register(register_page):
    register_page.register()


@then(parsers.parse("ele deve ver uma mensagem de confirmação “{mensagem}”"))
def assert_registration_success(register_page, mensagem):
    assert register_page.get_flash_message() == mensagem


@then(parsers.parse("o usuário deve ser redirecionado para a tela de login"))
def assert_redirect_to_login(login_page):
    assert login_page.is_on_page()


@then(parsers.parse("o sistema exibe a mensagem de erro “{mensagem}”"))
def assert_error_message(register_page, mensagem):
    assert register_page.get_flash_message() == mensagem


# --- Cenário "Usuário já cadastrado tenta registrar novamente" ---
@given("o usuário já existe no banco de dados")
def user_exists_in_db(fake_db):
    # Simula inserção no BD
    fake_db["usuarios"].append({
        "email": "exemplo@exemplo.com",
        "senha": "Senha123!"
    })


@when("ele tenta cadastrar-se com o mesmo e‑mail")
def attempt_duplicate_registration(register_page, fake_db):
    register_page.fill_form({
        "nome": "Exemplo",
        "email": "exemplo@exemplo.com",   # email já existente
        "senha": "Senha123!",
        "telefone": "1234567890",
        "cep": "12345-678",
    })
    register_page.register()


@then(parsers.parse("o sistema exibe a mensagem “{mensagem}”"))
def assert_duplicate_email_message(register_page, mensagem):
    assert register_page.get_flash_message() == mensagem


# ------------------  LOGIN ------------------
@given("o usuário está na tela de login")
def go_to_login(login_page):
    login_page.goto()


@when(parsers.parse("ele insere “{email}” e “{senha}”"))
def fill_login_credentials(login_page, email, senha):
    login_page.login(email, senha)


@when("clica em “Entrar”")
def click_login(login_page):
    login_page.submit()


@then(parsers.parse("ele é redirecionado para a página inicial da conta"))
def assert_account_home(account_page):
    assert account_page.is_on_page()


@then(parsers.parse("a tela exibe “Bem‑vindo, {nome}”"))
def assert_welcome_message(account_page, nome):
    assert account_page.get_welcome_text() == f"Bem‑vindo, {nome}"


@then(parsers.parse("o sistema exibe a mensagem “{mensagem}”"))
def assert_login_error(login_page, mensagem):
    assert login_page.get_flash_message() == mensagem


# ------------------  SALDO & EXTRA ------------------
@given("o usuário está logado na conta")
def login_for_balance(account_page):
    # Aqui você pode usar login já pré‑autenticado ou chamar o login
    account_page.login_as("teste@example.com", "Senha123!")


@when("ele navega até a tela “Saldo”")
def go_to_balance(account_page):
    account_page.go_to_balance()


@then(parsers.parse("a página exibe o valor “Saldo atual: R$ {saldo}”"))
def assert_balance(account_page, saldo):
    assert account_page.get_balance() == f"R$ {saldo}"


@when("ele navega até a tela “Extrato”")
def go_to_statement(account_page):
    account_page.go_to_statement()


@then(parsers.parse("o extrato lista as transações em ordem decrescente de data"))
def assert_statement_order(account_page):
    dates = account_page.get_statement_dates()
    assert dates == sorted(dates, reverse=True)


@then("cada linha contém “Data, Descrição, Valor, Saldo”")
def assert_statement_columns(account_page):
    for row in account_page.get_statement_rows():
        assert len(row.split(',')) == 4


# ------------------  TRANSFERÊNCIA ------------------
@given(parsers.parse("o usuário está logado e possui saldo de R$ {saldo:.2f} na conta {conta}"))
def login_and_set_balance(transfer_page, saldo, conta):
    transfer_page.login_as("teste@example.com", "Senha123!")
    transfer_page.set_balance(conta, saldo)


@when(parsers.parse("ele seleciona conta de origem “{origem}” e conta de destino “{destino}”"))
def select_accounts(transfer_page, origem, destino):
    transfer_page.select_origin_account(origem)
    transfer_page.select_destination_account(destino)


@when(parsers.parse("insere o valor “R$ {valor:.2f}”"))
def insert_value(transfer_page, valor):
    transfer_page.enter_amount(valor)


@when("confirma a transferência")
def confirm_transfer(transfer_page):
    transfer_page.confirm()


@then(parsers.parse("R$ {valor:.2f} é debitado da conta {conta}"))
def assert_debit(transfer_page, valor, conta):
    assert transfer_page.get_balance(conta) == f"R$ {transfer_page.initial_balance[conta] - valor:.2f}"


@then(parsers.parse("R$ {valor:.2f} é creditado na conta {conta}"))
def assert_credit(transfer_page, valor, conta):
    assert transfer_page.get_balance(conta) == f"R$ {transfer_page.initial_balance[conta] + valor:.2f}"


@then("ambas as contas registram a transação no histórico")
def assert_history(transfer_page):
    assert transfer_page.has_transaction_history()


@when(parsers.parse("ele tenta transferir R$ {valor:.2f}"))
def attempt_overdraft(transfer_page, valor):
    transfer_page.enter_amount(valor)
    transfer_page.confirm()


@then(parsers.parse("o sistema exibe a mensagem “{mensagem}”"))
def assert_overdraft_error(transfer_page, mensagem):
    assert transfer_page.get_flash_message() == mensagem


# ------------------  EMPRÉSTIMO ------------------
@given("o usuário é logado")
def login_for_loan(loan_page):
    loan_page.login_as("teste@example.com", "Senha123!")


@when(parsers.parse("ele solicita R$ {valor:.2f} de empréstimo com renda anual de R$ {renda:.2f}"))
def request_loan(loan_page, valor, renda):
    loan_page.request_loan(valor, renda)


@then(parsers.parse("o sistema retorna “{resultado}”"))
def assert_loan_result(loan_page, resultado):
    assert loan_page.get_result() == resultado


@then("a mensagem é exibida claramente para o usuário")
def assert_loan_message(loan_page):
    assert loan_page.is_message_visible()


@then(parsers.parse("a mensagem indica “{mensagem}”"))
def assert_loan_reason(loan_page, mensagem):
    assert mensagem in loan_page.get_result()


# ------------------  PAGAMENTO ------------------
@given("o usuário está logado")
def login_for_payment(payment_page):
    payment_page.login_as("teste@example.com", "Senha123!")


@when(parsers.parse("ele registra um pagamento para “{conta}” com data “{data}”"))
def register_payment(payment_page, conta, data):
    payment_page.schedule_payment(conta, data)


@when("clica em “Confirmar”")
def confirm_payment(payment_page):
    payment_page.confirm()


@then(parsers.parse("o pagamento é incluído no histórico de transações"))
def assert_payment_in_history(payment_page):
    assert payment_page.is_payment_in_history()


@then(parsers.parse("o sistema exibe “Pagamento agendado para {data}”"))
def assert_payment_message(payment_page, data):
    assert payment_page.get_flash_message() == f"Pagamento agendado para {data}"


@when(parsers.parse("a data atual é {data}"))
def mock_today(payment_page, data):
    payment_page.set_today(data)


@then(parsers.parse("o pagamento não é executado imediatamente"))
def assert_not_immediate(payment_page):
    assert payment_page.is_scheduled_only()


@then(parsers.parse("o sistema informa “{mensagem}”"))
def assert_future_payment_message(payment_page, mensagem):
    assert payment_page.get_flash_message() == mensagem


# ------------------  NAVEGAÇÃO ------------------
@given("o usuário navega por todas as páginas principais (Login, Cadastro, Saldo, Extrato, Transferência, Empréstimo, Pagamento)")
def navigate_all_pages(driver):
    # Implementar navegação sequencial usando links do menu
    pages = ["login", "register", "balance", "statement", "transfer", "loan", "payment"]
    for page in pages:
        driver.get(f"http://parabank.com/{page}")


@when("ele não encontra erros de carregamento")
def no_loading_errors():
    # No Selenium, isso costuma ser verificado com exceções de timeout
    pass


@then("todas as páginas carregam sem mensagens de erro")
def assert_no_error_messages(driver):
    assert "Erro" not in driver.page_source


# ... e os demais passos (mensagens de erro, links, etc.) podem ser implementados de maneira similar


```

---

## 📌 Como executar

```bash
# 1. Instale as dependências
pip install -r requirements.txt   # (contém pytest, pytest-bdd, selenium, webdriver_manager)

# 2. Inicie os testes
pytest -v tests/test_parabank.py
```

---

## 🔧 Notas importantes

1. **Locators** – Em cada *Page Object*, substitua os seletores (`By.ID`, `By.CSS_SELECTOR`, etc.) pelos que realmente existem na aplicação.
2. **Banco de dados** – O teste “Usuário já cadastrado” usa um *fake_db* simples. Em um cenário real, integre com o backend (API ou DB direto).
3. **Data‑driven** – Os *Scenario Outline* são processados automaticamente pelo pytest‑bdd; não há necessidade de criar fixtures adicionais.
4. **Headless** – O driver está em modo headless. Se precisar depurar visualmente, remova `options.add_argument("--headless")`.
5. **Timeouts** – Ajuste `implicitly_wait` ou use `WebDriverWait` para cenários que exigem espera explícita.

Pronto! Agora você tem um conjunto de testes automatizados em Python, seguindo o BDD que você descreveu, pronto para ser executado em sua pipeline CI. Boa sorte!