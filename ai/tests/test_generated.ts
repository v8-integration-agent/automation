**Playwright + TypeScript – Full Test Suite (BDD → Code)**  
*Every file below can be copied directly into a Playwright project created with `npx playwright install`.*

---

## 1️⃣  Project skeleton

```
project-root/
├─ .env                     ← environment variables (BASE_URL, TEST_USER, ...)
├─ playwright.config.ts
├─ tsconfig.json
├─ package.json
├─ tests/
│  ├─ registration.spec.ts
│  ├─ login.spec.ts
│  ├─ account.spec.ts
│  ├─ transfer.spec.ts
│  ├─ loan.spec.ts
│  ├─ payment.spec.ts
│  └─ navigation.spec.ts
└─ pages/
   ├─ RegistrationPage.ts
   ├─ LoginPage.ts
   ├─ AccountPage.ts
   ├─ TransferPage.ts
   ├─ LoanPage.ts
   ├─ PaymentPage.ts
   └─ NavigationPage.ts
```

> **Tip:** keep every feature in its own test file – this keeps the suite fast, readable and easy to debug.

---

## 2️⃣  Configuration

> `npm install -D @playwright/test ts-node dotenv`

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
import * as dotenv from 'dotenv';

dotenv.config();                     // <-- loads .env

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  retries: 2,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    browserName: 'chromium',
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 0,
    navigationTimeout: 0,
    ignoreHTTPSErrors: true,
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

```ts
// tsconfig.json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "lib": ["ESNext"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": ".",
    "typeRoots": ["node_modules/@types"]
  },
  "include": ["**/*.ts"]
}
```

> **.env** (example)

```
BASE_URL=http://localhost:3000
TEST_USER_EMAIL=demo@example.com
TEST_USER_PASSWORD=Passw0rd!
```

---

## 3️⃣  Page Objects

All page objects use *the Page Object Model (POM)* – they expose only actions that a user can perform.  
Selectors are kept **stable** (data‑testids) and are wrapped in helper methods that include appropriate waits.

> *If your app uses other selectors, replace them accordingly.*

```ts
// pages/RegistrationPage.ts
import { Page, expect } from '@playwright/test';

export class RegistrationPage {
  constructor(private readonly page: Page) {}

  // ---------- Locators ----------
  private form = this.page.locator('#registration-form');
  private name = this.form.locator('input[name="name"]');
  private email = this.form.locator('input[name="email"]');
  private password = this.form.locator('input[name="password"]');
  private cep = this.form.locator('input[name="cep"]');
  private phone = this.form.locator('input[name="phone"]');
  private submitBtn = this.form.locator('button[type="submit"]');
  private successMsg = this.page.locator('text=Cadastro concluído com sucesso');

  // ---------- Actions ----------
  async goto() {
    await this.page.goto('/register');
    await this.form.waitFor({ state: 'visible' });
  }

  async fillMandatoryFields(data: Partial<{
    name: string,
    email: string,
    password: string,
    cep: string,
    phone: string,
  }> = {}) {
    if (data.name !== undefined) await this.name.fill(data.name);
    if (data.email !== undefined) await this.email.fill(data.email);
    if (data.password !== undefined) await this.password.fill(data.password);
    if (data.cep !== undefined) await this.cep.fill(data.cep);
    if (data.phone !== undefined) await this.phone.fill(data.phone);
  }

  async submit() {
    await Promise.all([
      this.page.waitForNavigation({ url: /login/ }), // adjust depending on redirect
      this.submitBtn.click()
    ]);
  }

  async getErrorMessageFor(field: string) {
    // Assumes error is rendered next to the field with a data-testid like `error-email`
    return this.page.locator(`data-testid="error-${field.toLowerCase()}"`).innerText();
  }

  async hasSuccessMessage(): Promise<boolean> {
    return await this.successMsg.isVisible();
  }
}
```

```ts
// pages/LoginPage.ts
import { Page } from '@playwright/test';

export class LoginPage {
  constructor(private readonly page: Page) {}

  private form = this.page.locator('#login-form');
  private email = this.form.locator('input[name="email"]');
  private password = this.form.locator('input[name="password"]');
  private submitBtn = this.form.locator('button[type="submit"]');
  private errorMsg = this.page.locator('text=Credenciais inválidas');

  async goto() {
    await this.page.goto('/login');
    await this.form.waitFor({ state: 'visible' });
  }

  async login(email: string, password: string) {
    await this.email.fill(email);
    await this.password.fill(password);
    await Promise.all([
      this.page.waitForNavigation({ url: /account/ }), // adjust
      this.submitBtn.click()
    ]);
  }

  async getErrorMessage() {
    return await this.errorMsg.textContent();
  }
}
```

```ts
// pages/AccountPage.ts
import { Page } from '@playwright/test';

export class AccountPage {
  constructor(private readonly page: Page) {}

  private balance = this.page.locator('#account-balance');
  private statementBtn = this.page.locator('button:has-text("Extrato")');

  async goto() {
    await this.page.goto('/account');
    await this.page.waitForLoadState('networkidle');
  }

  async getBalance(): Promise<number> {
    const txt = await this.balance.textContent();
    return parseFloat(txt?.replace(/[^\d.,]/g, '').replace(',', '.') ?? '0');
  }

  async goToStatement() {
    await this.statementBtn.click();
    await this.page.waitForURL(/\/statement/);
  }
}
```

```ts
// pages/TransferPage.ts
import { Page } from '@playwright/test';

export class TransferPage {
  constructor(private readonly page: Page) {}

  private origin = this.page.locator('select[name="origin"]');
  private destination = this.page.locator('select[name="destination"]');
  private amount = this.page.locator('input[name="amount"]');
  private confirmBtn = this.page.locator('button:has-text("Confirmar")');
  private errorMsg = this.page.locator('#error-message');
  private history = this.page.locator('#transfer-history');

  async goto() {
    await this.page.goto('/transfer');
    await this.page.waitForLoadState('networkidle');
  }

  async setOrigin(value: string) {
    await this.origin.selectOption({ label: value });
  }

  async setDestination(value: string) {
    await this.destination.selectOption({ label: value });
  }

  async setAmount(value: string) {
    await this.amount.fill(value);
  }

  async confirm() {
    await Promise.all([
      this.page.waitForResponse(resp => resp.url().includes('/api/transfer') && resp.ok()),
      this.confirmBtn.click()
    ]);
  }

  async getError(): Promise<string | null> {
    return await this.errorMsg.isVisible() ? await this.errorMsg.textContent() : null;
  }

  async getHistory(): Promise<string[]> {
    return await this.history.locator('tbody tr').allTextContents();
  }
}
```

```ts
// pages/LoanPage.ts
import { Page } from '@playwright/test';

export class LoanPage {
  constructor(private readonly page: Page) {}

  private amount = this.page.locator('input[name="amount"]');
  private annualIncome = this.page.locator('input[name="income"]');
  private submitBtn = this.page.locator('button:has-text("Enviar")');
  private resultMsg = this.page.locator('#loan-result');

  async goto() {
    await this.page.goto('/loan');
    await this.page.waitForLoadState('networkidle');
  }

  async apply(amount: string, income: string) {
    await this.amount.fill(amount);
    await this.annualIncome.fill(income);
    await Promise.all([
      this.page.waitForResponse(resp => resp.url().includes('/api/loan') && resp.ok()),
      this.submitBtn.click()
    ]);
  }

  async getResult(): Promise<string> {
    return await this.resultMsg.textContent() ?? '';
  }
}
```

```ts
// pages/PaymentPage.ts
import { Page } from '@playwright/test';

export class PaymentPage {
  constructor(private readonly page: Page) {}

  private beneficiary = this.page.locator('input[name="beneficiary"]');
  private address = this.page.locator('input[name="address"]');
  private city = this.page.locator('input[name="city"]');
  private state = this.page.locator('input[name="state"]');
  private cep = this.page.locator('input[name="cep"]');
  private phone = this.page.locator('input[name="phone"]');
  private destinationAccount = this.page.locator('input[name="account"]');
  private amount = this.page.locator('input[name="amount"]');
  private date = this.page.locator('input[name="date"]');
  private confirmBtn = this.page.locator('button:has-text("Confirmar")');
  private history = this.page.locator('#payment-history');

  async goto() {
    await this.page.goto('/payment');
    await this.page.waitForLoadState('networkidle');
  }

  async fillAll(data: Partial<{
    beneficiary: string,
    address: string,
    city: string,
    state: string,
    cep: string,
    phone: string,
    destinationAccount: string,
    amount: string,
    date: string,
  }> = {}) {
    if (data.beneficiary) await this.beneficiary.fill(data.beneficiary);
    if (data.address) await this.address.fill(data.address);
    if (data.city) await this.city.fill(data.city);
    if (data.state) await this.state.fill(data.state);
    if (data.cep) await this.cep.fill(data.cep);
    if (data.phone) await this.phone.fill(data.phone);
    if (data.destinationAccount) await this.destinationAccount.fill(data.destinationAccount);
    if (data.amount) await this.amount.fill(data.amount);
    if (data.date) await this.date.fill(data.date);
  }

  async confirm() {
    await Promise.all([
      this.page.waitForResponse(resp => resp.url().includes('/api/payment') && resp.ok()),
      this.confirmBtn.click()
    ]);
  }

  async getErrorMessageFor(field: string): Promise<string | null> {
    return await this.page.locator(`data-testid="error-${field.toLowerCase()}"`).innerText();
  }

  async getLastHistoryEntry(): Promise<string[]> {
    const rows = await this.history.locator('tbody tr').all();
    if (rows.length === 0) return [];
    return await rows[rows.length - 1].allTextContents();
  }
}
```

```ts
// pages/NavigationPage.ts
import { Page } from '@playwright/test';

export class NavigationPage {
  constructor(private readonly page: Page) {}

  // ---------- Locators ----------
  private navLinks = this.page.locator('nav a');

  // ---------- Actions ----------
  async gotoHome() {
    await this.page.goto('/');
  }

  async navigateTo(page: string) {
    await this.page.goto(page);
    await this.page.waitForLoadState('networkidle');
  }

  async getNavLinks(): Promise<string[]> {
    return await this.navLinks.allTextContents();
  }

  async clickLink(linkText: string) {
    await this.navLinks.filter({ hasText: linkText }).click();
    await this.page.waitForLoadState('networkidle');
  }
}
```

---

## 4️⃣  Tests – each feature in its own file

> *All tests use **async/await** and **expect** from Playwright Test for assertions.*  
> *Where the Gherkin had an “Outline”, we use `test.each` for data‑driven tests.*

---

### 4.1  **tests/registration.spec.ts** – *Cadastro de Usuário*

```ts
// tests/registration.spec.ts
import { test, expect } from '@playwright/test';
import { RegistrationPage } from '../pages/RegistrationPage';
import { LoginPage } from '../pages/LoginPage';

const validUser = {
  name: 'Fulano de Tal',
  email: 'fulano.tal@example.com',
  password: 'P4ssw0rd!',
  cep: '01001-000',
  phone: '1199998888',
};

test.describe('Cadastro de Usuário', () => {

  test('Cadastro bem-sucedido', async ({ page }) => {
    const reg = new RegistrationPage(page);
    await reg.goto();
    await reg.fillMandatoryFields(validUser);
    await reg.submit();

    // ✅ Mensagem de sucesso
    expect(await reg.hasSuccessMessage()).toBeTruthy();

    // → Teste de login com as credenciais recém‑criado
    const login = new LoginPage(page);
    await login.goto();
    await login.login(validUser.email, validUser.password);

    // → Verifica que estamos na página inicial da conta
    await expect(page).toHaveURL(/\/account/);
  });

  // ---- Scenario Outline: campo obrigatório em branco
  const mandatoryFields = ['Nome', 'Email', 'Senha', 'CEP', 'Telefone'];
  test.each(mandatoryFields)('Cadastro com campo obrigatório em branco – %s', async (campo, { page }) => {
    const reg = new RegistrationPage(page);
    await reg.goto();

    // preenche tudo, exceto o campo <campo>
    const data = { ...validUser };
    delete data[ campo.toLowerCase() as keyof typeof data ];   // remove a propriedade

    await reg.fillMandatoryFields(data);
    await reg.submit();

    // Espera a mensagem de erro do campo
    const msg = await reg.getErrorMessageFor(campo);
    expect(msg).toContain(`Campo ${campo} é obrigatório`);
  });

  // ---- Scenario Outline: dados inválidos
  const invalidData = [
    { campo: 'Email', valor: 'usuario@', mensagem: 'Email inválido' },
    { campo: 'CEP', valor: '123', mensagem: 'CEP inválido' },
    { campo: 'Telefone', valor: '12abc', mensagem: 'Telefone inválido' },
  ];

  test.each(invalidData)('Cadastro com dados inválidos – $campo', async ({ campo, valor, mensagem }, { page }) => {
    const reg = new RegistrationPage(page);
    await reg.goto();

    const data = { ...validUser, [campo.toLowerCase()]: valor };
    await reg.fillMandatoryFields(data);
    await reg.submit();

    const msg = await reg.getErrorMessageFor(campo);
    expect(msg).toContain(mensagem);
  });

});
```

---

### 4.2  **tests/login.spec.ts** – *Login*

```ts
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

const testUser = {
  email: process.env.TEST_USER_EMAIL ?? 'demo@example.com',
  password: process.env.TEST_USER_PASSWORD ?? 'Passw0rd!'
};

test.describe('Login', () => {

  test('Login com credenciais válidas', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login(testUser.email, testUser.password);

    await expect(page).toHaveURL(/\/account/); // redireciona para a página inicial da conta
  });

  test('Login com credenciais inválidas', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login('invalid@example.com', 'wrongpass');

    const errMsg = await login.getErrorMessage();
    expect(errMsg).toContain('Credenciais inválidas');
  });

});
```

---

### 4.3  **tests/account.spec.ts** – *Acesso à Conta (Saldo e Extrato)*

```ts
// tests/account.spec.ts
import { test, expect } from '@playwright/test';
import { AccountPage } from '../pages/AccountPage';
import { TransferPage } from '../pages/TransferPage';

test.describe('Acesso à Conta', () => {

  test('Exibição de saldo atualizado', async ({ page }) => {
    const account = new AccountPage(page);
    await account.goto();

    const saldo = await account.getBalance();
    expect(saldo).toBeGreaterThan(0); // saldo deve estar disponível e atualizado
  });

  test('Lista de extrato em ordem cronológica (decrescente)', async ({ page }) => {
    const account = new AccountPage(page);
    await account.goto();
    await account.goToStatement();

    // Aqui supomos que cada linha tem a data no primeiro <td>
    const rows = page.locator('#statement-table tbody tr');
    const dates = await rows.locator('td:first-child').allTextContents();

    const sortedDates = [...dates].sort((a, b) => new Date(b).getTime() - new Date(a).getTime());
    expect(dates).toEqual(sortedDates); // garante ordem decrescente
  });

});
```

---

### 4.4  **tests/transfer.spec.ts** – *Transferência de Fundos*

```ts
// tests/transfer.spec.ts
import { test, expect } from '@playwright.test';
import { TransferPage } from '../pages/TransferPage';
import { AccountPage } from '../pages/AccountPage';

test.describe('Transferência de Fundos', () => {
  let transfer: TransferPage;
  let account: AccountPage;

  test.beforeEach(async ({ page }) => {
    transfer = new TransferPage(page);
    account = new AccountPage(page);
    await transfer.goto();
  });

  test('Transferência bem-sucedida', async ({ page }) => {
    // 1️⃣  Checa saldo atual da Conta A
    await account.goto();
    const saldoInicial = await account.getBalance();

    // 2️⃣  Executa transferência
    await transfer.setOrigin('Conta A');
    await transfer.setDestination('Conta B');
    const valor = '100.00';
    await transfer.setAmount(valor);
    await transfer.confirm();

    // 3️⃣  Verifica que o saldo da Conta A foi debitado
    await account.goto();
    const saldoFinal = await account.getBalance();
    expect(saldoFinal).toBeCloseTo(saldoInicial - parseFloat(valor), 2);

    // 4️⃣  Verifica que o histórico da Conta B contém a entrada
    await transfer.goto();
    const history = await transfer.getHistory();
    expect(history).toContain(valor); // simplificado – ajuste conforme formato real
  });

  test('Transferência com saldo insuficiente', async ({ page }) => {
    await transfer.setOrigin('Conta A');
    await transfer.setDestination('Conta B');
    await transfer.setAmount('2000.00');
    await transfer.confirm();

    const err = await transfer.getError();
    expect(err).toContain('Saldo insuficiente');
  });

  // ---- Scenario Outline: valor inválido
  const invalidValues = [
    { valor: '0', mensagem: 'Valor mínimo é 0,01' },
    { valor: '-50.00', mensagem: 'Valor negativo não permitido' },
  ];

  test.each(invalidValues)('Transferência com valor inválido – $valor', async ({ valor, mensagem }) => {
    await transfer.setOrigin('Conta A');
    await transfer.setDestination('Conta B');
    await transfer.setAmount(valor);
    await transfer.confirm();

    const err = await transfer.getError();
    expect(err).toContain(mensagem);
  });

});
```

---

### 4.5  **tests/loan.spec.ts** – *Solicitação de Empréstimo*

```ts
// tests/loan.spec.ts
import { test, expect } from '@playwright/test';
import { LoanPage } from '../pages/LoanPage';

test.describe('Solicitação de Empréstimo', () => {
  test('Empréstimo aprovado', async ({ page }) => {
    const loan = new LoanPage(page);
    await loan.goto();
    await loan.apply('5000', '60000');

    const result = await loan.getResult();
    expect(result).toContain('Aprovado');
  });

  test('Empréstimo negado', async ({ page }) => {
    const loan = new LoanPage(page);
    await loan.goto();
    await loan.apply('20000', '30000');

    const result = await loan.getResult();
    expect(result).toContain('Negado');
  });
});
```

---

### 4.6  **tests/payment.spec.ts** – *Pagamento de Contas*

```ts
// tests/payment.spec.ts
import { test, expect } from '@playwright/test';
import { PaymentPage } from '../pages/PaymentPage';

test.describe('Pagamento de Contas', () => {

  test('Pagamento futuro agendado', async ({ page }) => {
    const payment = new PaymentPage(page);
    await payment.goto();

    await payment.fillAll({
      beneficiary: 'Empresa XYZ',
      address: 'Rua das Flores',
      city: 'São Paulo',
      state: 'SP',
      cep: '01001-000',
      phone: '1199998888',
      destinationAccount: '987654321',
      amount: '150.00',
      date: '2025-12-31',
    });

    await payment.confirm();

    const lastEntry = await payment.getLastHistoryEntry();
    expect(lastEntry).toContain('150.00');
    expect(lastEntry).toContain('2025-12-31');
  });

  const mandatoryFields = [
    'Beneficiário',
    'Endereço',
    'Cidade',
    'Estado',
    'CEP',
    'Telefone',
    'Conta de destino',
    'Valor',
    'Data',
  ];

  test.each(mandatoryFields)('Pagamento com campo obrigatório em branco – %s', async (campo, { page }) => {
    const payment = new PaymentPage(page);
    await payment.goto();

    // preenche todos, exceto <campo>
    const data: Record<string, string> = {
      Beneficiário: 'Empresa XYZ',
      Endereço: 'Rua das Flores',
      Cidade: 'São Paulo',
      Estado: 'SP',
      CEP: '01001-000',
      Telefone: '1199998888',
      'Conta de destino': '987654321',
      Valor: '150.00',
      Data: '2025-12-31',
    };
    delete data[campo]; // remove

    await payment.fillAll(data as any);
    await payment.confirm();

    const errMsg = await payment.getErrorMessageFor(campo);
    expect(errMsg).toContain(`Campo ${campo} é obrigatório`);
  });

});
```

---

### 4.7  **tests/navigation.spec.ts** – *Requisitos Gerais de Navegação e Usabilidade*

```ts
// tests/navigation.spec.ts
import { test, expect } from '@playwright/test';
import { NavigationPage } from '../pages/NavigationPage';
import { TransferPage } from '../pages/TransferPage';

test.describe('Navegação e Usabilidade', () => {

  test('Todas as páginas carregam corretamente', async ({ page }) => {
    const nav = new NavigationPage(page);
    const pages = [
      '/register',
      '/login',
      '/account',
      '/transfer',
      '/loan',
      '/payment',
      '/statement',
    ];

    for (const path of pages) {
      await nav.navigateTo(path);
      // Garantimos que não há erro 500
      await expect(page.locator('body')).not.toContainText('Erro inesperado');
    }
  });

  test('Mensagens de erro claras e objetivas', async ({ page }) => {
    const transfer = new TransferPage(page);
    await transfer.goto();

    // Simula uma transferência com saldo insuficiente
    await transfer.setOrigin('Conta A');
    await transfer.setDestination('Conta B');
    await transfer.setAmount('2000.00');
    await transfer.confirm();

    const err = await transfer.getError();
    expect(err).toBeTruthy();
    // Exemplo de verificação de localização: o erro aparece abaixo do campo "amount"
    expect(err).toMatch(/saldo insuficiente/i);
    expect(await page.locator('input[name="amount"]').nextSibling()).toBeVisible();
  });

  test('Consistência de menus e links', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.gotoHome();

    const links = await nav.getNavLinks();
    const expected = ['Home', 'Conta', 'Transferência', 'Empréstimo', 'Pagamento'];
    for (const text of expected) {
      expect(links).toContain(text);
    }

    // Verifica que cada link leva à página correta
    for (const text of expected) {
      await nav.clickLink(text);
      if (text === 'Home') {
        await expect(page).toHaveURL(/\/$/);
      } else {
        const slug = text.toLowerCase().replace(' ', '-');
        await expect(page).toHaveURL(new RegExp(`/${slug}`));
      }
    }
  });

});
```

---

## 5️⃣  Running the test suite

```bash
# 1️⃣  install deps
npm install

# 2️⃣  run all tests
npx playwright test

# 3️⃣  see results in terminal and open the interactive reporter
npx playwright test --reporter=html
open reports/index.html
```

> **Debugging** – to run a single test file in headed mode:
> ```bash
> npx playwright test tests/registration.spec.ts --headed
> ```

---

## 6️⃣  What you get

| Feature | Test Coverage | Notes |
|---------|---------------|-------|
| Cadastro de Usuário | ✅ ✔️ | Valida campos, mensagens de erro e login pós‑cadastro |
| Login | ✅ | Testa credenciais válidas e inválidas |
| Conta (Saldo/Extrato) | ✅ | Verifica saldo atual e ordem de transações |
| Transferência | ✅ | Testa sucesso, saldo insuficiente e valores inválidos |
| Empréstimo | ✅ | Aprovação e negação |
| Pagamento | ✅ | Agendamento futuro e validação de campos obrigatórios |
| Navegação & Usabilidade | ✅ | Carregamento, mensagens e consistência do menu |

---

### 🔧  Extensões recomendadas

| Tool | Why |
|------|-----|
| **dotenv** | Mantém credenciais e URLs fora do código |
| **jest‑matcher‑types** | IntelliSense para `expect` |
| **cypress‑dashboard** | Relatórios avançados (opcional) |

---

**Happy testing!**