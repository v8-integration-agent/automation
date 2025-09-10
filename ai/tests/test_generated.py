## 1️⃣ Estrutura de pastas

```
para_bank/
├── conftest.py
├── features/
│   ├── cadastro.feature
│   ├── login.feature
│   ├── acesso_conta.feature
│   ├── transferencia.feature
│   ├── solicitacao_emprestimo.feature
│   ├── pagamento.feature
│   └── navegacao.feature
└── steps/
    ├── cadastro_steps.py
    ├── login_steps.py
    ├── acesso_conta_steps.py
    ├── transferencia_steps.py
    ├── emprestimo_steps.py
    ├── pagamento_steps.py
    └── navegacao_steps.py
```

> **Obs.:**  
> *Todos os arquivos `.feature` ficam no diretório `features/`.  
> *Cada arquivo `.py` na pasta `steps/` contém a implementação dos passos correspondentes à sua feature.*

---

## 2️⃣ `conftest.py`

```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.parabank.com/"  # troque pelo seu ambiente real


@pytest.fixture(scope="session")
def driver():
    """Configura o driver do Selenium."""
    options = Options()
    options.add_argument("--headless")          # roda sem UI
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def context():
    """Dicionário compartilhado entre os steps."""
    return {}


@pytest.fixture
def base_url():
    return BASE_URL
```

---

## 3️⃣ Feature Files

> Cada arquivo abaixo contém apenas o conteúdo *raw* do Gherkin.  
> Salve cada bloco com o nome indicado e com extensão `.feature`.

### 3.1 `features/cadastro.feature`

```gherkin
Feature: Cadastro de Usuário

  Scenario Outline: Cadastro com sucesso
    Given o usuário está na página de cadastro
    When preenche "<campo>" com "<valor>"
    And preenche os demais campos obrigatórios com valores válidos
    And clica em “Cadastrar”
    Then a mensagem de confirmação “Cadastro concluído!” deve ser exibida
    And o usuário pode fazer login com as credenciais recém‑criados

    Examples:
      | campo | valor         |
      | Nome  | João Silva    |
      | Email | joao@email.com|

  Scenario Outline: Cadastro falha por campo inválido
    Given o usuário está na página de cadastro
    When preenche "<campo>" com "<valor inválido>"
    And preenche os demais campos obrigatórios com valores válidos
    And clica em “Cadastrar”
    Then deve ser exibida a mensagem de erro "<mensagem>"

    Examples:
      | campo   | valor inválido | mensagem                                           |
      | Email   | joaoemail.com  | “Email inválido. Digite um e‑mail válido.”         |
      | Telefone| 123            | “Telefone inválido. Use apenas números.”           |
      | CEP     | abcde          | “CEP inválido. Digite apenas números.”             |
```

### 3.2 `features/login.feature`

```gherkin
Feature: Login

  Scenario: Login bem‑sucedido
    Given existe um usuário cadastrado com e‑mail “maria@email.com” e senha “Segura123”
    When o usuário insere “maria@email.com” no campo de e‑mail
    And insere “Segura123” no campo de senha
    And clica em “Entrar”
    Then o usuário é redirecionado para a página inicial da conta
    And o banner “Bem‑vindo Maria!” é exibido

  Scenario: Login falha por credenciais inválidas
    Given existe um usuário cadastrado com e‑mail “maria@email.com”
    When o usuário insere “maria@email.com” no campo de e‑mail
    And insere “Errada456” no campo de senha
    And clica em “Entrar”
    Then a mensagem “Credenciais inválidas. Tente novamente.” é exibida
```

### 3.3 `features/acesso_conta.feature`

```gherkin
Feature: Acesso à Conta (Saldo e Extrato)

  Scenario: Visualização do saldo atualizado após depósito
    Given o usuário está logado e possui saldo de R$ 1.000,00
    When realiza um depósito de R$ 500,00
    Then o saldo exibido deve ser R$ 1.500,00

  Scenario: Extrato lista transações recentes em ordem cronológica
    Given o usuário está logado
    And possui as seguintes transações:
      | Data       | Tipo      | Valor  |
      | 2024-09-08 | Depósito  | 1.000  |
      | 2024-09-10 | Saque     | 200    |
    When acessa a página de extrato
    Then a lista de transações deve mostrar:
      | 1 | 2024-09-10 | Saque | -200 |
      | 2 | 2024-09-08 | Depósito | +1.000 |
```

### 3.4 `features/transferencia.feature`

```gherkin
Feature: Transferência de Fundos

  Scenario: Transferência bem‑sucedida entre contas
    Given o usuário possui R$ 1.000,00 na conta A
    And a conta B possui R$ 500,00
    When o usuário seleciona conta A como origem
    And seleciona conta B como destino
    And define o valor R$ 300,00
    And confirma a transferência
    Then a conta A deve exibir saldo de R$ 700,00
    And a conta B deve exibir saldo de R$ 800,00
    And ambas as contas devem registrar a transação no histórico

  Scenario: Transferência falha por saldo insuficiente
    Given o usuário possui R$ 100,00 na conta A
    When tenta transferir R$ 200,00
    Then a mensagem “Saldo insuficiente” deve ser exibida
    And nenhuma conta é alterada
```

### 3.5 `features/solicitacao_emprestimo.feature`

```gherkin
Feature: Solicitação de Empréstimo

  Scenario: Empréstimo aprovado
    Given o usuário tem renda anual de R$ 120.000,00
    When solicita empréstimo de R$ 50.000,00
    Then o sistema deve retornar “Aprovado”
    And o valor será adicionado ao saldo da conta

  Scenario: Empréstimo negado
    Given o usuário tem renda anual de R$ 20.000,00
    When solicita empréstimo de R$ 50.000,00
    Then o sistema deve retornar “Negado”
    And nenhum valor é creditado
```

### 3.6 `features/pagamento.feature`

```gherkin
Feature: Pagamento de Contas

  Scenario: Pagamento imediato registrado no histórico
    Given o usuário possui saldo suficiente
    When registra pagamento com:
      | Beneficiário | Endereço      | Cidade     | Estado | CEP      | Telefone | Conta Destino | Valor      | Data       |
      | Luz Eletrônica | Rua A, 100 | São Paulo | SP     | 01234-567 | 12345678 | 1234-5       | R$ 150,00  | 2024-09-10 |
    And confirma o pagamento
    Then a transação deve aparecer no histórico de pagamento
    And o saldo deve ser debitado em R$ 150,00

  Scenario: Pagamento futuro agendado
    Given o usuário possui saldo suficiente
    When registra pagamento com data futura “2024-12-01”
    And confirma o pagamento
    Then o pagamento é marcado como “Agendado”
    And não aparece no extrato até a data de vencimento
```

### 3.7 `features/navegacao.feature`

```gherkin
Feature: Requisitos Gerais de Navegação e Usabilidade

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega entre as seções (Login, Cadastro, Extrato, Transferência, Empréstimo, Pagamento)
    When acessa cada página
    Then nenhuma página exibe erro de carregamento

  Scenario: Mensagens de erro são claras e objetivas
    When ocorre qualquer falha (ex.: campo obrigatório vazio)
    Then a mensagem exibida deve conter:
      | Contexto | Mensagem                |
      | Email   | “Campo email é obrigatório.” |

  Scenario: Links e menus são consistentes em todas as páginas
    Given o usuário está em qualquer página
    When verifica o menu principal
    Then todos os links (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento) estão presentes
    And ao clicar em cada link, a página correspondente é carregada corretamente
```

---

## 4️⃣ Implementação dos Steps

> Para cada arquivo `.feature` existe um arquivo `*_steps.py` correspondente.  
> Use *parsers* quando precisar capturar valores de parâmetros e *table* para tabelas.

> **Observação:**  
> Este exemplo usa **Selenium** em modo headless; altere os seletores (`By.ID`, `By.NAME`, etc.) para a sua aplicação real.  
> Se preferir, troque por chamadas a uma API REST usando `requests` + `pytest`.

### 4.1 `steps/cadastro_steps.py`

```python
# steps/cadastro_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/cadastro.feature')


# ---------- Givens ----------

@given('o usuário está na página de cadastro')
def navigate_to_registration(driver, base_url):
    driver.get(f"{base_url}/register")  # ajuste a rota
    assert "Register" in driver.title


# ---------- Wenes ----------

@when(parsers.parse('preenche "{campo}" com "{valor}"'))
def fill_field(driver, campo, valor):
    # mapeamento simplificado; adapte conforme a sua tela
    id_map = {
        "Nome": "customer.firstName",
        "Email": "customer.email",
        "Telefone": "customer.phoneNumber",
        "CEP": "customer.postalCode",
    }
    field_id = id_map.get(campo)
    assert field_id, f"Campo '{campo}' não mapeado"
    input_elem = driver.find_element(By.ID, field_id)
    input_elem.clear()
    input_elem.send_keys(valor)


@when('preenche os demais campos obrigatórios com valores válidos')
def fill_required_fields(driver):
    # Exemplo simples – ajuste para sua aplicação
    driver.find_element(By.ID, "customer.lastName").send_keys("Silva")
    driver.find_element(By.ID, "customer.address.street").send_keys("Rua X, 123")
    driver.find_element(By.ID, "customer.address.city").send_keys("São Paulo")
    driver.find_element(By.ID, "customer.address.state").send_keys("SP")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("01000-000")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("11987654321")
    driver.find_element(By.ID, "customer.ssn").send_keys("123-45-6789")
    driver.find_element(By.ID, "customer.username").send_keys("joao" + pytest.random.randint(1000, 9999))
    driver.find_element(By.ID, "customer.password").send_keys("Segura123")
    driver.find_element(By.ID, "customer.confirmPassword").send_keys("Segura123")


@when('clica em “Cadastrar”')
def click_register(driver):
    driver.find_element(By.ID, "registerBtn").click()


# ---------- Then ----------

@then('a mensagem de confirmação “Cadastro concluído!” deve ser exibida')
def confirm_message(driver):
    alert = driver.find_element(By.CLASS_NAME, "alert-success")
    assert "Cadastro concluído!" in alert.text


@then('o usuário pode fazer login com as credenciais recém‑criados')
def login_after_registration(driver, context):
    # armazenamos o username/Password no context
    username = driver.find_element(By.ID, "customer.username").get_attribute("value")
    password = driver.find_element(By.ID, "customer.password").get_attribute("value")
    context["login"] = (username, password)

    driver.get(f"{driver.current_url.split('/')[0]}/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginButton").click()

    assert "Login" not in driver.title
    assert f"Olá {username}" in driver.page_source


# ---------- Failure scenario steps ----------

@when(parsers.parse('preenche "{campo}" com "{valor_invalido}"'))
def fill_invalid_field(driver, campo, valor_invalido):
    fill_field(driver, campo, valor_invalido)


@then(parsers.parse('deve ser exibida a mensagem de erro "{mensagem}"'))
def check_error_message(driver, mensagem):
    alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert mensagem.strip("“”") in alert.text
```

> **Dica:** Se você preferir usar *page objects*, encapsule os elementos em classes.

### 4.2 `steps/login_steps.py`

```python
# steps/login_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/login.feature')


@given(parsers.parse('existe um usuário cadastrado com e‑mail "{email}" e senha "{senha}"'))
def create_user(driver, base_url, email, senha):
    """
    Cria um usuário de forma simples usando o endpoint de registro (ou via UI).
    Para fins de teste, vamos usar a página de registro diretamente.
    """
    driver.get(f"{base_url}/register")
    # preencher todos os campos exigidos – valores fictícios
    driver.find_element(By.ID, "customer.firstName").send_keys("Maria")
    driver.find_element(By.ID, "customer.lastName").send_keys("Silva")
    driver.find_element(By.ID, "customer.address.street").send_keys("Av. Brasil, 100")
    driver.find_element(By.ID, "customer.address.city").send_keys("Rio de Janeiro")
    driver.find_element(By.ID, "customer.address.state").send_keys("RJ")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("20000-000")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("21987654321")
    driver.find_element(By.ID, "customer.ssn").send_keys("987-65-4321")
    driver.find_element(By.ID, "customer.username").send_keys(email)
    driver.find_element(By.ID, "customer.password").send_keys(senha)
    driver.find_element(By.ID, "customer.confirmPassword").send_keys(senha)
    driver.find_element(By.ID, "registerBtn").click()

    # verifica que a mensagem de sucesso apareceu
    assert "Cadastro concluído!" in driver.page_source


@given(parsers.parse('existe um usuário cadastrado com e‑mail "{email}"'))
def create_user_no_pass(driver, base_url, email):
    # cria apenas com senha default (por simplicidade)
    create_user(driver, base_url, email, "Segura123")


@when(parsers.parse('o usuário insere "{email}" no campo de e‑mail'))
def enter_email(driver, email):
    driver.find_element(By.ID, "username").send_keys(email)


@when(parsers.parse('insere "{senha}" no campo de senha'))
def enter_password(driver, senha):
    driver.find_element(By.ID, "password").send_keys(senha)


@when('clica em “Entrar”')
def click_login(driver):
    driver.find_element(By.ID, "loginButton").click()


@then('o usuário é redirecionado para a página inicial da conta')
def check_redirection(driver):
    assert "/account" in driver.current_url
    assert "Account Overview" in driver.title


@then(parsers.parse('o banner “Bem‑vindo {nome}!” é exibido'))
def banner_welcome(driver, nome):
    banner = driver.find_element(By.ID, "welcomeBanner")
    assert f"Bem‑vindo {nome}!" in banner.text


@then(parsers.parse('a mensagem “{mensagem}” é exibida'))
def error_message(driver, mensagem):
    alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert mensagem in alert.text
```

### 4.3 `steps/acesso_conta_steps.py`

```python
# steps/acesso_conta_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/acesso_conta.feature')


# ---------- Given ----------

@given(parsers.parse('o usuário está logado e possui saldo de R$ {saldo:float},00'))
def login_and_set_balance(driver, base_url, saldo):
    # login prévio
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "username").send_keys("teste@conta.com")
    driver.find_element(By.ID, "password").send_keys("Segura123")
    driver.find_element(By.ID, "loginButton").click()

    # simula o saldo (apenas para teste)
    # em produção use um mock de backend ou API
    driver.execute_script(f"document.querySelector('#balance').innerText = 'R$ {saldo:.2f}';")


@given(parsers.parse('o usuário está logado'))
def login(driver, base_url):
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "username").send_keys("teste@conta.com")
    driver.find_element(By.ID, "password").send_keys("Segura123")
    driver.find_element(By.ID, "loginButton").click()


@given(parsers.parse('possui as seguintes transações:'))
def seed_transactions(driver, table):
    """
    table: pytest-bdd Table object
    Exemplo:
    | Data       | Tipo      | Valor  |
    | 2024-09-08 | Depósito  | 1.000  |
    | 2024-09-10 | Saque     | 200    |
    """
    # para demo, apenas gravamos no localStorage (ou use API)
    for row in table:
        driver.execute_script(
            f"window.localStorage.setItem('txn_{row['Data']}', JSON.stringify({{tipo:'{row['Tipo']}', valor:{row['Valor']}}}));"
        )


# ---------- When ----------

@when(parsers.parse('realiza um depósito de R$ {valor:float},00'))
def deposit(driver, valor):
    driver.find_element(By.ID, "depositAmount").send_keys(str(valor))
    driver.find_element(By.ID, "depositButton").click()


@when('acessa a página de extrato')
def go_to_statement(driver):
    driver.find_element(By.LINK_TEXT, "Statement").click()


# ---------- Then ----------

@then(parsers.parse('o saldo exibido deve ser R$ {saldo:float},00'))
def check_balance(driver, saldo):
    bal_text = driver.find_element(By.ID, "balance").text
    assert f"R$ {saldo:.2f}" == bal_text.strip()


@then(parsers.parse('a lista de transações deve mostrar:'))
def check_transactions(driver, expected_table):
    rows = driver.find_elements(By.CSS_SELECTOR, "#transactionTable tbody tr")
    assert len(rows) == len(expected_table)
    for row, expected in zip(rows, expected_table):
        cells = row.find_elements(By.TAG_NAME, "td")
        assert cells[0].text.strip() == expected['1']
        assert cells[1].text.strip() == expected['2']
        assert cells[2].text.strip() == expected['3']
        assert cells[3].text.strip() == expected['4']
```

> **Obs.:**  
> O código acima usa `window.localStorage` para simular o backend. Em um cenário real, use uma camada de *mock* ou *stubs*.

### 4.4 `steps/transferencia_steps.py`

```python
# steps/transferencia_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/transferencia.feature')


@given(parsers.parse('o usuário possui R$ {saldo_a:float},00 na conta A'))
def set_balance_a(driver, saldo_a):
    driver.execute_script(f"window.localStorage.setItem('balance_A', {saldo_a});")


@given(parsers.parse('a conta B possui R$ {saldo_b:float},00'))
def set_balance_b(driver, saldo_b):
    driver.execute_script(f"window.localStorage.setItem('balance_B', {saldo_b});")


@when(parsers.parse('o usuário seleciona conta {origem} como origem'))
def select_origin(driver, origem):
    driver.find_element(By.ID, f"origin_{origem}").click()


@when(parsers.parse('seleciona conta {destino} como destino'))
def select_destination(driver, destino):
    driver.find_element(By.ID, f"destination_{destino}").click()


@when(parsers.parse('define o valor R$ {valor:float},00'))
def set_value(driver, valor):
    driver.find_element(By.ID, "transferAmount").send_keys(str(valor))
    driver.driver.transfer_amount = valor  # guarda para validação


@when('confirma a transferência')
def confirm_transfer(driver):
    driver.find_element(By.ID, "transferButton").click()


@then(parsers.parse('a conta {conta} deve exibir saldo de R$ {saldo:float},00'))
def check_account_balance(driver, conta, saldo):
    actual = float(driver.execute_script(f"return window.localStorage.getItem('balance_{conta}')"))
    assert actual == saldo


@then(parsers.parse('ambas as contas devem registrar a transação no histórico'))
def check_history(driver):
    history = driver.execute_script("return JSON.parse(localStorage.getItem('history')) || []")
    assert len(history) == 1
    txn = history[0]
    assert txn["origin"] == "A" and txn["dest"] == "B" and txn["valor"] == driver.driver.transfer_amount


# ---------- Failure scenario steps ----------
@when(parsers.parse('tenta transferir R$ {valor:float},00'))
def transfer_insufficient(driver, valor):
    driver.find_element(By.ID, "origin_A").click()
    driver.find_element(By.ID, "destination_B").click()
    driver.find_element(By.ID, "transferAmount").send_keys(str(valor))
    driver.find_element(By.ID, "transferButton").click()


@then(parsers.parse('a mensagem “{mensagem}” deve ser exibida'))
def transfer_error(driver, mensagem):
    alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert mensagem in alert.text
```

### 4.5 `steps/emprestimo_steps.py`

```python
# steps/emprestimo_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/solicitacao_emprestimo.feature')


@given(parsers.parse('o usuário tem renda anual de R$ {renda:float},00'))
def set_income(driver, renda):
    driver.execute_script(f"window.localStorage.setItem('income', {renda});")


@when(parsers.parse('solicita empréstimo de R$ {valor:float},00'))
def request_loan(driver, valor):
    driver.find_element(By.ID, "loanAmount").send_keys(str(valor))
    driver.find_element(By.ID, "loanButton").click()


@then(parsers.parse('o sistema deve retornar “{resultado}”'))
def check_loan_result(driver, resultado):
    result = driver.find_element(By.ID, "loanResult").text
    assert resultado in result


@then('o valor será adicionado ao saldo da conta')
def loan_credit(driver):
    bal = float(driver.execute_script("return parseFloat(document.querySelector('#balance').innerText.replace(/[^0-9,]/g,'').replace(',','.') )"))
    # aqui assumimos que o saldo inicial era 0 e foi creditado
    assert bal > 0


@then('nenhum valor é creditado')
def loan_not_granted(driver):
    bal = float(driver.execute_script("return parseFloat(document.querySelector('#balance').innerText.replace(/[^0-9,]/g,'').replace(',','.') )"))
    assert bal == 0
```

### 4.6 `steps/pagamento_steps.py`

```python
# steps/pagamento_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/pagamento.feature')


@given('o usuário possui saldo suficiente')
def ensure_balance(driver):
    driver.execute_script("window.localStorage.setItem('balance', 1000);")  # valor arbitrário


@when(parsers.parse('registra pagamento com:'))
def register_payment(driver, table):
    # table: tabela com campos do cenário
    data = {col: row for col in table[0].keys() for row in table}
    driver.find_element(By.ID, "beneficiary").send_keys(data['Beneficiário'])
    driver.find_element(By.ID, "address").send_keys(data['Endereço'])
    driver.find_element(By.ID, "city").send_keys(data['Cidade'])
    driver.find_element(By.ID, "state").send_keys(data['Estado'])
    driver.find_element(By.ID, "zip").send_keys(data['CEP'])
    driver.find_element(By.ID, "phone").send_keys(data['Telefone'])
    driver.find_element(By.ID, "destinationAccount").send_keys(data['Conta Destino'])
    driver.find_element(By.ID, "amount").send_keys(data['Valor'].replace('R$ ', '').replace(',', '.'))
    if 'Data' in data:
        driver.find_element(By.ID, "paymentDate").send_keys(data['Data'])
    else:
        driver.find_element(By.ID, "paymentDate").clear()  # data atual


@when('confirma o pagamento')
def confirm_payment(driver):
    driver.find_element(By.ID, "submitPayment").click()


@then('a transação deve aparecer no histórico de pagamento')
def check_payment_history(driver):
    history = driver.execute_script("return JSON.parse(localStorage.getItem('paymentHistory')) || []")
    assert len(history) > 0


@then(parsers.parse('o saldo deve ser debitado em R$ {valor:float},00'))
def check_balance_debited(driver, valor):
    bal = float(driver.execute_script("return window.localStorage.getItem('balance')"))
    assert bal == 1000 - valor


@then(parsers.parse('o pagamento é marcado como “{status}”'))
def check_payment_status(driver, status):
    latest = driver.execute_script("return JSON.parse(localStorage.getItem('paymentHistory')).pop()")
    assert latest["status"] == status


@then('não aparece no extrato até a data de vencimento')
def check_future_extrato(driver):
    # garantimos que o extrato não inclui a transação futura
    extrato = driver.execute_script("return JSON.parse(localStorage.getItem('extrato')) || []")
    assert not any(txn["status"] == "Agendado" for txn in extrato)
```

### 4.7 `steps/navegacao_steps.py`

```python
# steps/navegacao_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/navegacao.feature')


@when('acessa cada página')
def visit_all_pages(driver, base_url):
    links = [
        ("Login", "/login"),
        ("Cadastro", "/register"),
        ("Extrato", "/statement"),
        ("Transferência", "/transfer"),
        ("Empréstimo", "/loan"),
        ("Pagamento", "/payment"),
    ]
    for name, path in links:
        driver.get(base_url + path)
        assert driver.find_element(By.TAG_NAME, "body")  # apenas garantimos que a página carregou


@then('nenhuma página exibe erro de carregamento')
def check_no_errors(driver):
    errors = driver.find_elements(By.CLASS_NAME, "alert-danger")
    assert len(errors) == 0


@when('ocorre qualquer falha (ex.: campo obrigatório vazio)')
def trigger_error(driver):
    # simula envio de formulário vazio
    driver.get(f"{driver.current_url}")
    driver.find_element(By.ID, "submitBtn").click()


@then(parsers.parse('a mensagem exibida deve conter:'))
def check_specific_error(driver, table):
    for row in table:
        context = row['Contexto']
        msg = row['Mensagem'].strip('“”')
        alert = driver.find_element(By.CLASS_NAME, "alert-danger")
        assert msg in alert.text, f"Esperava '{msg}' para o campo {context}"


@when('verifica o menu principal')
def verify_menu(driver):
    driver.get(f"{driver.current_url}")
    # não precisamos de assert aqui; o step seguinte fará
    pass


@then(parsers.parse('todos os links ({links}) estão presentes'))
def check_links(driver, links):
    for link in links.split(', '):
        assert driver.find_element(By.LINK_TEXT, link.strip())


@then('ao clicar em cada link, a página correspondente é carregada corretamente')
def click_and_verify(driver):
    menu_items = driver.find_elements(By.CSS_SELECTOR, "#mainMenu a")
    for item in menu_items:
        href = item.get_attribute("href")
        item.click()
        assert driver.current_url == href
        # volta para a página inicial
        driver.back()
```

---

## 5️⃣ Como rodar os testes

```bash
# 1. Instale as dependências
pip install pytest pytest-bdd selenium

# 2. (Opcional) Baixe o ChromeDriver e coloque em PATH
#    ou use `webdriver-manager`:
pip install webdriver-manager

# 3. Execute os testes
pytest
```

> **Dica:**  
> Para ambientes de CI (GitHub Actions, GitLab CI…) configure o ChromeDriver, abra o *headless* e exponha o port 4444 se usar Selenium Grid.

---

## 6️⃣ Próximos Passos

| Item | Próximo passo | Por que? |
|------|---------------|----------|
| **Mock de backend** | Crie *fixtures* que mockem APIs REST (ex.: usando `responses` ou `requests-mock`). | Evita chamadas reais e torna os testes determinísticos. |
| **Page Objects** | Encapsule a lógica de navegação em classes. | Torna o código mais legível e reutilizável. |
| **Reporting** | Integre `pytest-html` ou `Allure`. | Gera relatórios visualmente atraentes. |
| **Parallel** | Use `pytest-xdist`. | Reduz tempo de execução em grandes suítes. |
| **CI** | Adicione um workflow no GitHub Actions que rode os testes. | Garantia contínua de qualidade. |

---

**Pronto!**  
Você agora tem uma base completa de testes automatizados para todas as features do `ParaBank`, utilizando `pytest-bdd` com Selenium em modo headless. Basta ajustar os seletores e a lógica de mock para seu ambiente de produção. Boa sorte e bons testes!