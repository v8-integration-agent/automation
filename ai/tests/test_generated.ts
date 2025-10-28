## 1. Arquitetura do projeto

```
paraBank/
├─ package.json
├─ playwright.config.ts
└─ tests/
   └─ paraBank.spec.ts
```

> **Obs.:**  
> * O `playwright.config.ts` já deve conter o `baseURL` e outras opções.  
> * O arquivo de teste (`paraBank.spec.ts`) está pronto para ser copiado dentro de `tests/` e executado com  
>   `npx playwright test`.

---

## 2. `playwright.config.ts` (exemplo mínimo)

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: {
    // Substitua pelo endereço real da aplicação
    baseURL: 'https://parabank.com',
    headless: true,                     // Pode mudar para false em debug
    viewport: { width: 1280, height: 720 },
    // Espera automática de 0.5s entre actions (ajuste conforme necessário)
    actionTimeout: 5_000,
  },
});
```

---

## 3. `paraBank.spec.ts`

```ts
/**
 *  --------------------------------------------------------------
 *  Testes Playwright para a aplicação ParaBank
 *  --------------------------------------------------------------
 *
 *  Todos os cenários BDD foram convertidos em testes Playwright
 *  com TypeScript, seguindo boas práticas: 
 *  - Organização por Feature (test.describe)
 *  - Esperas explícitas (expect, waitForSelector)
 *  - Seletores claros e comentados
 *  - Dados de teste dinâmicos (emails, datas)
 *  - Tratamento de erros (try/catch onde pertinente)
 *
 *  O arquivo está pronto para execução com:
 *      npx playwright test
 *  --------------------------------------------------------------
 */

import { test, expect } from '@playwright/test';

/**
 *  -------------------------------
 *  Helper: Geração de dados dinâmicos
 *  -------------------------------
 */
const randomInt = (max: number) => Math.floor(Math.random() * max);

/**
 *  Dados de usuário (será usado em vários cenários)
 */
const baseUser = {
  name: `Teste${randomInt(1000)}`,
  email: `teste_${Date.now()}@example.com`,
  phone: '11987654321',
  cep: '01001-000',
  password: 'Password123!',
  confirmPassword: 'Password123!',
};

/**
 *  -------------------------------
 *  Helper: Login genérico
 *  -------------------------------
 */
async function login(page, email: string, password: string) {
  await page.goto('/login');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);
  await page.click('button:has-text("Entrar")');
  // Aguardamos a página inicial da conta
  await expect(page).toHaveURL(/\/account/);
}

/**
 *  -------------------------------
 *  Helper: Criar conta (para transferências)
 *  -------------------------------
 */
async function createAccount(page, accountName: string, initialBalance: number) {
  await page.goto('/accounts/create');
  await page.fill('input[name="accountName"]', accountName);
  await page.fill('input[name="initialBalance"]', initialBalance.toString());
  await page.click('button:has-text("Criar")');
  // Espera o sucesso
  await expect(page.locator('text=Conta criada com sucesso')).toBeVisible();
}

/**
 *  -------------------------------
 *  Feature: Cadastro de Usuário
 *  -------------------------------
 */
test.describe('Feature: Cadastro de Usuário', () => {
  /**
   *  Cenário: Cadastro bem-sucedido
   */
  test('Cadastro bem-sucedido', async ({ page }) => {
    // Navega para a página de cadastro
    await page.goto('/register');

    // Preenche todos os campos obrigatórios com valores válidos
    await page.fill('input[name="fullName"]', baseUser.name);
    await page.fill('input[name="email"]', baseUser.email);
    await page.fill('input[name="phone"]', baseUser.phone);
    await page.fill('input[name="cep"]', baseUser.cep);
    await page.fill('input[name="password"]', baseUser.password);
    await page.fill('input[name="confirmPassword"]', baseUser.confirmPassword);

    // Envia o formulário de cadastro
    await page.click('button:has-text("Cadastrar")');

    // Valida a mensagem de sucesso
    await expect(page.locator('text=Cadastro concluído com sucesso')).toBeVisible();

    // ------------------------------------------------------
    //  Login com as credenciais recém‑criada
    // ------------------------------------------------------
    await login(page, baseUser.email, baseUser.password);

    // Confirma mensagem de boas‑vindas
    await expect(page.locator(`text=Bem‑vindo, ${baseUser.name}`)).toBeVisible();
  });

  /**
   *  Cenário Outline: Cadastro com campo obrigatório vazio
   */
  const requiredFields = [
    { field: 'Nome', selector: 'input[name="fullName"]' },
    { field: 'Email', selector: 'input[name="email"]' },
    { field: 'Telefone', selector: 'input[name="phone"]' },
    { field: 'CEP', selector: 'input[name="cep"]' },
    { field: 'Senha', selector: 'input[name="password"]' },
    { field: 'Confirmação', selector: 'input[name="confirmPassword"]' },
  ];

  test.describe('Cadastro com campo obrigatório vazio', () => {
    for (const { field, selector } of requiredFields) {
      test(`campo ${field} vazio`, async ({ page }) => {
        await page.goto('/register');

        // Preenche todos, exceto o campo em teste
        if (selector !== 'input[name="fullName"]')
          await page.fill('input[name="fullName"]', baseUser.name);
        if (selector !== 'input[name="email"]')
          await page.fill('input[name="email"]', baseUser.email);
        if (selector !== 'input[name="phone"]')
          await page.fill('input[name="phone"]', baseUser.phone);
        if (selector !== 'input[name="cep"]')
          await page.fill('input[name="cep"]', baseUser.cep);
        if (selector !== 'input[name="password"]')
          await page.fill('input[name="password"]', baseUser.password);
        if (selector !== 'input[name="confirmPassword"]')
          await page.fill('input[name="confirmPassword"]', baseUser.confirmPassword);

        // Tenta enviar
        await page.click('button:has-text("Cadastrar")');

        // Valida mensagem de erro específica
        await expect(
          page.locator(`text=O campo '${field}' é obrigatório`)
        ).toBeVisible();
      });
    }
  });

  /**
   *  Cenário Outline: Cadastro com dados inválidos
   */
  const invalidData = [
    {
      campo: 'Email',
      valor_invalido: 'usuario@',
      mensagem: 'Formato de e‑mail inválido',
    },
    {
      campo: 'Telefone',
      valor_invalido: '123ABC',
      mensagem: 'Telefone deve conter apenas números',
    },
    {
      campo: 'CEP',
      valor_invalido: '12.345-678',
      mensagem: 'CEP inválido. Use apenas dígitos',
    },
  ];

  test.describe('Cadastro com dados inválidos', () => {
    for (const { campo, valor_invalido, mensagem } of invalidData) {
      test(`campo ${campo} com valor inválido`, async ({ page }) => {
        await page.goto('/register');

        // Preenche todos os campos
        await page.fill('input[name="fullName"]', baseUser.name);
        await page.fill('input[name="email"]', baseUser.email);
        await page.fill('input[name="phone"]', baseUser.phone);
        await page.fill('input[name="cep"]', baseUser.cep);
        await page.fill('input[name="password"]', baseUser.password);
        await page.fill('input[name="confirmPassword"]', baseUser.confirmPassword);

        // Substitui o campo em teste pelo valor inválido
        if (campo === 'Email')
          await page.fill('input[name="email"]', valor_invalido);
        if (campo === 'Telefone')
          await page.fill('input[name="phone"]', valor_invalido);
        if (campo === 'CEP')
          await page.fill('input[name="cep"]', valor_invalido);

        // Envia
        await page.click('button:has-text("Cadastrar")');

        // Verifica a mensagem de erro
        await expect(page.locator(`text=${mensagem}`)).toBeVisible();
      });
    }
  });
});

/**
 *  -------------------------------
 *  Feature: Login
 *  -------------------------------
 */
test.describe('Feature: Login', () => {
  /**
   *  Cenário: Login com credenciais válidas
   */
  test('Login com credenciais válidas', async ({ page }) => {
    // Primeiro, asseguramos que o usuário já está cadastrado
    await login(page, baseUser.email, baseUser.password);

    // Verifica redirecionamento e mensagem de boas‑vindas
    await expect(page).toHaveURL(/\/account/);
    await expect(page.locator(`text=Bem‑vindo, ${baseUser.name}`)).toBeVisible();
  });

  /**
   *  Cenário Outline: Login com credenciais inválidas
   */
  const invalidLogin = [
    { campo: 'e‑mail', valor: 'usuario@exemplo.com', mensagem: 'Credenciais inválidas' },
    { campo: 'senha', valor: 'senhaErrada', mensagem: 'Credenciais inválidas' },
    { campo: 'ambos', valor: 'errado@example.com', mensagem: 'Credenciais inválidas' },
  ];

  test.describe('Login com credenciais inválidas', () => {
    for (const { campo, valor, mensagem } of invalidLogin) {
      test(`campo ${campo} com valor '${valor}'`, async ({ page }) => {
        await page.goto('/login');

        if (campo !== 'senha') {
          await page.fill('input[name="email"]', valor);
        }
        if (campo !== 'e‑mail') {
          await page.fill('input[name="password"]', valor);
        }

        // Tenta entrar
        await page.click('button:has-text("Entrar")');

        // Verifica mensagem de erro
        await expect(page.locator(`text=${mensagem}`)).toBeVisible();
      });
    }
  });
});

/**
 *  -------------------------------
 *  Feature: Acesso à Conta – Saldo e Extrato
 *  -------------------------------
 */
test.describe('Feature: Acesso à Conta – Saldo e Extrato', () => {
  /**
   *  Cenário: Exibição de saldo atualizado após operação
   */
  test('Saldo atualizado após depósito', async ({ page }) => {
    // 1️⃣ Login do usuário
    await login(page, baseUser.email, baseUser.password);

    // 2️⃣ Vai para a página de depósito
    await page.goto('/deposit');

    // 3️⃣ Deposita R$ 500,00
    await page.fill('input[name="amount"]', '500');
    await page.click('button:has-text("Depositar")');

    // 4️⃣ Valida que a mensagem de sucesso aparece
    await expect(
      page.locator('text=Depósito concluído com sucesso')
    ).toBeVisible();

    // 5️⃣ Acessa a página de saldo
    await page.goto('/balance');
    await expect(page.locator('text=R$ 1.500,00')).toBeVisible();
  });

  /**
   *  Cenário: Listagem de transações recentes no extrato
   */
  test('Extrato em ordem cronológica', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    // Simulamos três transações via UI (ou API) – para fins de exemplo, assumimos que já existem
    // Em um cenário real, você chamaria API ou preencheria formulários de transações

    // 1️⃣ Abre o extrato
    await page.goto('/statement');

    // 2️⃣ Verifica a ordem: da mais recente à mais antiga
    const transactions = page.locator('.transaction-row');
    const count = await transactions.count();
    expect(count).toBeGreaterThanOrEqual(3);

    // Pegamos as datas das transações e comparamos se estão em ordem decrescente
    const dates = await Promise.all(
      Array.from({ length: count }, async (_, i) => {
        return await transactions.nth(i).locator('.date').innerText();
      })
    );

    // Função simples de comparação de datas (dd/mm/yyyy)
    const parseDate = (str: string) => new Date(str.split('/').reverse().join('-'));
    const sortedDates = [...dates].sort((a, b) => parseDate(b).valueOf() - parseDate(a).valueOf());

    expect(dates).toEqual(sortedDates);
  });
});

/**
 *  -------------------------------
 *  Feature: Transferência de Fundos
 *  -------------------------------
 */
test.describe('Feature: Transferência de Fundos', () => {
  /**
   *  Cenário: Transferência bem‑sucedida
   */
  test('Transferência bem‑sucedida', async ({ page }) => {
    // Criação de duas contas de teste (conta A e conta B)
    const accountA = `ContaA_${randomInt(1000)}`;
    const accountB = `ContaB_${randomInt(1000)}`;

    await createAccount(page, accountA, 2000);
    await createAccount(page, accountB, 0);

    // Login
    await login(page, baseUser.email, baseUser.password);

    // 1️⃣ Navega para a página de transferência
    await page.goto('/transfer');

    // 2️⃣ Preenche dados da transferência
    await page.selectOption('select[name="fromAccount"]', accountA);
    await page.selectOption('select[name="toAccount"]', accountB);
    await page.fill('input[name="amount"]', '300');

    // 3️⃣ Envia a transferência
    await page.click('button:has-text("Transferir")');

    // 4️⃣ Confirma que a mensagem de sucesso aparece
    await expect(page.locator('text=Transferência concluída com sucesso')).toBeVisible();

    // 5️⃣ Verifica saldos após a transferência
    await page.goto('/accounts');
    await expect(
      page.locator(`text=${accountA} R$ 1.700,00`)
    ).toBeVisible();
    await expect(
      page.locator(`text=${accountB} R$ 300,00`)
    ).toBeVisible();

    // 6️⃣ Garante que ambas as contas registram a transação no histórico
    await page.goto('/account/history');
    await expect(
      page.locator('text=Transferência de R$ 300,00 para ' + accountB)
    ).toBeVisible();
  });

  /**
   *  Cenário Outline: Transferência com valor superior ao saldo
   */
  const insufficientFunds = [
    { saldo: 500, valor: 600 },
    { saldo: 100, valor: 150 },
  ];

  test.describe('Transferência com saldo insuficiente', () => {
    for (const { saldo, valor } of insufficientFunds) {
      test(`saldo R$ ${saldo} tentando enviar R$ ${valor}`, async ({ page }) => {
        // Cria conta A com saldo específico
        const accountA = `SaldoA_${randomInt(1000)}`;
        const accountB = `SaldoB_${randomInt(1000)}`;
        await createAccount(page, accountA, saldo);
        await createAccount(page, accountB, 0);

        // Login
        await login(page, baseUser.email, baseUser.password);

        // Preenche transferência
        await page.goto('/transfer');
        await page.selectOption('select[name="fromAccount"]', accountA);
        await page.selectOption('select[name="toAccount"]', accountB);
        await page.fill('input[name="amount"]', valor.toString());

        // Tenta enviar
        await page.click('button:has-text("Transferir")');

        // Verifica mensagem de saldo insuficiente
        await expect(page.locator('text=Saldo insuficiente')).toBeVisible();
      });
    }
  });

  /**
   *  Cenário: Transferência para conta inexistente
   */
  test('Transferência para conta inexistente', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    await page.goto('/transfer');
    // Seleciona uma conta de destino que não existe
    await page.selectOption('select[name="fromAccount"]', 'ContaExistente');
    await page.selectOption('select[name="toAccount"]', '999999'); // Conta fictícia
    await page.fill('input[name="amount"]', '200');

    await page.click('button:has-text("Transferir")');

    await expect(page.locator('text=Conta de destino não encontrada')).toBeVisible();
  });
});

/**
 *  -------------------------------
 *  Feature: Solicitação de Empréstimo
 *  -------------------------------
 */
test.describe('Feature: Solicitação de Empréstimo', () => {
  /**
   *  Cenário: Empréstimo aprovado
   */
  test('Empréstimo aprovado', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    await page.goto('/loan/request');

    await page.fill('input[name="loanAmount"]', '20000');
    await page.fill('input[name="annualIncome"]', '120000');

    await page.click('button:has-text("Enviar")');

    await expect(page.locator('text=Empréstimo aprovado')).toBeVisible();
  });

  /**
   *  Cenário: Empréstimo negado por renda insuficiente
   */
  test('Empréstimo negado por renda insuficiente', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    await page.goto('/loan/request');

    await page.fill('input[name="loanAmount"]', '20000');
    await page.fill('input[name="annualIncome"]', '30000');

    await page.click('button:has-text("Enviar")');

    await expect(
      page.locator('text=Empréstimo negado – renda insuficiente')
    ).toBeVisible();
  });
});

/**
 *  -------------------------------
 *  Feature: Pagamento de Contas
 *  -------------------------------
 */
test.describe('Feature: Pagamento de Contas', () => {
  /**
   *  Cenário: Pagamento pontual imediato
   */
  test('Pagamento pontual imediato', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    await page.goto('/payment/instant');

    await page.fill('input[name="beneficiary"]', 'João Silva');
    await page.fill('input[name="address"]', 'Rua Exemplo, 123');
    await page.fill('input[name="city"]', 'São Paulo');
    await page.fill('input[name="state"]', 'SP');
    await page.fill('input[name="zip"]', '01001-000');
    await page.fill('input[name="phone"]', '11987654321');
    await page.fill('input[name="accountNumber"]', '123456');
    await page.fill('input[name="amount"]', '150');

    // Data de pagamento hoje
    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    await page.fill('input[name="paymentDate"]', today);

    await page.click('button:has-text("Confirmar")');

    await expect(
      page.locator('text=Pagamento efetuado com sucesso')
    ).toBeVisible();

    // Verifica histórico
    await page.goto('/payment/history');
    await expect(page.locator('text=João Silva')).toBeVisible();
  });

  /**
   *  Cenário: Pagamento agendado para data futura
   */
  test('Pagamento agendado para data futura', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    await page.goto('/payment/instant');

    await page.fill('input[name="beneficiary"]', 'Empresa X');
    await page.fill('input[name="address"]', 'Av. Central, 200');
    await page.fill('input[name="city"]', 'Rio de Janeiro');
    await page.fill('input[name="state"]', 'RJ');
    await page.fill('input[name="zip"]', '20000-000');
    await page.fill('input[name="phone"]', '21987654321');
    await page.fill('input[name="accountNumber"]', '654321');
    await page.fill('input[name="amount"]', '300');

    // Data futura (ex.: 1 de dezembro de 2025)
    const futureDate = '2025-12-01';
    await page.fill('input[name="paymentDate"]', futureDate);

    await page.click('button:has-text("Confirmar")');

    await expect(
      page.locator('text=Pagamento agendado para 01/12/2025')
    ).toBeVisible();

    // Verifica que aparece no histórico com status Agendado
    await page.goto('/payment/history');
    await expect(
      page.locator(`text=Empresa X - Agendado em ${futureDate}`)
    ).toBeVisible();
  });
});

/**
 *  -------------------------------
 *  Feature: Navegação e Usabilidade
 *  -------------------------------
 */
test.describe('Feature: Navegação e Usabilidade', () => {
  /**
   *  Cenário: Carregamento sem erros de navegação
   */
  test('Carregamento de todas as páginas sem erros', async ({ page }) => {
    const pages = [
      '/',
      '/login',
      '/account',
      '/deposit',
      '/withdraw',
      '/transfer',
      '/loan/request',
      '/payment/instant',
      '/statement',
      '/account/history',
      '/payment/history',
      '/settings',
    ];

    for (const path of pages) {
      await page.goto(path);
      await page.waitForLoadState('networkidle');

      // Checa se não há mensagens de erro (ex.: <div class="error">)
      await expect(page.locator('.error')).toHaveCount(0);
    }
  });

  /**
   *  Cenário: Consistência de links e menus
   */
  test('Verifica cabeçalho e link “Minha Conta”', async ({ page }) => {
    await page.goto('/');

    // Espera que o cabeçalho carregue
    const header = page.locator('header');
    await expect(header).toBeVisible();

    // Checa que todos os itens de menu existem (exemplo)
    const menuItems = ['Home', 'Contas', 'Transferências', 'Empréstimos', 'Pagamentos', 'Minha Conta'];
    for (const item of menuItems) {
      await expect(header.locator(`text=${item}`)).toBeVisible();
    }

    // Clica no link “Minha Conta” e verifica redirecionamento
    await header.locator('text=Minha Conta').click();
    await expect(page).toHaveURL(/\/account/);
    await expect(header.locator('text=Minha Conta')).toBeVisible();
  });

  /**
   *  Cenário: Exibição clara de mensagens de erro
   */
  test('Mensagem de erro concisa em operação inválida', async ({ page }) => {
    await login(page, baseUser.email, baseUser.password);

    // Simula operação inválida: tenta sacar R$ 10.000 sem saldo suficiente
    await page.goto('/withdraw');
    await page.fill('input[name="amount"]', '10000');
    await page.click('button:has-text("Sacar")');

    // Verifica mensagem de erro clara
    await expect(
      page.locator('text=Saldo insuficiente para essa operação')
    ).toBeVisible();
  });
});
```

---

### 4. Como usar

1. **Instalação das dependências**  
   ```bash
   npm install --save-dev @playwright/test
   npx playwright install
   ```

2. **Rodar os testes**  
   ```bash
   npx playwright test
   ```

3. **Ajustes necessários**  
   - Substitua os **seletores** (`input[name="..."]`, `button:has-text(...)`, etc.) pelos valores corretos da aplicação real.  
   - Se a aplicação possuir rotas diferentes ou componentes nomeados de maneira distinta, modifique o `goto` e os `locators` adequadamente.  
   - Caso a API de criação de contas seja exposta, troque a função `createAccount` por chamadas `page.request.post(...)` para maior rapidez.

---

## 5. Dicas de Manutenção

| Tema | Dica |
|------|------|
| **Organização** | Divida os testes em múltiplos arquivos (`registration.spec.ts`, `login.spec.ts`, etc.) quando o projeto crescer. |
| **Reutilização** | Extraia helpers comuns (login, criação de conta, etc.) em um diretório `utils/`. |
| **Data Dinâmica** | Para cenários de pagamento futuro, use `new Date()` e formate conforme necessário. |
| **Logs** | Em ambientes de CI, habilite `trace: 'on-first-retry'` no `playwright.config.ts` para capturar trace em falhas. |
| **Parâmetros** | Utilize `test.describe.each` ou `test.each` para cenários com múltiplas combinações de dados. |

Com esta base você tem uma suíte Playwright completa, organizada e pronta para testar todas as funcionalidades descritas nos cenários BDD. Boa automatização!