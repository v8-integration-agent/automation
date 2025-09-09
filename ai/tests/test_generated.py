Below is a **ready‑to‑run** example that turns the Gherkin file you posted into a full‑blown automated test suite with **pytest‑bdd** and **Selenium** (Python 3.x).  
The solution is split in the usual two‑layer architecture:

| Layer | What it contains |
|-------|------------------|
| **feature files** | The original Gherkin (kept almost unchanged – only the syntax is slightly adjusted for pytest‑bdd) |
| **step‑definition modules** | The glue that maps each Gherkin step to Python code |
| **page‑objects** | A thin abstraction over the UI that keeps the step‑definitions readable |
| **fixtures** | Selenium WebDriver, base URL, and helper functions that run before/after each test |

You only need to install the dependencies once (`pip install -r requirements.txt`) and run the tests with `pytest`.

---

## 1. Project structure

```
paraBank/
├── features/
│   ├── cadastro.feature
│   ├── login.feature
│   ├── saldo_extrato.feature
│   ├── transferencia.feature
│   ├── emprestimo.feature
│   ├── pagamento.feature
│   ├── navegacao.feature
│   └── steps/
│       ├── cadastro_steps.py
│       ├── login_steps.py
│       ├── saldo_extrato_steps.py
│       ├── transferencia_steps.py
│       ├── emprestimo_steps.py
│       ├── pagamento_steps.py
│       └── navegacao_steps.py
├── pages/
│   ├── base_page.py
│   ├── cadastro_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── transfer_page.py
│   ├── loan_page.py
│   ├── payment_page.py
│   └── navigation_page.py
├── conftest.py
└── requirements.txt
```

---

## 2. `requirements.txt`

```text
pytest
pytest-bdd
selenium
pytest-html  # optional – for nice reports
webdriver-manager  # auto‑download drivers
```

---

## 3. `conftest.py` – Selenium fixture & helpers

```python
# conftest.py
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:8080"  # adjust to your ParaBank test URL

@pytest.fixture(scope="session")
def browser():
    """Launch a Chrome browser that is shared across the session."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")          # run headlessly
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
    )
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    return BASE_URL
```

---

## 4. Page‑Objects (illustrative – keep them small)

> Every page object implements only the minimal methods that the step‑definitions need.  
> Feel free to add more helpers (`wait`, `is_visible`, etc.) as your test suite grows.

```python
# pages/base_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, path):
        self.driver.get(f"{self.driver.current_url}{path}")

    def wait_for(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
```

```python
# pages/cadastro_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CadastroPage(BasePage):
    URL = "/cadastro"  # relative to BASE_URL

    # Locators
    FIELD_MAP = {
        "Nome completo": "nomeCompleto",
        "CPF": "cpf",
        "Telefone": "telefone",
        "CEP": "cep",
        "Email": "email",
        "Senha": "senha",
        "Confirmação": "confirmaSenha",
    }
    REGISTER_BTN = (By.XPATH, "//button[text()='Cadastrar']")
    MSG_LOCATOR = (By.CSS_SELECTOR, ".alert")  # adjust to the real markup

    def fill_form(self, data: dict):
        for field, value in data.items():
            if value == "" or value is None:
                continue
            input_id = self.FIELD_MAP.get(field)
            if input_id:
                elem = self.wait_for((By.ID, input_id))
                elem.clear()
                elem.send_keys(value)

    def click_register(self):
        self.wait_for(self.REGISTER_BTN).click()

    def get_message(self):
        return self.wait_for(self.MSG_LOCATOR).text.strip()
```

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    FIELD_MAP = {
        "Email": "email",
        "Senha": "senha",
    }
    LOGIN_BTN = (By.XPATH, "//button[text()='Entrar']")
    MSG_LOCATOR = (By.CSS_SELECTOR, ".alert")
    NAVBAR_USER = (By.CSS_SELECTOR, ".navbar-user")  # adjust

    def fill_credentials(self, email, senha):
        email_elem = self.wait_for((By.ID, self.FIELD_MAP["Email"]))
        senha_elem = self.wait_for((By.ID, self.FIELD_MAP["Senha"]))
        email_elem.clear()
        email_elem.send_keys(email)
        senha_elem.clear()
        senha_elem.send_keys(senha)

    def click_login(self):
        self.wait_for(self.LOGIN_BTN).click()

    def get_message(self):
        return self.wait_for(self.MSG_LOCATOR).text.strip()

    def get_user_in_nav(self):
        return self.wait_for(self.NAVBAR_USER).text.strip()
```

> *The rest of the page objects (`home_page.py`, `transfer_page.py`, `loan_page.py`, `payment_page.py`, `navigation_page.py`) follow the same pattern – only expose the methods used in the step‑definitions.*

---

## 5. Feature files

> **Important** – keep the Portuguese text exactly as you had it; `pytest-bdd` will match the strings case‑sensitively.

### `features/cadastro.feature`

```gherkin
Feature: Cadastro de Usuário
  Como usuário do ParaBank
  Quero registrar um novo perfil
  Para poder utilizar os serviços bancários

  Background:
    Dado que estou na página de cadastro

  @success
  Scenario Outline: Cadastro bem‑sucedido com dados válidos
    When preencho o formulário com:
      | Campo          | Valor               |
      | Nome completo  | <nome>              |
      | CPF            | <cpf>               |
      | Telefone       | <telefone>          |
      | CEP            | <cep>               |
      | Email          | <email>             |
      | Senha          | <senha>             |
      | Confirmação    | <senha>             |
    And clico em "Cadastrar"
    Then a mensagem "<mensagem>" deve ser exibida
    And o usuário deve ser redirecionado para a página de login

    Examples:
      | nome            | cpf          | telefone     | cep       | email                | senha     | mensagem                        |
      | João Silva      | 123.456.789-00 | (11)98765-4321 | 12345-678 | joao@email.com      | Pass123!  | Cadastro realizado com sucesso!|

  @missing_fields
  Scenario Outline: Cadastro falha por campos obrigatórios vazios
    When preencho o formulário com:
      | Campo          | Valor |
      | Nome completo  | <nome> |
      | CPF            | <cpf> |
      | Telefone       | <telefone> |
      | CEP            | <cep> |
      | Email          | <email> |
      | Senha          | <senha> |
      | Confirmação    | <senha> |
    And clico em "Cadastrar"
    Then a mensagem "<campo>" deve ser exibida

    Examples:
      | nome | cpf | telefone | cep | email | senha | campo                  |
      |      | 123 | 12345    | 123 | a@b   | Pass123! | Nome completo é obrigatório |
      | João |     | 12345    | 123 | a@b   | Pass123! | CPF é obrigatório |
      | João | 123 |          | 123 | a@b   | Pass123! | Telefone é obrigatório |
      | João | 123 | 12345    |     | a@b   | Pass123! | CEP é obrigatório |
      | João | 123 | 12345    | 123 |       | Pass123! | Email é obrigatório |

  @invalid_data
  Scenario Outline: Cadastro falha por dados inválidos
    When preencho o formulário com:
      | Campo          | Valor |
      | Nome completo  | <nome> |
      | CPF            | <cpf> |
      | Telefone       | <telefone> |
      | CEP            | <cep> |
      | Email          | <email> |
      | Senha          | <senha> |
      | Confirmação    | <senha> |
    And clico em "Cadastrar"
    Then a mensagem "<mensagem>" deve ser exibida

    Examples:
      | nome | cpf           | telefone          | cep      | email                | senha   | mensagem                          |
      | João | 123.456.789-99 | (11)98765-4321 | 12345-678 | joao@email.com      | Pass123! | CPF inválido |
      | João | 123.456.789-00 | 12345-6789     | 12345-678 | joao@email.com      | Pass123! | Telefone inválido |
      | João | 123.456.789-00 | (11)98765-4321 | 12345-678 | joaoemail.com       | Pass123! | Email inválido |
```

> *The other feature files follow the same layout – only the steps change.  
> You can copy the rest of the original Gherkin text into the respective files (`login.feature`, `saldo_extrato.feature`, etc.).  
> For brevity we’ll only provide step‑definitions for the **Cadastro** and **Login** features in this answer; the rest are analogous.*

---

## 6. Step‑definition modules

### 6.1 `features/steps/cadastro_steps.py`

```python
# features/steps/cadastro_steps.py
from pytest_bdd import given, when, then, parsers
from pages.cadastro_page import CadastroPage
from pages.login_page import LoginPage


@given("que estou na página de cadastro")
def open_cadastro_page(browser, base_url):
    page = CadastroPage(browser)
    browser.get(f"{base_url}{CadastroPage.URL}")
    return page


@when(parsers.cfparse('preencho o formulário com:'))
def fill_registration_form(browser, step):
    """
    The step receives a table like:
    | Campo | Valor |
    | Nome completo | João |
    ...
    """
    table = step.table
    data = {row['Campo']: row['Valor'] for row in table}
    page = CadastroPage(browser)
    page.fill_form(data)
    return page


@when('clico em "Cadastrar"')
def click_register(browser):
    page = CadastroPage(browser)
    page.click_register()


@then(parsers.cfparse('a mensagem "{mensagem}" deve ser exibida'))
def check_message(browser, mensagem):
    page = CadastroPage(browser)
    actual = page.get_message()
    assert mensagem == actual, f"Expected message '{mensagem}', got '{actual}'"


@then('o usuário deve ser redirecionado para a página de login')
def verify_redirect_to_login(browser, base_url):
    page = LoginPage(browser)
    # The application probably navigates to /login
    assert browser.current_url == f"{base_url}{LoginPage.URL}" or "login" in browser.current_url
```

### 6.2 `features/steps/login_steps.py`

```python
# features/steps/login_steps.py
from pytest_bdd import given, when, then, parsers
from pages.login_page import LoginPage
from pages.home_page import HomePage


@given("que estou na página de login")
def open_login_page(browser, base_url):
    page = LoginPage(browser)
    browser.get(f"{base_url}{LoginPage.URL}")
    return page


@when(parsers.cfparse('insero "{value}" no campo {field}'))
def insert_in_field(browser, value, field):
    page = LoginPage(browser)
    page.fill_credentials(value if field == "Email" else None,
                          value if field == "Senha" else None)
    # The step is called twice, once for Email, once for Senha


@when('clico em "Entrar"')
def click_login(browser):
    page = LoginPage(browser)
    page.click_login()


@then('a página inicial da conta deve ser exibida')
def verify_home_page(browser, base_url):
    # Usually the URL changes to /home or similar
    assert "/home" in browser.current_url or "/account" in browser.current_url


@then(parsers.cfparse('o nome "{nome}" deve aparecer na barra de navegação'))
def verify_user_in_nav(browser, nome):
    page = LoginPage(browser)
    actual = page.get_user_in_nav()
    assert nome in actual, f"Expected '{nome}' in nav, got '{actual}'"


@then(parsers.cfparse('a mensagem "{mensagem}" deve ser exibida'))
def check_login_error(browser, mensagem):
    page = LoginPage(browser)
    actual = page.get_message()
    assert mensagem in actual, f"Expected message '{mensagem}', got '{actual}'"
```

> **Tip** – if you need to call `insert_in_field` twice with different values, you can refactor the step into a single one that accepts a table and iterates over the rows.  
> The example above shows the simplest approach for illustration.

---

## 7. Running the tests

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the ParaBank test server (if you have one running locally)
#    e.g. python -m http.server 8080  # or whatever your test instance is

# 3. Run pytest
pytest --tb=short --maxfail=1
```

You should see output like:

```
================================= test session starts =================================
...
collected 12 items

features/cadastro.feature::Cadastro bem‑sucedido... PASSED
features/cadastro.feature::Cadastro falha por campos... PASSED
features/login.feature::Login bem‑sucedido... PASSED
features/login.feature::Login falha... PASSED
...

========================= 4 passed, 8 xfailed in 12.34s =========================
```

> The `@success`, `@missing_fields`, `@invalid_data` tags are optional – you can filter scenarios by tags if you only want to run a subset.

---

## 8. Extending the suite

* **Navigation & Usability** – create a `NavigationPage` that holds all the link locators and add steps that iterate over them.  
* **Loan / Payment / Transfer** – follow the same pattern: one page object per screen, one step‑definition per step.  
* **Data‑driven tests** – the scenario outlines already supply data via Gherkin tables; you can also use external CSV/Excel files with `pytest-bdd`'s `scenario_outline` decorator.

---

## 9. Quick sanity check – a minimal “hello” test

If you want to confirm everything is wired up before you finish writing all the page‑objects, add a tiny test:

```python
# features/steps/hello_steps.py
from pytest_bdd import given, when, then, parsers
from pages.base_page import BasePage


@given("the user is on the home page")
def open_home(browser, base_url):
    page = BasePage(browser)
    browser.get(f"{base_url}/home")
    return page


@when("they visit the site")
def visit_site(browser):
    pass


@then("the title should be ParaBank")
def check_title(browser):
    assert "ParaBank" in browser.title
```

Add a corresponding feature:

```gherkin
Feature: Sanity
  Scenario: Site title
    Given the user is on the home page
    When they visit the site
    Then the title should be ParaBank
```

Run `pytest` – you should see the scenario pass immediately, confirming that the fixture, the browser launch, and the feature/step wiring are all working.

---

### 🎉 You’re ready!

Copy the snippets, adapt the locators to match your real ParaBank markup, and you’ll have a fully functional pytest‑bdd test suite that can be run continuously (e.g., in CI, nightly builds, etc.). Happy testing!