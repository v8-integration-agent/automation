**Resumo**

Abaixo está um *exemplo completo* de como transformar todos os cenários que você forneceu em testes automatizados usando **Python + pytest‑bdd** (e Selenium como driver de navegador).  
O código está organizado em:

| Pasta | Conteúdo | Por quê? |
|-------|----------|----------|
| `features/` | Arquivos Gherkin (.feature) | O arquivo original que o `pytest-bdd` lê |
| `features/*.feature` | Cada *Feature* em um arquivo | Mantém o código organizado e facilita a leitura |
| `steps/` | Implementações de *steps* | Reutilização de código e separação de responsabilidades |
| `pages/` | *Page Objects* | Abstração de UI, facilita manutenção |
| `conftest.py` | *Fixtures* globais | Selenium driver, dados de teste, etc. |
| `tests/` | Testes *pytest-bdd* (opcional) | Se preferir agrupar os testes em módulos |

> **Obs.**  
> • O exemplo abaixo **não** executa testes reais; ele contém apenas *placeholders* (`pass`, `assert False`, etc.) para que você possa preencher com a lógica da sua aplicação.  
> • Você precisará de **Selenium**, **pytest** e **pytest‑bdd** instalados (`pip install selenium pytest pytest-bdd`).

---

## 1. Estrutura de diretórios

```
project/
│
├── conftest.py          # Fixtures globais
├── requirements.txt
│
├── pages/
│   ├── base_page.py
│   ├── cadastro_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── extrato_page.py
│   ├── transferencia_page.py
│   ├── solicitacao_emprestimo_page.py
│   └── pagamento_page.py
│
├── features/
│   ├── cadastro.feature
│   ├── login.feature
│   ├── saldo_extrato.feature
│   ├── transferencia.feature
│   ├── solicitacao_emprestimo.feature
│   ├── pagamento_contas.feature
│   └── navegacao.feature
│
└── steps/
    ├── steps_cadastro.py
    ├── steps_login.py
    ├── steps_saldo_extrato.py
    ├── steps_transferencia.py
    ├── steps_solicitacao_emprestimo.py
    ├── steps_pagamento.py
    └── steps_navegacao.py
```

---

## 2. `conftest.py` – Fixtures globais

```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.base_page import BasePage

@pytest.fixture(scope="session")
def driver():
    """Inicia o WebDriver (Chrome headless por padrão)."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def base_page(driver):
    """Instância de página base para acessar utilitários comuns."""
    return BasePage(driver)

@pytest.fixture
def cadastro_page(driver):
    from pages.cadastro_page import CadastroPage
    return CadastroPage(driver)

# ... Adicione outras fixtures de página aqui (login_page, dashboard_page, etc.)
```

---

## 3. `pages/base_page.py` – Página base

```python
# pages/base_page.py
from selenium.webdriver.remote.webdriver import WebDriver

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)

    def get_text(self, selector: str) -> str:
        return self.driver.find_element_by_css_selector(selector).text

    def click(self, selector: str):
        self.driver.find_element_by_css_selector(selector).click()

    def type(self, selector: str, value: str):
        el = self.driver.find_element_by_css_selector(selector)
        el.clear()
        el.send_keys(value)

    def select(self, selector: str, visible_text: str):
        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element_by_css_selector(selector)).select_by_visible_text(visible_text)

    def assert_text(self, selector: str, expected: str):
        actual = self.get_text(selector)
        assert actual == expected, f'Esperado "{expected}", mas foi "{actual}"'
```

> **Sugestão**: Crie *Page Objects* para cada página (Cadastro, Login, Dashboard, etc.) estendendo `BasePage` e adicionando métodos específicos.

---

## 4. Features em Gherkin

### 4.1 `features/cadastro.feature`

```gherkin
Feature: Cadastro de Usuário

  Scenario: Cadastro bem‑sucesso com todos os campos obrigatórios preenchidos
    Given o usuário está na página de cadastro
    When ele preenche os campos: nome, CPF, telefone, CEP, email, senha e confirma a senha
    And clica em “Registrar”
    Then o sistema deve exibir a mensagem “Cadastro efetuado com sucesso”
    And o usuário deve ser redirecionado à página de login

  Scenario: Tentativa de cadastro com campo telefone inválido
    Given o usuário está na página de cadastro
    When ele preenche todos os campos, mas insere um telefone com caracteres inválidos
    And clica em “Registrar”
    Then o sistema deve exibir “Telefone inválido – use o formato (xx) xxxx‑xxxx”

  Scenario: Tentativa de cadastro com e‑mail duplicado
    Given um usuário já cadastrado com e‑mail “exemplo@teste.com”
    And o usuário está na página de cadastro
    When ele preenche todos os campos, usando o mesmo e‑mail
    And clica em “Registrar”
    Then o sistema deve exibir “E‑mail já cadastrado. Por favor, use outro endereço”

  Scenario: Campos obrigatórios em branco
    Given o usuário está na página de cadastro
    When ele clica em “Registrar” sem preencher nenhum campo
    Then o sistema deve exibir “Todos os campos são obrigatórios”
```

> **Obs.**: Salve este conteúdo no arquivo `features/cadastro.feature`.  
> Faça o mesmo para os demais arquivos de feature (`login.feature`, `saldo_extrato.feature`, etc.).

---

## 5. Implementação dos *steps* – Exemplo: Cadastro

### 5.1 `steps/steps_cadastro.py`

```python
# steps/steps_cadastro.py
import uuid
from pytest_bdd import scenarios, given, when, then, parsers
from pages.cadastro_page import CadastroPage

# Carrega os cenários deste arquivo
scenarios("../features/cadastro.feature")

@given('o usuário está na página de cadastro')
def open_cadastro_page(cadastro_page):
    cadastro_page.open("https://suaapp.com/cadastro")

@given(parsers.parse('um usuário já cadastrado com e‑mail "{email}"'))
def create_user_fixture(cadastro_page, email):
    # Aqui você pode usar API, banco, ou Selenium para criar o usuário.
    # Exemplo: cadastro_page.create_user(email=email, ... )
    pass  # IMPLEMENTE

@when(parsers.parse('ele preenche os campos: {fields}'))
def preencher_campos(cadastro_page, fields):
    # fields → "nome, CPF, telefone, CEP, email, senha e confirma a senha"
    dados = {
        "nome": "João Silva",
        "CPF": "123.456.789-00",
        "telefone": "(12) 3456-7890",
        "CEP": "01001-000",
        "email": f"joao+{uuid.uuid4()}@teste.com",
        "senha": "Pass1234!",
        "confirma_senha": "Pass1234!",
    }
    for campo in [f.strip() for f in fields.split(',')]:
        cadastro_page.fill_field(campo, dados[campo])

@when('clica em “Registrar”')
def clica_registrar(cadastro_page):
    cadastro_page.click_register()

@then(parsers.parse('o sistema deve exibir a mensagem "{message}"'))
def verifica_mensagem(cadastro_page, message):
    assert cadastro_page.get_message() == message

@then('o usuário deve ser redirecionado à página de login')
def verifica_redirecionamento_login(cadastro_page):
    assert cadastro_page.current_url.endswith("/login")
```

> **Dica**: O método `fill_field` em `CadastroPage` deve mapear os nomes dos campos (nome, CPF, telefone, etc.) para os seletores CSS corretos.

---

## 6. Page Object de exemplo – Cadastro

```python
# pages/cadastro_page.py
from pages.base_page import BasePage

class CadastroPage(BasePage):
    URL = "https://suaapp.com/cadastro"

    # Seletores CSS (exemplo; ajuste de acordo com seu código)
    SELECTORS = {
        "nome": "input[name='nome']",
        "CPF": "input[name='cpf']",
        "telefone": "input[name='telefone']",
        "CEP": "input[name='cep']",
        "email": "input[name='email']",
        "senha": "input[name='senha']",
        "confirma_senha": "input[name='confirma_senha']",
        "registrar": "button#registrar",
        "mensagem": "div.alert",
    }

    def fill_field(self, field_name: str, value: str):
        selector = self.SELECTORS[field_name]
        self.type(selector, value)

    def click_register(self):
        self.click(self.SELECTORS["registrar"])

    def get_message(self) -> str:
        return self.get_text(self.SELECTORS["mensagem"])
```

---

## 7. Reaproveitando *steps* em outras Features

A estrutura acima permite reutilizar *steps* em múltiplos cenários.  
Basta importar o arquivo de *steps* (`from steps.steps_cadastro import *`) nos arquivos de *steps* que precisam dele.

Por exemplo, em `steps/steps_login.py`:

```python
# steps/steps_login.py
from pytest_bdd import scenarios, given, when, then
from steps.steps_cadastro import create_user_fixture  # Reuso

scenarios("../features/login.feature")

@given('o usuário já está cadastrado')
def ensure_user_registered(create_user_fixture):
    pass  # já implementado em cadastro

# ... restante dos *steps* (login, senha, etc.)
```

---

## 8. Como executar

```bash
# Instale as dependências
pip install selenium pytest pytest-bdd

# Execute todos os testes
pytest
```

Para executar apenas uma feature, use:

```bash
pytest -k cadastro  # ou outro nome da feature
```

---

## 9. Exemplos de *steps* restantes

> **Observação**: Os exemplos abaixo não estão completos, apenas ilustram a ideia de reutilização.  
> Adapte os seletores CSS e a lógica de negócio de acordo com sua aplicação.

### 9.1 Login – `steps/steps_login.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage

scenarios("../features/login.feature")

@given('o usuário já está cadastrado')
def prepare_user(login_page):
    # Use API ou fixture para criar o usuário
    pass

@given('está na página de login')
def open_login_page(login_page):
    login_page.open()

@when('ele digita seu e‑mail e senha corretos')
def digita_credenciais(login_page):
    login_page.login(email="joao@teste.com", senha="Pass1234!")

@when('ele digita seu e‑mail e uma senha inválida')
def digita_credenciais_invalida(login_page):
    login_page.login(email="joao@teste.com", senha="wrong")

@when('clica em “Entrar”')
def clica_entrar(login_page):
    login_page.submit()

@then('o sistema deve redirecionar para a página inicial da conta')
def verifica_dashboard(login_page):
    assert login_page.current_url.endswith("/dashboard")

@then('o sistema deve exibir “Credenciais inválidas. Tente novamente”')
def verifica_erro_login(login_page):
    assert login_page.get_error_message() == "Credenciais inválidas. Tente novamente"
```

### 9.2 Saldo & Extrato – `steps/steps_saldo_extrato.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers
from pages.dashboard_page import DashboardPage

scenarios("../features/saldo_extrato.feature")

@given('o usuário está logado')
def login_automated(dashboard_page):
    dashboard_page.login()
    # ou use fixture para login

@given(parsers.parse('sua conta tem saldo de R$ {saldo:.2f}'))
def set_saldo(dashboard_page, saldo):
    dashboard_page.set_balance(saldo)

@when(parsers.parse('ele realiza um depósito de R$ {valor:.2f}'))
def deposito(dashboard_page, valor):
    dashboard_page.deposit(valor)

@then(parsers.parse('o saldo exibido na página inicial deve ser R$ {saldo_final:.2f}'))
def verifica_saldo(dashboard_page, saldo_final):
    assert dashboard_page.get_balance() == saldo_final
```

> *Continue desta forma para Transferência, Empréstimo, Pagamento e Navegação.*

---

## 10. Boas práticas

1. **Separar dados de teste**  
   Use *fixtures* para gerar dados aleatórios (UUIDs, emails, etc.).  
2. **Page Object**  
   Mantém os *steps* limpos e evita duplicação de seletores.  
3. **Mantenha os *steps* idempotentes**  
   Cada `Given`/`When`/`Then` deve ser executável em qualquer ordem.  
4. **Logs e capturas**  
   Se um teste falhar, capture tela (`driver.get_screenshot_as_file`) e logs de console.  
5. **Parâmetros de ambiente**  
   Use variáveis de ambiente (`os.getenv`) para URLs, credenciais, etc., permitindo rodar em *staging*, *prod*, *dev*, etc.

---

## 11. Próximos passos

1. **Implementar os *steps* restantes** – seguindo o modelo de cadastro e login.  
2. **Adicionar validações de banco de dados** (opcional) – para garantir que transações realmente ocorreram.  
3. **Criar relatório** – `pytest --html=report.html --self-contained-html`.  
4. **Integrar CI** – GitHub Actions, GitLab CI, etc.

Boa codificação e bons testes! 🚀