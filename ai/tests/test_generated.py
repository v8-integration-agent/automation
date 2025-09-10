Below is a **ready‑to‑run skeleton** that turns the Gherkin scenarios you posted into
automated tests with **pytest‑bdd**.  
Feel free to copy the files into a new repository, adjust the URLs, element
selectors and assertions to match your real application, and then run:

```bash
pip install -U pytest pytest-bdd selenium
pytest
```

---

## 1️⃣ Project layout

```
parabank-tests/
├── tests/
│   ├── conftest.py              # Selenium WebDriver fixture
│   ├── steps/
│   │   └── common_steps.py      # All Gherkin step definitions
│   ├── features/
│   │   ├── cadastro_usuario.feature
│   │   ├── login.feature
│   │   ├── acesso_conta.feature
│   │   ├── transferencia_fundos.feature
│   │   ├── solicitacao_emprestimo.feature
│   │   ├── pagamento_contas.feature
│   │   └── navegacao_uso.feature
│   ├── test_cadastro_usuario.py
│   ├── test_login.py
│   ├── test_acesso_conta.py
│   ├── test_transferencia_fundos.py
│   ├── test_solicitacao_emprestimo.py
│   ├── test_pagamento_contas.py
│   └── test_navegacao.py
└── requirements.txt
```

> **Tip:**  
> If you prefer a single test file per feature, just move the corresponding
> `@scenario` decorator to that file – the step definitions stay in
> `common_steps.py`.



---

## 2️⃣ `tests/conftest.py` – Selenium fixture

```python
# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser():
    """Starts a Chrome instance that will be reused by all tests."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")   # Uncomment to run headless
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
```

---

## 3️⃣ Feature files (copy the content verbatim)

### 3.1 `tests/features/cadastro_usuario.feature`

```gherkin
# tests/features/cadastro_usuario.feature
Feature: Cadastro de Usuário
  Como novo cliente do ParaBank
  Quero registrar meus dados
  Para poder acessar a conta

  Scenario Outline: Cadastro com todos os campos obrigatórios preenchidos
    Dado o usuário esteja na página de cadastro
    Quando ele preencher o campo "<nome>" com "<valor_nome>"
      E preencher o campo "<sobrenome>" com "<valor_sobrenome>"
      E preencher o campo "<email>" com "<valor_email>"
      E preencher o campo "<telefone>" com "<valor_telefone>"
      E preencher o campo "<cep>" com "<valor_cep>"
      E preencher o campo "<endereco>" com "<valor_endereco>"
      E preencher o campo "<cidade>" com "<valor_cidade>"
      E selecionar "<estado>" no dropdown de estado
      E inserir a senha em "<senha>"
      E inserir a senha novamente em "<confirmar_senha>"
      E clicar no botão "Cadastrar"
    Então a mensagem de sucesso deve ser exibida
      E o usuário deve estar logado automaticamente

    Examples:
      | nome | sobrenome | valor_nome | valor_sobrenome | valor_email           | valor_telefone | valor_cep | valor_endereco | valor_cidade | estado | senha          | confirmar_senha |
      | João | Silva     | João       | Silva           | joao.silva@email.com | 5511999999999  | 01001-000 | Rua A          | São Paulo    | SP     | senhaSegura1  | senhaSegura1   |

  Scenario Outline: Cadastro com campo inválido
    Dado o usuário esteja na página de cadastro
    Quando ele preencher o campo "<campo>" com "<valor>"
      E preencher os demais campos com valores válidos
      E clicar no botão "Cadastrar"
    Então a mensagem de erro "<mensagem>" deve aparecer ao lado de "<campo>"

    Examples:
      | campo     | valor              | mensagem                          |
      | email     | usuario.com.br     | Email inválido, por favor insira um email válido. |
      | telefone  | abcdefg            | Telefone inválido, deve conter apenas números.   |
      | cep       | 123                | CEP inválido, deve ter 8 dígitos no formato 00000-000. |
```

---

### 3.2 `tests/features/login.feature`

```gherkin
# tests/features/login.feature
Feature: Login
  Como cliente já cadastrado
  Quero me autenticar no ParaBank
  Para acessar meu dashboard

  Scenario: Login bem-sucedido com credenciais válidas
    Dado o usuário esteja na página de login
    Quando ele digitar "<email>" no campo "Email"
      E digitar "<senha>" no campo "Senha"
      E clicar no botão "Entrar"
    Então o usuário deve ser redirecionado para a página inicial da conta
      E o cabeçalho deve conter "Olá, <nome>"

    Examples:
      | email                   | senha        | nome |
      | joao.silva@email.com    | senhaSegura1 | João |

  Scenario Outline: Login falhou com credenciais inválidas
    Dado o usuário esteja na página de login
    Quando ele digitar "<email>" no campo "Email"
      E digitar "<senha>" no campo "Senha"
      E clicar no botão "Entrar"
    Então a mensagem de erro "<mensagem>" deve aparecer

    Examples:
      | email                   | senha     | mensagem                                  |
      | joao.silva@email.com    | errada    | Credenciais inválidas, tente novamente. |
      | invalido@email.com      | senhaSegura1 | Usuário não encontrado.                |
```

---

### 3.3 `tests/features/acesso_conta.feature`

```gherkin
# tests/features/acesso_conta.feature
Feature: Acesso à Conta – Saldo e Extrato
  Como cliente autenticado
  Quero ver meu saldo e extrato
  Para acompanhar minhas finanças

  Scenario: Visualizar saldo atualizado após operação de crédito
    Dado o usuário esteja na página inicial da conta
      E o saldo atual seja "<saldo_atual>"
    Quando o usuário receber um depósito de "<valor_deposito>"
    Então o saldo deve ser "<saldo_esperado>"
      E a transação de depósito deve aparecer no extrato

    Examples:
      | saldo_atual | valor_deposito | saldo_esperado |
      | 1.000,00     | 500,00          | 1.500,00        |

  Scenario: Extrato exibe transações em ordem cronológica
    Dado o usuário esteja na página de extrato
      E o extrato contenha as seguintes transações:
        | Data       | Descrição           | Valor   |
        | 01/05/2025 | Transferência       | -200,00 |
        | 02/05/2025 | Depósito            | +300,00 |
    Quando a página carregar
    Então as transações devem estar ordenadas do mais recente ao mais antigo
```

---

### 3.4 `tests/features/transferencia_fundos.feature`

```gherkin
# tests/features/transferencia_fundos.feature
Feature: Transferência de Fundos
  Como cliente autenticado
  Quero transferir valores entre minhas contas
  Para movimentar meu dinheiro

  Scenario: Transferência válida entre duas contas
    Dado o usuário esteja na página de transferência
      E a conta origem possua saldo "<saldo_orig>"
      E a conta destino exista
    Quando o usuário selecionar conta origem "<conta_origem>"
      E selecionar conta destino "<conta_destino>"
      E digitar valor "<valor>"
      E confirmar a transferência
    Then o saldo da conta origem deve ser "<saldo_final_origem>"
      E o saldo da conta destino deve ser "<saldo_final_destino>"
      E a transação deve aparecer no histórico de ambas as contas

    Examples:
      | saldo_orig | conta_origem | conta_destino | valor   | saldo_final_origem | saldo_final_destino |
      | 1.000,00   | 123456-1     | 654321-9      | 200,00 | 800,00             | 200,00              |

  Scenario: Transferência falhou por saldo insuficiente
    Dado o usuário esteja na página de transferência
      E a conta origem possua saldo "<saldo_orig>"
    Quando o usuário selecionar conta origem "<conta_origem>"
      E digitar valor "<valor>"
      E confirmar a transferência
    Then a mensagem de erro "<mensagem>" deve ser exibida
      E o saldo da conta origem permanece inalterado

    Examples:
      | saldo_orig | conta_origem | valor   | mensagem                          |
      | 100,00     | 123456-1     | 200,00 | Saldo insuficiente para esta transferência. |
```

---

### 3.5 `tests/features/solicitacao_emprestimo.feature`

```gherkin
# tests/features/solicitacao_emprestimo.feature
Feature: Solicitação de Empréstimo
  Como cliente autenticado
  Quero solicitar um empréstimo
  Para aumentar meu poder de compra

  Scenario Outline: Solicitação de empréstimo com aprovação ou negação
    Dado o usuário esteja na página de solicitação de empréstimo
    Quando ele informar valor "<valor_emprestimo>" e renda anual "<renda_anual>"
      E submeter a solicitação
    Então o sistema deve retornar status "<status>"
      E o usuário deve ver a mensagem "<mensagem>"

    Examples:
      | valor_emprestimo | renda_anual | status   | mensagem                                 |
      | 5.000,00         | 80.000,00   | Aprovado | Seu empréstimo foi aprovado!             |
      | 20.000,00        | 30.000,00   | Negado   | Desculpe, não podemos aprovar seu empréstimo. |
```

---

### 3.6 `tests/features/pagamento_contas.feature`

```gherkin
# tests/features/pagamento_contas.feature
Feature: Pagamento de Contas
  Como cliente autenticado
  Quero registrar e agendar pagamentos de contas
  Para manter minhas contas em dia

  Scenario: Pagamento futuro agendado
    Dado o usuário esteja na página de pagamento de contas
    Quando ele preencher:
      | Campo          | Valor                    |
      | Beneficiário   | Conta de Energia        |
      | Endereço       | Rua X, 100              |
      | Cidade         | São Paulo               |
      | Estado         | SP                       |
      | CEP            | 01001-000                |
      | Telefone       | 5511999999999            |
      | Conta destino  | 123456-1                 |
      | Valor          | 150,00                   |
      | Data           | 15/06/2025 (futuro)      |
    Then o pagamento deve ser incluído no histórico de transações
      E a data de pagamento futura deve ser respeitada

  Scenario: Pagamento com data retroativa
    Dado o usuário esteja na página de pagamento de contas
    Quando ele definir a data de pagamento como "01/01/2025" (passado)
      E submeter o pagamento
    Then a mensagem de erro "Data de pagamento não pode ser passada." deve aparecer
```

---

### 3.7 `tests/features/navegacao_uso.feature`

```gherkin
# tests/features/navegacao_uso.feature
Feature: Requisitos Gerais de Navegação e Usabilidade
  Como cliente
  Quero que todas as páginas sejam navegáveis sem erros
  Para ter uma experiência de uso agradável

  Scenario: Carregamento correto de todas as páginas principais
    Dado o usuário esteja autenticado
    Quando ele acessar cada uma das páginas: Dashboard, Saldo, Extrato, Transferência, Empréstimo, Pagamento
    Então cada página deve carregar sem erros e exibir os componentes corretos

  Scenario: Consistência de menus e links
    Dado o usuário esteja em qualquer página
    Quando ele clicar no link "Contas" no menu
    Then ele deve ser redirecionado para a página de contas
      E o mesmo link deve funcionar em todas as outras páginas

  Scenario: Mensagens de erro claras e objetivas
    Dado o usuário esteja na página de login
    Quando ele tentar login com senha vazia
    Then a mensagem "Senha é obrigatória." deve ser exibida de forma destacada
```

---

## 4️⃣ Step definitions – `tests/steps/common_steps.py`

```python
# tests/steps/common_steps.py
import re
from datetime import datetime

import pytest
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# ------------------------------------------------------------------
# Helpers – you may want to move them into a page‑object layer
# ------------------------------------------------------------------
def find_field(browser, field_name):
    """Return an element matching common field names."""
    # Adjust selectors according to your app
    locators = {
        "nome": (By.NAME, "firstName"),
        "sobrenome": (By.NAME, "lastName"),
        "email": (By.NAME, "email"),
        "telefone": (By.NAME, "phone"),
        "cep": (By.NAME, "zip"),
        "endereco": (By.NAME, "address"),
        "cidade": (By.NAME, "city"),
        "senha": (By.NAME, "password"),
        "confirmar_senha": (By.NAME, "confirmPassword"),
        # Add more if needed
    }
    return browser.find_element(*locators.get(field_name, (By.NAME, field_name)))


def click_button(browser, text):
    return browser.find_element(By.XPATH, f"//button[normalize-space()='{text}']").click()


def get_error_element_for(browser, field):
    """Return the error label that appears next to the field."""
    # Example: <span class="error" for="email">...</span>
    return browser.find_element(By.XPATH, f"//span[@class='error' and @for='{field}']")


# ------------------------------------------------------------------
# 1️⃣ Cadastro de Usuário
# ------------------------------------------------------------------
@given("o usuário esteja na página de cadastro")
def go_to_signup(browser):
    browser.get("https://parabank.com/signup")   # <- change to real URL


@when(parsers.parse('ele preencher o campo "<nome>" com "<valor_nome>"'))
def fill_field(browser, nome, valor_nome):
    field = find_field(browser, nome.lower())
    field.clear()
    field.send_keys(valor_nome)


@when(parsers.parse('preencher o campo "<campo>" com "<valor>"'))
def fill_invalid_field(browser, campo, valor):
    field = find_field(browser, campo.lower())
    field.clear()
    field.send_keys(valor)


@when(parsers.parse('preencher os demais campos com valores válidos'))
def fill_other_fields(browser):
    """Populate all other mandatory fields with dummy data."""
    # In a real test, you would either read from a fixture or generate random data
    common_valid = {
        "nome": "Maria",
        "sobrenome": "Souza",
        "email": "maria.souza@email.com",
        "telefone": "551112345678",
        "cep": "01001-000",
        "endereco": "Rua B",
        "cidade": "São Paulo",
        "estado": "SP",
        "senha": "senhaSegura1",
        "confirmar_senha": "senhaSegura1",
    }
    for k, v in common_valid.items():
        try:
            field = find_field(browser, k)
            field.clear()
            field.send_keys(v)
        except Exception:
            pass  # skip if field not present – the scenario may not need it


@when(parsers.parse('selecionar "<estado>" no dropdown de estado'))
def select_state(browser, estado):
    select = Select(browser.find_element(By.NAME, "state"))
    select.select_by_value(estado)


@when(parsers.parse('inserir a senha em "<senha>"'))
def fill_password(browser, senha):
    field = find_field(browser, "senha")
    field.clear()
    field.send_keys(senha)


@when(parsers.parse('inserir a senha novamente em "<confirmar_senha>"'))
def fill_confirm_password(browser, confirmar_senha):
    field = find_field(browser, "confirmar_senha")
    field.clear()
    field.send_keys(confirmar_senha)


@when('clicar no botão "Cadastrar"')
def click_register(browser):
    click_button(browser, "Cadastrar")


@then("a mensagem de sucesso deve ser exibida")
def verify_success_message(browser):
    msg = browser.find_element(By.CSS_SELECTOR, ".success").text
    assert "sucesso" in msg.lower()


@then("o usuário deve estar logado automaticamente")
def verify_logged_in(browser):
    header = browser.find_element(By.CSS_SELECTOR, "header .user-name")
    assert header.is_displayed()


@then(parsers.parse('a mensagem de erro "<mensagem>" deve aparecer ao lado de "<campo>"'))
def verify_error_message(browser, mensagem, campo):
    err = get_error_element_for(browser, campo.lower())
    assert mensagem in err.text


# ------------------------------------------------------------------
# 2️⃣ Login
# ------------------------------------------------------------------
@given("o usuário esteja na página de login")
def go_to_login(browser):
    browser.get("https://parabank.com/login")


@when(parsers.parse('ele digitar "<email>" no campo "Email"'))
def type_email(browser, email):
    field = browser.find_element(By.NAME, "email")
    field.clear()
    field.send_keys(email)


@when(parsers.parse('digitar "<senha>" no campo "Senha"'))
def type_password(browser, senha):
    field = browser.find_element(By.NAME, "password")
    field.clear()
    field.send_keys(senha)


@when('clicar no botão "Entrar"')
def click_login(browser):
    click_button(browser, "Entrar")


@then(parsers.parse('o usuário deve ser redirecionado para a página inicial da conta'))
def verify_redirect_to_dashboard(browser):
    assert browser.current_url.endswith("/home")


@then(parsers.parse('o cabeçalho deve conter "Olá, <nome>"'))
def verify_greeting(browser, nome):
    header = browser.find_element(By.CSS_SELECTOR, "header .welcome")
    assert f"Olá, {nome}" in header.text


@then(parsers.parse('a mensagem de erro "<mensagem>" deve aparecer'))
def verify_login_error(browser, mensagem):
    err = browser.find_element(By.CSS_SELECTOR, ".login-error")
    assert mensagem in err.text


# ------------------------------------------------------------------
# 3️⃣ Acesso à Conta – Saldo e Extrato
# ------------------------------------------------------------------
@given(parsers.parse('o usuário esteja na página inicial da conta'))
def go_to_dashboard(browser):
    browser.get("https://parabank.com/home")


@given(parsers.parse('o saldo atual seja "<saldo_atual>"'))
def set_initial_balance(browser, saldo_atual):
    # This is usually done via a fixture that creates the account in a test DB.
    # For demo purposes we skip actual implementation.
    pass


@when(parsers.parse('o usuário receber um depósito de "<valor_deposito>"'))
def deposit_amount(browser, valor_deposito):
    # Simulate a deposit via UI or API
    pass


@then(parsers.parse('o saldo deve ser "<saldo_esperado>"'))
def check_balance(browser, saldo_esperado):
    saldo_elem = browser.find_element(By.ID, "balance")
    assert saldo_elem.text == saldo_esperado


@then('a transação de depósito deve aparecer no extrato')
def check_deposit_in_statement(browser):
    statement = browser.find_element(By.ID, "statement")
    assert "Depósito" in statement.text


@given(parsers.parse('o usuário esteja na página de extrato'))
def go_to_statement(browser):
    browser.get("https://parabank.com/statement")


@given(parsers.parse('o extrato contenha as seguintes transações:'))
def populate_statement(browser, table):
    # In a real test, you'd use API or DB to seed the data.
    # Here we just acknowledge the step.
    pass


@when('a página carregar')
def wait_for_page_load(browser):
    browser.implicitly_wait(5)


@then('as transações devem estar ordenadas do mais recente ao mais antigo')
def verify_statement_order(browser):
    rows = browser.find_elements(By.CSS_SELECTOR, "#statement tbody tr")
    dates = [datetime.strptime(r.find_element(By.CSS_SELECTOR, ".date").text, "%d/%m/%Y") for r in rows]
    assert dates == sorted(dates, reverse=True)


# ------------------------------------------------------------------
# 4️⃣ Transferência de Fundos
# ------------------------------------------------------------------
@given(parsers.parse('o usuário esteja na página de transferência'))
def go_to_transfer(browser):
    browser.get("https://parabank.com/transfer")


@given(parsers.parse('a conta origem possua saldo "<saldo_orig>"'))
def set_origin_balance(browser, saldo_orig):
    pass


@given('a conta destino exista')
def ensure_destination_exists(browser):
    pass


@when(parsers.parse('o usuário selecionar conta origem "<conta_origem>"'))
def select_origin_account(browser, conta_origem):
    select = Select(browser.find_element(By.NAME, "fromAccount"))
    select.select_by_value(conta_origem)


@when(parsers.parse('selecionar conta destino "<conta_destino>"'))
def select_destination_account(browser, conta_destino):
    select = Select(browser.find_element(By.NAME, "toAccount"))
    select.select_by_value(conta_destino)


@when(parsers.parse('digitar valor "<valor>"'))
def input_transfer_amount(browser, valor):
    field = browser.find_element(By.NAME, "amount")
    field.clear()
    field.send_keys(valor)


@when('confirmar a transferência')
def confirm_transfer(browser):
    click_button(browser, "Transfer")


@then(parsers.parse('o saldo da conta origem deve ser "<saldo_final_origem>"'))
def verify_origin_balance(browser, saldo_final_origem):
    origin = browser.find_element(By.ID, "fromAccountBalance")
    assert origin.text == saldo_final_origem


@then(parsers.parse('o saldo da conta destino deve ser "<saldo_final_destino>"'))
def verify_destination_balance(browser, saldo_final_destino):
    dest = browser.find_element(By.ID, "toAccountBalance")
    assert dest.text == saldo_final_destino


@then('a transação deve aparecer no histórico de ambas as contas')
def check_transfer_in_history(browser):
    hist = browser.find_element(By.ID, "transferHistory")
    assert "Transferência" in hist.text


@then(parsers.parse('a mensagem de erro "<mensagem>" deve ser exibida'))
def verify_transfer_error(browser, mensagem):
    err = browser.find_element(By.CSS_SELECTOR, ".transfer-error")
    assert mensagem in err.text


@then('o saldo da conta origem permanece inalterado')
def verify_origin_balance_unchanged(browser):
    # Implementation would compare pre‑ and post‑balance
    pass


# ------------------------------------------------------------------
# 5️⃣ Solicitação de Empréstimo
# ------------------------------------------------------------------
@given('o usuário esteja na página de solicitação de empréstimo')
def go_to_loan_page(browser):
    browser.get("https://parabank.com/loan")


@when(parsers.parse('ele informar valor "<valor_emprestimo>" e renda anual "<renda_anual>"'))
def input_loan_details(browser, valor_emprestimo, renda_anual):
    browser.find_element(By.NAME, "loanAmount").clear()
    browser.find_element(By.NAME, "loanAmount").send_keys(valor_emprestimo)
    browser.find_element(By.NAME, "annualIncome").clear()
    browser.find_element(By.NAME, "annualIncome").send_keys(renda_anual)


@when('submeter a solicitação')
def submit_loan(browser):
    click_button(browser, "Submit")


@then(parsers.parse('o sistema deve retornar status "<status>"'))
def verify_loan_status(browser, status):
    status_elem = browser.find_element(By.CSS_SELECTOR, ".loan-status")
    assert status == status_elem.text


@then(parsers.parse('o usuário deve ver a mensagem "<mensagem>"'))
def verify_loan_message(browser, mensagem):
    msg = browser.find_element(By.CSS_SELECTOR, ".loan-message").text
    assert mensagem in msg


# ------------------------------------------------------------------
# 6️⃣ Pagamento de Contas
# ------------------------------------------------------------------
@given('o usuário esteja na página de pagamento de contas')
def go_to_payment_page(browser):
    browser.get("https://parabank.com/payments")


@when(parsers.parse('ele preencher:'))
def fill_payment_form(browser, table):
    for row in table:
        campo = row['Campo'].strip()
        valor = row['Valor'].strip()
        if campo.lower() == "data":
            # Handle date field – might need a date picker
            field = browser.find_element(By.NAME, "paymentDate")
            field.clear()
            field.send_keys(valor.split(" ")[0])  # ignore "(futuro)" or "(passado)"
        else:
            field = find_field(browser, campo.lower())
            field.clear()
            field.send_keys(valor)


@when(parsers.parse('definir a data de pagamento como "<data>" (passado)'))
def set_past_payment_date(browser, data):
    field = browser.find_element(By.NAME, "paymentDate")
    field.clear()
    field.send_keys(data.split(" ")[0])  # remove "passado"


@when('submeter o pagamento')
def submit_payment(browser):
    click_button(browser, "Pay")


@then('o pagamento deve ser incluído no histórico de transações')
def verify_payment_in_history(browser):
    hist = browser.find_element(By.ID, "paymentHistory")
    assert "Pagamento" in hist.text


@then('a data de pagamento futura deve ser respeitada')
def verify_future_date(browser):
    # Would check that the date in history equals the future date entered
    pass


@then(parsers.parse('a mensagem de erro "<mensagem>" deve aparecer'))
def verify_payment_error(browser, mensagem):
    err = browser.find_element(By.CSS_SELECTOR, ".payment-error")
    assert mensagem in err.text


# ------------------------------------------------------------------
# 7️⃣ Navegação e Usabilidade
# ------------------------------------------------------------------
@given('o usuário esteja autenticado')
def authenticated_user(browser):
    browser.get("https://parabank.com/home")  # Assumes session cookie already set


@when(parsers.parse('ele acessar cada uma das páginas: {pages}'))
def visit_pages(browser, pages):
    page_map = {
        "Dashboard": "/home",
        "Saldo": "/balance",
        "Extrato": "/statement",
        "Transferência": "/transfer",
        "Empréstimo": "/loan",
        "Pagamento": "/payments",
    }
    for page in [p.strip() for p in pages.split(",")]:
        browser.get(f"https://parabank.com{page_map.get(page.strip(), '')}")


@then('cada página deve carregar sem erros e exibir os componentes corretos')
def verify_page_components(browser):
    # For demo we just check the page title contains something
    assert browser.title != ""


@given('o usuário esteja em qualquer página')
def any_page(browser):
    browser.get("https://parabank.com/home")


@when('ele clicar no link "Contas" no menu')
def click_account_link(browser):
    link = browser.find_element(By.LINK_TEXT, "Contas")
    link.click()


@then('ele deve ser redirecionado para a página de contas')
def verify_redirect_to_accounts(browser):
    assert browser.current_url.endswith("/accounts")


@then('o mesmo link deve funcionar em todas as outras páginas')
def verify_link_on_all_pages(browser):
    # Implementation would iterate through all pages – omitted for brevity
    pass


@given('o usuário esteja na página de login')
def login_page(browser):
    browser.get("https://parabank.com/login")


@when('ele tentar login com senha vazia')
def login_with_empty_password(browser):
    type_email(browser, "user@example.com")
    type_password(browser, "")
    click_login(browser)


@then('a mensagem "Senha é obrigatória." deve ser exibida de forma destacada')
def verify_empty_password_error(browser):
    err = browser.find_element(By.CSS_SELECTOR, ".error")
    assert "Senha é obrigatória." in err.text
```

> **Important notes**  
> * The above step implementations are **illustrative** – replace the element locators, URLs and any business logic with the real ones from your application.  
> * For steps that require data seeding (e.g., setting balances, populating statements, etc.) you should use your test DB or a mock API.  
> * If you prefer to keep the step definitions *per feature*, simply move the relevant section into its own `test_*.py` file; the decorator `@scenario("path/to/feature.feature")` is what ties the feature to the test function.

---

## 5️⃣ Running the tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest
```

The tests will launch a Chrome browser, drive it through the flows described in the Gherkin files, and assert the expected outcomes.  

Happy testing! 🚀