## 🚀 Automação BDD → Pytest‑BDD (Python)

> **Obs.**  
> Os exemplos abaixo são *esqueleto* – não há seletores reais, nem lógica de negócio, apenas a estrutura que você precisará preencher para transformar os *features* BDD em testes automatizados com Selenium + pytest‑bdd.

---

### 1. Estrutura de Diretórios

```
paraBank/
├── tests/
│   ├── conftest.py                 # fixtures globais (webdriver, fixtures de dados, etc.)
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── signup_page.py
│   │   ├── login_page.py
│   │   ├── dashboard_page.py
│   │   ├── transfer_page.py
│   │   ├── loan_page.py
│   │   └── payment_page.py
│   ├── features/
│   │   ├── cadastro.feature
│   │   ├── login.feature
│   │   ├── saldo_extrato.feature
│   │   ├── transferencia.feature
│   │   ├── solicitacao_emprestimo.feature
│   │   ├── pagamento_contas.feature
│   │   └── navegacao_uso.feature
│   └── steps/
│       ├── cadastro_steps.py
│       ├── login_steps.py
│       ├── saldo_extrato_steps.py
│       ├── transferencia_steps.py
│       ├── solicitacao_emprestimo_steps.py
│       ├── pagamento_contas_steps.py
│       └── navegacao_uso_steps.py
└── requirements.txt
```

> **Tip** – Use *Page Objects* (`pages/*.py`) para manter a manutenção de seletores longe dos steps.

---

### 2. `requirements.txt`

```txt
pytest==8.0.0
pytest-bdd==4.1.0
selenium==4.22.0
webdriver-manager==4.0.1
```

Instale tudo:

```bash
pip install -r requirements.txt
```

---

### 3. `conftest.py`

```python
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="session")
def driver():
    """Inicializa um driver Selenium (Chrome)."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")          # Remova se quiser ver o navegador
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# Se desejar usar fixtures de dados (ex.: criar usuários via API) faça aqui.
```

---

### 4. Page Objects (exemplo: `signup_page.py`)

```python
from selenium.webdriver.common.by import By

class SignUpPage:
    URL = "https://parabank.com/signup"

    # Seletores (exemplo)
    _name = (By.ID, "name")
    _address = (By.ID, "address")
    _city = (By.ID, "city")
    _state = (By.ID, "state")
    _zip = (By.ID, "zip")
    _phone = (By.ID, "phone")
    _email = (By.ID, "email")
    _password = (By.ID, "password")
    _create_btn = (By.ID, "createAccount")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def fill_form(self, data: dict):
        for field, selector in {
            "Nome": self._name,
            "Endereço": self._address,
            "Cidade": self._city,
            "Estado": self._state,
            "CEP": self._zip,
            "Telefone": self._phone,
            "Email": self._email,
            "Senha": self._password,
        }.items():
            if field in data:
                self.driver.find_element(*selector).clear()
                self.driver.find_element(*selector).send_keys(data[field])

    def click_create(self):
        self.driver.find_element(*self._create_btn).click()

    def get_flash_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".alert").text
```

> **Obs.** Faça o mesmo para as demais páginas: `LoginPage`, `DashboardPage`, `TransferPage`, `LoanPage`, `PaymentPage`.

---

### 5. Feature Files

> **Exemplo**: `cadastro.feature`

```gherkin
Feature: Cadastro de Usuário (ParaBank)
  Como usuário do ParaBank
  Quero criar uma conta
  Para que eu possa utilizar os serviços bancários.

  Scenario: Cadastro de usuário com todos os campos obrigatórios preenchidos
    Given que eu estou na página de cadastro
    When eu preencho todos os campos obrigatórios com valores válidos
      | Campo        | Valor                   |
      | Nome         | João Silva              |
      | Endereço     | Rua A, 123              |
      | Cidade       | São Paulo               |
      | Estado       | SP                      |
      | CEP          | 01234-567                |
      | Telefone     | (11) 98765-4321          |
      | Email        | joao.silva@example.com  |
      | Senha        | SenhaSegura123!         |
    And eu clico em “Criar Conta”
    Then devo ver a mensagem de confirmação “Registro concluído com sucesso”
    And devo poder acessar a tela de login

  Scenario: Cadastro de usuário com telefone inválido
    Given que eu estou na página de cadastro
    When eu preencho todos os campos obrigatórios
      | Campo        | Valor           |
      | Nome         | Maria Pereira   |
      | Endereço     | Av B, 456       |
      | Cidade       | Rio de Janeiro  |
      | Estado       | RJ              |
      | CEP          | 12345-678        |
      | Telefone     | 123abc          |
      | Email        | maria@exemplo.com |
      | Senha        | Senha1234!      |
    And eu clico em “Criar Conta”
    Then devo ver a mensagem de erro “Telefone inválido, por favor insira apenas números”
```

> Copie a estrutura (apenas alterando os textos) para os demais arquivos de feature listados.

---

### 6. Steps – `cadastro_steps.py`

```python
import pytest
from pytest_bdd import scenario, given, when, then, parsers

from pages.signup_page import SignUpPage

# --------------------------------------------
#  Feature: Cadastro de Usuário (ParaBank)
# --------------------------------------------

@pytest.mark.usefixtures("driver")
@scenario("features/cadastro.feature", "Cadastro de usuário com todos os campos obrigatórios preenchidos")
def test_cadastro_completo(driver):
    pass

@pytest.mark.usefixtures("driver")
@scenario("features/cadastro.feature", "Cadastro de usuário com telefone inválido")
def test_cadastro_telefone_invalido(driver):
    pass


# ---------- Givens ----------

@given("que eu estou na página de cadastro")
def open_signup(driver):
    page = SignUpPage(driver)
    page.open()
    return page

# ---------- Whens ----------

@when(parsers.parse('eu preencho todos os campos obrigatórios com valores válidos\n{table}'))
def preenche_cadastro_completo(driver, table, open_signup):
    """
    table: objeto pandas DataFrame (colunas Campo/Valor)
    """
    dados = {row["Campo"]: row["Valor"] for _, row in table.iterrows()}
    open_signup.fill_form(dados)

@when(parsers.parse('eu preencho todos os campos obrigatórios\n{table}'))
def preenche_cadastro_valores(driver, table, open_signup):
    dados = {row["Campo"]: row["Valor"] for _, row in table.iterrows()}
    open_signup.fill_form(dados)

@when('eu clico em “Criar Conta”')
def clicar_criar_conta(open_signup):
    open_signup.click_create()

# ---------- Thens ----------

@then('devo ver a mensagem de confirmação “Registro concluído com sucesso”')
def ver_mensagem_confirmacao(open_signup):
    assert "Registro concluído com sucesso" in open_signup.get_flash_message()

@then('devo poder acessar a tela de login')
def verificar_login_page(driver):
    # Um exemplo simples – substitua pelo seu selector de login
    assert "Login" in driver.title

@then('devo ver a mensagem de erro “Telefone inválido, por favor insira apenas números”')
def ver_mensagem_erro_telefone(open_signup):
    assert "Telefone inválido" in open_signup.get_flash_message()
```

> **Notas**  
> 1. `parsers.parse` permite capturar a tabela como *pandas DataFrame* (pytest‑bdd já converte).  
> 2. Se você preferir usar `@given`, `@when`, `@then` sem parâmetros, basta passar o texto exato.  
> 3. Crie arquivos *steps* semelhantes para cada feature (login, saldo, transferência, etc.).

---

### 7. Exemplo de Steps para **Login** – `login_steps.py`

```python
import pytest
from pytest_bdd import scenario, given, when, then, parsers

from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
@scenario("features/login.feature", "Login com credenciais válidas")
def test_login_credenciais_validas(driver):
    pass

@pytest.mark.usefixtures("driver")
@scenario("features/login.feature", "Login com credenciais inválidas – e‑mail não cadastrado")
def test_login_email_nao_cadastrado(driver):
    pass

@pytest.mark.usefixtures("driver")
@scenario("features/login.feature", "Login com credenciais inválidas – senha incorreta")
def test_login_senha_incorreta(driver):
    pass


# -------- Givens --------

@given("que eu estou na página de login")
def abrir_login(driver):
    page = LoginPage(driver)
    page.open()
    return page


# -------- Whens --------

@when(parsers.parse('eu informo meu e‑mail "{email}" e senha "{senha}"'))
def informar_login(driver, email, senha, abrir_login):
    abrir_login.login(email, senha)


@when('eu clico em “Entrar”')
def clicar_entrar(abrir_login):
    abrir_login.click_enter()


# -------- Thens --------

@then('devo ser redirecionado para a página inicial da minha conta')
def verificar_redirecionamento(driver):
    # Exemplo: esperar título ou URL específica
    assert "Dashboard" in driver.title


@then('devo ver o cabeçalho “Bem‑vindo, João”')
def verificar_cabecalho(driver):
    assert "Bem‑vindo, João" in driver.page_source


@then('devo ver a mensagem de erro “E‑mail ou senha inválidos”')
def verificar_mensagem_erro(driver):
    login_page = LoginPage(driver)
    assert "E‑mail ou senha inválidos" in login_page.get_error_message()
```

> Repita a lógica para **saldo/extra**, **transferência**, **empréstimo**, **pagamento**, **navegação**.  
> Cada feature possui seu *scenario* e os *steps* correspondentes.

---

### 8. Como executar

```bash
# Na raiz do projeto
pytest tests
```

O pytest‑bdd irá ler os arquivos `.feature`, mapear os passos com os *functions* e executar os testes.

---

## 📌 Boas práticas

1. **Page Objects**  
   Mantenha a lógica de interação com a UI dentro das classes de página. Assim, se os seletores mudarem, só precisa ajustar uma vez.

2. **Data‑Driven**  
   Use arquivos de dados (`csv`, `json`) ou *fixtures* para gerar usuários aleatórios – evita repetir dados estáticos em cada teste.

3. **Assertas**  
   Use `assert` de forma clara – mensagem de erro útil quando algo falha.

4. **Headless vs Visual**  
   Para debugging, remova `options.add_argument("--headless")` e rode o navegador de forma visível.

5. **Parallel**  
   Se precisar, configure o pytest para rodar testes em paralelo (ex.: `pytest -n 4` com `pytest-xdist`).

---

> **Próximo passo**: Preencher os seletores reais nas classes de página, adaptar as ações (ex.: `login()`, `click_enter()`, `get_error_message()`), e, se desejar, adicionar *hooks* de *setup/teardown* para criar e deletar usuários via API antes do teste.  

Boa codificação! 🚀