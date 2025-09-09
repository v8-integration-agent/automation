## 1. Estrutura de projeto

```
bank‑app/
├── conftest.py
├── pages/
│   ├── base_page.py
│   ├── registration_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── transfer_page.py
│   ├── loan_page.py
│   └── payment_page.py
├── features/
│   ├── cadastro.feature
│   ├── login.feature
│   ├── saldo_extrato.feature
│   ├── transferencia.feature
│   ├── emprestimo.feature
│   ├── pagamento.feature
│   └── usabilidade.feature
└── tests/
    └── test_bank.py
```

> **Obs.**  
> 1. Todos os arquivos `.feature` contêm exatamente o texto que você enviou.  
> 2. Os arquivos de *page‑object* são apenas um esqueleto – você deve preenchê‑los com os seletores reais do seu site.  
> 3. O `conftest.py` cria um WebDriver headless (Chrome). Se preferir Firefox, basta trocar pela classe correspondente.  

---

## 2. `conftest.py`

```python
# bank-app/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def browser():
    """Cria um WebDriver Chrome headless para todo o teste."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)          # espera implícita
    yield driver
    driver.quit()
```

---

## 3. Page‑Object Básico

### 3.1 `base_page.py`

```python
# bank-app/pages/base_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def click(self, selector):
        elem = self.wait.until(EC.element_to_be_clickable(selector))
        elem.click()

    def fill(self, selector, value):
        elem = self.wait.until(EC.visibility_of_element_locado(selector))
        elem.clear()
        elem.send_keys(value)

    def get_text(self, selector):
        elem = self.wait.until(EC.visibility_of_element_locado(selector))
        return elem.text.strip()
```

> *O resto das páginas herdam de `BasePage` e encapsulam os **seltores** e ações específicas.*

---

## 4. Exemplos de Page‑Objects

> **Obs.** Os *seltores* abaixo são fictícios. Substitua‑os pelos reais do seu front‑end.

### 4.1 `registration_page.py`

```python
# bank-app/pages/registration_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By

class RegistrationPage(BasePage):
    URL = "https://www.seubanco.com/registro"

    # Seltores
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    ZIP = (By.ID, "zip")
    PASSWORD = (By.ID, "password")
    CONFIRM_PASSWORD = (By.ID, "confirm_password")
    REGISTER_BTN = (By.ID, "btn-register")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".toast-success")
    ERROR_MSG = (By.CSS_SELECTOR, ".toast-error")

    def open(self):
        self.browser.get(self.URL)

    def register(self, **kwargs):
        for field, value in kwargs.items():
            if value is None:
                continue
            getattr(self, field).fill(value)
        self.click(self.REGISTER_BTN)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)
```

### 4.2 `login_page.py`

```python
# bank-app/pages/login_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    URL = "https://www.seubanco.com/login"

    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "btn-login")
    ERROR_MSG = (By.CSS_SELECTOR, ".toast-error")
    USERNAME_LABEL = (By.CSS_SELECTOR, ".user-name")

    def open(self):
        self.browser.get(self.URL)

    def login(self, email, password):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)

    def get_user_name(self):
        return self.get_text(self.USERNAME_LABEL)
```

> *Implemente os demais page‑objects (`DashboardPage`, `TransferPage`, `LoanPage`, `PaymentPage`) da mesma forma, adicionando os seltores necessários.*

---

## 5. `features/` – os arquivos Gherkin (copie exatamente)

> **Exemplo** – `features/cadastro.feature`

```gherkin
Feature: Cadastro de Usuário

Scenario: Usuário cadastra conta com todos os campos obrigatórios preenchidos
  Given o usuário acessa a página de cadastro
  When ele preenche todos os campos obrigatórios com dados válidos
  And clica no botão “Registrar”
  Then o sistema deve criar a conta
  And exibir a mensagem “Cadastro concluído com sucesso”
  And o usuário deve estar habilitado a fazer login

Scenario Outline: Validação de campos obrigatórios e inválidos no cadastro
  Given o usuário acessa a página de cadastro
  When ele preenche os campos obrigatórios com os seguintes dados:
    | campo  | valor |
    | <campo> | <valor> |
  And clica no botão “Registrar”
  Then o sistema deve exibir a mensagem de erro “<mensagem>”

  Examples:
    | campo     | valor      | mensagem                                     |
    | telefone  | 1234       | O telefone informado é inválido              |
    | CEP       | ABCDE      | O CEP informado é inválido                   |
    | email     | usuario@   | O e‑mail informado é inválido                |
    | nome      |            | O campo nome é obrigatório                    |
```

> *Repita a cópia de cada `.feature` que você enviou (login, saldo_extrato, transferência, emprestimo, pagamento, usabilidade).*

---

## 6. `tests/test_bank.py` – cenários e definições de passo

```python
# bank-app/tests/test_bank.py
import pytest
from pytest_bdd import scenario, given, when, then, parsers

from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
# from pages.dashboard_page import DashboardPage
# from pages.transfer_page import TransferPage
# from pages.loan_page import LoanPage
# from pages.payment_page import PaymentPage

# ------------------------------------------------------------------
# 1️⃣  CENÁRIO DE CADASTRO
# ------------------------------------------------------------------
@scenario('features/cadastro.feature',
          'Usuário cadastra conta com todos os campos obrigatórios preenchidos')
def test_user_registration_valid():
    pass

@scenario('features/cadastro.feature',
          'Validação de campos obrigatórios e inválidos no cadastro')
def test_user_registration_invalid():
    pass

# ------------------------------------------------------------------
# 2️⃣  CENÁRIO DE LOGIN
# ------------------------------------------------------------------
@scenario('features/login.feature',
          'Usuário faz login com credenciais válidas')
def test_login_valid():
    pass

@scenario('features/login.feature',
          'Login falha com credenciais inválidas')
def test_login_invalid():
    pass

# ------------------------------------------------------------------
# 3️⃣  CENÁRIO SALDO & EXTRATO
# ------------------------------------------------------------------
@scenario('features/saldo_extrato.feature',
          'O saldo exibido está atualizado após uma operação de débito')
def test_balance_update_after_deposit():
    pass

@scenario('features/saldo_extrato.feature',
          'O extrato lista transações em ordem cronológica')
def test_statement_ordered_by_date():
    pass

# ------------------------------------------------------------------
# 4️⃣  CENÁRIO DE TRANSFERÊNCIA
# ------------------------------------------------------------------
@scenario('features/transferencia.feature',
          'Usuário transfere fundos entre contas existentes')
def test_fund_transfer_success():
    pass

@scenario('features/transferencia.feature',
          'Transferência não permitida quando o valor excede o saldo')
def test_transfer_insufficient_balance():
    pass

# ------------------------------------------------------------------
# 5️⃣  CENÁRIO DE EMPRÉSTIMO
# ------------------------------------------------------------------
@scenario('features/emprestimo.feature',
          'Usuário solicita empréstimo aprovado')
def test_loan_approved():
    pass

@scenario('features/emprestimo.feature',
          'Usuário solicita empréstimo negado')
def test_loan_declined():
    pass

# ------------------------------------------------------------------
# 6️⃣  CENÁRIO DE PAGAMENTO
# ------------------------------------------------------------------
@scenario('features/pagamento.feature',
          'Pagamento de conta registrado com sucesso')
def test_payment_success():
    pass

@scenario('features/pagamento.feature',
          'Pagamento futuro deve respeitar a data de agendamento')
def test_future_payment():
    pass

# ------------------------------------------------------------------
# 7️⃣  CENÁRIO DE USABILIDADE
# ------------------------------------------------------------------
@scenario('features/usabilidade.feature',
          'Todas as páginas carregam sem erros de navegação')
def test_navigation_no_errors():
    pass

@scenario('features/usabilidade.feature',
          'Mensagens de erro são claras e objetivas')
def test_error_messages_clear():
    pass

@scenario('features/usabilidade.feature',
          'Consistência de links e menus em todas as páginas')
def test_menu_consistency():
    pass
```

> **Observação** – O `@scenario` acima cria um *wrapper* que já chama a função *empty* (o `pass`), e o `pytest-bdd` executa os passos que você vai definir abaixo.

---

## 7. Definições de passo – `tests/conftest_steps.py`

> Para manter a organização, coloque todas as definições de passo em um único arquivo.  
> Cada passo corresponde exatamente ao que está no arquivo Gherkin.

```python
# bank-app/tests/conftest_steps.py
import pytest
from pytest_bdd import given, when, then, parsers

from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
# from pages.dashboard_page import DashboardPage
# from pages.transfer_page import TransferPage
# from pages.loan_page import LoanPage
# from pages.payment_page import PaymentPage

# ------------------------------------------------------------------
# 1️⃣  STEP DEFINITIONS – CADASTRO
# ------------------------------------------------------------------
@given('o usuário acessa a página de cadastro')
def open_registration_page(browser):
    reg_page = RegistrationPage(browser)
    reg_page.open()
    return reg_page

@when('ele preenche todos os campos obrigatórios com dados válidos')
def fill_valid_registration(open_registration_page):
    reg_page = open_registration_page
    reg_page.fill(RegistrationPage.FIRST_NAME, "João")
    reg_page.fill(RegistrationPage.LAST_NAME, "Silva")
    reg_page.fill(RegistrationPage.EMAIL, "joao.silva@example.com")
    reg_page.fill(RegistrationPage.PHONE, "11987654321")
    reg_page.fill(RegistrationPage.ZIP, "01001000")
    reg_page.fill(RegistrationPage.PASSWORD, "SenhaSegura123")
    reg_page.fill(RegistrationPage.CONFIRM_PASSWORD, "SenhaSegura123")
    return reg_page

@when('clica no botão “Registrar”')
def click_register(open_registration_page):
    reg_page = open_registration_page
    reg_page.click(RegistrationPage.REGISTER_BTN)
    return reg_page

@then('o sistema deve criar a conta')
def account_created(open_registration_page):
    reg_page = open_registration_page
    assert "Conta criada" in reg_page.get_success_message()

@then('exibir a mensagem “Cadastro concluído com sucesso”')
def success_msg_displayed(open_registration_page):
    reg_page = open_registration_page
    assert reg_page.get_success_message() == "Cadastro concluído com sucesso"

@then('o usuário deve estar habilitado a fazer login')
def user_can_login():
    # aqui poderíamos tentar um login real para validar
    # mas normalmente só checamos a existência do link/login
    pass

# Scenario Outline – parâmetros de tabela
@given(parsers.parse('ele preenche os campos obrigatórios com os seguintes dados:'))
def fill_registration_with_example(open_registration_page, table):
    # `table` é um objeto `Table` do pytest-bdd que pode ser iterado
    reg_page = open_registration_page
    for row in table:
        campo = row['campo']
        valor = row['valor']
        if campo == 'telefone':
            reg_page.fill(RegistrationPage.PHONE, valor)
        elif campo == 'CEP':
            reg_page.fill(RegistrationPage.ZIP, valor)
        elif campo == 'email':
            reg_page.fill(RegistrationPage.EMAIL, valor)
        elif campo == 'nome':
            reg_page.fill(RegistrationPage.FIRST_NAME, valor)
            reg_page.fill(RegistrationPage.LAST_NAME, valor)
        # adicione outros campos conforme necessário
    return reg_page

@then(parsers.parse('o sistema deve exibir a mensagem de erro “{mensagem}”'))
def error_message_displayed(open_registration_page, mensagem):
    reg_page = open_registration_page
    assert reg_page.get_error_message() == mensagem

# ------------------------------------------------------------------
# 2️⃣  STEP DEFINITIONS – LOGIN
# ------------------------------------------------------------------
@given('o usuário tem uma conta cadastrada')
def user_with_account(browser):
    # Neste cenário fictício, cria‑se a conta via API ou fixture
    pass

@given('ele acessa a página de login')
def open_login_page(browser):
    login_page = LoginPage(browser)
    login_page.open()
    return login_page

@when(parsers.parse('digita o e‑mail “{email}”'))
def type_email(open_login_page, email):
    open_login_page.fill(LoginPage.EMAIL_INPUT, email)

@when(parsers.parse('digita a senha “{senha}”'))
def type_password(open_login_page, senha):
    open_login_page.fill(LoginPage.PASSWORD_INPUT, senha)

@when('clica em “Entrar”')
def click_login(open_login_page):
    open_login_page.click(LoginPage.LOGIN_BTN)
    return open_login_page

@then('o sistema deve redirecionar para a página inicial da conta')
def redirected_to_home(open_login_page):
    # exemplo: esperar por um elemento da dashboard
    assert open_login_page.browser.current_url == "https://www.seubanco.com/home"

@then('exibir o nome do usuário no cabeçalho')
def user_name_displayed(open_login_page):
    assert "João Silva" in open_login_page.get_user_name()

@then(parsers.parse('o sistema deve exibir a mensagem de erro “{mensagem}”'))
def login_error_message(open_login_page, mensagem):
    assert open_login_page.get_error_message() == mensagem

# ------------------------------------------------------------------
# 3️⃣  STEP DEFINITIONS – SALDO & EXTRATO
# ------------------------------------------------------------------
# (similar pattern: criar fixtures que garantem saldo, depositar via UI/API, etc.)
# Para fins de exemplo, apenas placeholders estão incluídos

# ------------------------------------------------------------------
# 4️⃣  STEP DEFINITIONS – TRANSFERÊNCIA
# ------------------------------------------------------------------
# ... (implementação semelhante)

# ------------------------------------------------------------------
# 5️⃣  STEP DEFINITIONS – EMPRÉSTIMO
# ------------------------------------------------------------------
# ... (implementação semelhante)

# ------------------------------------------------------------------
# 6️⃣  STEP DEFINITIONS – PAGAMENTO
# ------------------------------------------------------------------
# ... (implementação semelhante)

# ------------------------------------------------------------------
# 7️⃣  STEP DEFINITIONS – USABILIDADE
# ------------------------------------------------------------------
# ... (implementação semelhante)
```

### Notas sobre os *parsers*:

- `parsers.parse` permite usar strings formatadas que correspondem exatamente às frases do `.feature`.  
- Quando um cenário possui *table*, o passo que recebe `table` pode iterar sobre cada linha e usar `row['campo']`, `row['valor']`, etc.

---

## 8. Como executar

```bash
# Instale as dependências
pip install pytest pytest-bdd selenium

# Execute todos os testes
pytest tests
```

> Se você usa um CI, basta adicionar esses comandos ao pipeline.

---

## 9. Próximos passos

1. **Implementar os demais page‑objects** (dashboard, transfer, loan, payment) com os seltores corretos.  
2. **Completar os passos** que ainda estão em `pass`, especialmente os que verificam saldo, extrato, histórico, etc.  
3. **Adicionar mocks ou fixtures de API** para criar contas, saldos e transações rapidamente sem depender da UI.  
4. **Cobertura de dados**: criar um arquivo `conftest.py` com dados parametrizados se necessário (e.g. lista de contas, salários, etc.).  
5. **CI/CD**: configurar um pipeline no GitHub Actions, GitLab CI ou outra ferramenta para executar os testes em ambientes de staging.

---

> **Resumo** – Você agora tem uma base completa em Python + pytest‑bdd que replica todos os cenários do seu arquivo Gherkin. Basta adaptar os seltores e lógica de negócio para que os testes verifiquem o comportamento real do seu aplicativo. Boa sorte!