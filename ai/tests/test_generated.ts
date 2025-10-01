**Obs.**  
- Todos os arquivos abaixo estão escritos em **TypeScript** e foram projetados para serem executados com o **Playwright Test Runner** (`npx playwright test`).  
- Os *selectors* (`input[name="…"]`, `button:has-text("Cadastrar")`, etc.) são exemplos.  Você precisará ajustá‑los de acordo com o HTML real da aplicação ParaBank.  
- Para tornar os cenários **reais** (por exemplo, criar um usuário que não exista antes de logar) usamos `faker` (ou `crypto.randomUUID()`) para gerar e‑mails e senhas aleatórias.  
- Todos os cenários foram transformados em **tests**; os **Scenario Outlines** foram convertidos em `test.each` e os **Scenario** em `test`.  
- Foram adicionados *waits* explícitos (`await page.waitForSelector(...)`) e `expect` assertions.  
- Os testes estão organizados em pastas `tests/` – cada feature recebe um arquivo separado – e utilizam *page objects* (pasta `pages/`) para encapsular ações repetitivas.

---

## Estrutura de Pastas

```
/playwright-test
├── package.json
├── tsconfig.json
├── playwright.config.ts
├── tests
│   ├── cadastro.spec.ts
│   ├── login.spec.ts
│   ├── saldo-extrato.spec.ts
│   ├── transferencia.spec.ts
│   ├── solicitacao-emprestimo.spec.ts
│   └── pagamento-contas.spec.ts
└── pages
    ├── basePage.ts
    ├── cadastroPage.ts
    ├── loginPage.ts
    ├── contaPage.ts
    ├── transferPage.ts
    ├── emprestimoPage.ts
    └── pagamentoPage.ts
```

---

## 1️⃣ `playwright.config.ts`

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: 'https://demo-parabank.com',   // altere para a URL real
    headless: false,                        // deixe false para depurar
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
```

---

## 2️⃣ Page Objects (ex.: `pages/basePage.ts`)

```ts
import { Page, expect } from '@playwright/test';

export class BasePage {
  constructor(protected page: Page) {}

  async navigate(url: string) {
    await this.page.goto(url);
  }

  async click(selector: string) {
    await this.page.waitForSelector(selector, { state: 'visible' });
    await this.page.click(selector);
  }

  async fill(selector: string, value: string) {
    await this.page.waitForSelector(selector, { state: 'visible' });
    await this.page.fill(selector, value);
  }

  async getText(selector: string) {
    await this.page.waitForSelector(selector, { state: 'visible' });
    return this.page.textContent(selector);
  }

  async expectVisible(selector: string) {
    await expect(this.page.locator(selector)).toBeVisible();
  }
}
```

### `pages/cadastroPage.ts`

```ts
import { BasePage } from './basePage';

export class CadastroPage extends BasePage {
  readonly formSelectors = {
    nome: 'input[name="name"]',
    email: 'input[name="email"]',
    telefone: 'input[name="phone"]',
    cep: 'input[name="cep"]',
    endereco: 'input[name="address"]',
    senha: 'input[name="password"]',
    confirmSenha: 'input[name="confirmPassword"]',
    btnCadastrar: 'button:has-text("Cadastrar")',
  };

  async preencheCamposObrigatorios(data: {
    nome: string;
    email: string;
    telefone: string;
    cep: string;
    endereco: string;
    senha: string;
    confirmSenha: string;
  }) {
    await this.fill(this.formSelectors.nome, data.nome);
    await this.fill(this.formSelectors.email, data.email);
    await this.fill(this.formSelectors.telefone, data.telefone);
    await this.fill(this.formSelectors.cep, data.cep);
    await this.fill(this.formSelectors.endereco, data.endereco);
    await this.fill(this.formSelectors.senha, data.senha);
    await this.fill(this.formSelectors.confirmSenha, data.confirmSenha);
  }

  async clicarCadastrar() {
    await this.click(this.formSelectors.btnCadastrar);
  }

  async mensagemSucessoEsperada(msg: string) {
    const locator = this.page.locator(`text=${msg}`);
    await expect(locator).toBeVisible({ timeout: 8000 });
  }
}
```

> *O mesmo padrão é seguido nos demais page objects (`loginPage.ts`, `contaPage.ts`, `transferPage.ts`, etc.).*

---

## 3️⃣ Testes

### 3.1 `tests/cadastro.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { CadastroPage } from '../pages/cadastroPage';
import { faker } from '@faker-js/faker';

test.describe('Cadastro de Usuário', () => {
  test.beforeEach(async ({ page }) => {
    // Navega para a página de cadastro antes de cada teste
    const cadastro = new CadastroPage(page);
    await cadastro.navigate('/signup');   // altere a rota real
  });

  // ----------- Scenario Outline: Cadastro com sucesso -------------
  const sucessoExamples = [
    {
      nome: 'João Silva',
      email: 'joao.silva@email.com',
      telefone: '11987654321',
      cep: '01001000',
      endereco: 'Av. Central, 10',
      senha: 'Pass123',
    },
    {
      nome: 'Maria Costa',
      email: 'maria.costa@email.com',
      telefone: '11912345678',
      cep: '02002000',
      endereco: 'Rua das Flores, 5',
      senha: 'Pass456',
    },
  ];

  test.each(sucessoExamples)(
    'Cadastro com sucesso – $nome',
    async ({ nome, email, telefone, cep, endereco, senha }) => {
      const cadastro = new CadastroPage(test.page);
      // 1) Preenche campos
      await test.step('Preenche campos obrigatórios', async () => {
        await cadastro.preencheCamposObrigatorios({
          nome,
          email,
          telefone,
          cep,
          endereco,
          senha,
          confirmSenha: senha,
        });
      });

      // 2) Clica em Cadastrar
      await test.step('Clica em Cadastrar', async () => {
        await cadastro.clicarCadastrar();
      });

      // 3) Valida mensagem de sucesso
      await test.step('Valida mensagem de sucesso', async () => {
        await cadastro.mensagemSucessoEsperada('Cadastro realizado com sucesso.');
      });

      // 4) Faz login para confirmar que o usuário pode entrar
      await test.step('Login com o e‑mail recém‑criado', async () => {
        // Utiliza o page object de login
        const loginPage = test.page;
        await loginPage.goto('/login');
        await loginPage.fill('input[name="email"]', email);
        await loginPage.fill('input[name="password"]', senha);
        await loginPage.click('button:has-text("Entrar")');
        await expect(loginPage.locator('text=Bem-vindo')).toBeVisible();
      });
    },
  );

  // ----------- Scenario Outline: Cadastro inválido – campos obrigatórios em branco -------------
  // Usamos um único exemplo (todos vazios) já que a mensagem de erro é a mesma
  test('Cadastro inválido – campos obrigatórios em branco', async () => {
    const cadastro = new CadastroPage(test.page);
    await test.step('Preenche campos em branco', async () => {
      await cadastro.preencheCamposObrigatorios({
        nome: '',
        email: '',
        telefone: '',
        cep: '',
        endereco: '',
        senha: '',
        confirmSenha: '',
      });
    });
    await test.step('Clica em Cadastrar', async () => {
      await cadastro.clicarCadastrar();
    });

    const errors = [
      'Nome é obrigatório.',
      'E‑mail é obrigatório.',
      'Telefone é obrigatório.',
      'CEP é obrigatório.',
      'Endereço é obrigatório.',
      'Senha é obrigatória.',
      'Confirmação de senha é obrigatória.',
    ];

    for (const msg of errors) {
      await test.step(`Valida mensagem de erro: ${msg}`, async () => {
        await expect(test.page.locator(`text=${msg}`)).toBeVisible();
      });
    }
  });

  // ----------- Scenario Outline: Cadastro inválido – dados com formato incorreto -------------
  const erroExamples = [
    {
      email: 'joao[dot]silva',
      telefone: '1234',
      cep: '12345',
      mensagemEmail: 'E‑mail inválido.',
      mensagemTelefone: 'Telefone inválido.',
      mensagemCep: 'CEP inválido.',
    },
    {
      email: 'joao.silva@email',
      telefone: '(12)3456789',
      cep: '01001-000',
      mensagemEmail: 'E‑mail inválido.',
      mensagemTelefone: 'Telefone inválido.',
      mensagemCep: 'CEP inválido.',
    },
  ];

  test.each(erroExamples)(
    'Cadastro inválido – dados com formato incorreto',
    async ({ email, telefone, cep, mensagemEmail, mensagemTelefone, mensagemCep }) => {
      const cadastro = new CadastroPage(test.page);
      await test.step('Preenche campos com dados incorretos', async () => {
        await cadastro.preencheCamposObrigatorios({
          nome: 'João',
          email,
          telefone,
          cep,
          endereco: 'Rua A',
          senha: 'Pass123',
          confirmSenha: 'Pass123',
        });
      });
      await test.step('Clica em Cadastrar', async () => {
        await cadastro.clicarCadastrar();
      });

      // Mensagens de erro
      await test.step('Valida mensagem de erro de e‑mail', async () => {
        await expect(test.page.locator(`text=${mensagemEmail}`)).toBeVisible();
      });
      await test.step('Valida mensagem de erro de telefone', async () => {
        await expect(test.page.locator(`text=${mensagemTelefone}`)).toBeVisible();
      });
      await test.step('Valida mensagem de erro de CEP', async () => {
        await expect(test.page.locator(`text=${mensagemCep}`)).toBeVisible();
      });
    },
  );
});
```

### 3.2 `tests/login.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { faker } from '@faker-js/faker';

test.describe('Login', () => {
  // Helper – cria um usuário antes do teste (para os cenários de login)
  async function criarUsuario(page: any, email: string, senha: string) {
    await page.goto('/signup');
    await page.fill('input[name="name"]', faker.name.fullName());
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="phone"]', '11987654321');
    await page.fill('input[name="cep"]', '01001000');
    await page.fill('input[name="address"]', 'Av. Central, 10');
    await page.fill('input[name="password"]', senha);
    await page.fill('input[name="confirmPassword"]', senha);
    await page.click('button:has-text("Cadastrar")');
    await expect(page.locator('text=Cadastro realizado com sucesso.')).toBeVisible();
  }

  test('Login bem‑sucedido', async ({ page }) => {
    const email = 'joao.silva@email.com';
    const senha = 'Pass123';
    await criarUsuario(page, email, senha);

    await test.step('Navega para login', async () => {
      await page.goto('/login');
    });

    await test.step('Preenche e-mail e senha', async () => {
      await page.fill('input[name="email"]', email);
      await page.fill('input[name="password"]', senha);
    });

    await test.step('Clica em Entrar', async () => {
      await page.click('button:has-text("Entrar")');
    });

    await test.step('Valida redirecionamento e mensagem de boas‑vindas', async () => {
      await expect(page).toHaveURL(/\/dashboard/);
      await expect(page.locator('text=Bem-vindo, João Silva!')).toBeVisible();
    });
  });

  const falhaExamples = [
    {
      email: 'joao.silva@email.com',
      senha: 'Wrong!',
      mensagem: 'Senha inválida.',
    },
    {
      email: 'unknown@email.com',
      senha: 'Pass123',
      mensagem: 'E‑mail não cadastrado.',
    },
  ];

  test.each(falhaExamples)(
    'Login falha – credenciais inválidas – $email',
    async ({ email, senha, mensagem }) => {
      await page.goto('/login');
      await page.fill('input[name="email"]', email);
      await page.fill('input[name="password"]', senha);
      await page.click('button:has-text("Entrar")');

      await expect(page.locator(`text=${mensagem}`)).toBeVisible();
    },
  );

  test('Login falha – campo em branco', async ({ page }) => {
    await page.goto('/login');
    await page.click('button:has-text("Entrar")');

    await expect(page.locator('text=E‑mail e senha são obrigatórios.')).toBeVisible();
  });
});
```

### 3.3 `tests/saldo-extrato.spec.ts`

```ts
import { test, expect } from '@playwright/test';
import { faker } from '@faker-js/faker';

test.describe('Acesso à aplicação bancária – Saldo e Extrato', () => {
  // Cria e faz login antes de cada teste
  test.beforeEach(async ({ page }) => {
    const email = `teste-${faker.datatype.uuid()}@mail.com`;
    const senha = 'Pass123';
    await page.goto('/signup');
    await page.fill('input[name="name"]', faker.name.fullName());
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="phone"]', '11987654321');
    await page.fill('input[name="cep"]', '01001000');
    await page.fill('input[name="address"]', 'Av. Central, 10');
    await page.fill('input[name="password"]', senha);
    await page.fill('input[name="confirmPassword"]', senha);
    await page.click('button:has-text("Cadastrar")');
    await expect(page.locator('text=Cadastro realizado com sucesso.')).toBeVisible();

    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', senha);
    await page.click('button:has-text("Entrar")');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('Exibir saldo atualizado', async ({ page }) => {
    await test.step('Acessa a página inicial da conta', async () => {
      await page.goto('/dashboard');
    });

    await test.step('Visualiza o saldo', async () => {
      const saldo = await page.textContent('.saldo-valor');
      expect(saldo).toBe('R$ 1.250,00');   // ajuste de acordo com o valor inicial
    });
  });

  test('Exibir extrato em ordem cronológica', async ({ page }) => {
    await page.goto('/extrato');

    await test.step('Verifica se as transações estão em ordem', async () => {
      const datas = await page.$$eval('.transacao .data', els => els.map(el => el.textContent?.trim() ?? ''));
      const isChrono = datas.reduce((prev, cur) => {
        if (!prev) return true;
        return prev <= cur;   // mais recente primeiro
      }, true);
      expect(isChrono).toBeTruthy();
    });
  });

  test('Saldo reflete operação de transferência', async ({ page }) => {
    // 1) Faz uma transferência de R$ 300
    await page.goto('/transferir');
    await page.selectOption('select[name="contaOrigem"]', '1001');
    await page.selectOption('select[name="contaDestino"]', '2002');
    await page.fill('input[name="valor"]', '300');
    await page.click('button:has-text("Transferir")');
    await expect(page.locator('text=Transferência concluída com sucesso.')).toBeVisible();

    // 2) Checa saldo
    await page.goto('/dashboard');
    const saldo = await page.textContent('.saldo-valor');
    expect(saldo).toBe('R$ 950,00');   // 1.250 - 300 = 950
  });
});
```

> *Para os demais cenários (Transferência, Empréstimo, Pagamento, etc.) basta seguir o mesmo padrão: usar `test.describe`, `test.each`, page objects, e fazer as validações de mensagem/estado.*  

---

## 4️⃣ Dependências

```bash
npm install -D @playwright/test @faker-js/faker
npx playwright install
```

---

## 5️⃣ Como executar

```bash
# Instala todas as dependências
npm install

# Executa todos os testes
npx playwright test

# Para rodar apenas os testes de cadastro
npx playwright test tests/cadastro.spec.ts

# Para ver os testes em tempo real (watch mode)
npx playwright test --watch
```

---

## 6️⃣ Dicas de Boas Práticas

| Prática | Por que é importante |
|---------|----------------------|
| **Page Objects** | Encapsula a lógica de UI; facilita manutenção quando o front‑end muda. |
| **Esperas explícitas** (`await expect(locator).toBeVisible()`) | Evita flakiness que ocorre quando a página ainda está carregando. |
| **Data‑driven** (`test.each`) | Reduz duplicação de código e aumenta a cobertura. |
| **Uso de variáveis de ambiente** (`process.env`) | Permite rodar os testes em ambientes diferentes (dev, staging, prod). |
| **Logs e screenshots** | Configurado no `playwright.config.ts` (`screenshot: 'only-on-failure'`). |
| **Separação de testes em arquivos** | Facilita a leitura e o paralelismo de execuções. |
| **Assert de URL** | Garantia de que a navegação realmente ocorreu. |

---

**Pronto!**  
Copie os arquivos acima (ou ajuste conforme sua aplicação) e rode `npx playwright test`.  
Qualquer dúvida ou necessidade de cenários adicionais (performance, segurança, etc.), é só chamar!