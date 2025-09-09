**What you’ll get**

| Folder | Purpose |
|--------|---------|
| `features/` | All Gherkin `.feature` files (exact copy of what you pasted). |
| `tests/` | A `conftest.py` that creates a Selenium WebDriver fixture and a `steps/` package with all step‑definitions. |
| `tests/steps/` | One Python module per feature (or a single module – both work). Each module contains `@given`, `@when`, `@then` steps that match the Gherkin phrases. |
| `tests/pages/` | (Optional) Page‑Object skeletons that the steps call – you can replace the `TODO` blocks with real Selenium code. |

Below is a **ready‑to‑copy** skeleton.  
Copy each block into a file with the name shown in the comment, then run `pytest` (make sure you have `pytest‑bdd` and `selenium` installed).

---

## 1. Feature files (`features/*.feature`)

> **NOTE** – The features are *exactly* what you posted; only minor formatting changes were made for readability.

```gherkin
# features/cadastro.feature
Feature: Cadastro de Usuário

Scenario: Usuário cadastra conta com todos os campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche os campos: nome="Ana Silva", email="ana.silva@example.com", telefone="(11) 98765‑4321", CEP="01234‑567", endereço="Rua A, 123"
  And clica em “Cadastrar”
  Then o sistema exibe a mensagem de confirmação “Cadastro concluído com sucesso”
  And o usuário pode fazer login com as credenciais recém‑criadas

Scenario Outline: Usuário tenta cadastrar conta com campo inválido
  Given o usuário acessa a página de cadastro
  When ele preenche os campos: nome="<nome>", email="<email>", telefone="<telefone>", CEP="<cep>", endereço="Rua A, 123"
  And clica em “Cadastrar”
  Then o sistema exibe a mensagem de erro "<mensagem_erro>"
  And a conta não é criada

  Examples:
    | nome | email               | telefone | cep      | mensagem_erro                                 |
    |      | ana.silva@ex.com    | (11)9876 | 01234-567| "Nome é obrigatório"                          |
    | Ana  | anasilvaexample.com | (11)9876 | 01234-567| "Email inválido"                              |
    | Ana  | ana.silva@ex.com    | 111111   | 01234-567| "Telefone inválido"                           |
    | Ana  | ana.silva@ex.com    | (11)98765-4321 | 0123-567 | "CEP inválido"                                 |
```

```gherkin
# features/login.feature
Feature: Login

Scenario: Usuário faz login com credenciais válidas
  Given o usuário está na página de login
  When ele insere o email "<email>" e a senha "<senha>"
  And clica em “Login”
  Then o usuário é redirecionado para a página inicial da conta
  And o banner de boas‑vindas exibe “Bem‑vindo, <nome>”

  Examples:
    | email                      | senha  | nome |
    | ana.silva@example.com | 123456 | Ana  |

Scenario: Usuário tenta login com credenciais inválidas
  Given o usuário está na página de login
  When ele insere o email "<email>" e a senha "<senha>"
  And clica em “Login”
  Then o sistema exibe a mensagem de erro “Credenciais inválidas”
  And permanece na página de login
```

```gherkin
# features/acesso.feature
Feature: Acesso à aplicação bancária (Saldo e Extrato)

Scenario: Usuário visualiza saldo atualizado após operação
  Given o usuário está autenticado
  When ele realiza a operação de “Transferência” de R$100,00
  And volta à tela principal
  Then o saldo exibido deve ser “R$<saldo_atualizado>”

Scenario: Usuário visualiza extrato em ordem cronológica
  Given o usuário está autenticado
  When ele acessa a aba “Extrato”
  Then o extrato lista as transações recentes em ordem decrescente de data
  And cada linha exibe data, descrição, valor e saldo final
```

```gherkin
# features/transferencia.feature
Feature: Transferência de Fundos

Scenario: Usuário transfere fundos entre contas válidas
  Given o usuário está autenticado
  And a conta “Corrente” tem saldo de R$500,00
  When ele seleciona a origem “Corrente”, destino “Poupança” e valor “R$200,00”
  And confirma a transferência
  Then o saldo da conta “Corrente” é de R$300,00
  And o saldo da conta “Poupança” é de R$200,00
  And a transação aparece no histórico de ambas as contas

Scenario Outline: Transferência não permitida por saldo insuficiente
  Given o usuário está autenticado
  And a conta “Corrente” tem saldo de R$<saldo>
  When ele tenta transferir R$<valor> da “Corrente” para “Poupança”
  Then o sistema exibe a mensagem de erro “Saldo insuficiente para esta transferência”
  And a conta não é debitada

  Examples:
    | saldo | valor |
    | 300   | 400   |
    | 100   | 101   |
```

```gherkin
# features/emprestimo.feature
Feature: Solicitação de Empréstimo

Scenario: Usuário solicita empréstimo e recebe aprovação
  Given o usuário está autenticado
  When ele insere valor do empréstimo “R$10.000,00” e renda anual “R$80.000,00”
  And submete a solicitação
  Then o sistema exibe “Status: Aprovado”

Scenario: Usuário solicita empréstimo e recebe negação
  Given o usuário está autenticado
  When ele insere valor do empréstimo “R$50.000,00” e renda anual “R$30.000,00”
  And submete a solicitação
  Then o sistema exibe “Status: Negado”
```

```gherkin
# features/pagamento.feature
Feature: Pagamento de Contas

Scenario: Usuário registra pagamento de conta com dados completos
  Given o usuário está autenticado
  When ele preenche: beneficiário="Empresa XYZ", endereço="Av. B, 200", cidade="São Paulo", estado="SP", CEP="01000‑000", telefone="(11) 91234‑5678", conta="1234-5", valor="R$250,00", data="2025‑10‑01"
  And confirma o pagamento
  Then o sistema registra “Pagamento confirmado”
  And o pagamento aparece no histórico de transações
  And a conta de destino é debitada do valor correspondente

Scenario: Pagamento futuro respeita data de agendamento
  Given o usuário está autenticado
  When ele agenda pagamento de R$150,00 para “2025‑12‑15”
  And confirma
  Then o sistema exibe “Pagamento agendado para 15/12/2025”
  And o pagamento só aparece no histórico após a data agendada
```

```gherkin
# features/requisitos_generais.feature
Feature: Requisitos Gerais de Navegação e Usabilidade

Scenario: Todas as páginas carregam sem erros de navegação
  Given o usuário está autenticado
  When ele navega entre todas as páginas principais: “Conta”, “Transferência”, “Extrato”, “Empréstimo”, “Pagamento”
  Then cada página carrega sem erros ou mensagens de “404”

Scenario: Mensagens de erro são claras e objetivas
  Given o usuário tenta cadastrar conta com telefone inválido
  When ele submete o formulário
  Then a mensagem exibida deve ser “Telefone inválido. Use o formato (xx) xxxxx‑xxxx”

Scenario: Menus e links são consistentes em todas as páginas
  Given o usuário está em qualquer página do ParaBank
  When ele verifica o menu de navegação
  Then ele encontra os mesmos itens: “Conta”, “Transferência”, “Extrato”, “Empréstimo”, “Pagamento”, “Sair”
  And os links redirecionam para as páginas corretas
```

---

## 2. `conftest.py` – Selenium fixture

```python
# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    """Instantiate a Chrome WebDriver once per test session."""
    options = Options()
    options.add_argument("--headless")          # remove if you want a visible browser
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options)
    driver.implicitly_wait(10)  # seconds
    yield driver
    driver.quit()
```

---

## 3. Page‑Object skeleton (optional but recommended)

> Put this under `tests/pages/`.

```python
# tests/pages/base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def click(self, locator):
        self.driver.find_element(*locator).click()

    def type(self, locator, text):
        elem = self.driver.find_element(*locator)
        elem.clear()
        elem.send_keys(text)

    def get_text(self, locator):
        return self.driver.find_element(*locator).text
```

> You can extend this with `CadastroPage`, `LoginPage`, `DashboardPage`, etc.  
> For brevity, the step‑definitions below use raw Selenium calls – replace the `TODO` comments with your own page‑object methods when you build the real test suite.

---

## 4. Step‑definitions

Below is a **single** `steps/steps.py` that contains all steps.  
Feel free to split them into separate files (`cadastro_steps.py`, `login_steps.py`, …) – pytest‑bdd will still find them.

```python
# tests/steps/steps.py
import re
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By

# ---------- Helpers ----------
def parse_currency(value):
    """Converts a string like 'R$1.200,00' to a float."""
    return float(value.replace('R$', '').replace('.', '').replace(',', '.'))

# ---------- Cadastro Steps ----------
@given(parsers.parse('o usuário acessa a página de cadastro'))
def open_cadastro_page(driver):
    driver.get("https://www.parabank.com/signup.htm")  # replace with real URL

@when(parsers.parse('ele preenche os campos: nome="{nome}", email="{email}", telefone="{telefone}", CEP="{cep}", endereço="{endereco}"'))
def preenche_campos_cadastro(driver, nome, email, telefone, cep, endereco):
    # TODO: Replace the locators with the real ones.
    driver.find_element(By.ID, "name").send_keys(nome)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(telefone)
    driver.find_element(By.ID, "zip").send_keys(cep)
    driver.find_element(By.ID, "address").send_keys(endereco)

@when(parsers.parse('clica em “Cadastrar”'))
def clicar_cadastrar(driver):
    driver.find_element(By.ID, "registerBtn").click()

@then(parsers.parse('o sistema exibe a mensagem de confirmação “{msg}”'))
def verifica_mensagem_confirmacao(driver, msg):
    alert = driver.find_element(By.CLASS_NAME, "success-msg")
    assert msg in alert.text

@then(parsers.parse('o usuário pode fazer login com as credenciais recém‑criadas'))
def verifica_login_pos_cadastro(driver):
    driver.find_element(By.ID, "logoutBtn").click()
    driver.find_element(By.ID, "loginBtn").click()
    # Assert that we reach the dashboard
    assert "Welcome" in driver.title

# ---------- Login Steps ----------
@given(parsers.parse('o usuário está na página de login'))
def open_login_page(driver):
    driver.get("https://www.parabank.com/login.htm")  # replace

@when(parsers.parse('ele insere o email "{email}" e a senha "{senha}"'))
def insere_login(driver, email, senha):
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(senha)

@when(parsers.parse('clica em “Login”'))
def clicar_login(driver):
    driver.find_element(By.ID, "loginBtn").click()

@then(parsers.parse('o usuário é redirecionado para a página inicial da conta'))
def verifica_redirecionamento(driver):
    assert "Dashboard" in driver.title

@then(parsers.parse('o banner de boas‑vindas exibe “Bem‑vindo, {nome}”'))
def verifica_banner_boas_vindas(driver, nome):
    banner = driver.find_element(By.ID, "welcomeBanner")
    assert f"Bem‑vindo, {nome}" in banner.text

@then(parsers.parse('o sistema exibe a mensagem de erro “{msg}”'))
def verifica_mensagem_erro(driver, msg):
    alert = driver.find_element(By.CLASS_NAME, "error-msg")
    assert msg in alert.text

@then(parsers.parse('permanece na página de login'))
def permanece_login(driver):
    assert "Login" in driver.title

# ---------- Acesso (Saldo/Extrato) ----------
@given(parsers.parse('o usuário está autenticado'))
def ensure_authenticated(driver):
    # This is a stub – implement real login if needed
    if "login" in driver.current_url:
        open_login_page(driver)
        insere_login(driver, "ana.silva@example.com", "123456")
        clicar_login(driver)

@when(parsers.parse('ele realiza a operação de “Transferência” de R${valor:float}'))
def realiza_transferencia(driver, valor):
    driver.find_element(By.LINK_TEXT, "Transferência").click()
    driver.find_element(By.ID, "amount").send_keys(str(valor))
    driver.find_element(By.ID, "transferBtn").click()

@when(parsers.parse('volta à tela principal'))
def volta_tela_principal(driver):
    driver.find_element(By.ID, "homeBtn").click()

@then(parsers.parse('o saldo exibido deve ser “R$<saldo>”'))
def verifica_saldo(driver, saldo):
    saldo_elem = driver.find_element(By.ID, "balance")
    assert parse_currency(saldo_elem.text) == parse_currency(saldo)

@when(parsers.parse('ele acessa a aba “Extrato”'))
def acessa_extrato(driver):
    driver.find_element(By.LINK_TEXT, "Extrato").click()

@then(parsers.parse('o extrato lista as transações recentes em ordem decrescente de data'))
def verifica_ordenacao_extrato(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "table#transactions tbody tr")
    datas = [row.find_element(By.CSS_SELECTOR, "td.date").text for row in rows]
    assert datas == sorted(datas, reverse=True)

@then(parsers.parse('cada linha exibe data, descrição, valor e saldo final'))
def verifica_colunas_extrato(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "table#transactions tbody tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        assert len(cells) == 4  # date, description, value, balance

# ---------- Transferência de Fundos ----------
@given(parsers.parse('a conta “Corrente” tem saldo de R${saldo:float}'))
def set_saldo_corrente(driver, saldo):
    # Stub – in a real test you would adjust the account via API or UI
    driver.execute_script(f"window.localStorage.setItem('corrente_balance', '{saldo}');")

@when(parsers.parse('ele seleciona a origem “{origem}”, destino “{destino}” e valor “R${valor:float}”'))
def selecionar_transferencia(driver, origem, destino, valor):
    driver.find_element(By.ID, "sourceAccount").send_keys(origem)
    driver.find_element(By.ID, "destinationAccount").send_keys(destino)
    driver.find_element(By.ID, "transferAmount").send_keys(str(valor))

@when(parsers.parse('confirma a transferência'))
def confirma_transferencia(driver):
    driver.find_element(By.ID, "confirmTransferBtn").click()

@then(parsers.parse('o saldo da conta “{conta}” é de R${valor:float}'))
def verifica_saldo_conta(driver, conta, valor):
    balance = driver.execute_script(f"return window.localStorage.getItem('{conta}_balance');")
    assert float(balance) == valor

@then(parsers.parse('a transação aparece no histórico de ambas as contas'))
def verifica_historia(driver):
    # Stub – implement actual verification
    driver.find_element(By.LINK_TEXT, "Histórico").click()
    rows = driver.find_elements(By.CSS_SELECTOR, "table#history tbody tr")
    assert any("Transferência" in row.text for row in rows)

@when(parsers.parse('ele tenta transferir R${valor:float} da “{origem}” para “{destino}”'))
def tenta_transferir_insuficiente(driver, valor, origem, destino):
    driver.find_element(By.LINK_TEXT, "Transferência").click()
    driver.find_element(By.ID, "sourceAccount").send_keys(origem)
    driver.find_element(By.ID, "destinationAccount").send_keys(destino)
    driver.find_element(By.ID, "transferAmount").send_keys(str(valor))

@then(parsers.parse('o sistema exibe a mensagem de erro “{msg}”'))
def verifica_mensagem_erro_transferencia(driver, msg):
    alert = driver.find_element(By.CLASS_NAME, "error-msg")
    assert msg in alert.text

# ---------- Empréstimo ----------
@when(parsers.parse('ele insere valor do empréstimo “{valor}” e renda anual “{renda}”'))
def insere_emprestimo(driver, valor, renda):
    driver.find_element(By.ID, "loanAmount").send_keys(valor.replace("R$", "").replace(".", "").replace(",", "."))
    driver.find_element(By.ID, "annualIncome").send_keys(renda.replace("R$", "").replace(".", "").replace(",", "."))

@when(parsers.parse('submete a solicitação'))
def submete_emprestimo(driver):
    driver.find_element(By.ID, "submitLoanBtn").click()

@then(parsers.parse('o sistema exibe “Status: {status}”'))
def verifica_status_emprestimo(driver, status):
    status_elem = driver.find_element(By.ID, "loanStatus")
    assert status in status_elem.text

# ---------- Pagamento ----------
@when(parsers.parse('ele preenche: beneficiário="{beneficiario}", endereço="{endereco}", cidade="{cidade}", estado="{estado}", CEP="{cep}", telefone="{telefone}", conta="{conta}", valor="{valor}", data="{data}"'))
def preenche_pagamento(driver, beneficiario, endereco, cidade, estado, cep, telefone, conta, valor, data):
    driver.find_element(By.ID, "beneficiary").send_keys(beneficiario)
    driver.find_element(By.ID, "address").send_keys(endereco)
    driver.find_element(By.ID, "city").send_keys(cidade)
    driver.find_element(By.ID, "state").send_keys(estado)
    driver.find_element(By.ID, "zip").send_keys(cep)
    driver.find_element(By.ID, "phone").send_keys(telefone)
    driver.find_element(By.ID, "account").send_keys(conta)
    driver.find_element(By.ID, "amount").send_keys(valor.replace("R$", "").replace(".", "").replace(",", "."))
    driver.find_element(By.ID, "dueDate").send_keys(data)

@when(parsers.parse('confirma o pagamento'))
def confirma_pagamento(driver):
    driver.find_element(By.ID, "confirmPaymentBtn").click()

@then(parsers.parse('o sistema registra “{msg}”'))
def verifica_pagamento_confirmado(driver, msg):
    alert = driver.find_element(By.CLASS_NAME, "success-msg")
    assert msg in alert.text

@then(parsers.parse('o pagamento aparece no histórico de transações'))
def verifica_pagamento_historia(driver):
    driver.find_element(By.LINK_TEXT, "Histórico").click()
    rows = driver.find_elements(By.CSS_SELECTOR, "table#payments tbody tr")
    assert any("Empresa XYZ" in row.text for row in rows)

@when(parsers.parse('ele agenda pagamento de R${valor:float} para “{data}”'))
def agenda_pagamento(driver, valor, data):
    driver.find_element(By.ID, "scheduledPaymentBtn").click()
    driver.find_element(By.ID, "amount").send_keys(str(valor))
    driver.find_element(By.ID, "dueDate").send_keys(data)

@then(parsers.parse('o sistema exibe “{msg}”'))
def verifica_mensagem_agendamento(driver, msg):
    alert = driver.find_element(By.CLASS_NAME, "success-msg")
    assert msg in alert.text

# ---------- Navegação e Usabilidade ----------
@when(parsers.parse('ele navega entre todas as páginas principais: “{paginas}”'))
def navega_paginas(driver, paginas):
    pages = re.split(r'[,"]+', paginas)
    for p in pages:
        p = p.strip()
        if p:
            driver.find_element(By.LINK_TEXT, p).click()
            assert f"{p} - ParaBank" in driver.title  # simple check

@then(parsers.parse('cada página carrega sem erros ou mensagens de “404”'))
def verifica_paginas_ok(driver):
    body = driver.find_element(By.TAG_NAME, "body")
    assert "404" not in body.text

@when(parsers.parse('ele submete o formulário'))
def submete_formulario(driver):
    driver.find_element(By.ID, "submitBtn").click()

@when(parsers.parse('ele verifica o menu de navegação'))
def verifica_menu(driver):
    menu_items = driver.find_elements(By.CSS_SELECTOR, "ul#nav li a")
    items = [item.text for item in menu_items]
    expected = ["Conta", "Transferência", "Extrato", "Empréstimo", "Pagamento", "Sair"]
    assert all(e in items for e in expected)
```

---

## 5. Running the tests

1. Install dependencies:

```bash
pip install pytest pytest-bdd selenium webdriver-manager
```

2. Run the suite:

```bash
pytest
```

Pytest will automatically discover the `.feature` files and the matching step definitions, executing each scenario (including the Scenario Outlines, which will be expanded into individual test cases).  
If you prefer to run a *single* feature, use:

```bash
pytest features/cadastro.feature
```

---

## 6. Tips for a real test suite

| What | How |
|------|-----|
| **Real URLs** | Replace the placeholder URLs with the actual ParaBank test environment. |
| **Locators** | Switch the dummy `By.ID`/`By.LINK_TEXT` locators to the real ones from your application. |
| **Page Objects** | Wrap every page interaction in a class (`CadastroPage`, `LoginPage`, …) – keeps the steps readable. |
| **Test Data** | Store the example data in a separate fixture or a JSON file and load it in `conftest.py`. |
| **Parallelism** | Use `pytest-xdist` (`pytest -n auto`) to run scenarios in parallel; you’ll need to make the `driver` fixture `scope='function'`. |
| **Reporting** | Add `pytest-html` or `Allure` for rich test reports. |
| **Continuous Integration** | Add the `pytest` command to your CI pipeline (GitHub Actions, GitLab CI, Jenkins, etc.). |

Happy testing! 🎉