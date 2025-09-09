## 1.  Estrutura de diretórios recomendada  

```
paraBank/
├── conftest.py                     # Fixtures globais (driver, db, etc.)
├── features/
│   ├── registration.feature        # Cadastro de Usuário
│   ├── login.feature               # Login
│   ├── account.feature             # Saldo & Extrato
│   ├── transfer.feature            # Transferência de Fundos
│   ├── loan.feature                # Solicitação de Empréstimo
│   ├── payment.feature             # Pagamento de Contas
│   └── navigation.feature          # Navegação e Usabilidade
└── steps/
    ├── registration_steps.py
    ├── login_steps.py
    ├── account_steps.py
    ├── transfer_steps.py
    ├── loan_steps.py
    ├── payment_steps.py
    └── navigation_steps.py
```

> **Obs.:**  
>  * Os arquivos `.feature` são copiados exatamente como o Gherkin acima.  
>  * Para cada feature criamos um arquivo de passos correspondente.  
>  * `conftest.py` pode conter fixtures de Selenium (WebDriver), banco de dados ou mocks.

---

## 2.  `conftest.py` – Fixtures básicas (Selenium + Pytest‑BDD)

```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    """Instancia o WebDriver uma única vez por sessão."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")   # Remove se quiser visualizar o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return "http://localhost:8000"   # URL de teste da aplicação ParaBank
```

> **Dica:**  
> Se a aplicação for apenas uma API, troque o driver por um cliente `requests` e adapte os passos.

---

## 3.  Feature Files (exemplo de `registration.feature`)

```gherkin
# features/registration.feature
Feature: Cadastro de Usuário
  Para que novos clientes possam utilizar o ParaBank, o sistema deve permitir a criação de contas com todos os campos obrigatórios preenchidos e validar os dados de entrada.

  Scenario: Cadastro bem‑sucedido com dados válidos
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com “Ana Silva”
    And preenche "Email" com “ana.silva@example.com”
    And preenche "Telefone" com “(11) 91234-5678”
    And preenche "CEP" com “01001-000”
    And preenche "Senha" com “Password123”
    And confirma a senha com “Password123”
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Cadastro concluído com sucesso.”
    And o usuário deve ser redirecionado para a tela de login

  Scenario Outline: Cadastro falha com campos obrigatórios vazios
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com "<nome>"
    And preenche "Email" com "<email>"
    And preenche "Telefone" com "<telefone>"
    And preenche "CEP" com "<cep>"
    And preenche "Senha" com "<senha>"
    And confirma a senha com "<confirmação>"
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “<mensagem>”

    Examples:
      | nome | email                | telefone | cep       | senha      | confirmação | mensagem                                  |
      |      | ana.silva@example.com | (11) 91234-5678 | 01001-000 | Password123 | Password123 | Nome é obrigatório                         |
      | Ana  |                       | (11) 91234-5678 | 01001-000 | Password123 | Password123 | Email é obrigatório                        |
      | Ana  | ana.silva@example.com |           | 01001-000 | Password123 | Password123 | Telefone é obrigatório                     |
      | Ana  | ana.silva@example.com | (11) 91234-5678 |           | Password123 | Password123 | CEP é obrigatório                          |
      | Ana  | ana.silva@example.com | (11) 91234-5678 | 01001-000 |            |            | Senha e confirmação são obrigatórias      |

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a tela de registro
    When ele preenche "Nome" com “Ana Silva”
    And preenche "Email" com "<email>"
    And preenche "Telefone" com "<telefone>"
    And preenche "CEP" com "<cep>"
    And preenche "Senha" com “Password123”
    And confirma a senha com “Password123”
    And clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “<mensagem>”

    Examples:
      | email                   | telefone       | cep       | mensagem                                   |
      | ana.silvaexample.com    | (11) 91234-5678 | 01001-000 | Email inválido                             |
      | ana.silva@example.com   | 912345678       | 01001-000 | Telefone inválido                          |
      | ana.silva@example.com   | (11) 91234-5678 | 01         | CEP inválido                               |
```

> **Observação:**  
> Copie o mesmo padrão para os demais arquivos `.feature`.  

---

## 4.  Passos – Exemplo: `registration_steps.py`

```python
# steps/registration_steps.py
import re
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------  CARGA DO FEATURE --------------------
scenarios("../features/registration.feature")

# --------------------  UTILITÁRIOS -------------------------
def find(driver, locator):
    """Abstração de busca para melhorar legibilidade."""
    return driver.find_element(*locator)

def wait_for_text(driver, text, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
    )

# --------------------  GIVEN --------------------
@given("o usuário acessa a tela de registro")
def access_registration_page(driver, base_url):
    driver.get(f"{base_url}/register")
    assert driver.title == "Registro – ParaBank"

# --------------------  WHEN --------------------
@when(parsers.cfparse('ele preenche "{field}" com "{value}"'))
def fill_field(driver, field, value):
    locators = {
        "Nome": (By.ID, "id_name"),
        "Email": (By.ID, "id_email"),
        "Telefone": (By.ID, "id_phone"),
        "CEP": (By.ID, "id_cep"),
        "Senha": (By.ID, "id_password"),
    }
    element = find(driver, locators[field])
    element.clear()
    element.send_keys(value)

@when(parsers.cfparse('confirma a senha com "{value}"'))
def confirm_password(driver, value):
    element = find(driver, (By.ID, "id_password_confirm"))
    element.clear()
    element.send_keys(value)

@when(parsers.cfparse('clica em "{button}"'))
def click_button(driver, button):
    button_map = {
        "Cadastrar": (By.XPATH, "//button[contains(text(), 'Cadastrar')]"),
        "Entrar": (By.XPATH, "//button[contains(text(), 'Entrar')]"),
    }
    find(driver, button_map[button]).click()

# --------------------  THEN --------------------
@then(parsers.cfparse('o sistema deve exibir a mensagem "{message}"'))
def verify_message(driver, message):
    wait_for_text(driver, message)
    body = driver.find_element(By.TAG_NAME, "body").text
    assert message in body

@then(parsers.cfparse('o usuário deve ser redirecionado para a tela de login'))
def check_login_redirect(driver, base_url):
    WebDriverWait(driver, 5).until(EC.url_contains("/login"))
    assert driver.current_url.endswith("/login")
```

> **Explicação rápida:**
> * `scenarios()` importa automaticamente o arquivo de feature.  
> * Usamos `parsers.cfparse()` para extrair parâmetros de steps em português.  
> * As localizações (`ID`, `XPATH`) são placeholders – substitua pelos valores corretos da sua aplicação.  
> * `wait_for_text()` garante que o texto apareça antes do `assert`.

---

## 5.  Passos – `login_steps.py`

```python
# steps/login_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scenarios("../features/login.feature")

@given("o usuário está na página de login")
def access_login_page(driver, base_url):
    driver.get(f"{base_url}/login")
    assert "Login – ParaBank" in driver.title

@when(parsers.cfparse('ele insere "{field}" com "{value}"'))
def insert_field(driver, field, value):
    locators = {"Username": (By.ID, "id_username"),
                "Password": (By.ID, "id_password")}
    find(driver, locators[field]).clear()
    find(driver, locators[field]).send_keys(value)

@then(parsers.cfparse('o sistema deve redirecionar para a página inicial da conta'))
def redirect_to_home(driver, base_url):
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))
    assert driver.current_url.endswith("/dashboard")

@then(parsers.cfparse('exibir "{message}"'))
def verify_welcome(driver, message):
    body = driver.find_element(By.TAG_NAME, "body").text
    assert message in body
```

---

## 6.  Passos – `account_steps.py` (Saldo & Extrato)

```python
# steps/account_steps.py
import pytest
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scenarios("../features/account.feature")

@when(parsers.cfparse('ele faz um depósito de {value}'))
def deposit_money(driver, value):
    # Ex.: "R$ 1.000,00" -> 1000.00
    amount = float(value.replace("R$", "").replace(".", "").replace(",", ".").strip())
    driver.find_element(By.ID, "id_deposit").send_keys(str(amount))
    driver.find_element(By.ID, "id_deposit_btn").click()

@then(parsers.cfparse('o saldo deve ser {value}'))
def verify_balance(driver, value):
    amount = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    balance_text = driver.find_element(By.ID, "id_balance").text
    assert balance_text == f"R$ {float(amount):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@then(parsers.cfparse('o extrato deve mostrar as transações em ordem decrescente de data'))
def check_statement_order(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")
    dates = [row.find_element(By.CSS_SELECTOR, ".date").text for row in rows]
    assert dates == sorted(dates, reverse=True)

@then(parsers.cfparse('a transação mais recente deve aparecer primeiro'))
def check_latest_transaction(driver):
    first = driver.find_element(By.CSS_SELECTOR, ".transaction-row:first-child")
    # aqui você pode validar data/valor conforme a implementação
```

> **Nota:**  
> Se a aplicação usar **REST API** para depósito/saldo, troque os passos por chamadas `requests.post` e verificações JSON.

---

## 7.  Passos – `transfer_steps.py`

```python
# steps/transfer_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scenarios("../features/transfer.feature")

@given("o usuário está autenticado e na página de transferência")
def auth_and_transfer_page(driver, base_url):
    # login mock, ou reutilize o step de login
    driver.get(f"{base_url}/transfer")
    assert "Transferências – ParaBank" in driver.title

@given(parsers.cfparse('a conta "{account}" possui saldo de {amount}'))
def set_account_balance(driver, account, amount):
    # Este step normalmente seria feito via API ou fixture de banco de dados.
    # Aqui usamos um placeholder – a aplicação deve expor uma rota de mock
    # ou um script de seed.
    pass

@when(parsers.cfparse('ele seleciona conta de origem "{origin}"'))
def choose_origin(driver, origin):
    find(driver, (By.ID, "id_origin")).click()
    find(driver, (By.XPATH, f"//option[text()='{origin}']")).click()

@when(parsers.cfparse('seleciona conta de destino "{dest}"'))
def choose_dest(driver, dest):
    find(driver, (By.ID, "id_destination")).click()
    find(driver, (By.XPATH, f"//option[text()='{dest}']")).click()

@when(parsers.cfparse('digita valor {value}'))
def input_amount(driver, value):
    amount = float(value.replace("R$", "").replace(".", "").replace(",", ".").strip())
    find(driver, (By.ID, "id_amount")).send_keys(str(amount))

@when(parsers.cfparse('confirma a transferência'))
def confirm_transfer(driver):
    find(driver, (By.ID, "id_confirm")).click()

@then(parsers.cfparse('a conta "{account}" deve mostrar saldo de {amount}'))
def check_balance(driver, account, amount):
    expected = float(amount.replace("R$", "").replace(".", "").replace(",", ".").strip())
    actual = float(find(driver, (By.ID, f"id_balance_{account.lower()}")).text.replace("R$", "").replace(".", "").replace(",", "."))
    assert actual == expected

@then(parsers.cfparse('ambas as contas devem registrar a transação no histórico'))
def history_contains(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")
    assert any("Transferência" in row.text for row in rows)

@then(parsers.cfparse('o sistema deve exibir a mensagem “{msg}”'))
def verify_error(driver, msg):
    body = driver.find_element(By.TAG_NAME, "body").text
    assert msg in body
```

---

## 8.  Passos – `loan_steps.py`

```python
# steps/loan_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scenarios("../features/loan.feature")

@given("o usuário está autenticado e na página de empréstimos")
def access_loan_page(driver, base_url):
    driver.get(f"{base_url}/loans")
    assert "Empréstimos – ParaBank" in driver.title

@when(parsers.cfparse('ele insere valor {value}'))
def insert_loan_amount(driver, value):
    amount = float(value.replace("R$", "").replace(".", "").replace(",", ".").strip())
    find(driver, (By.ID, "id_amount")).send_keys(str(amount))

@when(parsers.cfparse('insere renda anual {value}'))
def insert_annual_income(driver, value):
    income = float(value.replace("R$", "").replace(".", "").replace(",", ".").strip())
    find(driver, (By.ID, "id_income")).send_keys(str(income))

@when(parsers.cfparse('clica em "{button}"'))
def click_button(driver, button):
    find(driver, (By.XPATH, f"//button[text()='{button}']")).click()

@then(parsers.cfparse('o sistema deve exibir a mensagem “{msg}”'))
def verify_loan_msg(driver, msg):
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), msg))
    body = driver.find_element(By.TAG_NAME, "body").text
    assert msg in body

@then(parsers.cfparse('o valor deve aparecer no extrato como crédito'))
def check_loan_in_statement(driver):
    # suposição: existe um ícone de “+” no extrato para créditos
    rows = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")
    assert any("Crédito" in row.text for row in rows)
```

---

## 9.  Passos – `payment_steps.py`

```python
# steps/payment_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from datetime import datetime

scenarios("../features/payment.feature")

@given("o usuário está autenticado e na página de pagamentos")
def access_payment_page(driver, base_url):
    driver.get(f"{base_url}/payments")
    assert "Pagamentos – ParaBank" in driver.title

@given(parsers.cfparse('a conta "{account}" possui saldo de {amount}'))
def set_account_balance(driver, account, amount):
    pass  # mock ou fixture

@when(parsers.cfparse('ele preenche "{field}" com “{value}”'))
def fill_payment_field(driver, field, value):
    loc = {
        "Beneficiário": (By.ID, "id_beneficiary"),
        "Endereço": (By.ID, "id_address"),
        "Cidade": (By.ID, "id_city"),
        "Estado": (By.ID, "id_state"),
        "CEP": (By.ID, "id_cep"),
        "Telefone": (By.ID, "id_phone"),
        "Conta de destino": (By.ID, "id_dest_account"),
        "Valor": (By.ID, "id_amount"),
        "Data": (By.ID, "id_date"),
    }
    elem = find(driver, loc[field])
    elem.clear()
    elem.send_keys(value)

@when(parsers.cfparse('clica em “{button}”'))
def click_button(driver, button):
    find(driver, (By.XPATH, f"//button[text()='{button}']")).click()

@then(parsers.cfparse('o saldo da conta “{account}” deve diminuir em {amount}'))
def check_balance_decrement(driver, account, amount):
    # suposição: ID do saldo da conta principal
    balance_elem = find(driver, (By.ID, f"id_balance_{account.lower()}"))
    new_balance = float(balance_elem.text.replace("R$", "").replace(".", "").replace(",", "."))
    # a lógica de cálculo seria feita em um fixture ou em uma API de mock
    pass

@then(parsers.cfparse('a transação deve aparecer no histórico'))
def verify_transaction_in_history(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")
    assert any("Pagamento" in row.text for row in rows)

@then(parsers.cfparse('a transação deve aparecer no histórico com data agendada “{date}”'))
def verify_scheduled(driver, date):
    rows = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")
    assert any(date in row.text for row in rows)

@then(parsers.cfparse('o saldo não deve ser debitado imediatamente'))
def check_no_immediate_debit(driver):
    # comparar com saldo antes de clicar, guardado em fixture
    pass
```

---

## 10.  Passos – `navigation_steps.py`

```python
# steps/navigation_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios("../features/navigation.feature")

@when(parsers.cfparse('o usuário navega para “{path}”'))
def navigate_to(driver, base_url, path):
    driver.get(f"{base_url}{path}")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

@then(parsers.cfparse('a página deve carregar sem mensagens de erro'))
def verify_no_error(driver):
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "erro" not in body.lower()

@then(parsers.cfparse('o cabeçalho deve exibir “ParaBank”'))
def verify_header(driver):
    header = driver.find_element(By.TAG_NAME, "header").text
    assert "ParaBank" in header

@then(parsers.cfparse('o menu principal deve conter os links: “{links}”'))
def check_main_menu(driver, links):
    link_list = [l.strip() for l in links.split("”, “")]
    menu_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
    texts = [l.text for l in menu_links]
    for l in link_list:
        assert l in texts
```

---

## 11.  Como rodar os testes

```bash
# 1. Instale as dependências
pip install pytest pytest-bdd selenium webdriver-manager

# 2. Execute
pytest
```

> **Dicas de melhoria:**
> * Use **Page Objects** para abstrair elementos e reduzir duplicação.  
> * Se a aplicação for API‑only, troque Selenium por `requests` e altere os steps para chamadas HTTP + validação JSON.  
> * Para dados sensíveis (senhas, e‑mails), armazene em arquivos `.env` ou use `pytest.fixture(params=...)` para parametrização.  
> * Para cenários de integração mais complexos, crie fixtures que configuram banco de dados ou mocks de serviços externos (ex.: `pytest-django`, `pytest-flask`).  

---

## 12.  Resumo rápido

| Feature | Arquivo `.feature` | Steps |
|---------|--------------------|-------|
| Cadastro | `registration.feature` | `registration_steps.py` |
| Login | `login.feature` | `login_steps.py` |
| Saldo & Extrato | `account.feature` | `account_steps.py` |
| Transferência | `transfer.feature` | `transfer_steps.py` |
| Empréstimo | `loan.feature` | `loan_steps.py` |
| Pagamento | `payment.feature` | `payment_steps.py` |
| Navegação | `navigation.feature` | `navigation_steps.py` |

Cada arquivo de steps contém:

1. **Importação dos scenarios** – conecta o Gherkin ao código.  
2. **Fixtures** (ex.: driver, base_url).  
3. **Givens** – navegação/estado inicial.  
4. **Whens** – interações.  
5. **Thens** – validações/asserts.

Pronto! Agora você tem um conjunto completo de testes automatizados BDD em Python usando **pytest‑bdd** que cobre todos os cenários descritos no seu documento Gherkin. Basta adaptar os seletores e a lógica de negócio para a sua aplicação específica. 🚀