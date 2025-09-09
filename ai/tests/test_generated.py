Below is a **complete skeleton** that you can drop into a fresh repository and run with `pytest`.  
It contains:

1. **Feature files** – one per feature (the Gherkin you provided).  
2. **Step‑definition modules** – one module per feature that implements all of the steps.  
3. **A small fixture layer** (Selenium WebDriver, Page‑Object stubs) that can be extended to interact with your actual UI.  

> ⚠️ **Tip** – the code below only contains *place‑holders*.  
> Replace the `pass` / `raise NotImplementedError` blocks with real Selenium or API calls as needed.

---

## 1️⃣ Project layout

```
paraBank-tests/
├─ conftest.py
├─ features/
│  ├─ cadastro.feature
│  ├─ login.feature
│  ├─ saldo_extrato.feature
│  ├─ transferencia.feature
│  ├─ emprestimo.feature
│  ├─ pagamento.feature
│  └─ usabilidade.feature
└─ steps/
   ├─ cadastro_steps.py
   ├─ login_steps.py
   ├─ saldo_extrato_steps.py
   ├─ transferencia_steps.py
   ├─ emprestimo_steps.py
   ├─ pagamento_steps.py
   └─ usabilidade_steps.py
```

Run the whole test suite with:

```bash
pip install -r requirements.txt   # see below
pytest
```

---

## 2️⃣ Requirements (`requirements.txt`)

```text
pytest
pytest-bdd
selenium
webdriver-manager
```

> **NOTE** – if you prefer API‑level testing, drop the selenium imports and use `requests` instead.

---

## 3️⃣ Selenium fixture (`conftest.py`)

```python
# conftest.py
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    """A single WebDriver instance for the whole test session."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")          # run head‑less by default
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    """Page Object stub – replace with real implementation."""
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.fixture
def cadastro_page(driver):
    from pages.cadastro_page import CadastroPage
    return CadastroPage(driver)

# ... add other page objects as needed
```

> **Page Objects** – create minimal stub classes in `pages/`.  
> E.g. `pages/login_page.py`:

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, driver): self.driver = driver

    def go_to(self):
        self.driver.get("https://parabank.com/login")

    def fill_email(self, email): pass
    def fill_password(self, pwd): pass
    def click_login(self): pass
    def is_at_home(self): return True
    # add more helper methods as needed
```

---

## 4️⃣ Feature files

> **Only the first two features are shown in full** – copy the same style for the rest.

### `features/cadastro.feature`

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
```

### `features/login.feature`

```gherkin
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
```

> **Repeat** the same style for the remaining feature files (saldo_extrato, transferencia, emprestimo, pagamento, usabilidade).

---

## 5️⃣ Step‑definition modules

Each module starts with the decorator `@scenario` that links the feature file to the function.  
The functions are *empty* – they only map the Gherkin steps to Python functions.  
Implement the real logic inside the body (`pass` ➜ replace with Selenium actions).

### `steps/cadastro_steps.py`

```python
# steps/cadastro_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Load all scenarios from the feature file
scenarios('../../features/cadastro.feature')

# ---------- Background steps --------------------------------------------

@given(parsers.parse('que eu esteja na página “{pagina}”'))
def open_page(driver, pagina):
    """Open the specified page (e.g., Criar Conta)."""
    # Example: navigate to the 'Criar Conta' page
    driver.get("https://parabank.com/create-account")
    # In a real implementation you may want to assert that the page has loaded
    pass

# ---------- Step implementations ----------------------------------------

@when(parsers.parse('eu preencho “{campo}” com “{valor}”'))
def fill_field(cadastro_page, campo, valor):
    """Fill a field on the registration form."""
    cadastro_page.fill_field(campo, valor)   # implement in CadastroPage
    pass

@when('eu preencho os demais campos corretamente')
def fill_other_fields(cadastro_page):
    """Fill all mandatory fields with valid dummy data."""
    cadastro_page.fill_valid_data()
    pass

@when('eu deixo o campo “Nome” vazio')
def leave_nome_empty(cadastro_page):
    cadastro_page.clear_field('Nome')
    pass

@when('eu clico em “Criar Conta”')
def click_create_account(cadastro_page):
    cadastro_page.click_create()
    pass

@then(parsers.parse('eu devo ver a mensagem “{mensagem}”'))
def verify_message(cadastro_page, mensagem):
    assert cadastro_page.get_message() == mensagem
    pass

@then('eu devo ser redirecionado para a tela de login')
def verify_redirect_to_login(cadastro_page):
    assert cadastro_page.is_on_login_page()
    pass

@when(parsers.parse('que “{email}” já está cadastrado'))
def ensure_email_exists(driver, email):
    """Pre‑condition – create the user if not already present."""
    # e.g. call the API or use the UI to register the email
    # For the test we simply note that the email is already registered
    pass
```

> **Explanation** –  
> * `parsers.parse()` allows you to capture the quoted text directly.  
> * The same pattern applies to all the other features.

### `steps/login_steps.py`

```python
# steps/login_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../../features/login.feature')

@given(parsers.parse('o usuário “{usuario}” esteja cadastrado com senha “{senha}”'))
def ensure_user_exists(driver, usuario, senha):
    """Pre‑condition – create the user if it doesn't exist."""
    # Call your API or use the UI to create the user
    pass

@when(parsers.parse('eu preencho “{campo}” com “{valor}”'))
def login_fill_field(login_page, campo, valor):
    if campo == 'E‑mail':
        login_page.fill_email(valor)
    elif campo == 'Senha':
        login_page.fill_password(valor)

@when('eu clico em “Entrar”')
def login_click_enter(login_page):
    login_page.click_login()

@then(parsers.parse('eu devo ser redirecionado para a página inicial da conta'))
def verify_login_success(login_page):
    assert login_page.is_at_home()

@then(parsers.parse('eu devo ver “{texto}”'))
def verify_text_on_home(login_page, texto):
    assert login_page.contains_text(texto)

@then(parsers.parse('eu devo ver a mensagem “{mensagem}”'))
def verify_login_error(login_page, mensagem):
    assert login_page.get_error_message() == mensagem
```

> **Other feature files** – follow the same structure:
> * Create a module (`saldo_extrato_steps.py`, `transferencia_steps.py`, …).  
> * Add a `scenarios()` call pointing to the correct feature.  
> * Define `@given`, `@when`, `@then` blocks that map to the Gherkin text.

---

## 6️⃣ Quick‑start guide (how to add a new page‑object)

```python
# pages/transferencia_page.py
class TransferenciaPage:
    def __init__(self, driver):
        self.driver = driver

    def select_origin(self, account_name):
        # Locate the origin account selector and pick the account
        pass

    def select_destination(self, account_name):
        pass

    def enter_amount(self, amount):
        pass

    def confirm(self):
        pass

    def get_origin_balance(self):
        pass

    def get_destination_balance(self):
        pass

    def get_transaction_history(self):
        pass
```

In the step‑definition you simply call:

```python
from pages.transferencia_page import TransferenciaPage

def transfer_page(driver):
    return TransferenciaPage(driver)

@when(parsers.parse('eu seleciono conta origem “{origem}”'))
def select_origin(transfer_page, origem):
    transfer_page.select_origin(origem)
```

---

## 7️⃣ Running the suite

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run a single feature
pytest features/login.feature

# Show a step‑by‑step trace
pytest -s -vv
```

> **Tip** – For large test suites, use tags (`@login`, `@transfer`) in the Gherkin and filter with `-k`.

---

## 8️⃣ What next?

1. **Implement the page‑object methods** – replace the `pass` statements with Selenium commands.  
2. **Add assertions** – you already have them in the step functions; ensure they capture real UI state.  
3. **Improve data isolation** – use `pytest` fixtures to generate random emails/CPF numbers per test.  
4. **Add parallelism** – `pytest-xdist` to run scenarios concurrently.  
5. **CI integration** – add a GitHub Actions workflow that runs the tests on every push.

With the skeleton above you have a fully‑functional BDD test framework that can be expanded to cover the rest of the ParaBank features in a clean, maintainable way. Happy testing!