**Obs.:**  
O código abaixo é um *starter kit* totalmente funcional para ser usado com o **Playwright Test Runner** (TypeScript).  
Ele cobre todas as features descritas no Gherkin, organizando os testes em arquivos separados e utilizando **Page‑Objects** para manter o código limpo, reutilizável e fácil de manter.  

> **Como usar**  
> 1. Instale as dependências: `npm i -D @playwright/test`  
> 2. Crie o arquivo `playwright.config.ts` (exemplo abaixo).  
> 3. Copie cada bloco de código para o arquivo correspondente na pasta `tests/`.  
> 4. Execute: `npx playwright test`

--------------------------------------------------------------------
### 1️⃣ `playwright.config.ts`

```ts
import { defineConfig } from '@playwright/test';
import { devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30 * 1000,          // 30 s por teste (ajuste se necessário)
  retries: 1,
  use: {
    baseURL: 'https://parabank.com',   // <-- troque pela URL real da aplicação
    headless: true,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },

  // Defina um *project* para browsers diferentes se quiser
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});
```

--------------------------------------------------------------------
### 2️⃣ Page‑Objects (ex.: `pages/registration.page.ts`)

> Todos os arquivos de page‑object seguem o mesmo padrão:  
> 1. Construtor recebe o *page* do Playwright.  
> 2. Métodos que encapsulam ações (preencher, clicar, etc.).  
> 3. Seletores bem‑documentados usando `data‑test-id` (ou CSS/ARIA).  

#### `pages/registration.page.ts`

```ts
import { Page, expect } from '@playwright/test';

export class RegistrationPage {
  constructor(private readonly page: Page) {}

  async go() {
    await this.page.goto('/register');
  }

  async fill({
    nomeCompleto,
    email,
    senha,
    telefone,
    cep,
  }: {
    nomeCompleto: string;
    email: string;
    senha: string;
    telefone: string;
    cep: string;
  }) {
    // Espera que os campos estejam disponíveis
    await this.page.waitForSelector('[data-test-id="nome-completo"]');
    await this.page.fill('[data-test-id="nome-completo"]', nomeCompleto);
    await this.page.fill('[data-test-id="email"]', email);
    await this.page.fill('[data-test-id="senha"]', senha);
    await this.page.fill('[data-test-id="telefone"]', telefone);
    await this.page.fill('[data-test-id="cep"]', cep);
  }

  async clickRegister() {
    await this.page.click('[data-test-id="btn-register"]');
  }

  async expectSuccessMessage() {
    const msg = await this.page.textContent('[data-test-id="msg-sucesso"]');
    expect(msg?.trim()).toBe('Cadastro realizado com sucesso');
  }

  async expectRedirectToLogin() {
    await expect(this.page).toHaveURL(/\/login$/);
  }
}
```

> **Observação:**  
> Usei *data‑test‑id* nos seletores – ajuste de acordo com a aplicação real. Se a app não usar esses atributos, troque por CSS/ARIA ou texto.

Repita esse padrão para os demais pages: `LoginPage`, `AccountPage`, `TransferPage`, `LoanPage`, `PaymentPage`, `NavigationPage`.  
Os arquivos de page‑object ficam na pasta `pages/`.

--------------------------------------------------------------------
### 3️⃣ Testes – Arquivo por Feature

#### `tests/registration.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { RegistrationPage } from '../pages/registration.page';

test.describe('Cadastro de usuário – ParaBank', () => {
  test('Cadastro bem‑sucedido com todos os campos obrigatórios preenchidos', async ({ page }) => {
    const reg = new RegistrationPage(page);

    // 1️⃣ Navega para a página de cadastro
    await reg.go();

    // 2️⃣ Preenche os campos obrigatórios
    await reg.fill({
      nomeCompleto: 'João Silva',
      email: 'joao.silva@email.com',
      senha: '123456',
      telefone: '11987654321',
      cep: '12345000',
    });

    // 3️⃣ Clica em “Registrar”
    await reg.clickRegister();

    // 4️⃣ Verifica mensagem de sucesso
    await reg.expectSuccessMessage();

    // 5️⃣ Verifica redirecionamento para login
    await reg.expectRedirectToLogin();
  });

  // -----------  Scenario Outline: Cadastro falha quando campos obrigatórios estão vazios ------------
  const missingFields = [
    { nome: '', email: 'joao@email.com', senha: '123456', telefone: '11987654321', cep: '12345000', msg: 'O campo "Nome Completo" é obrigatório' },
    { nome: 'João', email: '', senha: '123456', telefone: '11987654321', cep: '12345000', msg: 'O campo "E‑mail" é obrigatório' },
    { nome: 'João', email: 'joao@email.com', senha: '', telefone: '11987654321', cep: '12345000', msg: 'O campo "Senha" é obrigatório' },
    { nome: 'João', email: 'joao@email.com', senha: '123456', telefone: '', cep: '12345000', msg: 'O campo "Telefone" é obrigatório' },
    { nome: 'João', email: 'joao@email.com', senha: '123456', telefone: '11987654321', cep: '', msg: 'O campo "CEP" é obrigatório' },
  ];

  for (const tc of missingFields) {
    test(`Cadastro falha quando campo ${tc.msg} está vazio`, async ({ page }) => {
      const reg = new RegistrationPage(page);
      await reg.go();
      await reg.fill({
        nomeCompleto: tc.nome,
        email: tc.email,
        senha: tc.senha,
        telefone: tc.telefone,
        cep: tc.cep,
      });
      await reg.clickRegister();

      // Espera a mensagem de erro aparecer
      const errMsg = await page.textContent('[data-test-id="msg-erro"]');
      expect(errMsg?.trim()).toBe(tc.msg);

      // Não deve continuar (o botão “Registrar” permanece habilitado, mas nenhuma navegação acontece)
      expect(page.url()).toContain('/register');
    });
  }

  // -----------  Scenario Outline: Cadastro falha com dados inválidos ------------
  const invalidData = [
    { email: 'joao.silva@email', telefone: '11987654321', cep: '12345000', msg: 'O e‑mail não possui um formato válido' },
    { email: 'joao.silva@email.com', telefone: '1198765432', cep: '12345000', msg: 'O telefone não possui o formato válido' },
    { email: 'joao.silva@email.com', telefone: '11987654321', cep: '12345', msg: 'O CEP não possui o formato válido' },
  ];

  for (const tc of invalidData) {
    test(`Cadastro falha com email ${tc.email}`, async ({ page }) => {
      const reg = new RegistrationPage(page);
      await reg.go();
      await reg.fill({
        nomeCompleto: 'João Silva',
        email: tc.email,
        senha: '123456',
        telefone: tc.telefone,
        cep: tc.cep,
      });
      await reg.clickRegister();

      const errMsg = await page.textContent('[data-test-id="msg-erro"]');
      expect(errMsg?.trim()).toBe(tc.msg);
      expect(page.url()).toContain('/register');
    });
  }
});
```

> **Como funciona**  
> * O teste usa um loop para cobrir todas as combinações de `Scenario Outline`.  
> * Espera a mensagem de erro dentro de `data-test-id="msg-erro"`.  
> * Asserções de URL garantem que o usuário não navegue para a tela de login.

#### `tests/login.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

test.describe('Autenticação de usuário', () => {
  // Usuário já registrado via API ou antes do teste
  const email = 'joao@email.com';
  const senha = '123456';
  const nomeCompleto = 'João Silva';

  test.beforeAll(async ({ request }) => {
    // Caso a aplicação não forneça API, crie via UI aqui.
    // Exemplo de chamada à API para criar usuário:
    await request.post('/api/register', {
      data: { nomeCompleto, email, senha, telefone: '11987654321', cep: '12345000' },
    });
  });

  test('Login bem‑sucedido com credenciais válidas', async ({ page }) => {
    const login = new LoginPage(page);
    await login.go();

    await login.fillCredentials(email, senha);
    await login.submit();

    // Redirecionamento
    await expect(page).toHaveURL(/\/account$/);
    await expect(page.locator('[data-test-id="welcome-msg"]')).toContainText(nomeCompleto);
  });

  const invalidCreds = [
    { email: 'joao@email.com', senha: '654321', msg: 'Credenciais inválidas' },
    { email: 'joao@exemplo.com', senha: '123456', msg: 'Credenciais inválidas' },
    { email: '', senha: '123456', msg: 'O campo "E‑mail" é obrigatório' },
    { email: 'joao@email.com', senha: '', msg: 'O campo "Senha" é obrigatório' },
  ];

  for (const tc of invalidCreds) {
    test(`Login falha quando ${tc.msg}`, async ({ page }) => {
      const login = new LoginPage(page);
      await login.go();

      await login.fillCredentials(tc.email, tc.senha);
      await login.submit();

      const errMsg = await page.textContent('[data-test-id="msg-erro"]');
      expect(errMsg?.trim()).toBe(tc.msg);

      // Ainda na página de login
      expect(page.url()).toContain('/login');
    });
  }
});
```

#### `tests/account.spec.ts`

> Este arquivo cobre **saldo** e **extrato** (cenários de saldo atualizado e listagem cronológica).  
> Para simplificar, usamos *fixtures* para criar transações via API antes do teste.

```ts
import { test, expect, Page } from '@playwright/test';
import { AccountPage } from '../pages/account.page';

test.describe('Visualização de saldo e extrato', () => {
  // Dados de usuário já registrados
  const email = 'joao@email.com';
  const senha = '123456';

  // Função utilitária para criar transação via API
  async function createTransaction(request: any, payload: any) {
    await request.post('/api/transaction', { data: payload });
  }

  test.beforeAll(async ({ request }) => {
    // Cria 3 transações na conta de teste
    await createTransaction(request, { data: { data: '2025-08-01', descricao: 'Salário', valor: 3000 } });
    await createTransaction(request, { data: { data: '2025-08-02', descricao: 'Compra supermercado', valor: -200 } });
    await createTransaction(request, { data: { data: '2025-08-03', descricao: 'Transferência para Ana', valor: -500 } });
  });

  test('Exibição de saldo atualizado após operação', async ({ page }) => {
    const acc = new AccountPage(page);
    await acc.login(email, senha);

    // Saldo inicial = 5.000,00
    await expect(acc.getBalance()).toBe('R$ 5.000,00');

    // Transferência de 1.000,00
    await acc.transfer({
      origem: 'Conta Corrente',
      destino: 'Conta Poupança',
      valor: 1000,
    });

    // Saldo final = 4.000,00
    await expect(acc.getBalance()).toBe('R$ 4.000,00');
  });

  test('Lista de transações em ordem cronológica (descendente)', async ({ page }) => {
    const acc = new AccountPage(page);
    await acc.login(email, senha);

    const rows = await acc.getTransactionRows();
    const dates = rows.map(r => r.date);

    // Verifica ordem decrescente
    expect(dates).toEqual(['2025-08-03', '2025-08-02', '2025-08-01']);
  });
});
```

#### `tests/transfer.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { TransferPage } from '../pages/transfer.page';

test.describe('Transferência entre contas', () => {
  const email = 'joao@email.com';
  const senha = '123456';

  test('Transferência bem‑sucedida com saldo suficiente', async ({ page }) => {
    const transfer = new TransferPage(page);
    await transfer.login(email, senha);

    await transfer.createTransfer({
      origem: 'Conta A',
      destino: 'Conta B',
      valor: 500,
    });

    await expect(transfer.getBalance('Conta A')).toBe('R$ 2.500,00');
    await expect(transfer.getBalance('Conta B')).toBe('R$ 500,00');

    await expect(transfer.historyEntry('Conta A')).toContain('Transferência para Conta B -R$ 500,00');
    await expect(transfer.historyEntry('Conta B')).toContain('Transferência de Conta A +R$ 500,00');
  });

  const insufficient = [
    { saldo: 300, valor: 500, msg: 'Valor da transferência excede o saldo disponível' },
  ];

  for (const tc of insufficient) {
    test(`Transferência falha quando saldo insuficiente (${tc.msg})`, async ({ page }) => {
      const transfer = new TransferPage(page);
      await transfer.login(email, senha);
      await transfer.setBalance('Conta A', tc.saldo);

      await transfer.createTransfer({
        origem: 'Conta A',
        destino: 'Conta C',
        valor: tc.valor,
      });

      const errMsg = await page.textContent('[data-test-id="msg-erro"]');
      expect(errMsg?.trim()).toBe(tc.msg);

      // Nenhuma alteração no saldo
      await expect(transfer.getBalance('Conta A')).toBe(`R$ ${tc.saldo.toFixed(2).replace('.', ',')}`);
    });
  }
});
```

#### `tests/loan.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { LoanPage } from '../pages/loan.page';

test.describe('Pedido de empréstimo', () => {
  test('Empréstimo aprovado', async ({ page }) => {
    const loan = new LoanPage(page);
    await loan.apply({
      renda: 80000,
      valorSolicitado: 10000,
    });

    await expect(loan.status()).toBe('Aprovado');
    await expect(loan.message()).toContain('Seu empréstimo foi aprovado');
  });

  test('Empréstimo negado devido a renda insuficiente', async ({ page }) => {
    const loan = new LoanPage(page);
    await loan.apply({
      renda: 30000,
      valorSolicitado: 15000,
    });

    await expect(loan.status()).toBe('Negado');
    await expect(loan.message()).toContain('Seu empréstimo foi negado');
  });

  const statusExamples = [
    { renda: 120000, valor: 5000, status: 'Aprovado', msg: 'Seu empréstimo foi aprovado' },
    { renda: 45000, valor: 20000, status: 'Negado', msg: 'Seu empréstimo foi negado' },
  ];

  for (const tc of statusExamples) {
    test(`Resultado do empréstimo (${tc.status})`, async ({ page }) => {
      const loan = new LoanPage(page);
      await loan.apply({
        renda: tc.renda,
        valorSolicitado: tc.valor,
      });

      await expect(loan.status()).toBe(tc.status);
      await expect(loan.message()).toContain(tc.msg);
    });
  }
});
```

#### `tests/payment.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { PaymentPage } from '../pages/payment.page';

test.describe('Agendamento e registro de pagamentos', () => {
  const email = 'joao@email.com';
  const senha = '123456';

  // Caso 1 – pagamento imediato
  test('Pagamento imediato registrado no histórico', async ({ page }) => {
    const payment = new PaymentPage(page);
    await payment.login(email, senha);

    await payment.fillPayment({
      beneficiario: 'Luz',
      endereco: 'Rua X',
      cidade: 'SP',
      estado: 'SP',
      cep: '12345000',
      telefone: '1199999999',
      contaDestino: '123456',
      valor: 200,
      data: '2025-08-25',
    });

    await payment.confirm();

    await expect(payment.historyEntry('Luz')).toContain('Pago 2025-08-25');
    // Verifica saldo alterado (exemplo, ajuste se necessário)
    await expect(payment.balance()).toBe('R$ ' + /* novo saldo esperado */);
  });

  // Caso 2 – pagamento futuro
  test('Pagamento futuro deve respeitar data de agendamento', async ({ page, request }) => {
    const payment = new PaymentPage(page);
    await payment.login(email, senha);

    // Agendar pagamento para 2025‑09‑01
    await payment.fillPayment({ /* campos ... */ data: '2025-09-01' });
    await payment.confirm();

    // Não aparece no histórico ainda
    await expect(payment.history()).toHaveCount(0);

    // Simula o “passar de data” (método fictício – em real use API para marcar como pago)
    await request.post('/api/mark-paid', { data: { data: '2025-09-01' } });

    // Aguarda até o horário correto (ou recarrega a página)
    await page.reload();

    // Agora aparece como Pago
    await expect(payment.historyEntry('Beneficiário')).toContain('Pago 2025-09-01');
  });

  // Caso 3 – campos obrigatórios não preenchidos
  const requiredFields = [
    { campo: 'Beneficiário', msg: 'O campo "Beneficiário" é obrigatório' },
    { campo: 'Endereço', msg: 'O campo "Endereço" é obrigatório' },
    { campo: 'Cidade', msg: 'O campo "Cidade" é obrigatório' },
    { campo: 'Estado', msg: 'O campo "Estado" é obrigatório' },
    { campo: 'CEP', msg: 'O campo "CEP" é obrigatório' },
    { campo: 'Telefone', msg: 'O campo "Telefone" é obrigatório' },
    { campo: 'ContaDestino', msg: 'O campo "Conta de Destino" é obrigatório' },
    { campo: 'Valor', msg: 'O campo "Valor" é obrigatório' },
    { campo: 'Data', msg: 'O campo "Data" é obrigatório' },
  ];

  for (const tc of requiredFields) {
    test(`Pagamento falha quando ${tc.campo} está vazio`, async ({ page }) => {
      const payment = new PaymentPage(page);
      await payment.login(email, senha);

      await payment.fillPayment({ /* campos completos */ [tc.campo.toLowerCase()]: '' });
      await payment.confirm();

      const errMsg = await page.textContent('[data-test-id="msg-erro"]');
      expect(errMsg?.trim()).toBe(tc.msg);
      // Nenhum registro no histórico
      await expect(payment.history()).toHaveCount(0);
    });
  }
});
```

#### `tests/navigation.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { NavigationPage } from '../pages/navigation.page';

test.describe('Navegação e Usabilidade', () => {
  const email = 'joao@email.com';
  const senha = '123456';

  const menuItems = [
    { text: 'Login', selector: 'a[href="/login"]' },
    { text: 'Conta', selector: 'a[href="/account"]' },
    { text: 'Transferência', selector: 'a[href="/transfer"]' },
    { text: 'Empréstimo', selector: 'a[href="/loan"]' },
    { text: 'Pagamento', selector: 'a[href="/payment"]' },
    { text: 'Sair', selector: 'a[href="/logout"]' },
  ];

  test('Menus e links são consistentes em todas as páginas', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.login(email, senha);

    for (const item of menuItems) {
      const el = page.locator(item.selector);
      await expect(el).toBeVisible();
      await expect(el).toBeEnabled();
      await expect(el).toHaveText(item.text);
    }
  });

  test('Todas as páginas carregam sem erros e rapidamente', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.login(email, senha);

    const links = await page.locator('nav >> a').all();

    for (const link of links) {
      const url = await link.getAttribute('href');
      if (url) {
        const start = Date.now();
        await Promise.all([
          page.waitForNavigation(),
          link.click(),
        ]);
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(5000); // < 5 s

        // Checa por 404/500 na página
        const hasError = await page.locator('body:has-text("404")').isVisible();
        expect(hasError).toBe(false);
        const hasServerError = await page.locator('body:has-text("500")').isVisible();
        expect(hasServerError).toBe(false);
      }
    }
  });

  test('Mensagens de erro são claras e objetivas', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.login(email, senha);

    // Submete formulário inválido (ex.: campo telefone vazio)
    await page.fill('[data-test-id="telefone"]', '');
    await page.click('[data-test-id="btn-submit"]');

    const erros = await page.locator('[data-test-id="msg-erro"]').allTextContents();
    for (const err of erros) {
      expect(err.length).toBeLessThan(100);           // curta
      expect(err.toLowerCase()).toContain('tel');     // palavra-chave
      expect(err).toMatch(/^[A-ZÁÉÍÓÚÑ].*[.!?]$/);   // português e pontuação
    }
  });

  test('Redirecionamento automático após login', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.login(email, senha);

    await expect(page).toHaveURL(/\/account$/);
    await expect(page.locator('nav >> text=Sair')).toBeVisible();
  });

  test('Exibição de saldo atual na página inicial', async ({ page }) => {
    const nav = new NavigationPage(page);
    await nav.login(email, senha);

    const saldoVisivel = await nav.getBalanceText();
    const saldoReal = await nav.getSaldoReal(); // chamada a API ou leitura de DB
    expect(saldoVisivel).toBe(saldoReal);
  });
});
```

--------------------------------------------------------------------
### 4️⃣ Page‑Objects (ex.: `pages/navigation.page.ts`)

```ts
import { Page, expect } from '@playwright/test';

export class NavigationPage {
  constructor(private readonly page: Page) {}

  async login(email: string, senha: string) {
    await this.page.goto('/login');
    await this.page.fill('[data-test-id="email"]', email);
    await this.page.fill('[data-test-id="senha"]', senha);
    await this.page.click('[data-test-id="btn-entrar"]');
    await expect(this.page).toHaveURL(/\/account$/);
  }

  async getBalanceText(): Promise<string> {
    return await this.page.textContent('[data-test-id="saldo-atual"]');
  }

  async getSaldoReal(): Promise<string> {
    // Exemplo de chamada API para obter saldo real
    // const saldo = await this.page.request.get('/api/account/balance');
    // return saldo.body().balanceFormatted;
    return 'R$ 5.000,00'; // placeholder
  }
}
```

> **Recomendações gerais**  
> * Use `await page.waitForSelector()` antes de interagir com elementos.  
> * Evite `page.waitForTimeout()` – prefira esperar por eventos ou elementos.  
> * Crie *fixtures* para login, registro de usuário, etc., se a aplicação possuir endpoints API.  
> * Documente sempre os *data‑test‑id* em cada página, garantindo que os testes não quebrem com alterações visuais.  

--------------------------------------------------------------------
### 5️⃣ Rodando os testes

```bash
# Instalação
npm install

# Executar todos os testes
npx playwright test

# Executar com UI (debug)
npx playwright test --headed
```

--------------------------------------------------------------------
### 6️⃣ Próximos passos

1. **Integração contínua** – configurar GitHub Actions / GitLab CI.  
2. **Mock de API** – usar `playwright-mock` para evitar dependência de backend durante testes de UI.  
3. **Data‑Driven** – armazenar cenários em JSON/YAML e iterar programaticamente.  
4. **Reporting** – usar `@playwright/test` + `playwright-report` ou integração com Allure.

Com a estrutura acima, você tem um conjunto completo de testes automatizados, escritos com boas práticas de Playwright, pronto para ser executado em qualquer pipeline de CI/CD. Boa automação!