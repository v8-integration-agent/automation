Below is a **complete, ready‑to‑run skeleton** that translates the BDD specification you pasted into Python/pytest‑bdd tests.  
The layout follows the usual `pytest‑bdd` conventions:

```
project_root/
│
├── features/                     # Gherkin feature files
│   ├── cadastro.feature
│   ├── login.feature
│   ├── saldo_extrato.feature
│   ├── transferencia.feature
│   ├── emprestimo.feature
│   ├── pagamento.feature
│   └── usabilidade.feature
│
├── steps/                        # All step implementations (one file is enough)
│   └── steps.py
│
├── conftest.py                   # Shared fixtures (browser, db, …)
└── requirements.txt              # pip deps (pytest, pytest-bdd, selenium, …)
```

> ⚠️ **Important** – this code only contains *placeholders*.  
> Replace the `TODO` comments with actual logic (Selenium calls, API requests, database asserts, …) that matches your application under test.

---

## 1️⃣  Feature files

Below are the exact contents that should live inside `features/*.feature`.

> **Tip:**  Keep the feature names (the `Feature:` line) *exactly* as shown – `pytest‑bdd` uses the file path and the scenario name to locate the step definitions.

### 1.1 `features/cadastro.feature`

```gherkin
# Feature: Cadastro de Usuário
# @cadastro
Feature: Registro de novos usuários no ParaBank
  Como usuário que ainda não possui conta,
  Eu quero me cadastrar no sistema,
  Para que eu possa usar os serviços bancários.

  Scenario: Cadastro bem‑sucedido com todos os campos preenchidos
    Given o usuário acessa a página de cadastro
    When preenche os campos obrigatórios com dados válidos
      | Campo            | Valor             |
      | Nome             | João da Silva     |
      | Email            | joao@email.com    |
      | Telefone         | (11) 98765-4321   |
      | CEP              | 12345-678          |
      | Endereço         | Rua A, 123        |
      | Cidade           | São Paulo         |
      | Estado           | SP                |
      | Senha            | P@ssw0rd!         |
      | Confirmação Senha| P@ssw0rd!         |
    When clica em “Cadastrar”
    Then o sistema deve exibir a mensagem “Cadastro concluído com sucesso”
    And o usuário deve ser redirecionado para a tela de login

  Scenario: Cadastro falha quando campos obrigatórios estão vazios
    Given o usuário acessa a página de cadastro
    When deixa os campos obrigatórios em branco
    Then o sistema deve exibir mensagem de erro “Este campo é obrigatório” para cada campo vazio
    And nenhuma conta deve ser criada

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a página de cadastro
    When preenche os campos obrigatórios com os valores abaixo
      | Campo    | Valor |
      | <Campo>  | <Valor> |
    And preenche os demais campos com dados válidos
    When clica em “Cadastrar”
    Then o sistema exibe a mensagem de erro “<MensagemErro>”

    Examples:
      | Campo      | Valor               | MensagemErro                      |
      | Telefone   | 1234                | Telefone inválido                |
      | CEP        | ABCDE               | CEP inválido                     |
      | Email      | joao[at]email.com   | Email inválido                   |
```

---

### 1.2 `features/login.feature`

```gherkin
# Feature: Login
# @login
Feature: Acesso ao sistema
  Como usuário registrado,
  Eu quero fazer login com credenciais válidas,
  Para que eu possa acessar minha conta.

  Scenario: Login bem‑sucedido com credenciais válidas
    Given o usuário está na página de login
    When preenche “Email” com “joao@email.com”
    And preenche “Senha” com “P@ssw0rd!”
    And clica em “Entrar”
    Then o usuário deve ser redirecionado para a página inicial da conta
    And o saldo inicial deve ser exibido

  Scenario: Login falha com credenciais inválidas
    Given o usuário está na página de login
    When preenche “Email” com “joao@email.com”
    And preenche “Senha” com “errada123”
    And clica em “Entrar”
    Then o sistema exibe a mensagem de erro “Credenciais inválidas”
```

---

### 1.3 `features/saldo_extrato.feature`

```gherkin
# Feature: Acesso à aplicação bancária (Saldo e Extrato)
# @saldo @extrato
Feature: Visualização de saldo e extrato
  Como cliente logado,
  Eu quero ver meu saldo atualizado e extrato recente,
  Para que eu possa monitorar minhas transações.

  Scenario: Saldo atualizado após depósito
    Given o usuário já fez um depósito de R$ 100,00
    When acessa a página inicial
    Then o saldo exibido deve refletir o depósito

  Scenario: Extrato lista transações em ordem cronológica
    Given o usuário tem as seguintes transações:
      | Data       | Descrição           | Valor      |
      | 01/10/2024 | Saldo Inicial       | R$ 1.000  |
      | 02/10/2024 | Depósito            | R$ 100    |
      | 03/10/2024 | Transferência       | -R$ 50    |
    When acessa a aba “Extrato”
    Then o extrato deve listar as transações da mais recente à mais antiga
```

---

### 1.4 `features/transferencia.feature`

```gherkin
# Feature: Transferência de Fundos
# @transferencia
Feature: Transferir dinheiro entre contas
  Como usuário,
  Eu quero transferir fundos de uma conta para outra,
  Para que eu possa mover recursos entre minhas contas.

  Scenario: Transferência bem‑sucedida
    Given o usuário tem saldo de R$ 500,00 em Conta A
    And existe a Conta B
    When seleciona Conta A como origem
    And seleciona Conta B como destino
    And entra o valor R$ 200,00
    And confirma a transferência
    Then o saldo de Conta A deve ser R$ 300,00
    And o saldo de Conta B deve ser R$ 200,00
    And a transação aparece no histórico de ambas as contas

  Scenario Outline: Transferência falha quando valor excede saldo
    Given o usuário tem saldo de R$ <Saldo> em Conta A
    When tenta transferir R$ <Transferir> de Conta A para Conta B
    Then o sistema exibe a mensagem “Saldo insuficiente”
    And a transferência não é realizada

    Examples:
      | Saldo | Transferir |
      | 150   | 200        |
      | 100   | 150        |
```

---

### 1.5 `features/emprestimo.feature`

```gherkin
# Feature: Solicitação de Empréstimo
# @emprestimo
Feature: Pedir um empréstimo
  Como cliente,
  Eu quero solicitar um empréstimo,
  Para que eu possa obter recursos adicionais.

  Scenario: Empréstimo aprovado
    Given o usuário informa valor R$ 10.000 e renda anual R$ 80.000
    When envia a solicitação de empréstimo
    Then o sistema deve exibir “Solicitação Aprovada”

  Scenario: Empréstimo negado
    Given o usuário informa valor R$ 50.000 e renda anual R$ 30.000
    When envia a solicitação de empréstimo
    Then o sistema deve exibir “Solicitação Negada”
```

---

### 1.6 `features/pagamento.feature`

```gherkin
# Feature: Pagamento de Contas
# @pagamento
Feature: Registrar pagamento de contas
  Como cliente,
  Eu quero registrar um pagamento de conta,
  Para que eu possa acompanhar meus débitos.

  Scenario: Pagamento imediato
    Given o usuário informa:
      | Beneficiário | Endereço         | Cidade    | Estado | CEP     | Telefone     | Conta Destino | Valor | Data        |
      | Luz          | Av. Central, 10  | Rio       | RJ     | 10000-000 | (21) 1234-5678 | 987654321 | R$ 80 | 05/10/2024 |
    When confirma o pagamento
    Then o sistema deve registrar a transação no histórico
    And exibir mensagem “Pagamento realizado com sucesso”

  Scenario: Pagamento agendado futuro
    Given o usuário informa data de pagamento “12/10/2024”
    When confirma o pagamento
    Then o sistema deve marcar a transação como “Agendada”
    And a data de vencimento deve ser exibida no extrato
```

---

### 1.7 `features/usabilidade.feature`

```gherkin
# Feature: Navegação e Usabilidade
# @usabilidade
Feature: Navegação consistente e mensagens claras
  Como usuário,
  Eu quero que todas as páginas carreguem corretamente e que as mensagens de erro sejam claras,
  Para que eu tenha uma experiência de uso fluída.

  Scenario: Todas as páginas carregam sem erros
    Given o usuário navega por todas as funcionalidades do sistema
    Then nenhuma página deve apresentar erros de carregamento ou links quebrados

  Scenario: Mensagens de erro são claras e objetivas
    Given o usuário tenta enviar um formulário com dados inválidos
    When submete o formulário
    Then cada campo com erro exibe uma mensagem explicativa em linguagem simples

  Scenario: Menus e links são consistentes em todas as páginas
    Given o usuário navega entre diferentes seções do aplicativo
    When verifica a presença de menus e links
    Then os mesmos itens de menu devem estar disponíveis em todas as páginas
```

---

## 2️⃣  Step definitions – `steps/steps.py`

```python
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------------
# Fixtures (common browser instance, test data, etc.)
# --------------------------------------------------
@pytest.fixture
def browser():
    """Initializes a Selenium WebDriver. Replace with your own driver."""
    from selenium import webdriver
    driver = webdriver.Chrome()          # or webdriver.Firefox(), etc.
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# --------------------------------------------------
# Generic helper functions (implement with your app)
# --------------------------------------------------
def open_url(browser, url: str):
    """Navigate to a given URL."""
    browser.get(url)


def find_and_type(browser, field_name: str, value: str):
    """Find an input by its label or name and send keys."""
    # TODO: Adjust the locator strategy to match your form.
    elem = browser.find_element(By.NAME, field_name)
    elem.clear()
    elem.send_keys(value)


def click_button(browser, button_label: str):
    """Click a button identified by its visible text."""
    btn = browser.find_element(By.XPATH, f"//button[normalize-space()='{button_label}']")
    btn.click()


def wait_for_text(browser, text: str, timeout=10):
    """Wait until a given text appears somewhere on the page."""
    WebDriverWait(browser, timeout).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text))


# --------------------------------------------------
# Feature: Cadastro de Usuário
# --------------------------------------------------
@scenario("features/cadastro.feature", "Cadastro bem‑sucedido com todos os campos preenchidos")
def test_cadastro_bem_sucedido():
    pass


@scenario("features/cadastro.feature", "Cadastro falha quando campos obrigatórios estão vazios")
def test_cadastro_campos_vazios():
    pass


@scenario("features/cadastro.feature", "Cadastro falha com dados inválidos")
def test_cadastro_dados_invalidos():
    pass


# ----------------- Given -----------------
@given(parsers.parse('o usuário acessa a página de cadastro'))
def user_visits_registration_page(browser):
    open_url(browser, "https://www.parabank.com/register")  # <-- update URL


# ----------------- When -----------------
@when(parsers.parse('preenche os campos obrigatórios com dados válidos'))
def preencher_campos_obrigatorios_validos(browser, table):
    """
    table – a DataTable object containing the rows from the feature.
    """
    for row in table:
        campo, valor = row["Campo"], row["Valor"]
        find_and_type(browser, campo, valor)


@when(parsers.parse('preenche os campos obrigatórios com os valores abaixo'))
def preencher_campos_obrigatorios_invalidos(browser, table):
    for row in table:
        campo, valor = row["Campo"], row["Valor"]
        find_and_type(browser, campo, valor)


@when(parsers.parse('preenche os demais campos com dados válidos'))
def preencher_campos_demais_valores(browser):
    # TODO: Supply any data needed for the remaining fields
    pass


@when(parsers.parse('deixa os campos obrigatórios em branco'))
def deixar_campos_vazios(browser):
    # Just don't fill anything or explicitly clear fields
    pass


@when(parsers.parse('clica em “Cadastrar”'))
def clica_cadastrar(browser):
    click_button(browser, "Cadastrar")   # button text may vary


# ----------------- Then -----------------
@then(parsers.parse('o sistema deve exibir a mensagem “{msg}”'))
def assert_mensagem_exibida(browser, msg):
    wait_for_text(browser, msg)


@then(parsers.parse('o usuário deve ser redirecionado para a tela de login'))
def assert_redirecionamento_login(browser):
    wait_for_text(browser, "Login")  # or check URL


@then(parsers.parse('o sistema deve exibir mensagem de erro “{msg}” para cada campo vazio'))
def assert_erro_campos_vazios(browser, msg):
    # Example: find elements with class 'error' or data attributes
    errors = browser.find_elements(By.CLASS_NAME, "error")
    assert all(msg in e.text for e in errors)


@then(parsers.parse('nenhuma conta deve ser criada'))
def assert_nenhuma_conta(browser):
    # TODO: verify by checking DB or API, e.g. no user record for the email
    pass


@then(parsers.parse('o sistema exibe a mensagem de erro “{msg}”'))
def assert_mensagem_erro(browser, msg):
    wait_for_text(browser, msg)

# --------------------------------------------------
# Feature: Login
# --------------------------------------------------
@scenario("features/login.feature", "Login bem‑sucedido com credenciais válidas")
def test_login_bem_sucedido():
    pass


@scenario("features/login.feature", "Login falha com credenciais inválidas")
def test_login_falha_credenciais():
    pass


@given(parsers.parse('o usuário está na página de login'))
def user_visits_login_page(browser):
    open_url(browser, "https://www.parabank.com/login")


@when(parsers.parse('preenche “{campo}” com “{valor}”'))
def preenche_login_field(browser, campo, valor):
    find_and_type(browser, campo, valor)


@when(parsers.parse('clica em “Entrar”'))
def clica_entrar(browser):
    click_button(browser, "Entrar")


@then(parsers.parse('o usuário deve ser redirecionado para a página inicial da conta'))
def assert_redirecionamento_home(browser):
    wait_for_text(browser, "Conta")  # adjust to your app


@then(parsers.parse('o saldo inicial deve ser exibido'))
def assert_saldo_exibido(browser):
    # TODO: verify balance is visible
    pass


@then(parsers.parse('o sistema exibe a mensagem de erro “{msg}”'))
def assert_mensagem_login_erro(browser, msg):
    wait_for_text(browser, msg)

# --------------------------------------------------
# Feature: Saldo & Extrato
# --------------------------------------------------
@scenario("features/saldo_extrato.feature", "Saldo atualizado após depósito")
def test_saldo_após_deposito():
    pass


@scenario("features/saldo_extrato.feature", "Extrato lista transações em ordem cronológica")
def test_extrato_ordem_cronologica():
    pass


@given(parsers.parse('o usuário já fez um depósito de R$ {valor}'))
def usuario_depositou(browser, valor):
    # TODO: use API or UI to deposit
    pass


@when(parsers.parse('acessa a página inicial'))
def acessar_pagina_inicial(browser):
    open_url(browser, "https://www.parabank.com/home")


@then(parsers.parse('o saldo exibido deve refletir o depósito'))
def assert_saldo_reflete_deposito(browser):
    # TODO: get balance element and compare
    pass


@given(parsers.parse('o usuário tem as seguintes transações:'))
def usuario_tem_transacoes(browser, table):
    # TODO: create transactions via API or seed DB
    pass


@when(parsers.parse('acessa a aba “Extrato”'))
def acessar_aba_extrato(browser):
    click_button(browser, "Extrato")


@then(parsers.parse('o extrato deve listar as transações da mais recente à mais antiga'))
def assert_extrato_ordenado(browser):
    # TODO: collect transaction rows and assert order
    pass

# --------------------------------------------------
# Feature: Transferência de Fundos
# --------------------------------------------------
@scenario("features/transferencia.feature", "Transferência bem‑sucedida")
def test_transferencia_bensucedida():
    pass


@scenario("features/transferencia.feature", "Transferência falha quando valor excede saldo")
def test_transferencia_falha_saldo_insuficiente():
    pass


@given(parsers.parse('o usuário tem saldo de R$ {saldo} em Conta A'))
def usuario_saldo_conta_a(browser, saldo):
    # TODO: set balance
    pass


@given(parsers.parse('existe a Conta B'))
def conta_b_existe(browser):
    # TODO: create account B if necessary
    pass


@when(parsers.parse('seleciona Conta A como origem'))
def selecionar_origem_conta_a(browser):
    # TODO: pick account from dropdown
    pass


@when(parsers.parse('seleciona Conta B como destino'))
def selecionar_destino_conta_b(browser):
    pass


@when(parsers.parse('entra o valor R$ {valor}'))
def entra_valor_transferencia(browser, valor):
    find_and_type(browser, "Valor", valor)


@when(parsers.parse('confirma a transferência'))
def confirma_transferencia(browser):
    click_button(browser, "Confirmar")


@then(parsers.parse('o saldo de Conta A deve ser R$ {saldo}'))
def assert_saldo_conta_a(browser, saldo):
    # TODO: verify balance
    pass


@then(parsers.parse('o saldo de Conta B deve ser R$ {saldo}'))
def assert_saldo_conta_b(browser, saldo):
    # TODO: verify balance
    pass


@then(parsers.parse('a transação aparece no histórico de ambas as contas'))
def assert_transacao_no_historico(browser):
    # TODO: check transaction logs
    pass


@when(parsers.parse('tenta transferir R$ {valor} de Conta A para Conta B'))
def tenta_transferir(browser, valor):
    entra_valor_transferencia(browser, valor)
    confirma_transferencia(browser)


# --------------------------------------------------
# Feature: Empréstimo
# --------------------------------------------------
@scenario("features/emprestimo.feature", "Empréstimo aprovado")
def test_emprestimo_aprovado():
    pass


@scenario("features/emprestimo.feature", "Empréstimo negado")
def test_emprestimo_negado():
    pass


@given(parsers.parse('o usuário informa valor R$ {valor} e renda anual R$ {renda}'))
def usuario_informa_emprestimo(browser, valor, renda):
    find_and_type(browser, "Valor", valor)
    find_and_type(browser, "Renda", renda)


@when(parsers.parse('envia a solicitação de empréstimo'))
def envia_solicitacao_emprestimo(browser):
    click_button(browser, "Enviar")

# --------------------------------------------------
# Feature: Pagamento de Contas
# --------------------------------------------------
@scenario("features/pagamento.feature", "Pagamento imediato")
def test_pagamento_imediato():
    pass


@scenario("features/pagamento.feature", "Pagamento agendado futuro")
def test_pagamento_futuro():
    pass


@given(parsers.parse('o usuário informa:'))
def usuario_informa_pagamento(browser, table):
    # Map table to form fields
    for row in table:
        campo = row["Beneficiário"]  # adjust as needed
        # TODO: fill each field
        pass


@given(parsers.parse('o usuário informa data de pagamento “{data}”'))
def usuario_informa_data_pagamento(browser, data):
    find_and_type(browser, "Data", data)


@when(parsers.parse('confirma o pagamento'))
def confirma_pagamento(browser):
    click_button(browser, "Confirmar")


@then(parsers.parse('o sistema deve registrar a transação no histórico'))
def assert_pagamento_no_historico(browser):
    # TODO
    pass


@then(parsers.parse('exibir mensagem “{msg}”'))
def assert_mensagem_pagamento(browser, msg):
    wait_for_text(browser, msg)


@then(parsers.parse('o sistema deve marcar a transação como “Agendada”'))
def assert_transacao_agendada(browser):
    # TODO
    pass


@then(parsers.parse('a data de vencimento deve ser exibida no extrato'))
def assert_data_vencimento(browser):
    # TODO
    pass

# --------------------------------------------------
# Feature: Usabilidade
# --------------------------------------------------
@scenario("features/usabilidade.feature", "Todas as páginas carregam sem erros")
def test_navegacao_sem_erro():
    pass


@scenario("features/usabilidade.feature", "Mensagens de erro são claras e objetivas")
def test_mensagens_erro_claras():
    pass


@scenario("features/usabilidade.feature", "Menus e links são consistentes em todas as páginas")
def test_menus_consistentes():
    pass

# --------------------------------------------------
# Common utilities (for all scenarios)
# --------------------------------------------------
@then(parsers.parse('nada mais a fazer'))
def nothing_to_do():
    pass
```

---

## 3️⃣  Shared fixtures – `conftest.py`

```python
import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    """Create and tear down a WebDriver instance."""
    # Use Chrome headless for CI, change as needed.
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
```

---

## 4️⃣  Dependencies – `requirements.txt`

```txt
pytest>=8.0
pytest-bdd>=4.0
selenium>=4.0
```

---

## 5️⃣  Running the test suite

```bash
# Install dependencies
pip install -r requirements.txt

# Run all scenarios
pytest --gherkin-terminal-tester

# Run a specific tag (e.g. cadastro)
pytest -m cadastro
```

> The `--gherkin-terminal-tester` flag gives a nice BDD‑style output in the terminal (you can remove it if you prefer raw `pytest` output).

---

## 6️⃣  Next steps

1. **Implement the TODOs** – Replace the placeholder comments with real Selenium or API logic that matches your ParaBank UI/API.  
2. **Add assertions** – Use `assert` or `pytest`/`selenium` helpers to validate balances, transaction histories, etc.  
3. **Data‑driven tables** – The `table` argument in the step definitions gives you a list of dictionaries; use it to populate forms or create test data.  
4. **Mocking / Fixtures** – If you prefer to avoid hitting the real database, create fixtures that seed the system with known users/accounts before each scenario.  
5. **CI integration** – Add the test run to your GitHub Actions/Travis/TeamCity pipeline.

---

### TL;DR

* 7 feature files → 7 scenarios + 1 outline each  
* 1 step‑definition file (`steps.py`) with matching `@scenario` decorators  
* 1 shared `browser` fixture (Selenium) in `conftest.py`  
* `pytest-bdd` automatically binds each Gherkin step to the right Python function  
* All logic still has to be written (TODO blocks) – this skeleton is the complete test harness.  

Happy automating! 🚀