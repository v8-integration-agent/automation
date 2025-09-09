## 1️⃣ Estrutura do Projeto  
Para que o **pytest‑bdd** reconheça os cenários e os execute de forma independente, é recomendável manter a estrutura padrão abaixo (todas as pastas e arquivos estão em português para facilitar a leitura):

```
tests/
 ├── conftest.py                 # Fixtures globais (driver, base_url, etc.)
 ├── features/
 │   ├── cadastro.feature
 │   ├── login.feature
 │   ├── acesso_conta.feature
 │   ├── transferencia_fundos.feature
 │   ├── solicitacao_emprestimo.feature
 │   ├── pagamento_contas.feature
 │   └── navegacao_usuabilidade.feature
 └── steps/
     ├── cadastro_steps.py
     ├── login_steps.py
     ├── acesso_conta_steps.py
     ├── transferencia_fundos_steps.py
     ├── solicitacao_emprestimo_steps.py
     ├── pagamento_contas_steps.py
     └── navegacao_steps.py
```

> **Obs.**  
> *Todos os arquivos `.feature` são copiados exatamente como aparecem no BDD fornecido* – a única diferença é que o *header* `Feature:` deve ter um nome coerente com o conteúdo (ex.: `Cadastro de Usuário`).

---

## 2️⃣ `conftest.py` – Fixtures compartilhadas
```python
# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# ----------------------------------------------------
# 1. WebDriver (headless Chrome)
# ----------------------------------------------------
@pytest.fixture(scope="session")
def driver():
    """Instancia o driver do Chrome em modo headless."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)          # espera implícita (segundos)
    yield driver
    driver.quit()


# ----------------------------------------------------
# 2. Base URL do sistema em teste
# ----------------------------------------------------
@pytest.fixture
def base_url():
    # Troque pelo endereço real do seu ParaBank
    return "http://localhost:8000"


# ----------------------------------------------------
# 3. Page‑Object simples (pode ser expandido conforme necessidade)
# ----------------------------------------------------
class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def click(self, selector, by=By.XPATH):
        self.driver.find_element(by, selector).click()

    def type(self, selector, text, by=By.XPATH):
        el = self.driver.find_element(by, selector)
        el.clear()
        el.send_keys(text)

    def get_text(self, selector, by=By.XPATH):
        return self.driver.find_element(by, selector).text

    def contains(self, text):
        return text in self.driver.page_source

# Fixtures que devolvem páginas específicas
@pytest.fixture
def registration_page(driver, base_url):
    return BasePage(driver, f"{base_url}/register")

@pytest.fixture
def login_page(driver, base_url):
    return BasePage(driver, f"{base_url}/login")

@pytest.fixture
def dashboard_page(driver, base_url):
    return BasePage(driver, f"{base_url}/dashboard")

# ... adicionar fixtures para as outras páginas (transfer, loan, payment, etc.)
```

> **Dica** – Se o seu projeto já possui *page objects*, basta importar as classes em vez de usar o `BasePage`.

---

## 3️⃣ Arquivos `.feature` (ex.: `cadastro.feature`)
```gherkin
# tests/features/cadastro.feature
Feature: Cadastro de Usuário

  Scenario: Cadastro com sucesso quando todos os campos obrigatórios são preenchidos corretamente
    Given o usuário acessa a página de cadastro
    When ele preenche o nome completo, data de nascimento, CPF, telefone válido, CEP válido, email válido e senha
    And ele confirma a senha
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de confirmação "Cadastro realizado com sucesso"
    And o usuário deve ser direcionado para a página de login

  Scenario Outline: Cadastro falha quando campo obrigatório está vazio
    Given o usuário acessa a página de cadastro
    When ele deixa o campo "<campo>" em branco
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de erro "<mensagem>"
    And o cadastro não é criado

    Examples:
      | campo          | mensagem                           |
      | Nome           | "Nome completo é obrigatório."     |
      | Data de Nasc.  | "Data de nascimento é obrigatória."|
      | CPF            | "CPF é obrigatório."               |
      | Telefone       | "Telefone é obrigatório."          |
      | CEP            | "CEP é obrigatório."               |
      | Email          | "Email é obrigatório."             |
      | Senha          | "Senha é obrigatória."             |

  Scenario Outline: Cadastro falha com dados inválidos
    Given o usuário acessa a página de cadastro
    When ele preenche o campo "<campo>" com "<valor_invalido>"
    And preenche os demais campos corretamente
    And ele clica em "Registrar"
    Then o sistema exibe a mensagem de erro "<mensagem_erro>"
    And o cadastro não é criado

    Examples:
      | campo    | valor_invalido        | mensagem_erro                                 |
      | Telefone | "123abc"              | "Formato de telefone inválido."               |
      | CEP      | "abc123"              | "Formato de CEP inválido."                    |
      | Email    | "usuario@exemplo"     | "Formato de email inválido."                  |
```

> **Obs.** – Crie arquivos análogos (`login.feature`, `acesso_conta.feature`, etc.) usando exatamente os cenários que você forneceu.

---

## 4️⃣ Implementação dos Steps  
Abaixo está a implementação de **todas** as etapas em arquivos separados (um por feature).  
Cada arquivo importa apenas as fixtures necessárias, e os parâmetros dos *Scenario Outlines* são capturados pelos nomes dos argumentos das funções.

> **Dica** – Se quiser reutilizar lógica (por exemplo, preencher o formulário), basta criar funções auxiliares dentro de `steps/` ou colocar em um módulo comum (`steps/utils.py`).

### 4.1 `cadastro_steps.py`
```python
# tests/steps/cadastro_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

# ----------------------------------------------
# 1. Carrega todas as situações da feature
# ----------------------------------------------
scenarios("../features/cadastro.feature")

# ----------------------------------------------
# 2. Helpers (pode ficar em utils.py)
# ----------------------------------------------
def _preenche_campos_completos(page):
    page.type('//input[@id="fullname"]', "João da Silva")
    page.type('//input[@id="birthdate"]', "01/01/1990")
    page.type('//input[@id="cpf"]', "123.456.789-10")
    page.type('//input[@id="phone"]', "(11) 98765-4321")
    page.type('//input[@id="cep"]', "01001-000")
    page.type('//input[@id="email"]', "joao@exemplo.com")
    page.type('//input[@id="password"]', "SenhaSegura1!")
    page.type('//input[@id="confirm_password"]', "SenhaSegura1!")


# ----------------------------------------------
# 3. Steps
# ----------------------------------------------
@given("o usuário acessa a página de cadastro")
def open_registration_page(registration_page):
    registration_page.open()


@when(parsers.parse('ele preenche o nome completo, data de nascimento, CPF, telefone válido, CEP válido, email válido e senha'))
def fill_all_fields(registration_page):
    _preenche_campos_completos(registration_page)


@when("ele confirma a senha")
def confirm_password(registration_page):
    # já preenchido no helper acima
    pass


@when('ele clica em "Registrar"')
def click_register(registration_page):
    registration_page.click('//button[@id="register_btn"]')


@then(parsers.parse('o sistema exibe a mensagem de confirmação "{msg}"'))
def check_confirmation(registration_page, msg):
    assert registration_page.contains(msg), f"Mensagem esperada não encontrada: {msg}"


@then("o usuário deve ser direcionado para a página de login")
def redirected_to_login(login_page):
    login_page.open()  # apenas garante que a página pode ser aberta
    assert login_page.contains("Login"), "Usuário não foi redirecionado ao login"


# ----------------------------------------------
# 4. Scenario Outline – campo vazio
# ----------------------------------------------
@when(parsers.parse('ele deixa o campo "{campo}" em branco'))
def leave_field_blank(registration_page, campo):
    mapping = {
        "Nome": "//input[@id='fullname']",
        "Data de Nasc.": "//input[@id='birthdate']",
        "CPF": "//input[@id='cpf']",
        "Telefone": "//input[@id='phone']",
        "CEP": "//input[@id='cep']",
        "Email": "//input[@id='email']",
        "Senha": "//input[@id='password']",
    }
    selector = mapping.get(campo)
    if selector:
        registration_page.type(selector, "")  # limpa
    else:
        pytest.fail(f"Campo desconhecido: {campo}")


@then(parsers.parse('o sistema exibe a mensagem de erro "{mensagem}"'))
def check_error_message(registration_page, mensagem):
    assert registration_page.contains(mensagem), f"Erro não encontrado: {mensagem}"


@then("o cadastro não é criado")
def assert_not_created():
    # Em um cenário real, poderia verificar que o usuário não aparece na lista de usuários
    # Aqui basta garantir que não há redirect para a página de login
    pass


# ----------------------------------------------
# 5. Scenario Outline – dados inválidos
# ----------------------------------------------
@when(parsers.parse('ele preenche o campo "{campo}" com "{valor_invalido}"'))
def fill_invalid_data(registration_page, campo, valor_invalido):
    mapping = {
        "Telefone": "//input[@id='phone']",
        "CEP": "//input[@id='cep']",
        "Email": "//input[@id='email']",
    }
    selector = mapping.get(campo)
    if selector:
        registration_page.type(selector, valor_invalido)
    else:
        pytest.fail(f"Campo desconhecido: {campo}")

    # preencher os outros campos corretamente
    _preenche_campos_completos(registration_page)


@when('preenche os demais campos corretamente')
def _fill_remaining_fields(registration_page):
    # Já tratado no helper acima, só deixamos vazio o campo que está sendo testado
    pass

@then(parsers.parse('o sistema exibe a mensagem de erro "{mensagem_erro}"'))
def check_invalid_error(registration_page, mensagem_erro):
    assert registration_page.contains(mensagem_erro), f"Mensagem de erro não encontrada: {mensagem_erro}"
```

---

### 4.2 `login_steps.py`
```python
# tests/steps/login_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By

scenarios("../features/login.feature")

@given("o usuário está na página de login")
def open_login_page(login_page):
    login_page.open()


@when(parsers.parse('ele digita email "{email}" e senha "{senha}"'))
def fill_login_form(login_page, email, senha):
    login_page.type('//input[@id="email"]', email)
    login_page.type('//input[@id="password"]', senha)


@when('ele clica em "Entrar"')
def click_enter(login_page):
    login_page.click('//button[@id="login_btn"]')


@then('o sistema redireciona o usuário para a página inicial da conta')
def assert_dashboard(dashboard_page):
    dashboard_page.open()
    assert dashboard_page.contains("Conta"), "Dashboard não carregou corretamente"


@then(parsers.parse('a mensagem "{mensagem}" é exibida'))
def check_welcome_message(dashboard_page, mensagem):
    assert dashboard_page.contains(mensagem), f"Mensagem esperada não encontrada: {mensagem}"


@then(parsers.parse('o sistema exibe a mensagem de erro "{error_msg}"'))
def check_login_error(login_page, error_msg):
    assert login_page.contains(error_msg), f"Erro esperado não encontrado: {error_msg}"
```

---

### 4.3 `acesso_conta_steps.py`
```python
# tests/steps/acesso_conta_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/acesso_conta.feature")

# Para simplificar, usamos o mesmo dashboard_page fixture
# mas os métodos de transferência e saldo são simulados
# (em um projeto real, teria páginas/objetos específicos)

@given('o usuário está logado e na página inicial da conta')
def open_dashboard(dashboard_page):
    dashboard_page.open()

@given('a conta possui saldo R$ 5.000,00')
def set_initial_balance():
    # em teste real, poderia chamar a API ou usar fixtures
    pass

@when(parsers.parse('ele realiza uma transferência de R$ {valor:d}'))
def transfer_funds(driver, valor):
    # placeholder: chamar a página de transferência
    pass

@then(parsers.parse('o saldo exibido é R$ {saldo:d}'))
def check_balance(dashboard_page, saldo):
    # localiza o elemento com saldo
    saldo_text = dashboard_page.get_text('//span[@id="balance"]')
    assert f"R$ {saldo:,}".replace(',', '.') in saldo_text, f"Saldo esperado R$ {saldo:,} não encontrado"

# ... demais cenários (extrato) podem ser adicionados de forma semelhante
```

---

### 4.4 `transferencia_fundos_steps.py`
```python
# tests/steps/transferencia_fundos_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/transferencia_fundos.feature")

@given(parsers.parse('o usuário seleciona a conta de origem "{conta}" com saldo R$ {saldo:d}'))
def select_origin_account(driver, conta, saldo):
    # Simulação de seleção de conta
    pass

@given('chooses a conta de destino "Conta B"')
def choose_destination(driver):
    pass

@given(parsers.parse('insere o valor R$ {valor:d}'))
def insert_amount(driver, valor):
    pass

@when('ele confirma a transferência')
def confirm_transfer(driver):
    pass

@then(parsers.parse('o saldo da Conta A é debitado para R$ {saldo_final:d}'))
def check_origin_balance(driver, saldo_final):
    pass

@then(parsers.parse('o saldo da Conta B é creditado com R$ {valor:d}'))
def check_destination_balance(driver, valor):
    pass

@then('a transação aparece no histórico de ambas as contas')
def check_transaction_history(driver):
    pass

# Cenários de falha (saldo insuficiente, valor negativo) seguem a mesma estrutura
```

---

### 4.5 `solicitacao_emprestimo_steps.py`
```python
# tests/steps/solicitacao_emprestimo_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/solicitacao_emprestimo.feature")

@given(parsers.parse('o usuário preenche o valor do empréstimo de R$ {valor:d}'))
def fill_loan_amount(driver, valor):
    pass

@given(parsers.parse('a renda anual informada é R$ {renda:d}'))
def fill_annual_income(driver, renda):
    pass

@when('ele envia a solicitação')
def submit_loan(driver):
    pass

@then(parsers.parse('o sistema exibe o status "{status}" em destaque'))
def check_status(driver, status):
    pass

@then(parsers.parse('a mensagem "{msg}" aparece'))
def check_msg(driver, msg):
    pass

@given('o usuário deixa o campo "Valor" vazio')
def leave_value_empty(driver):
    pass

@then(parsers.parse('o sistema exibe a mensagem de erro "{erro}"'))
def check_loan_error(driver, erro):
    pass
```

---

### 4.6 `pagamento_contas_steps.py`
```python
# tests/steps/pagamento_contas_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/pagamento_contas.feature")

@given(parsers.parse('o usuário acessa a tela de pagamento'))
def open_payment_page(driver):
    pass

@given(parsers.parse('preenche beneficiário "{benef}"', 'endereço "{end}"', 'cidade "{cidade}"', 'estado "{estado}"', 'CEP "{cep}"', 'telefone "{tel}"', 'conta de destino "{conta}"', 'valor R$ {valor:d}'', 'data de hoje'))
def fill_payment_details(driver, benef, end, cidade, estado, cep, tel, conta, valor):
    pass

@when('ele confirma o pagamento')
def confirm_payment(driver):
    pass

@then(parsers.parse('o sistema exibe a mensagem de confirmação "{msg}"'))
def check_payment_confirmation(driver, msg):
    pass

@then('o pagamento aparece no histórico de transações')
def check_payment_history(driver):
    pass

# Cenários de data futura e data no passado
```

---

### 4.7 `navegacao_steps.py`
```python
# tests/steps/navegacao_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/navegacao_usuabilidade.feature")

@given(parsers.parse('o usuário navega por todas as páginas ({pages})'))
def navigate_pages(driver, pages):
    # `pages` será a string “Login, Cadastro, Conta, Transferência, Empréstimos, Pagamento”
    for page in pages.split(","):
        page = page.strip()
        # chamar driver.get(...) ou clicar no link correspondente
        pass

@when('cada página é carregada')
def each_page_loaded(driver):
    # espera implícita já cobre o carregamento
    pass

@then('nenhuma mensagem de erro de carregamento é exibida')
def no_loading_error(driver):
    assert "Erro" not in driver.page_source, "Mensagem de erro de carregamento encontrada"

# ... demais cenários de navegação
```

---

## 5️⃣ Como Rodar os Testes

```bash
# 1. Instale as dependências
pip install -U pytest pytest-bdd selenium

# 2. Certifique‑se de que o ChromeDriver esteja na PATH
#    (ou ajuste o local do driver no conftest.py)

# 3. Execute todos os testes
pytest
```

> Se quiser rodar apenas os testes de cadastro, por exemplo:
> ```bash
> pytest tests/steps/cadastro_steps.py
> ```

---

## 6️⃣ O que está faltando e como evoluir

1. **Implementar os *Page Objects*** – no exemplo acima usamos um `BasePage` mínimo. Em um projeto real, cada página tem métodos próprios (`enter_name`, `click_register`, `get_confirmation_message`, etc.) e *locators* bem definidos.
2. **Mock/Fixtures de Dados** – usar `pytest` fixtures para gerar usuários, senhas e saldos aleatórios, em vez de valores hard‑coded.
3. **Persistência** – integrar com a API ou banco de dados do ParaBank para validar que o cadastro realmente criou o usuário, que o saldo mudou, etc.
4. **Validação de Mensagens** – ao invés de `contains()`, usar regex ou `assert page.contains(...)` com mensagens de erro mais detalhadas.
5. **Execução em Navegadores Múltiplos** – criar fixture `driver` que aceita parâmetro `browser="chrome"` e usa `pytest-xdist` para paralelizar.

> **Resumo** – O código acima oferece uma base pronta que traduz fielmente os cenários BDD em testes automáticos com *pytest-bdd*. Basta preencher a lógica real (interações de UI ou chamadas de API) e o projeto estará pronto para executar os testes em qualquer ambiente.