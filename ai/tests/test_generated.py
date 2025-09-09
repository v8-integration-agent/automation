## 1.  Estrutura de pastas

```
para_bank/
├── conftest.py
├── features/
│   ├── cadastro.feature
│   ├── login.feature
│   ├── saldo_extrato.feature
│   ├── transferencia.feature
│   ├── emprestimo.feature
│   ├── pagamento.feature
│   └── navegacao_mensagens_menus.feature
└── tests/
    ├── test_cadastro.py
    ├── test_login.py
    ├── test_saldo_extrato.py
    ├── test_transferencia.py
    ├── test_emprestimo.py
    ├── test_pagamento.py
    └── test_navegacao_mensagens_menus.py
```

> **Obs.**  
> 1. **`conftest.py`** contém fixtures comuns (ex.: browser, login, page‑objects).  
> 2. Os arquivos `.feature` são copiados exatamente como você forneceu (sem as tags `@cadastro`, `@login` etc.).  
> 3. Cada *feature* tem seu módulo de testes correspondente que importa apenas os *scenarios* que pertencem a ela.

---

## 2.  `conftest.py` – Fixtures e Page‑Objects

```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------
# Fixtures
# ----------------------
@pytest.fixture(scope="session")
def browser():
    """Inicia um driver do Chrome em modo headless."""
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login(browser):
    """Login pré‑requisito para cenários que precisam de conta válida."""
    browser.get("https://www.para-bank.com/login")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "email"))
    ).send_keys("usuario@exemplo.com")
    browser.find_element(By.ID, "senha").send_keys("SenhaSegura123")
    browser.find_element(By.ID, "entrar").click()
    # espera a página inicial aparecer
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "saldo_inicial"))
    )
    return browser


# ----------------------
# Page‑Object helpers
# ----------------------
class Page:
    """Base para todas as páginas – apenas exemplos de helpers."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill(self, locator, value):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(value)

    def text_of(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text


# Exemplo de Page‑Object para a tela de cadastro
class CadastroPage(Page):
    _email = (By.ID, "email")
    _senha = (By.ID, "senha")
    _confirma_senha = (By.ID, "confirma_senha")
    _nome = (By.ID, "nome")
    _telefone = (By.ID, "telefone")
    _endereco = (By.ID, "endereco")
    _cadastrar_btn = (By.ID, "cadastrar")

    def go_to(self):
        self.driver.get("https://www.para-bank.com/registrar")
        return self

    def preenche_dados_gerais(self, dados):
        for campo, valor in dados.items():
            locator = getattr(self, f"_{campo.lower()}")
            self.fill(locator, valor)

    def preenche_erro(self, campo):
        # deixa o campo <campo> em branco
        locator = getattr(self, f"_{campo.lower()}")
        self.fill(locator, "")

    def clicar_cadastrar(self):
        self.click(self._cadastrar_btn)

    def mensagem_confirmação(self):
        return self.text_of((By.ID, "mensagem_confirmacao"))

    def mensagem_erro(self):
        return self.text_of((By.ID, "mensagem_erro"))


# Outras páginas (LoginPage, SaldoPage, TransferenciaPage, etc.) seguem a mesma lógica
# -------------------------------------------------------------
```

> **Nota** – O código acima é apenas um *esqueleto*.  
> Você deve ajustá‑lo de acordo com os *locators* reais da sua aplicação (IDs, classes, XPaths…).

---

## 3.  Arquivos `.feature`

> **Obs.**  
> Copie os trechos **exatamente** abaixo – eles já contêm todas as *tags* e *examples*.

### 3.1 `features/cadastro.feature`

```gherkin
Feature: Cadastro de Usuário

@cadastro
Scenario: Usuário cadastra-se com sucesso
  Given que eu estou na tela de cadastro
  When preencho todos os campos obrigatórios com dados válidos
  And clico em "Cadastrar"
  Then devo ver uma mensagem de confirmação "Cadastro concluído com sucesso"
  And devo conseguir fazer login com as credenciais recém‑criadas

@cadastro
Scenario Outline: Usuário tenta se cadastrar com campo obrigatório em branco
  Given que eu estou na tela de cadastro
  When deixo o campo "<campo>" em branco
  And preencho os demais campos com dados válidos
  And clico em "Cadastrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo           | mensagem                                 |
    | Nome            | "O nome é obrigatório"                   |
    | Email           | "O email é obrigatório"                  |
    | Senha           | "A senha é obrigatória"                  |
    | Confirmação Senha | "A confirmação de senha é obrigatória" |

@cadastro
Scenario Outline: Usuário tenta se cadastrar com dados inválidos
  Given que eu estou na tela de cadastro
  When preencho o campo "<campo>" com "<valor>"
  And preencho os demais campos com dados válidos
  And clico em "Cadastrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo    | valor           | mensagem                                |
    | Email    | "usuario.com"   | "Formato de email inválido"             |
    | Telefone | "123"           | "Formato de telefone inválido"          |
    | CEP      | "abcde"         | "Formato de CEP inválido"               |
```

### 3.2 `features/login.feature`

```gherkin
Feature: Login

@login
Scenario: Usuário faz login com credenciais válidas
  Given que eu tenho uma conta válida
  When eu entro na tela de login
  And preencho o campo "Email" com "usuario@exemplo.com"
  And preencho o campo "Senha" com "SenhaSegura123"
  And clico em "Entrar"
  Then devo ser redirecionado para a página inicial da conta
  And devo ver o saldo atualizado

@login
Scenario Outline: Usuário tenta fazer login com credenciais inválidas
  Given que eu tenho uma conta válida
  When eu entro na tela de login
  And preencho o campo "Email" com "<email>"
  And preencho o campo "Senha" com "<senha>"
  And clico em "Entrar"
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | email                     | senha       | mensagem                                               |
    | "invalido@exemplo.com"    | "senhaErrada" | "Credenciais inválidas. Tente novamente."           |
    | ""                         | "SenhaSegura123" | "O email é obrigatório."                         |
    | "usuario@exemplo.com"      | ""               | "A senha é obrigatória."                           |
```

### 3.3 `features/saldo_extrato.feature`

```gherkin
Feature: Acesso à Conta – Saldo e Extrato

@saldo
Scenario: Exibição do saldo após operação financeira
  Given que o usuário está autenticado
  And possui saldo inicial de R$ 1.000,00
  When realizo uma transferência de R$ 200,00
  Then o saldo exibido deve ser R$ 800,00

@extrato
Scenario: O extrato lista transações recentes em ordem cronológica
  Given que o usuário está autenticado
  And já realizou as seguintes transações:
    | Data        | Descrição          | Valor  |
    | 01/10/2023 | Depósito           | +R$500 |
    | 02/10/2023 | Transferência      | -R$200 |
  When acesso a página de extrato
  Then devo ver a lista de transações ordenada por data mais recente para mais antiga
```

### 3.4 `features/transferencia.feature`

```gherkin
Feature: Transferência de Fundos

@transferencia
Scenario: Usuário transfere fundos entre contas
  Given que o usuário possui a conta origem com saldo R$ 1.000,00
  And possui a conta destino
  When seleciono a conta origem
  And seleciono a conta destino
  And informo o valor de R$ 300,00
  And confirmo a transferência
  Then o saldo da conta origem deve ser R$ 700,00
  And o saldo da conta destino deve ser R$ 300,00
  And a transação deve aparecer no histórico de ambas as contas

@transferencia
Scenario: Usuário não pode transferir valor superior ao saldo disponível
  Given que o usuário possui a conta origem com saldo R$ 100,00
  When tento transferir R$ 200,00
  Then devo ver a mensagem de erro "Transferência não pode exceder o saldo disponível"

@transferencia
Scenario Outline: Usuário tenta transferir com dados incompletos
  Given que o usuário possui conta origem com saldo R$ 500,00
  When informo o valor "<valor>" e deixo "<campo>" vazio
  And confirmo a transferência
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo          | valor  | mensagem                                |
    | Conta Destino  | 100    | "A conta de destino é obrigatória"     |
    | Valor          | ""     | "O valor da transferência é obrigatório"|
```

### 3.5 `features/emprestimo.feature`

```gherkin
Feature: Solicitação de Empréstimo

@emprestimo
Scenario: Usuário solicita empréstimo e recebe aprovação
  Given que o usuário possui renda anual de R$ 80.000,00
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo R$ 20.000,00
  And confirmo a solicitação
  Then o sistema deve retornar o status "Aprovado"
  And devo ver a mensagem "Empréstimo aprovado em até 3 dias úteis"

@emprestimo
Scenario: Usuário solicita empréstimo e é negado
  Given que o usuário possui renda anual de R$ 30.000,00
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo R$ 20.000,00
  And confirmo a solicitação
  Then o sistema deve retornar o status "Negado"
  And devo ver a mensagem "Empréstimo negado por insuficiência de renda"

@emprestimo
Scenario Outline: Usuário fornece dados inválidos na solicitação de empréstimo
  Given que o usuário tem renda anual de "<renda>"
  When acesso a página de solicitação de empréstimo
  And informo o valor do empréstimo "<valor>"
  And confirmo a solicitação
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | renda    | valor | mensagem                                   |
    | 80.000   | "-500"| "O valor do empréstimo deve ser positivo" |
    | 80.000   | "0"   | "O valor do empréstimo deve ser maior que zero" |
```

### 3.6 `features/pagamento.feature`

```gherkin
Feature: Pagamento de Contas

@pagamento
Scenario: Usuário registra pagamento de conta
  Given que o usuário está autenticado
  When acesso a página de pagamento de contas
  And preencho:
    | Beneficiário | Endereço | Cidade | Estado | CEP   | Telefone     | Conta | Valor | Data   |
    | "Eletricidade" | "Av. X" | "SP"   | "SP"   | "12345-678" | "(11) 98765-4321" | "123456" | 200 | 15/11/2023 |
  And confirmo o pagamento
  Then devo ver a mensagem "Pagamento confirmado"
  And o pagamento deve aparecer no histórico de transações na data correta

@pagamento
Scenario: Pagamento futuro respeita data de agendamento
  Given que o usuário está autenticado
  When registro pagamento agendado para 01/12/2023
  And confirmo
  Then a data de vencimento exibida deve ser 01/12/2023
  And o pagamento só deve aparecer no extrato após 01/12/2023

@pagamento
Scenario Outline: Usuário tenta registrar pagamento com campo inválido
  Given que o usuário está autenticado
  When preencho o campo "<campo>" com "<valor>"
  And confirmo o pagamento
  Then devo ver a mensagem de erro "<mensagem>"
  
  Examples:
    | campo        | valor          | mensagem                                |
    | CEP          | "abcde"        | "Formato de CEP inválido"               |
    | Telefone     | "123"          | "Formato de telefone inválido"          |
    | Valor        | "-100"         | "Valor do pagamento deve ser positivo" |
```

### 3.7 `features/navegacao_mensagens_menus.feature`

```gherkin
Feature: Requisitos Gerais de Navegação e Usabilidade

@navegacao
Scenario: Todas as páginas carregam sem erros de navegação
  Given que estou autenticado
  When navego entre todas as páginas do aplicativo
  Then cada página deve carregar com sucesso e sem mensagens de erro

@mensagens
Scenario: Mensagens de erro são claras e objetivas
  Given que eu realizo uma ação inválida
  When a aplicação exibe um erro
  Then a mensagem deve conter a razão do erro e instruções de correção

@menus
Scenario: Links e menus são consistentes em todas as páginas
  Given que estou em qualquer página do aplicativo
  When verifico os itens de navegação no cabeçalho
  Then eles devem ser os mesmos que na página inicial
```

---

## 4.  Módulos de testes – *Scenario* → *Test File*

> **Obs.**  
> Cada arquivo de teste importa os *scenarios* de sua feature e contém as definições de *steps* que interagem com os *Page Objects* criados em `conftest.py`.

### 4.1 `tests/test_cadastro.py`

```python
# tests/test_cadastro.py
from pytest_bdd import scenario, given, when, then, parsers
from .conftest import CadastroPage


@scenario("features/cadastro.feature", "Usuário cadastra-se com sucesso")
def test_cadastro_sucesso():
    pass


@scenario("features/cadastro.feature", "Usuário tenta se cadastrar com campo obrigatório em branco")
def test_cadastro_campo_obrigatorio_branco():
    pass


@scenario("features/cadastro.feature", "Usuário tenta se cadastrar com dados inválidos")
def test_cadastro_dados_invalidos():
    pass


# ----------------- Step Definitions -----------------
@given("que eu estou na tela de cadastro")
def go_to_cadastro(browser):
    page = CadastroPage(browser)
    page.go_to()
    return page


@given(parsers.parse('preencho todos os campos obrigatórios com dados válidos'))
def preenche_todos_os_campos_gerais(page):
    dados = {
        "nome": "João Silva",
        "email": "joao.silva+{random}@exemplo.com",
        "senha": "SenhaSegura123",
        "confirma_senha": "SenhaSegura123",
        "telefone": "(11) 98765-4321",
        "endereco": "Rua X, 123",
        "cep": "12345-678"
    }
    page.preenche_dados_gerais(dados)


@given(parsers.parse('preencho os demais campos com dados válidos'))
def preenche_campos_gerais(page):
    preenche_todos_os_campos_gerais(page)


@given(parsers.parse('deixo o campo "{campo}" em branco'))
def deixa_campo_branco(page, campo):
    page.preenche_erro(campo)


@given(parsers.parse('preencho o campo "{campo}" com "{valor}"'))
def preenche_campo_com_valor(page, campo, valor):
    locator = getattr(page, f"_{campo.lower()}")
    page.fill(locator, valor)


@when(parsers.parse('clico em "{btn}"'))
def clicar_btn(page, btn):
    if btn.lower() == "cadastrar":
        page.clicar_cadastrar()


@then(parsers.parse('devo ver uma mensagem de confirmação "{msg}"'))
def mensagem_confirmacao(page, msg):
    assert page.mensagem_confirmação() == msg


@then(parsers.parse('devo ver a mensagem de erro "{msg}"'))
def mensagem_erro(page, msg):
    assert page.mensagem_erro() == msg
```

> **Obs.**  
> O passo `preencho todos os campos obrigatórios com dados válidos` cria um endereço aleatório para evitar colisões.  
> Para o teste de login que utiliza as credenciais recém‑criadas, você pode reutilizar o *fixture* `login` e fazer a verificação de login no `then`.

---

### 4.2 `tests/test_login.py`

```python
# tests/test_login.py
from pytest_bdd import scenario, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@scenario("features/login.feature", "Usuário faz login com credenciais válidas")
def test_login_credenciais_validas():
    pass


@scenario("features/login.feature", "Usuário tenta fazer login com credenciais inválidas")
def test_login_credenciais_invalidas():
    pass


# ----------------- Step Definitions -----------------
@given("que eu tenho uma conta válida")
def conta_valida(browser):
    # já está em browser, mas não logou
    return browser


@given("eu entro na tela de login")
def abre_login_page(browser):
    browser.get("https://www.para-bank.com/login")
    return browser


@given(parsers.parse('preencho o campo "{campo}" com "{valor}"'))
def preenche_campo(browser, campo, valor):
    locator = {
        "Email": (By.ID, "email"),
        "Senha": (By.ID, "senha")
    }[campo]
    browser.find_element(*locator).clear()
    browser.find_element(*locator).send_keys(valor)


@when(parsers.parse('clico em "{btn}"'))
def clicar_btn(browser, btn):
    if btn.lower() == "entrar":
        browser.find_element(By.ID, "entrar").click()


@then(parsers.parse('devo ser redirecionado para a página inicial da conta'))
def verifica_redirecionamento(browser):
    WebDriverWait(browser, 10).until(
        EC.url_contains("/conta/")  # ou qualquer substring que indique a página inicial
    )


@then(parsers.parse('devo ver o saldo atualizado'))
def verifica_saldo(browser):
    saldo = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "saldo_inicial"))
    ).text
    assert saldo.startswith("R$")


@then(parsers.parse('devo ver a mensagem de erro "{msg}"'))
def verifica_mensagem_erro(browser, msg):
    erro = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "mensagem_erro"))
    ).text
    assert erro == msg
```

---

### 4.3 `tests/test_saldo_extrato.py`

```python
# tests/test_saldo_extrato.py
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@scenario("features/saldo_extrato.feature", "Exibição do saldo após operação financeira")
def test_saldo_pos_transferencia():
    pass


@scenario("features/saldo_extrato.feature", "O extrato lista transações recentes em ordem cronológica")
def test_extrato_ordem_cronologica():
    pass


# ----------------- Step Definitions -----------------
@given("que o usuário está autenticado")
def login(browser):
    # re‑usa a fixture de login
    return browser


@given(parsers.parse('possui saldo inicial de R$ {valor}'))
def set_saldo_inicial(browser, valor):
    # normalmente isso seria feito via API, mas para testes de UI você pode
    # usar uma página de "gerenciar saldo" ou alterar diretamente no banco
    # (não implementado aqui)
    pass


@given(parsers.parse('realizo uma transferência de R$ {valor}'))
def realiza_transferencia(browser, valor):
    # navega até a tela de transferências
    browser.get("https://www.para-bank.com/transferir")
    # preencher conta destino, etc.
    # não implementado – placeholder
    pass


@given(parsers.parse('o saldo exibido deve ser R$ {valor}'))
def verifica_saldo(browser, valor):
    saldo = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "saldo_inicial"))
    ).text
    assert saldo.strip() == f"R$ {valor}"


@given("já realizou as seguintes transações:")
def carregar_transacoes(browser, table):
    # table é um objeto Table de pytest-bdd. Você pode usar API ou mockar
    pass


@given("acesso a página de extrato")
def abre_extrato(browser):
    browser.get("https://www.para-bank.com/extrato")


@given("devo ver a lista de transações ordenada por data mais recente para mais antiga")
def verifica_ordenacao_extrato(browser):
    linhas = browser.find_elements(By.CSS_SELECTOR, ".transacao")
    datas = [l.text.split("|")[0] for l in linhas]  # simplificação
    assert datas == sorted(datas, reverse=True)
```

> **Obs.** – Para cenários que dependem de *backend* (saldo inicial, transações pré‑existentes) a recomendação é usar mocks ou APIs de preparação.  
> O exemplo acima mostra apenas a estrutura de *steps*.

---

### 4.4 `tests/test_transferencia.py`

```python
# tests/test_transferencia.py
from pytest_bdd import scenario, given, when, then, parsers


@scenario("features/transferencia.feature", "Usuário transfere fundos entre contas")
def test_transferencia_bancaria():
    pass


@scenario("features/transferencia.feature", "Usuário não pode transferir valor superior ao saldo disponível")
def test_transferencia_saldo_insuficiente():
    pass


@scenario("features/transferencia.feature", "Usuário tenta transferir com dados incompletos")
def test_transferencia_dados_incompletos():
    pass


# ----------------- Step Definitions -----------------
@given(parsers.parse('que o usuário possui a conta origem com saldo R$ {saldo}'))
def set_conta_orig(browser, saldo):
    # placeholder
    pass


@given("possui a conta destino")
def conta_dest(browser):
    # placeholder
    pass


@given("seleciono a conta origem")
def seleciona_origem(browser):
    # placeholder
    pass


@given("seleciono a conta destino")
def seleciona_destino(browser):
    # placeholder
    pass


@given(parsers.parse('informo o valor de R$ {valor}'))
def preenche_valor(browser, valor):
    # placeholder
    pass


@given("confirmo a transferência")
def confirma_transferencia(browser):
    # placeholder
    pass


@then(parsers.parse('o saldo da conta origem deve ser R$ {saldo}'))
def verifica_saldo_orig(browser, saldo):
    # placeholder
    pass


@then(parsers.parse('o saldo da conta destino deve ser R$ {saldo}'))
def verifica_saldo_dest(browser, saldo):
    # placeholder
    pass


@then(parsers.parse('a transação deve aparecer no histórico de ambas as contas'))
def verifica_historico(browser):
    # placeholder
    pass


@given(parsers.parse('tento transferir R$ {valor}'))
def tenta_transferir(browser, valor):
    # placeholder
    pass


@then(parsers.parse('devo ver a mensagem de erro "{msg}"'))
def mensagem_erro(browser, msg):
    # placeholder
    pass


# dados incompletos
@given(parsers.parse('informo o valor "{valor}" e deixo "{campo}" vazio'))
def informo_dados_incompletos(browser, valor, campo):
    # placeholder
    pass
```

> **Obs.** – Cada *step* que interage com a interface deve usar os *locators* corretos da sua aplicação.  
> Para evitar repetições, você pode criar um *Page Object* `TransferenciaPage` com métodos como `seleciona_conta`, `preenche_valor`, `confirmar` etc.

---

### 4.5 `tests/test_emprestimo.py`

```python
# tests/test_emprestimo.py
from pytest_bdd import scenario, given, when, then, parsers


@scenario("features/emprestimo.feature", "Usuário solicita empréstimo e recebe aprovação")
def test_emprestimo_aprovado():
    pass


@scenario("features/emprestimo.feature", "Usuário solicita empréstimo e é negado")
def test_emprestimo_negado():
    pass


@scenario("features/emprestimo.feature", "Usuário fornece dados inválidos na solicitação de empréstimo")
def test_emprestimo_dados_invalidos():
    pass


# ----------------- Step Definitions -----------------
@given(parsers.parse('que o usuário possui renda anual de R$ {renda}'))
def set_renda(browser, renda):
    # placeholder – em teste real, você pode fazer POST na API
    pass


@given("acesso a página de solicitação de empréstimo")
def abre_emprestimo_page(browser):
    browser.get("https://www.para-bank.com/emprestimo")


@given(parsers.parse('informo o valor do empréstimo R$ {valor}'))
def preenche_valor_emprestimo(browser, valor):
    # placeholder
    pass


@given("confirmo a solicitação")
def confirma_emprestimo(browser):
    # placeholder
    pass


@then(parsers.parse('o sistema deve retornar o status "{status}"'))
def verifica_status_emprestimo(browser, status):
    # placeholder
    pass


@then(parsers.parse('devo ver a mensagem "{msg}"'))
def verifica_mensagem_emprestimo(browser, msg):
    # placeholder
    pass


@then(parsers.parse('devo ver a mensagem de erro "{msg}"'))
def verifica_mensagem_erro_emprestimo(browser, msg):
    # placeholder
    pass
```

---

### 4.6 `tests/test_pagamento.py`

```python
# tests/test_pagamento.py
from pytest_bdd import scenario, given, when, then, parsers
from selenium.webdriver.common.by import By


@scenario("features/pagamento.feature", "Usuário registra pagamento de conta")
def test_registro_pagamento():
    pass


@scenario("features/pagamento.feature", "Pagamento futuro respeita data de agendamento")
def test_pagamento_futuro():
    pass


@scenario("features/pagamento.feature", "Usuário tenta registrar pagamento com campo inválido")
def test_pagamento_campo_invalido():
    pass


# ----------------- Step Definitions -----------------
@given("que o usuário está autenticado")
def login(browser):
    # placeholder – use fixture login
    pass


@given("acesso a página de pagamento de contas")
def abre_pagamento_page(browser):
    browser.get("https://www.para-bank.com/pagamento")


@given(parsers.parse('preencho:'))
def preenche_pagamento(browser, table):
    # table é um objeto Table (cada linha -> dict)
    # Ex.: {"Beneficiário":"Eletricidade", "Endereço":"Av. X", ...}
    for row in table:
        for campo, valor in row.items():
            # localizar campo via ID/Name
            browser.find_element(By.ID, campo.lower()).clear()
            browser.find_element(By.ID, campo.lower()).send_keys(valor)


@given(parsers.parse('registro pagamento agendado para {data}'))
def preenche_data_agendada(browser, data):
    browser.find_element(By.ID, "data_vencimento").send_keys(data)


@given("confirmo")
def confirmar_pagamento(browser):
    browser.find_element(By.ID, "confirmar_pagamento").click()


@given("confirmo o pagamento")
def confirmar_pagamento(browser):
    browser.find_element(By.ID, "confirmar_pagamento").click()


@then(parsers.parse('devo ver a mensagem "{msg}"'))
def verifica_mensagem_pagamento(browser, msg):
    # placeholder
    pass


@then(parsers.parse('o pagamento deve aparecer no histórico de transações na data correta'))
def verifica_historico_pagamento(browser):
    # placeholder
    pass


@then(parsers.parse('a data de vencimento exibida deve ser {data}'))
def verifica_data_vencimento(browser, data):
    # placeholder
    pass


@then(parsers.parse('o pagamento só deve aparecer no extrato após {data}'))
def verifica_futuro_extrato(browser, data):
    # placeholder
    pass


@then(parsers.parse('devo ver a mensagem de erro "{msg}"'))
def mensagem_erro_pagamento(browser, msg):
    # placeholder
    pass
```

---

### 4.7 `tests/test_navegacao_mensagens_menus.py`

```python
# tests/test_navegacao_mensagens_menus.py
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@scenario("features/navegacao_mensagens_menus.feature", "Todas as páginas carregam sem erros de navegação")
def test_navegacao_sem_erros():
    pass


@scenario("features/navegacao_mensagens_menus.feature", "Mensagens de erro são claras e objetivas")
def test_mensagens_claras():
    pass


@scenario("features/navegacao_mensagens_menus.feature", "Links e menus são consistentes em todas as páginas")
def test_menus_consistentes():
    pass


# ----------------- Step Definitions -----------------
@given("que estou autenticado")
def login(browser):
    # placeholder
    pass


@given("navego entre todas as páginas do aplicativo")
def navega_paginas(browser):
    urls = [
        "/conta",
        "/extrato",
        "/transferir",
        "/pagamento",
        "/emprestimo",
        "/ajuda",
        "/perfil"
    ]
    for u in urls:
        browser.get("https://www.para-bank.com" + u)
        # espera que o título carregue
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


@given("cada página deve carregar com sucesso e sem mensagens de erro")
def verifica_carregamento(browser):
    # placeholder – verifica se não existe elemento de erro
    pass


@given("eu realizo uma ação inválida")
def acao_invalida(browser):
    # placeholder – por exemplo, tenta enviar formulário vazio
    pass


@given("a aplicação exibe um erro")
def espera_erro(browser):
    # placeholder
    pass


@given("a mensagem deve conter a razão do erro e instruções de correção")
def verifica_mensagem(browser):
    # placeholder
    pass


@given("estou em qualquer página do aplicativo")
def qualquer_pagina(browser):
    # placeholder
    pass


@given("verifico os itens de navegação no cabeçalho")
def verifica_navegacao_header(browser):
    # placeholder
    pass


@given("eles devem ser os mesmos que na página inicial")
def verifica_consistencia_navegacao(browser):
    # placeholder
    pass
```

---

## 5.  Execução

```bash
$ pip install pytest pytest-bdd selenium
$ pytest
```

> **Dica**  
> Para acelerar a execução em ambientes CI, considere:
> * Usar *Docker* com `selenium/standalone-chrome`  
> * Mockar APIs de backend (ex.: com `requests_mock`)  
> * Criar *fixtures* que pre‑preenchem dados via API (saldo, contas, transações).  

---

## 6.  Próximos passos

1. **Implementar locators** – ajuste cada `By.ID`, `By.CSS_SELECTOR`, etc.  
2. **Page Objects completos** – para cada tela, crie um arquivo `pages/*.py`.  
3. **Dados de teste** – use `pytest` `parametrize` ou `pytest-factoryboy` para gerar usuários/contas.  
4. **Integração contínua** – adicione *hooks* no `pytest.ini` para gerar relatórios HTML.  
5. **Testes de API** – para cenários que exigem estado pré‑existente (saldo, transações), pre‑popule via API.

Com essa base você já pode começar a rodar os testes, preenchendo os placeholders conforme a sua aplicação. Boa sorte!