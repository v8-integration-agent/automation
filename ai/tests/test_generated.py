## 1.  Visão geral

- **Ferramenta**: `pytest‑bdd` (que combina o `pytest` com a sintaxe Gherkin).  
- **Estrutura**:
  ```
  /project
  ├── features/
  │   ├── cadastro_de_usuario.feature
  │   ├── login.feature
  │   ├── acesso_a_conta.feature
  │   ├── transferencia_fundos.feature
  │   ├── solicitacao_emprestimo.feature
  │   ├── pagamento_de_contas.feature
  │   └── navegacao_uso.feature
  ├── tests/
  │   ├── conftest.py          # fixtures globais (driver, fixtures de banco, etc.)
  │   ├── steps/
  │   │   └── common_steps.py # step‑definitions compartilhadas
  │   └── test_features.py    # arquivo de cenários que chama os *.feature
  ├── page_objects/
  │   ├── base_page.py
  │   ├── cadastro_page.py
  │   ├── login_page.py
  │   └── ...                  # outras páginas
  └── requirements.txt
  ```

> **Obs.** O exemplo abaixo usa **Selenium** como driver Web, mas você pode trocar por Playwright, Cypress‑Python, ou até um mock de API, dependendo da sua aplicação.  

---

## 2.  `requirements.txt`

```txt
pytest>=6
pytest-bdd>=3
selenium>=4
webdriver-manager>=3
```

> Se preferir outro driver, ajuste o import e a criação do driver.

---

## 3.  Feature Files

Crie um arquivo para cada *Feature* (o conteúdo abaixo já está pronto).  
Por convenção, usamos a codificação UTF‑8 e a extensão `.feature`.

### `features/cadastro_de_usuario.feature`

```gherkin
# Feature: Cadastro de Usuário
Feature: Cadastro de Usuário

  Scenario: Cadastros completos são aceitos
    Given o usuário está na página de cadastro
    When ele preenche todos os campos obrigatórios com dados válidos
    And clica no botão “Registrar”
    Then o sistema exibe a mensagem “Cadastro concluído com sucesso”
    And o usuário aparece autenticado na página de login

  Scenario Outline: Dados inválidos bloqueiam o cadastro
    Given o usuário está na página de cadastro
    When ele preenche os campos obrigatórios com "<campo>" inválido
    And clica em “Registrar”
    Then o sistema exibe a mensagem de erro correspondente ao "<campo>"
    And nenhum dado é salvo no banco

    Examples:
      | campo   |
      | telefone|
      | CEP      |
      | email    |

  Scenario: Campos obrigatórios não preenchidos impedem o cadastro
    Given o usuário está na página de cadastro
    When ele deixa o campo “Nome” em branco
    And clica em “Registrar”
    Then o sistema exibe a mensagem “Nome é obrigatório”
```

*(Faça o mesmo para os demais features – basta copiar o texto acima nas respectivas pastas.)*

---

## 4.  Fixtures (`tests/conftest.py`)

```python
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from page_objects.base_page import BasePage

# ----------------------------------------------------------------------
# Driver (Chrome em modo headless)
# ----------------------------------------------------------------------
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ----------------------------------------------------------------------
# Página principal (usada por quase todos os passos)
# ----------------------------------------------------------------------
@pytest.fixture
def base_page(driver):
    return BasePage(driver)
```

> **Obs.** Se sua aplicação for um API (sem UI), troque `driver` por um cliente HTTP (por ex.: `requests.Session()`).

---

## 5.  Page Objects (exemplo mínimo)

### `page_objects/base_page.py`

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to(self, url):
        self.driver.get(url)

    def find(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)
```

### `page_objects/cadastro_page.py`

```python
class CadastroPage(BasePage):
    URL = "https://app.exemplo.com/cadastro"

    # Elementos (usando locators que você deve adaptar)
    btn_registrar = ("css selector", "button#registrar")
    mensagem = ("css selector", "div.alert-success")

    def open(self):
        self.go_to(self.URL)

    def preenche_campos_validos(self):
        # Exemplo simples – preencha os campos necessários
        self.find("id", "nome").send_keys("João Silva")
        self.find("id", "email").send_keys("joao.silva@email.com")
        self.find("id", "telefone").send_keys("11987654321")
        self.find("id", "cep").send_keys("01000-000")
        # ... outros campos

    def preenche_campo_invalido(self, campo):
        if campo == "telefone":
            self.find("id", "telefone").send_keys("abc")          # inválido
        elif campo == "CEP":
            self.find("id", "cep").send_keys("123")              # inválido
        elif campo == "email":
            self.find("id", "email").send_keys("email.com")      # inválido

    def preenche_nome_vazio(self):
        self.find("id", "nome").clear()

    def click_registrar(self):
        self.find(*self.btn_registrar).click()

    def get_mensagem(self):
        return self.find(*self.mensagem).text
```

*(Implemente páginas semelhantes para login, transferências, etc.)*

---

## 6.  Step‑Definitions (`tests/steps/common_steps.py`)

```python
import pytest
from pytest_bdd import given, when, then, parsers

# ----------------------------------------------------------------------
# Cadastro de Usuário
# ----------------------------------------------------------------------
@given("o usuário está na página de cadastro")
def user_on_cadastro_page(base_page):
    page = base_page.__class__(base_page.driver)  # instancia a página específica
    # Se você já tem `CadastroPage` importado, basta usar diretamente
    from page_objects.cadastro_page import CadastroPage
    page = CadastroPage(base_page.driver)
    page.open()
    return page

@when("ele preenche todos os campos obrigatórios com dados válidos")
def fill_all_valid_fields(user_on_cadastro_page):
    user_on_cadastro_page.preenche_campos_validos()

@when("clica no botão “Registrar”")
def click_register(user_on_cadastro_page):
    user_on_cadastro_page.click_registrar()

@then("o sistema exibe a mensagem “Cadastro concluído com sucesso”")
def assert_success_message(user_on_cadastro_page):
    assert "Cadastro concluído com sucesso" in user_on_cadastro_page.get_mensagem()

@then("o usuário aparece autenticado na página de login")
def assert_user_logged_in(base_page):
    # Simples verificação de elemento que só aparece após login
    assert base_page.find("css selector", "div.logged-in").is_displayed()


# ----------------------------------------------------------------------
# Dados inválidos (Scenario Outline)
# ----------------------------------------------------------------------
@when(parsers.cfparse('ele preenche os campos obrigatórios com "<campo>" inválido'))
def fill_invalid_field(user_on_cadastro_page, campo):
    user_on_cadastro_page.preenche_campo_invalido(campo)

@then(parsers.cfparse('o sistema exibe a mensagem de erro correspondente ao "<campo>"'))
def assert_error_message(user_on_cadastro_page, campo):
    mensagem = user_on_cadastro_page.get_mensagem()
    # Mapeamento simples – adapte conforme sua UI
    mensagens_erro = {
        "telefone": "Telefone inválido",
        "CEP": "CEP inválido",
        "email": "Email inválido",
    }
    assert mensagens_erro[campo] in mensagem


@then("nenhum dado é salvo no banco")
def assert_no_data_saved(base_page):
    # Aqui você pode chamar sua camada de persistência ou fazer um GET no endpoint
    # Exemplo fictício:
    from api_client import get_user_by_email  # suponha que exista
    assert get_user_by_email("joao.silva@email.com") is None


# ----------------------------------------------------------------------
# Campos obrigatórios não preenchidos
# ----------------------------------------------------------------------
@when("ele deixa o campo “Nome” em branco")
def leave_name_empty(user_on_cadastro_page):
    user_on_cadastro_page.preenche_nome_vazio()

@then('o sistema exibe a mensagem “Nome é obrigatório”')
def assert_name_required(user_on_cadastro_page):
    assert "Nome é obrigatório" in user_on_cadastro_page.get_mensagem()


# ----------------------------------------------------------------------
# Login – você pode seguir o mesmo padrão
# ----------------------------------------------------------------------
```

> **Dica:** Para cenários que necessitam de dados de banco, use *fixtures* que criam/limpam registros antes de cada teste.

---

## 7.  Testes que carregam os Features (`tests/test_features.py`)

```python
import pytest
from pytest_bdd import scenario

# Cada cenário de cada feature
# -----------------------------------------
# Cadastro
from features.cadastro_de_usuario import (
    cadastro_de_usuario
)

# Login
# -----------------------------------------
# import e assim por diante

# Exemplo de cenário de cadastro completo
@scenario("features/cadastro_de_usuario.feature", "Cadastros completos são aceitos")
def test_cadastro_completo():
    pass  # o corpo fica vazio – o pytest‑bdd já liga os steps

# Cenário Outline – o pytest‑bdd gera 3 cenários automaticamente
@scenario("features/cadastro_de_usuario.feature", "Dados inválidos bloqueiam o cadastro")
def test_dados_invalidos():
    pass

# Cenário de campos vazios
@scenario("features/cadastro_de_usuario.feature", "Campos obrigatórios não preenchidos impedem o cadastro")
def test_campos_obrigatorios():
    pass

# Repita o padrão para as demais features...
```

> Se preferir, basta criar um arquivo `__init__.py` vazio dentro de `tests/steps` para que o `pytest-bdd` descubra os step‑definitions automaticamente.

---

## 8.  Como executar

```bash
$ pip install -r requirements.txt
$ pytest --gherkin-terminal-reporter
```

O parâmetro `--gherkin-terminal-reporter` fornece saída legível (tipo “✓” ou “✗”) – útil para CI.

---

## 9.  Dicas de melhoria

| Item | Como melhorar |
|------|---------------|
| **Mock de API** | Se seu front‑end chama serviços, use `responses` ou `requests-mock` para simular respostas. |
| **Fixture de dados** | Crie uma fixture `user_fixture` que crie um usuário antes dos testes de login. |
| **Páginas mais detalhadas** | Crie métodos separados (por exemplo, `fill_account_number`, `select_destination`) para cada ação. |
| **Logs e screenshots** | Em caso de falha, capture screenshot (`driver.save_screenshot`). |
| **CI** | Adicione um job no GitHub Actions com `pytest` e reporte em formato JUnit. |

---

## 10.  Resumo

- **Estrutura**: Features, Step‑definitions, Fixtures + Page Objects.  
- **Ferramenta**: `pytest-bdd` + Selenium.  
- **Testes**: Cada cenário é carregado via `@scenario`.  
- **Extensibilidade**: É só criar novas páginas e passos quando a UI mudar.

Agora, com esses arquivos de base, você já tem um framework completo que traduz diretamente os cenários BDD em testes automatizados em Python. Boa codificação!