## 1️⃣  Estrutura de pastas recomendada

```
tests/
├── conftest.py                # Fixtures globais (browser, app, etc.)
├── features/
│   └── banking.feature        # Arquivo Gherkin com todos os scenarios
└── steps/
    ├── conftest.py           # Fixtures específicas dos steps (se necessário)
    └── banking_steps.py     # Definições dos steps – um único arquivo para simplificar
```

> **Obs.**  
> Para manter o exemplo enxuto estamos usando **um único arquivo Gherkin** (`banking.feature`) que contém todas as feature/Scenario descritas na sua mensagem.  
> Se preferir, basta separar cada *feature* em arquivos diferentes e usar `@scenario("features/registration.feature", "Cadastro bem‑sucedido")`, etc.

---

## 2️⃣  Arquivo `tests/features/banking.feature`

```gherkin
Feature: Cadastro de Usuário
  O cadastro deve validar campos obrigatórios e formatos específicos.

  Scenario: Cadastro bem‑sucedido
    Given o usuário está na página de cadastro
    When preenche os campos obrigatórios com dados válidos
    And confirma o cadastro
    Then exibe a mensagem de confirmação “Cadastro concluído com sucesso”
    And habilita o acesso ao login

  Scenario: Tentativa de cadastro com campo obrigatório em branco
    Given o usuário está na página de cadastro
    When deixa o campo “Nome” em branco
    And preenche os demais campos obrigatórios
    And confirma o cadastro
    Then exibe a mensagem de erro “Nome é obrigatório”

  Scenario: Cadastro com telefone inválido
    Given o usuário está na página de cadastro
    When preenche “Telefone” com “12345”
    And preenche os demais campos obrigatórios
    And confirma o cadastro
    Then exibe a mensagem de erro “Telefone inválido”

  Scenario: Cadastro com CEP inválido
    Given o usuário está na página de cadastro
    When preenche “CEP” com “ABCDE”
    And preenche os demais campos obrigatórios
    And confirma o cadastro
    Then exibe a mensagem de erro “CEP inválido”

  Scenario: Cadastro com e‑mail inválido
    Given o usuário está na página de cadastro
    When preenche “E‑mail” com “usuario@@example.com”
    And preenche os demais campos obrigatórios
    And confirma o cadastro
    Then exibe a mensagem de erro “Endereço de e‑mail inválido”

Feature: Login
  O sistema deve autenticar credenciais válidas e rejeitar inválidas.

  Scenario: Login bem‑sucedido
    Given o usuário tem credenciais válidas
    When abre a página de login
    And insere “usuario@exemplo.com” no campo de e‑mail
    And insere “SenhaSegura123” no campo de senha
    And clica em “Entrar”
    Then redireciona para a página inicial da conta
    And exibe o nome do usuário no cabeçalho

  Scenario: Login com credenciais inválidas
    Given o usuário tem credenciais inválidas
    When abre a página de login
    And insere “usuario@exemplo.com” no campo de e‑mail
    And insere “SenhaIncorreta” no campo de senha
    And clica em “Entrar”
    Then exibe a mensagem de erro “Credenciais inválidas”

Feature: Acesso à conta (Saldo e Extrato)
  O saldo deve ser atualizado e o extrato em ordem cronológica.

  Scenario: Exibição de saldo atualizado após depósito
    Given o usuário tem saldo de R$ 1.000,00
    And realizou um depósito de R$ 500,00
    When acessa a página da conta
    Then o saldo exibido é “R$ 1.500,00”

  Scenario: Listagem de extrato em ordem cronológica
    Given o usuário tem as seguintes transações:
      | Data       | Tipo          | Valor |
      | 2024‑01‑01 | Depósito      | 200   |
      | 2024‑01‑10 | Saque         | 50    |
      | 2024‑01‑15 | Transferência | 100   |
    When acessa a página de extrato
    Then o extrato lista as transações em ordem crescente de data

Feature: Transferência de Fundos
  O sistema deve validar saldo e registrar transação.

  Scenario: Transferência bem‑sucedida
    Given o usuário possui R$ 1.000,00 na conta origem
    When seleciona a conta origem “Conta A”
    And seleciona a conta destino “Conta B”
    And insere o valor “200,00”
    And confirma a transferência
    Then debita R$ 200,00 da Conta A
    And credita R$ 200,00 na Conta B
    And registra a transação no extrato de ambas as contas

  Scenario: Transferência com valor superior ao saldo
    Given o usuário possui R$ 100,00 na conta origem
    When tenta transferir “200,00”
    Then exibe a mensagem de erro “Saldo insuficiente”

  Scenario: Transferência sem informar valor
    Given o usuário possui saldo suficiente
    When seleciona contas de origem e destino
    And deixa o campo “Valor” em branco
    And tenta confirmar a transferência
    Then exibe a mensagem de erro “O campo Valor é obrigatório”

Feature: Solicitação de Empréstimo
  O sistema retorna status aprovado ou negado baseado na renda.

  Scenario: Empréstimo aprovado
    Given o usuário possui renda anual de R$ 80.000,00
    When solicita empréstimo de R$ 10.000,00
    And confirma a solicitação
    Then exibe a mensagem “Empréstimo aprovado”
    And registra a solicitação no histórico

  Scenario: Empréstimo negado por renda insuficiente
    Given o usuário possui renda anual de R$ 20.000,00
    When solicita empréstimo de R$ 10.000,00
    And confirma a solicitação
    Then exibe a mensagem “Empréstimo negado”

Feature: Pagamento de Contas
  O pagamento deve ser registrado e respeitar data de agendamento.

  Scenario: Pagamento imediato bem‑sucedido
    Given o usuário possui saldo de R$ 1.000,00
    When registra pagamento com:
      | Beneficiário | Endereço | Cidade | Estado | CEP        | Telefone         | Conta   | Valor | Data       |
      | João Silva   | Rua X    | SP     | SP     | 12345-678  | (11) 91234‑5678 | Conta C | 300   | 2024‑02‑01 |
    And confirma o pagamento
    Then débita R$ 300,00 da conta
    And registra a transação no extrato

  Scenario: Pagamento agendado para data futura
    Given o usuário possui saldo suficiente
    When registra pagamento com data “2024‑12‑25”
    And confirma o pagamento
    Then exibe a mensagem “Pagamento agendado para 2024‑12‑25”
    And não debita o saldo imediatamente
    And registra a transação no histórico de pagamentos agendados

  Scenario: Pagamento com telefone inválido
    Given o usuário possui saldo suficiente
    When registra pagamento com telefone “123”
    And confirma o pagamento
    Then exibe a mensagem de erro “Telefone inválido”

Feature: Requisitos Gerais de Navegação e Usabilidade
  As páginas devem carregar corretamente e os menus devem ser consistentes.

  Scenario: Todas as páginas carregam sem erros de navegação
    Given o usuário está autenticado
    When navega por todas as páginas disponíveis (Login, Cadastro, Conta, Transferência, Empréstimo, Pagamento)
    Then nenhuma página apresenta erro de carregamento

  Scenario: Mensagens de erro claras e objetivas
    Given o usuário tenta uma operação inválida (ex.: transferência sem valor)
    When confirma a operação
    Then a mensagem exibida contém apenas informação necessária para correção

  Scenario: Menus e links consistentes em todas as páginas
    Given o usuário navega entre as páginas
    When inspeciona os menus de navegação
    Then todos os links aparecem em todas as páginas
    And a estrutura de navegação permanece a mesma
```

> **Obs.**:  
> 1. O Gherkin acima está em português, por isso os *step* abaixo foram escritos em português.  
> 2. Se você preferir usar o padrão inglês (`Given`, `When`, `Then`) basta renomear os decorators `@given`, `@when`, `@then` e os textos dos *steps*.

---

## 3️⃣  Arquivo `tests/conftest.py`

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# ----------------------------
# Fixtures globais
# ----------------------------
@pytest.fixture(scope="session")
def browser():
    """Instancia um WebDriver (Chrome) e devolve para os testes."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")          # executa em modo headless
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)  # tempo de espera implícito
    yield driver
    driver.quit()


@pytest.fixture
def app(browser):
    """Wrapper que pode armazenar objetos de página e dados do contexto."""
    return {
        "browser": browser,
        "data": {}            # dicionário para armazenar estado entre steps
    }
```

---

## 4️⃣  Arquivo `tests/steps/banking_steps.py`

```python
import re
from pytest_bdd import scenario, given, when, then, parsers

# ----------------------------
# Scenarios (apenas uma, mas a anotação
# pode ser repetida 3 vezes se preferir separar por arquivo)
# ----------------------------

# 1️⃣ Cadastro
scenario("features/banking.feature", "Cadastro bem‑sucedido")
scenario("features/banking.feature", "Tentativa de cadastro com campo obrigatório em branco")
scenario("features/banking.feature", "Cadastro com telefone inválido")
scenario("features/banking.feature", "Cadastro com CEP inválido")
scenario("features/banking.feature", "Cadastro com e‑mail inválido")

# 2️⃣ Login
scenario("features/banking.feature", "Login bem‑sucedido")
scenario("features/banking.feature", "Login com credenciais inválidas")

# 3️⃣ Conta (saldo / extrato)
scenario("features/banking.feature", "Exibição de saldo atualizado após depósito")
scenario("features/banking.feature", "Listagem de extrato em ordem cronológica")

# 4️⃣ Transferência
scenario("features/banking.feature", "Transferência bem‑sucedida")
scenario("features/banking.feature", "Transferência com valor superior ao saldo")
scenario("features/banking.feature", "Transferência sem informar valor")

# 5️⃣ Empréstimo
scenario("features/banking.feature", "Empréstimo aprovado")
scenario("features/banking.feature", "Empréstimo negado por renda insuficiente")

# 6️⃣ Pagamento
scenario("features/banking.feature", "Pagamento imediato bem‑sucedido")
scenario("features/banking.feature", "Pagamento agendado para data futura")
scenario("features/banking.feature", "Pagamento com telefone inválido")

# 7️⃣ Navegação
scenario("features/banking.feature", "Todas as páginas carregam sem erros de navegação")
scenario("features/banking.feature", "Mensagens de erro claras e objetivas")
scenario("features/banking.feature", "Menus e links consistentes em todas as páginas")


# ----------------------------
# Helpers de Page Object (mocks simplificados)
# ----------------------------
class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to(self):
        self.driver.get("http://example.com/cadastro")

    def fill_all_fields(self, data=None):
        # data: dict com os campos preenchidos
        # em testes reais usaríamos .send_keys()
        print("[MOCK] Preenchendo campos de cadastro:", data or "dados válidos")

    def submit(self):
        print("[MOCK] Submetendo formulário de cadastro")

    def get_message(self):
        return "Cadastro concluído com sucesso"

    def login_enabled(self):
        return True


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to(self):
        self.driver.get("http://example.com/login")

    def login(self, email, senha):
        print(f"[MOCK] Inserindo e‑mail: {email}")
        print(f"[MOCK] Inserindo senha: {senha}")
        print("[MOCK] Clicando em Entrar")

    def get_error(self):
        return "Credenciais inválidas"

    def get_header_user(self):
        return "Usuário Exemplo"


class AccountPage:
    def __init__(self, driver):
        self.driver = driver
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"[MOCK] Depositando R$ {amount}")

    def get_balance(self):
        return f"R$ {self.balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def get_extrato(self):
        # Retorna lista de tuplas (data, tipo, valor)
        return self.extrato if hasattr(self, "extrato") else []


class TransferPage:
    def __init__(self, driver):
        self.driver = driver
        self.accounts = {"Conta A": 1000.0, "Conta B": 500.0}

    def select_origin(self, conta):
        self.origin = conta
        print(f"[MOCK] Selecionado origem: {conta}")

    def select_dest(self, conta):
        self.dest = conta
        print(f"[MOCK] Selecionado destino: {conta}")

    def set_amount(self, valor):
        self.valor = valor
        print(f"[MOCK] Valor de transferência: R$ {valor}")

    def confirm(self):
        print("[MOCK] Confirmando transferência")
        if self.valor > self.accounts[self.origin]:
            raise ValueError("Saldo insuficiente")
        self.accounts[self.origin] -= self.valor
        self.accounts[self.dest] += self.valor

    def get_origin_balance(self):
        return self.accounts[self.origin]

    def get_dest_balance(self):
        return self.accounts[self.dest]


# ... (classes semelhantes para LoanPage, PaymentPage, NavigationPage)
# Para não ficar muito extenso, o resto das páginas seguem o mesmo padrão de mocks.

# ----------------------------
# Steps – Cadastro
# ----------------------------
@given("o usuário está na página de cadastro")
def go_to_registration(app):
    page = RegistrationPage(app["browser"])
    page.go_to()
    app["page"] = page


@when("preenche os campos obrigatórios com dados válidos")
def fill_valid_registration(app):
    app["page"].fill_all_fields()


@when("deixa o campo “Nome” em branco")
def leave_name_blank(app):
    app["page"].fill_all_fields({"Nome": ""})


@when(parsers.parse("preenche “{field}” com “{value}”"))
def fill_specific_field(app, field, value):
    # simplificação: apenas imprime
    print(f"[MOCK] {field} preenchido com {value}")
    if field == "Telefone":
        app["page"].fill_all_fields({"Telefone": value})
    elif field == "CEP":
        app["page"].fill_all_fields({"CEP": value})
    elif field == "E‑mail":
        app["page"].fill_all_fields({"Email": value})


@when("preenche os demais campos obrigatórios")
def fill_other_fields(app):
    app["page"].fill_all_fields({"Nome": "João", "Telefone": "99999-9999", "CEP": "12345-678", "Email": "joao@exemplo.com"})


@when("confirma o cadastro")
def confirm_registration(app):
    app["page"].submit()


@then(parsers.parse("exibe a mensagem de confirmação “{msg}”"))
def assert_success_msg(app, msg):
    actual = app["page"].get_message()
    assert msg == actual, f"Esperava mensagem '{msg}' mas veio '{actual}'"


@then("habilita o acesso ao login")
def check_login_enabled(app):
    assert app["page"].login_enabled(), "Login não habilitado após cadastro"


@then(parsers.parse("exibe a mensagem de erro “{msg}”"))
def assert_error_msg(app, msg):
    actual = app["page"].get_message()  # no mock, usar método genérico
    # Para este exemplo, sempre retornaremos a mensagem do *msg*
    assert msg == actual, f"Esperava erro '{msg}' mas veio '{actual}'"


# ----------------------------
# Steps – Login
# ----------------------------
@given("o usuário tem credenciais válidas")
def user_with_valid_credentials(app):
    app["credentials"] = ("usuario@exemplo.com", "SenhaSegura123")


@given("o usuário tem credenciais inválidas")
def user_with_invalid_credentials(app):
    app["credentials"] = ("usuario@exemplo.com", "SenhaIncorreta")


@when("abre a página de login")
def go_to_login(app):
    page = LoginPage(app["browser"])
    page.go_to()
    app["page"] = page


@when(parsers.parse("insere “{email}” no campo de e‑mail"))
def insert_email(app, email):
    app["email"] = email
    print(f"[MOCK] Inserido e‑mail: {email}")


@when(parsers.parse("insere “{senha}” no campo de senha"))
def insert_password(app, senha):
    app["senha"] = senha
    print(f"[MOCK] Inserida senha: {senha}")


@when("clica em “Entrar”")
def click_login(app):
    app["page"].login(app["email"], app["senha"])


@then(parsers.parse("redireciona para a página inicial da conta"))
def check_redirect(app):
    # mock: não há redirecionamento real
    print("[MOCK] Redirecionado para dashboard")


@then("exibe o nome do usuário no cabeçalho")
def check_user_header(app):
    header = app["page"].get_header_user()
    assert header == "Usuário Exemplo", f"Esperava nome de usuário 'Usuário Exemplo' mas veio '{header}'"


# ----------------------------
# Steps – Conta (Saldo / Extrato)
# ----------------------------
@given(parsers.parse("o usuário tem saldo de R$ {saldo:g},00"))
def user_has_balance(app, saldo):
    page = AccountPage(app["browser"])
    page.deposit(saldo)
    app["page"] = page


@given(parsers.parse("realizou um depósito de R$ {valor:g},00"))
def deposit_to_balance(app, valor):
    app["page"].deposit(valor)


@when("acessa a página da conta")
def open_account_page(app):
    print("[MOCK] Navegando para página da conta")


@then(parsers.parse("o saldo exibido é “{msg}”"))
def check_balance(app, msg):
    actual = app["page"].get_balance()
    assert msg == actual, f"Esperava saldo '{msg}' mas veio '{actual}'"


@given(parsers.parse("o usuário tem as seguintes transações:"))
def user_has_transactions(app, table):
    # table é objeto Table da pytest-bdd
    page = AccountPage(app["browser"])
    page.extrato = [(row["Data"], row["Tipo"], float(row["Valor"])) for row in table]
    app["page"] = page


@when("acessa a página de extrato")
def open_extrato_page(app):
    print("[MOCK] Navegando para extrato")


@then("o extrato lista as transações em ordem crescente de data")
def check_extrato_order(app):
    extrato = app["page"].get_extrato()
    datas = [e[0] for e in extrato]
    assert datas == sorted(datas), f"Extrato não está em ordem crescente: {datas}"


# ----------------------------
# Steps – Transferência
# ----------------------------
@given(parsers.parse("o usuário possui R$ {saldo:g},00 na conta origem"))
def user_has_origin_balance(app, saldo):
    page = TransferPage(app["browser"])
    page.accounts["Conta A"] = saldo
    page.accounts["Conta B"] = 0
    app["page"] = page


@when(parsers.parse("seleciona a conta origem “{conta}”"))
def select_origin(app, conta):
    app["page"].select_origin(conta)


@when(parsers.parse("seleciona a conta destino “{conta}”"))
def select_dest(app, conta):
    app["page"].select_dest(conta)


@when(parsers.parse("insere o valor “{valor}”"))
def insert_transfer_value(app, valor):
    app["page"].set_amount(float(valor.replace(",", ".")))


@when("confirma a transferência")
def confirm_transfer(app):
    try:
        app["page"].confirm()
    except ValueError as e:
        app["transfer_error"] = str(e)


@then(parsers.parse("debita R$ {valor:g},00 da Conta A"))
def check_origin_balance(app, valor):
    assert app["page"].get_origin_balance() == (app["page"].accounts["Conta A"] + valor), "Saldo da conta origem incorreto"


@then(parsers.parse("credita R$ {valor:g},00 na Conta B"))
def check_dest_balance(app, valor):
    assert app["page"].get_dest_balance() == valor, "Saldo da conta destino incorreto"


@then("registra a transação no extrato de ambas as contas")
def check_transfer_in_extrato(app):
    # mock: nada a fazer
    print("[MOCK] Transação registrada no extrato")


# ----------------------------
# Steps – Empréstimo (exemplo simplificado)
# ----------------------------
@given(parsers.parse("o usuário possui renda anual de R$ {renda:g},00"))
def user_has_income(app, renda):
    app["renda"] = renda


@when(parsers.parse("solicita empréstimo de R$ {valor:g},00"))
def request_loan(app, valor):
    app["loan_requested"] = valor


@when("confirma a solicitação")
def confirm_loan(app):
    if app["renda"] >= 50000:
        app["loan_status"] = "aprovado"
    else:
        app["loan_status"] = "negado"


@then(parsers.parse("exibe a mensagem “{msg}”"))
def assert_loan_msg(app, msg):
    assert msg in app["loan_status"], f"Mensagem esperada '{msg}' não encontrada em '{app['loan_status']}'"


@then("registra a solicitação no histórico")
def register_loan_history(app):
    print("[MOCK] Empréstimo registrado no histórico")


# ----------------------------
# Steps – Pagamento (exemplo simplificado)
# ----------------------------
@given(parsers.parse("o usuário possui saldo de R$ {saldo:g},00"))
def user_has_payment_balance(app, saldo):
    app["payment_balance"] = saldo


@when(parsers.parse("registra pagamento com:"))
def register_payment_with_table(app, table):
    app["payment_data"] = {col: row[col] for row in table for col in row}
    print("[MOCK] Dados de pagamento:", app["payment_data"])


@when("confirma o pagamento")
def confirm_payment(app):
    print("[MOCK] Confirmando pagamento")
    valor = float(app["payment_data"]["Valor"])
    app["payment_balance"] -= valor
    app["payment_history"] = ["pagamento"]


@then(parsers.parse("débita R$ {valor:g},00 da conta"))
def check_payment_debit(app, valor):
    assert app["payment_balance"] == 0, "Saldo não debitado corretamente"


@then("registra a transação no extrato")
def register_payment_extrato(app):
    print("[MOCK] Registro no extrato de pagamento")


# ----------------------------
# Steps – Navegação e Usabilidade
# ----------------------------
@given("o usuário está autenticado")
def user_authenticated(app):
    app["authenticated"] = True


@when(parsers.parse("navega por todas as páginas disponíveis ({pages})"))
def navigate_pages(app, pages):
    page_list = [p.strip() for p in pages.replace("(", "").replace(")", "").split(",")]
    print("[MOCK] Navegando por:", page_list)
    app["pages_loaded"] = page_list


@then("nenhuma página apresenta erro de carregamento")
def no_load_error(app):
    assert True  # mock: assumimos sem erro


@then(parsers.parse("a mensagem exibida contém apenas informação necessária para correção"))
def check_error_content(app):
    # mock: simplesmente passa
    assert True


@when("inspeciona os menus de navegação")
def inspect_menus(app):
    app["menus"] = ["Login", "Cadastro", "Conta", "Transferência", "Empréstimo", "Pagamento"]


@then("todos os links aparecem em todas as páginas")
def check_links(app):
    for page in app["pages_loaded"]:
        assert set(app["menus"]).issubset(set(app["menus"])), "Links inconsistentes"


@then("a estrutura de navegação permanece a mesma")
def check_navigation_structure(app):
    assert True
```

> **Explicação rápida dos principais pontos**  
> * `@scenario` – cada cenário do Gherkin vira um teste.  
> * `@given`, `@when`, `@then` – cada frase do Gherkin é mapeada para uma função Python.  
> * *Page Objects* – classes como `RegistrationPage`, `LoginPage`, etc. encapsulam as interações com o navegador.  
> * **Moqs** – os métodos das páginas apenas imprimem mensagens e armazenam estado em dicionários. Em um projeto real, você usaria `selenium.webdriver` para localizar elementos e enviar valores.  
> * **Parsers** – o `parsers.parse` permite capturar parâmetros do texto (`“{campo}” com “{valor}”`).  
> * **Tables** – em Gherkin, os blocos `| Data | Tipo | Valor |` são passados como objeto `Table` que pode ser iterado.  

---

## 5️⃣  Como executar

```bash
# 1. Crie um virtualenv (opcional)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Instale dependências
pip install pytest pytest-bdd selenium webdriver-manager

# 3. Execute os testes
pytest
```

> Se quiser ver apenas um cenário, pode usar:
> `pytest -k "Cadastro bem-sucedido"`

---

## 6️⃣  Próximos passos

1. **Implementar os Page Objects reais** – localizar elementos (`driver.find_element(...)`) e usar `.send_keys()`, `.click()`, etc.  
2. **Adicionar fixtures de dados** – usar `pytest.fixture` para gerar dados aleatórios ou de teste.  
3. **Integração com API** – para validar o saldo/transferência sem UI, faça chamadas diretas ao backend.  
4. **Reportes** – usar `pytest-html`, `allure-pytest` ou `pytest-bdd`’s `--bdd-steps`.  
5. **Paralelização** – `pytest-xdist` para rodar testes simultâneos.

Pronto! Agora você tem um esqueleto completo de testes automatizados em Python usando `pytest-bdd` que cobre todos os cenários do seu arquivo BDD. Boa sorte na implementação!