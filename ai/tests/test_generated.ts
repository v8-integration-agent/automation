## 🎉 Playwright Test Suite – “ParaBank”  
*(Tudo em **TypeScript** – pronto para ser copiado e executado com `npx playwright test`)*  

> **Como filtrar por tags**  
> 1. Use a flag `--grep` na linha de comando.  
> 2. Ex.: `npx playwright test --grep @Cadastro` – executa somente cenários com a tag **@Cadastro**.  
>  
> 3. Você também pode combinar: `--grep @Login --grep @Validacao` → ambos.  

---

## Estrutura de Pastas

```
/tests
├─ registration.spec.ts
├─ login.spec.ts
├─ account.spec.ts
├─ transfer.spec.ts
├─ loan.spec.ts
├─ payment.spec.ts
└─ navigation.spec.ts
```

> Cada arquivo corresponde a uma **Feature** do Gherkin.  
> Os testes estão organizados em blocos `test.describe(...)` e cada *Scenario Outline* usa `test.each(...)`.

---

## Common Setup (shared helpers)

> Crie um arquivo `tests/helpers.ts` (ou `utils.ts`) para evitar código duplicado.  
> Aqui está apenas a *API* de exemplos – adapte os seletores e rotas à sua aplicação.

```ts
// tests/helpers.ts
import { Page, Locator } from '@playwright/test';

/** ---------- Página de Cadastro ---------- */
export const goToRegister = async (page: Page) =>
  await page.goto('/register');

export const fillRegistrationForm = async (page: Page, data: {
  nome: string; sobrenome: string; email: string; telefone: string;
  cep: string; senha: string;
}) => {
  await page.fill('[data-test="firstName"]', data.nome);
  await page.fill('[data-test="lastName"]', data.sobrenome);
  await page.fill('[data-test="email"]', data.email);
  await page.fill('[data-test="phone"]', data.telefone);
  await page.fill('[data-test="zip"]', data.cep);
  await page.fill('[data-test="password"]', data.senha);
};

export const clickRegister = async (page: Page) =>
  await page.click('[data-test="btn-register"]');

/** ---------- Página de Login ---------- */
export const goToLogin = async (page: Page) =>
  await page.goto('/login');

export const fillLoginForm = async (page: Page, data: { email: string; senha: string; }) => {
  await page.fill('[data-test="email"]', data.email);
  await page.fill('[data-test="password"]', data.senha);
};

export const clickLogin = async (page: Page) =>
  await page.click('[data-test="btn-login"]');

/** ---------- Mensagens ---------- */
export const expectSuccessMessage = async (page: Page, text: string) => {
  await expect(page.locator('[data-test="alert-success"]')).toHaveText(text);
};

export const expectErrorMessage = async (page: Page, text: string) => {
  await expect(page.locator('[data-test="alert-error"]')).toHaveText(text);
};
```

> **Tip:** Se sua aplicação usa `data-testid`, prefira esses atributos.  
> Se não tiver, adapte os seletores para `input[name="..."]` ou `label >> input`.

---

## 1️⃣ Feature: Cadastro de Usuário

```ts
// tests/registration.spec.ts
import { test, expect } from '@playwright/test';
import {
  goToRegister,
  fillRegistrationForm,
  clickRegister,
  expectSuccessMessage,
  expectErrorMessage,
  goToLogin,
  fillLoginForm,
  clickLogin,
} from './helpers';

test.describe('@Cadastro', () => {
  // ---- Cadastro bem‑sucedido ----
  test.describe('Cadastro bem-sucedido', () => {
    test.each([
      {
        nome: 'João',
        sobrenome: 'Silva',
        email: 'joao.silva@email.com',
        telefone: '(11)987654321',
        cep: '01001000',
        senha: 'senha123',
        mensagemSucesso: 'Cadastro realizado com sucesso!',
      },
    ])(
      'Deve registrar %s %s com sucesso',
      async ({ nome, sobrenome, email, telefone, cep, senha, mensagemSucesso }) => {
        const page = test.newContext().page;

        // Dado que o usuário acessa a tela de cadastro
        await goToRegister(page);

        // Quando ele preenche os campos obrigatórios
        await fillRegistrationForm(page, { nome, sobrenome, email, telefone, cep, senha });

        // E clica em “Cadastrar”
        await clickRegister(page);

        // Então a mensagem de sucesso deve ser exibida
        await expectSuccessMessage(page, mensagemSucesso);

        // E o usuário deve conseguir fazer login com os mesmos dados
        await goToLogin(page);
        await fillLoginForm(page, { email, senha });
        await clickLogin(page);

        await expect(page.locator('text=Bem‑vindo')).toBeVisible();
        await expect(page.locator(`text=Bem‑vindo, ${nome}`)).toBeVisible();
      }
    );
  });

  // ---- Campos obrigatórios em branco ----
  test.describe('Cadastro com campo obrigatório em branco', () => {
    test.each([
      { campo: 'firstName', mensagemErro: 'Nome é obrigatório' },
      { campo: 'lastName', mensagemErro: 'Sobrenome é obrigatório' },
      { campo: 'email', mensagemErro: 'Email é obrigatório' },
      { campo: 'phone', mensagemErro: 'Telefone é obrigatório' },
      { campo: 'zip', mensagemErro: 'CEP é obrigatório' },
      { campo: 'password', mensagemErro: 'Senha é obrigatória' },
    ])('deve exibir erro quando $campo fica em branco', async ({ campo, mensagemErro }) => {
      const page = test.newContext().page;

      await goToRegister(page);

      // Preenche todos os campos
      await fillRegistrationForm(page, {
        nome: 'João',
        sobrenome: 'Silva',
        email: 'joao.silva@email.com',
        telefone: '(11)987654321',
        cep: '01001000',
        senha: 'senha123',
      });

      // Limpa apenas o campo em teste
      await page.fill(`[data-test="${campo}"]`, '');

      await clickRegister(page);

      await expectErrorMessage(page, mensagemErro);
    });
  });

  // ---- Dados inválidos ----
  test.describe('Cadastro com dados inválidos', () => {
    test.each([
      { campo: 'phone', valor: 'abc123', mensagem: 'Telefone inválido. Use apenas números.' },
      { campo: 'zip', valor: '123', mensagem: 'CEP inválido. Deve conter 8 dígitos.' },
      { campo: 'email', valor: 'usuario.com', mensagem: 'Email inválido. Use o formato nome@domínio.' },
    ])('deve exibir erro para $campo com valor inválido', async ({ campo, valor, mensagem }) => {
      const page = test.newContext().page;

      await goToRegister(page);

      // Preenche todos os campos com valores válidos
      await fillRegistrationForm(page, {
        nome: 'João',
        sobrenome: 'Silva',
        email: 'joao.silva@email.com',
        telefone: '(11)987654321',
        cep: '01001000',
        senha: 'senha123',
      });

      // Substitui o campo alvo por valor inválido
      await page.fill(`[data-test="${campo}"]`, valor);

      await clickRegister(page);

      await expectErrorMessage(page, mensagem);
    });
  });
});
```

---

## 2️⃣ Feature: Login

```ts
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import {
  goToLogin,
  fillLoginForm,
  clickLogin,
  expectErrorMessage,
} from './helpers';

test.describe('@Login', () => {
  // ---- Login bem‑sucedido ----
  test.describe('Login bem‑sucedido', () => {
    test.each([
      {
        email: 'joao.silva@email.com',
        senha: 'senha123',
        nome: 'João',
      },
    ])(
      'deve logar %s e exibir “Bem‑vindo, %s”',
      async ({ email, senha, nome }) => {
        const page = test.newContext().page;
        await goToLogin(page);
        await fillLoginForm(page, { email, senha });
        await clickLogin(page);
        await expect(page.locator(`text=Bem‑vindo, ${nome}`)).toBeVisible();
      }
    );
  });

  // ---- Login com credenciais inválidas ----
  test.describe('Login com credenciais inválidas', () => {
    test.each([
      { email: 'joao.silva@email.com', senha: 'wrong', mensagem: 'Credenciais inválidas.' },
      { email: 'wrong@email.com', senha: 'senha123', mensagem: 'Credenciais inválidas.' },
      { email: '', senha: '', mensagem: 'Preencha email e senha.' },
    ])('deve exibir erro quando credenciais são $email/$senha', async ({ email, senha, mensagem }) => {
      const page = test.newContext().page;
      await goToLogin(page);
      await fillLoginForm(page, { email, senha });
      await clickLogin(page);
      await expectErrorMessage(page, mensagem);
    });
  });
});
```

---

## 3️⃣ Feature: Acesso à Conta – Saldo e Extrato

```ts
// tests/account.spec.ts
import { test, expect } from '@playwright/test';

test.describe('@Conta', () => {
  // ---- Visualização do saldo após transação ----
  test('Visualização do saldo após transação', async ({ page }) => {
    // 1. Acesso à página inicial (já logado)
    await page.goto('/home'); // ajuste conforme sua rota

    // 2. Faz uma transferência de R$ 500,00
    await page.goto('/transfer'); // rota de transferência
    await page.fill('[data-test="amount"]', '500');
    await page.click('[data-test="btn-transfer"]');

    // 3. Confirma (pode ser automática se o fluxo não pede confirm)
    // 4. Verifica saldo atualizado
    await expect(page.locator('[data-test="balance"]')).toHaveText('R$ 2.500,00');

    // 5. Extrato lista a transferência em ordem cronológica
    await page.goto('/statement');
    const firstRow = page.locator('[data-test="transaction-row"]').first();
    await expect(firstRow).toContainText('Transferência de R$ 500,00');
  });

  // ---- Exibição de extrato em ordem cronológica ----
  test('Extrato em ordem cronológica', async ({ page }) => {
    await page.goto('/statement');
    const rows = page.locator('[data-test="transaction-row"]');

    const texts = await rows.allTextContents();
    // Verifica que a lista está em ordem decrescente de data
    const sorted = [...texts].sort((a, b) => (a > b ? -1 : 1));
    expect(texts).toEqual(sorted);
  });
});
```

> **Obs:**  
> - Se a sua aplicação usa *date pickers* ou modais, adicione esperas (`await page.waitForSelector(...)`) antes de interagir.  
> - Os seletores `data-test` são apenas exemplos. Adapte‑os à sua base de código.

---

## 4️⃣ Feature: Transferência de Fundos

```ts
// tests/transfer.spec.ts
import { test, expect } from '@playwright/test';

test.describe('@Transferencia', () => {
  // ---- Transferência válida ----
  test.each([
    { contaOrig: '123456', contaDest: '654321', valor: '200' },
  ])('Transferência válida de R$ %s', async ({ contaOrig, contaDest, valor }) => {
    const page = test.newContext().page;
    await page.goto('/transfer');

    await page.fill('[data-test="sourceAccount"]', contaOrig);
    await page.fill('[data-test="destAccount"]', contaDest);
    await page.fill('[data-test="amount"]', valor);
    await page.click('[data-test="btn-confirm"]');

    // Debitado e creditado
    await expect(page.locator(`[data-test="balance-${contaOrig}"]`)).toHaveText(`-R$ ${valor}`);
    await expect(page.locator(`[data-test="balance-${contaDest}"]`)).toHaveText(`+R$ ${valor}`);

    // Histórico
    await page.goto('/history');
    const rows = page.locator('[data-test="transaction-row"]');
    await expect(rows.first()).toContainText(`Transferência de R$ ${valor}`);
  });

  // ---- Transferência com saldo insuficiente ----
  test.each([
    { contaOrig: '123456', contaDest: '654321', valor: '10000', mensagem: 'Saldo insuficiente para essa transferência.' },
  ])('Transferência com saldo insuficiente', async ({ contaOrig, contaDest, valor, mensagem }) => {
    const page = test.newContext().page;
    await page.goto('/transfer');

    await page.fill('[data-test="sourceAccount"]', contaOrig);
    await page.fill('[data-test="destAccount"]', contaDest);
    await page.fill('[data-test="amount"]', valor);
    await page.click('[data-test="btn-confirm"]');

    await expect(page.locator('[data-test="alert-error"]')).toHaveText(mensagem);

    // Confirme que não houve alteração nos saldos
    const saldoOrig = await page.locator(`[data-test="balance-${contaOrig}"]`).innerText();
    const saldoDest = await page.locator(`[data-test="balance-${contaDest}"]`).innerText();
    // Saldo inicial esperado, adapte conforme cenário de teste
    expect(saldoOrig).not.toContain(`-${valor}`);
    expect(saldoDest).not.toContain(`+${valor}`);
  });
});
```

---

## 5️⃣ Feature: Solicitação de Empréstimo

```ts
// tests/loan.spec.ts
import { test, expect } from '@playwright/test';

test.describe('@Emprestimo', () => {
  // ---- Empréstimo aprovado ----
  test.each([
    { valor: '5000', renda: '50000', mensagem: 'Empréstimo aprovado!' },
  ])('Empréstimo aprovado', async ({ valor, renda, mensagem }) => {
    const page = test.newContext().page;
    await page.goto('/loan');

    await page.fill('[data-test="loanAmount"]', valor);
    await page.fill('[data-test="annualIncome"]', renda);
    await page.click('[data-test="btn-submit"]');

    await expect(page.locator('[data-test="alert-success"]')).toHaveText(mensagem);
    await expect(page.locator('[data-test="loan-status"]')).toHaveText('Aprovado');
  });

  // ---- Empréstimo negado ----
  test.each([
    { valor: '50000', renda: '10000', mensagem: 'Empréstimo negado: renda insuficiente.' },
  ])('Empréstimo negado', async ({ valor, renda, mensagem }) => {
    const page = test.newContext().page;
    await page.goto('/loan');

    await page.fill('[data-test="loanAmount"]', valor);
    await page.fill('[data-test="annualIncome"]', renda);
    await page.click('[data-test="btn-submit"]');

    await expect(page.locator('[data-test="alert-error"]')).toHaveText(mensagem);
    await expect(page.locator('[data-test="loan-status"]')).toHaveText('Negado');
  });
});
```

---

## 6️⃣ Feature: Pagamento de Contas

```ts
// tests/payment.spec.ts
import { test, expect } from '@playwright/test';

test.describe('@Pagamento', () => {
  // ---- Pagamento agendado com sucesso ----
  test.each([
    {
      beneficiario: 'Maria',
      endereco: 'Rua das Flores, 10',
      cidade: 'SP',
      estado: 'SP',
      cep: '01001-000',
      telefone: '(11)912345678',
      contaDest: '123456',
      valor: '150',
      data: '2025-11-01',
      mensagem: 'Pagamento agendado com sucesso!',
    },
  ])(
    'Pagamento agendado – %s',
    async ({ beneficiario, endereco, cidade, estado, cep, telefone, contaDest, valor, data, mensagem }) => {
      const page = test.newContext().page;
      await page.goto('/payment');

      await page.fill('[data-test="beneficiary"]', beneficiario);
      await page.fill('[data-test="address"]', endereco);
      await page.fill('[data-test="city"]', cidade);
      await page.fill('[data-test="state"]', estado);
      await page.fill('[data-test="zip"]', cep);
      await page.fill('[data-test="phone"]', telefone);
      await page.fill('[data-test="destAccount"]', contaDest);
      await page.fill('[data-test="amount"]', valor);
      await page.fill('[data-test="date"]', data);

      await page.click('[data-test="btn-submit"]');

      await expect(page.locator('[data-test="alert-success"]')).toHaveText(mensagem);
      await expect(page.locator('[data-test="payment-history"]')).toContainText(beneficiario);
      await expect(page.locator('[data-test="payment-date"]')).toContainText(data);
    }
  );

  // ---- Campos obrigatórios vazios ----
  test.describe('Pagamento com campo obrigatório vazio', () => {
    const campos = [
      { campo: 'beneficiary', mensagem: 'Beneficiário é obrigatório' },
      { campo: 'address', mensagem: 'Endereço é obrigatório' },
      { campo: 'city', mensagem: 'Cidade é obrigatória' },
      { campo: 'state', mensagem: 'Estado é obrigatório' },
      { campo: 'zip', mensagem: 'CEP é obrigatório' },
      { campo: 'phone', mensagem: 'Telefone é obrigatório' },
      { campo: 'destAccount', mensagem: 'Conta de destino é obrigatória' },
      { campo: 'amount', mensagem: 'Valor é obrigatório' },
      { campo: 'date', mensagem: 'Data de pagamento é obrigatória' },
    ];

    campos.forEach(({ campo, mensagem }) => {
      test(`deve exibir erro quando ${campo} está vazio`, async () => {
        const page = test.newContext().page;
        await page.goto('/payment');

        // Preenche todos os campos com valores válidos
        await page.fill('[data-test="beneficiary"]', 'Maria');
        await page.fill('[data-test="address"]', 'Rua das Flores, 10');
        await page.fill('[data-test="city"]', 'SP');
        await page.fill('[data-test="state"]', 'SP');
        await page.fill('[data-test="zip"]', '01001-000');
        await page.fill('[data-test="phone"]', '(11)912345678');
        await page.fill('[data-test="destAccount"]', '123456');
        await page.fill('[data-test="amount"]', '150');
        await page.fill('[data-test="date"]', '2025-11-01');

        // Limpa o campo em teste
        await page.fill(`[data-test="${campo}"]`, '');

        await page.click('[data-test="btn-submit"]');

        await expect(page.locator('[data-test="alert-error"]')).toHaveText(mensagem);
      });
    });
  });
});
```

---

## 7️⃣ Feature: Navegação e Usabilidade Geral

```ts
// tests/navigation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('@Navegacao @Carregamento', () => {
  const routes = ['/login', '/register', '/home', '/transfer', '/statement', '/loan', '/payment'];
  test('Todas as páginas carregam sem erros', async ({ page }) => {
    for (const route of routes) {
      await page.goto(route);
      // Espera que a página carregue completamente
      await page.waitForLoadState('networkidle');
      // Verifica que não há mensagens de erro globais
      const errorAlert = page.locator('[data-test="alert-error"]');
      await expect(errorAlert).toHaveCount(0);
    }
  });
});

test.describe('@Usabilidade @Consistencia', () => {
  test('Menus e links são consistentes em todas as páginas', async ({ page }) => {
    const menuSelector = '[data-test="main-menu"]';
    const expectedLinks = ['Home', 'Conta', 'Transferência', 'Pagamentos', 'Empréstimo', 'Login', 'Cadastro'];

    for (const route of ['/login', '/register', '/home', '/transfer', '/statement', '/loan', '/payment']) {
      await page.goto(route);
      await expect(page.locator(menuSelector)).toBeVisible();

      for (const link of expectedLinks) {
        const menuItem = page.locator(`${menuSelector} >> text=${link}`);
        await expect(menuItem).toBeVisible();
      }
    }
  });
});

test.describe('@Usabilidade @Mensagens', () => {
  test('Mensagens de erro são claras e objetivas', async ({ page }) => {
    await page.goto('/login');
    // Simula login inválido
    await page.fill('[data-test="email"]', '');
    await page.fill('[data-test="password"]', '');
    await page.click('[data-test="btn-login"]');

    await expect(page.locator('[data-test="alert-error"]')).toHaveText('Preencha email e senha.');
    // Pode validar que a mensagem possui menos de 80 caracteres, por exemplo
    const errorText = await page.textContent('[data-test="alert-error"]');
    expect(errorText!.length).toBeLessThanOrEqual(80);
  });
});
```

---

## 🚀 Como rodar

```bash
# 1. Instale dependências
npm i @playwright/test

# 2. Execute todos os testes
npx playwright test

# 3. Filtre por tag
npx playwright test --grep @Cadastro
npx playwright test --grep @Login --grep @Validacao   # ambos

# 4. Gere um relatório HTML
npx playwright test --reporter html
npx playwright show-report
```

> Se quiser usar **JavaScript** em vez de **TypeScript**, basta trocar as extensões de `.ts` para `.js` e remover os tipos.  
> Os seletores `data-test` devem existir em seu código; caso contrário, adapte para `input[name="..."]`, `label >> input`, etc.

---

## 📌 Dicas de Boa Prática

| Prática | Por quê? | Como aplicar? |
|---------|----------|----------------|
| **Page Object Model** | Organiza o código, facilita manutenção | Crie classes `RegisterPage`, `LoginPage` etc. |
| **`data-testid`** | Seletores não quebram com mudança de UI | Adicione atributos `data-testid` nos elementos. |
| **`test.describe.each` / `test.each`** | Reduz repetições | Use os exemplos do Gherkin em `test.each`. |
| **`await page.waitForSelector(...)`** | Evita flakiness | Use antes de interações ou validações. |
| **`--grep`** | Execução seletiva | Filtre cenários por tags. |
| **Comentários** | Legibilidade | Explicite cada passo em `test.step` ou nos comentários. |

---

### 🎉 Pronto para usar!  
Copie os arquivos acima, adapte os seletores e rotas ao seu projeto, e rode `npx playwright test`.  
Se precisar de mais cenários ou de ajuda com **fixtures**, **mocking** ou **CI/CD**, é só chamar!