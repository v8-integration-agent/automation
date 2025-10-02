**`pbank.spec.ts`** – Test‑suite completo (Playwright Test + TypeScript)  
```ts
// ==========================================================================
//  pbank.spec.ts
//  Playwright Test Runner – Automação dos cenários BDD em Português
// ==========================================================================

import { test, expect, Page, Locator } from '@playwright/test';

/**
 * --------------------------------------------------------------------------
 *  Helpers (Page Object – simplificados)
 * --------------------------------------------------------------------------
 */

/**
 * Encapsula a página de cadastro
 */
class RegisterPage {
  constructor(public page: Page) {}

  // Selectors
  readonly inputNome = this.page.locator('input[name="nome"]');
  readonly inputEmail = this.page.locator('input[name="email"]');
  readonly inputTelefone = this.page.locator('input[name="telefone"]');
  readonly inputCep = this.page.locator('input[name="cep"]');
  readonly inputEndereco = this.page.locator('input[name="endereco"]');
  readonly inputCidade = this.page.locator('input[name="cidade"]');
  readonly inputEstado = this.page.locator('input[name="estado"]');
  readonly inputSenha = this.page.locator('input[name="senha"]');
  readonly inputConfirmSenha = this.page.locator('input[name="confirmacaoSenha"]');
  readonly btnCadastrar = this.page.locator('button:has-text("Cadastrar")');
  readonly msg = this.page.locator('.alert');          // ex.: <div class="alert">Registro concluído</div>

  async navigate() {
    await this.page.goto('https://example.com/register');
  }

  /** Preenche os campos obrigatórios a partir de um objeto */
  async fillMandatoryFields(fields: Record<string, string>) {
    for (const [key, value] of Object.entries(fields)) {
      switch (key) {
        case 'nome': await this.inputNome.fill(value); break;
        case 'email': await this.inputEmail.fill(value); break;
        case 'telefone': await this.inputTelefone.fill(value); break;
        case 'cep': await this.inputCep.fill(value); break;
        case 'endereço': await this.inputEndereco.fill(value); break;
        case 'cidade': await this.inputCidade.fill(value); break;
        case 'estado': await this.inputEstado.fill(value); break;
        case 'senha': await this.inputSenha.fill(value); break;
        case 'confirmaçãoSenha': await this.inputConfirmSenha.fill(value); break;
      }
    }
  }

  async clickCadastrar() {
    await this.btnCadastrar.click();
  }

  async getMessage() : Promise<string> {
    await this.msg.waitFor({ state: 'visible' });
    return this.msg.textContent() ?? '';
  }
}

/**
 * Encapsula a página de login
 */
class LoginPage {
  constructor(public page: Page) {}

  readonly inputUsuario = this.page.locator('input[name="usuario"]');
  readonly inputSenha = this.page.locator('input[name="senha"]');
  readonly btnEntrar = this.page.locator('button:has-text("Entrar")');
  readonly msg = this.page.locator('.alert');

  async navigate() {
    await this.page.goto('https://example.com/login');
  }

  async login(usuario: string, senha: string) {
    await this.inputUsuario.fill(usuario);
    await this.inputSenha.fill(senha);
    await this.btnEntrar.click();
  }

  async getMessage() : Promise<string> {
    await this.msg.waitFor({ state: 'visible' });
    return this.msg.textContent() ?? '';
  }

  /** Espera redirecionamento para a dashboard – simplificação */
  async waitForDashboard() {
    await this.page.waitForURL('**/dashboard');
  }
}

/**
 * Encapsula a página de transferências
 */
class TransferPage {
  constructor(public page: Page) {}

  readonly inputContaDestino = this.page.locator('input[name="contaDestino"]');
  readonly inputValor = this.page.locator('input[name="valor"]');
  readonly btnTransferir = this.page.locator('button:has-text("Transferir")');
  readonly btnConfirmar = this.page.locator('button:has-text("Confirmar")');
  readonly msg = this.page.locator('.alert');

  async navigate() {
    await this.page.goto('https://example.com/transfer');
  }

  async transferir(conta: string, valor: number) {
    await this.inputContaDestino.fill(conta);
    await this.inputValor.fill(valor.toString());
    await this.btnTransferir.click();
    await this.btnConfirmar.click();
  }

  async getMessage() : Promise<string> {
    await this.msg.waitFor({ state: 'visible' });
    return this.msg.textContent() ?? '';
  }
}

/**
 * Encapsula a página de empréstimos
 */
class LoanPage {
  constructor(public page: Page) {}

  readonly inputValor = this.page.locator('input[name="valor"]');
  readonly inputRenda = this.page.locator('input[name="rendaAnual"]');
  readonly btnSolicitar = this.page.locator('button:has-text("Solicitar")');
  readonly msg = this.page.locator('.alert');

  async navigate() {
    await this.page.goto('https://example.com/loan');
  }

  async solicitar(valor: number, renda: number) {
    await this.inputValor.fill(valor.toString());
    await this.inputRenda.fill(renda.toString());
    await this.btnSolicitar.click();
  }

  async getMessage() : Promise<string> {
    await this.msg.waitFor({ state: 'visible' });
    return this.msg.textContent() ?? '';
  }
}

/**
 * Encapsula a página de pagamento
 */
class PaymentPage {
  constructor(public page: Page) {}

  readonly inputBeneficiario = this.page.locator('input[name="beneficiario"]');
  readonly inputEndereco = this.page.locator('input[name="endereco"]');
  readonly inputCidade = this.page.locator('input[name="cidade"]');
  readonly inputEstado = this.page.locator('input[name="estado"]');
  readonly inputCep = this.page.locator('input[name="cep"]');
  readonly inputTelefone = this.page.locator('input[name="telefone"]');
  readonly inputContaDestino = this.page.locator('input[name="contaDestino"]');
  readonly inputValor = this.page.locator('input[name="valor"]');
  readonly inputData = this.page.locator('input[name="data"]');
  readonly btnConfirmar = this.page.locator('button:has-text("Confirmar")');
  readonly msg = this.page.locator('.alert');

  async navigate() {
    await this.page.goto('https://example.com/payment/new');
  }

  async cadastrarPagamento(dados: {
    beneficiario: string,
    endereco: string,
    cidade: string,
    estado: string,
    cep: string,
    telefone: string,
    conta: string,
    valor: number,
    data: string
  }) {
    await this.inputBeneficiario.fill(dados.beneficiario);
    await this.inputEndereco.fill(dados.endereco);
    await this.inputCidade.fill(dados.cidade);
    await this.inputEstado.fill(dados.estado);
    await this.inputCep.fill(dados.cep);
    await this.inputTelefone.fill(dados.telefone);
    await this.inputContaDestino.fill(dados.conta);
    await this.inputValor.fill(dados.valor.toString());
    await this.inputData.fill(dados.data);
    await this.btnConfirmar.click();
  }

  async getMessage() : Promise<string> {
    await this.msg.waitFor({ state: 'visible' });
    return this.msg.textContent() ?? '';
  }
}

/**
 * Encapsula a página de navegação (menu)
 */
class NavigationPage {
  constructor(public page: Page) {}

  readonly menuLinks = this.page.locator('.main-menu a');   // todos os links do menu principal

  /** Navega para todas as páginas do sistema e verifica carregamento */
  async verifyAllPages() {
    const hrefs = await this.menuLinks.evaluateAll(nodes => nodes.map(n => (n as HTMLAnchorElement).href));
    for (const href of hrefs) {
      await this.page.goto(href);
      await this.page.waitForLoadState('domcontentloaded');
      // Verifica se não há mensagens de erro (ex.: <div class="error">...)
      const errorMsg = await this.page.locator('.error').count();
      expect(errorMsg).toBe(0);
    }
  }

  /** Garante que todos os links estão presentes em todas as páginas */
  async verifyMenuConsistency() {
    const hrefs = await this.menuLinks.evaluateAll(nodes => nodes.map(n => (n as HTMLAnchorElement).href));
    for (const href of hrefs) {
      await this.page.goto(href);
      const linkText = await this.page.locator(`a[href="${href}"]`).textContent();
      expect(linkText).not.toBeNull();
      await this.page.goBack();
    }
  }
}

/**
 * --------------------------------------------------------------------------
 *  Test Suite – Cenários BDD
 * --------------------------------------------------------------------------
 */

test.describe('Cadastro de Usuário', () => {
  const register = (page: Page) => new RegisterPage(page);

  test('Cadastro bem-sucedido', async ({ page }) => {
    const r = register(page);
    await r.navigate();

    // Dados de exemplo (conforme tabela Examples)
    const fields = {
      nome: 'João Silva',
      email: 'joao.silva@example.com',
      telefone: '9999999999',
      cep: '12345678',
      endereço: 'Rua A, 123',
      cidade: 'São Paulo',
      estado: 'SP',
      senha: 'senha123',
      confirmaçãoSenha: 'senha123'
    };

    await r.fillMandatoryFields(fields);
    await r.clickCadastrar();

    const msg = await r.getMessage();
    expect(msg).toContain('Registro concluído');

    // Pós‑cadastro: login automático (supondo redirecionamento)
    await r.page.waitForURL('**/dashboard');
  });

  test('Campos obrigatórios ausentes – exibir mensagem de campo obrigatório', async ({ page }) => {
    const r = register(page);
    await r.navigate();

    // Preenche apenas os campos obrigatórios *exceto* "endereço" e "cidade" (exemplo de falha)
    const fields = {
      nome: 'João Silva',
      email: 'joao.silva@example.com',
      telefone: '9999999999',
      cep: '12345678',
      senha: 'senha123',
      confirmaçãoSenha: 'senha123'
    };

    await r.fillMandatoryFields(fields);
    await r.clickCadastrar();

    const msg = await r.getMessage();
    expect(msg).toContain('O campo endereço é obrigatório');
  });

  test('Validação de dados inválidos – email inválido', async ({ page }) => {
    const r = register(page);
    await r.navigate();

    const fields = {
      nome: 'João Silva',
      email: 'invalido@exemplo', // sem domínio
      telefone: '9999999999',
      cep: '12345678',
      endereço: 'Rua A, 123',
      cidade: 'São Paulo',
      estado: 'SP',
      senha: 'senha123',
      confirmaçãoSenha: 'senha123'
    };

    await r.fillMandatoryFields(fields);
    await r.clickCadastrar();

    const msg = await r.getMessage();
    expect(msg).toContain('Email inválido');
  });
});

test.describe('Login', () => {
  const login = (page: Page) => new LoginPage(page);

  test('Login bem‑sucedido', async ({ page }) => {
    const l = login(page);
    await l.navigate();
    await l.login('joao.silva', 'senha123');
    await l.waitForDashboard();

    const currentURL = page.url();
    expect(currentURL).toMatch(/\/dashboard/);
  });

  test.describe('Login com credenciais inválidas', () => {
    const scenarios = [
      { usuario: 'joao.silva', senha: 'wrongpass' },
      { usuario: 'unknown', senha: 'senha123' },
      { usuario: '', senha: 'senha123' }
    ];

    for (const { usuario, senha } of scenarios) {
      test(`Credenciais inválidas – usuário="${usuario}", senha="${senha}"`, async ({ page }) => {
        const l = login(page);
        await l.navigate();
        await l.login(usuario, senha);

        const msg = await l.getMessage();
        expect(msg).toContain('Credenciais inválidas');
      });
    }
  });
});

test.describe('Acesso à Conta (Saldo e Extrato)', () => {
  const login = (page: Page) => new LoginPage(page);

  // Antes de cada teste, o usuário já estará logado
  test.beforeEach(async ({ page }) => {
    const l = login(page);
    await l.navigate();
    await l.login('joao.silva', 'senha123');
    await l.waitForDashboard();
  });

  test('Exibição de saldo após operação', async ({ page }) => {
    // Assumimos que a dashboard exibe o saldo em um elemento específico
    const saldoAntes = await page.locator('#saldo').innerText(); // "$1000"
    const saldoNum = parseFloat(saldoAntes.replace(/[^\d.,]/g, '').replace(',', '.'));

    // Realiza transferência de $200 para conta X (id fictício "9999")
    await page.goto('https://example.com/transfer');
    await page.fill('input[name="contaDestino"]', '9999');
    await page.fill('input[name="valor"]', '200');
    await page.click('button:has-text("Transferir")');
    await page.click('button:has-text("Confirmar")');

    const saldoDepois = await page.locator('#saldo').innerText();
    const saldoNumDepois = parseFloat(saldoDepois.replace(/[^\d.,]/g, '').replace(',', '.'));
    expect(saldoNumDepois).toBeCloseTo(saldoNum - 200, 2);
  });

  test('Extrato em ordem cronológica', async ({ page }) => {
    await page.goto('https://example.com/statement');
    const rows = await page.locator('.transaction-row').all();
    const dates = await Promise.all(rows.map(row => row.locator('.date').innerText()));
    // Converte as strings para Date
    const parsedDates = dates.map(d => new Date(d));
    // Verifica se a lista está em ordem decrescente (mais recente no topo)
    for (let i = 0; i < parsedDates.length - 1; i++) {
      expect(parsedDates[i].getTime()).toBeGreaterThanOrEqual(parsedDates[i + 1].getTime());
    }
  });
});

test.describe('Transferência de Fundos', () => {
  const transfer = (page: Page) => new TransferPage(page);
  const login = (page: Page) => new LoginPage(page);

  test.beforeEach(async ({ page }) => {
    const l = login(page);
    await l.navigate();
    await l.login('joao.silva', 'senha123');
    await l.waitForDashboard();
  });

  test('Transferência com saldo suficiente', async ({ page }) => {
    const t = transfer(page);
    await t.navigate();

    // Supondo que o saldo já é de $500 na conta origem (configuração de teste)
    await t.transferir('1234', 200);

    const msg = await t.getMessage();
    expect(msg).toContain('Transferência realizada com sucesso');

    // Verifica débito e crédito em tabelas de histórico – simplificação
    const origemSaldo = await page.locator('#saldo-conta-origem').innerText();
    const destinoSaldo = await page.locator('#saldo-conta-destino').innerText();
    expect(parseFloat(origemSaldo.replace(/[^\d.,]/g, '').replace(',', '.'))).toBeCloseTo(300, 2);
    expect(parseFloat(destinoSaldo.replace(/[^\d.,]/g, '').replace(',', '.'))).toBeCloseTo(200, 2);
  });

  test.describe('Transferência com saldo insuficiente', () => {
    const scenarios = [
      { saldo: 100, valor: 200 },
      { saldo: 50, valor: 75 }
    ];

    for (const { saldo, valor } of scenarios) {
      test(`Saldo ${saldo} – tentativa de transferir ${valor}`, async ({ page }) => {
        const t = transfer(page);
        await t.navigate();

        // Simulamos o saldo com dados de teste (não há API real → usar fixture)
        await page.evaluate((s) => { window.localStorage.setItem('saldo', s); }, saldo.toString());

        await t.transferir('1234', valor);
        const msg = await t.getMessage();
        expect(msg).toContain('Saldo insuficiente');
      });
    }
  });
});

test.describe('Solicitação de Empréstimo', () => {
  const loan = (page: Page) => new LoanPage(page);
  const login = (page: Page) => new LoginPage(page);

  test.beforeEach(async ({ page }) => {
    const l = login(page);
    await l.navigate();
    await l.login('joao.silva', 'senha123');
    await l.waitForDashboard();
  });

  test.describe('Aprovação de empréstimo', () => {
    const scenarios = [
      { valor: 5000, renda: 70000 },
      { valor: 10000, renda: 120000 }
    ];

    for (const { valor, renda } of scenarios) {
      test(`Aprovação – valor ${valor}, renda ${renda}`, async ({ page }) => {
        const l = loan(page);
        await l.navigate();
        await l.solicitar(valor, renda);
        const msg = await l.getMessage();
        expect(msg).toContain('Aprovado');
      });
    }
  });

  test.describe('Negação de empréstimo', () => {
    const scenarios = [
      { valor: 20000, renda: 40000 },
      { valor: 15000, renda: 30000 }
    ];

    for (const { valor, renda } of scenarios) {
      test(`Negação – valor ${valor}, renda ${renda}`, async ({ page }) => {
        const l = loan(page);
        await l.navigate();
        await l.solicitar(valor, renda);
        const msg = await l.getMessage();
        expect(msg).toContain('Negado');
      });
    }
  });
});

test.describe('Pagamento de Contas', () => {
  const payment = (page: Page) => new PaymentPage(page);
  const login = (page: Page) => new LoginPage(page);

  test.beforeEach(async ({ page }) => {
    const l = login(page);
    await l.navigate();
    await l.login('joao.silva', 'senha123');
    await l.waitForDashboard();
  });

  test('Pagamento único', async ({ page }) => {
    const p = payment(page);
    await p.navigate();

    const dados = {
      beneficiario: 'Conta de Luz',
      endereco: 'Av. Paulista, 100',
      cidade: 'São Paulo',
      estado: 'SP',
      cep: '01001000',
      telefone: '11999999999',
      conta: '5678',
      valor: 120,
      data: '2025-12-01'
    };

    await p.cadastrarPagamento(dados);
    const msg = await p.getMessage();
    expect(msg).toContain(`$${dados.valor}`);
    expect(msg).toContain(dados.data);
  });

  test.describe('Pagamento futuro respeitando data agendada', () => {
    const scenarios = [
      { data: '2025-12-15', hoje: '2025-12-10' }
    ];

    for (const { data, hoje } of scenarios) {
      test(`Data agendada ${data} – hoje ${hoje}`, async ({ page }) => {
        // Simulamos a data atual via mock Date (Playwright não possui API direta)
        await page.evaluate(() => {
          const realDate = Date;
          // Override Date constructor
          globalThis.Date = function (...args: any[]) { return new realDate('2025-12-10'); } as any;
          globalThis.Date.now = () => new realDate('2025-12-10').getTime();
          globalThis.Date.UTC = realDate.UTC;
          globalThis.Date.parse = realDate.parse;
        });

        const p = payment(page);
        await p.navigate();

        // Preenche o pagamento futuro
        const dados = {
          beneficiario: 'Conta de Luz',
          endereco: 'Av. Paulista, 100',
          cidade: 'São Paulo',
          estado: 'SP',
          cep: '01001000',
          telefone: '11999999999',
          conta: '5678',
          valor: 120,
          data: data
        };

        await p.cadastrarPagamento(dados);

        const msg = await p.getMessage();
        expect(msg).toContain('Pagamento agendado para');
        expect(msg).toContain(data);
      });
    }
  });
});

test.describe('Navegação e Usabilidade', () => {
  const nav = (page: Page) => new NavigationPage(page);

  test('Carregamento de todas as páginas', async ({ page }) => {
    const n = nav(page);
    await n.verifyAllPages();
  });

  test('Consistência de menus e links', async ({ page }) => {
    const n = nav(page);
    await n.verifyMenuConsistency();
  });

  test('Clareza nas mensagens de erro', async ({ page }) => {
    const r = new RegisterPage(page);
    await r.navigate();

    // Faz uma ação inválida: preenche email inválido e tenta cadastrar
    await r.fillMandatoryFields({
      nome: 'João Silva',
      email: 'invalid',
      telefone: '9999999999',
      cep: '12345678',
      endereço: 'Rua A, 123',
      cidade: 'São Paulo',
      estado: 'SP',
      senha: 'senha123',
      confirmaçãoSenha: 'senha123'
    });

    await r.clickCadastrar();
    const msgEl = r.msg;
    await msgEl.waitFor({ state: 'visible' });

    // Verifica que a mensagem está em vermelho (ex.: CSS color = rgb(255,0,0))
    const color = await msgEl.evaluate(el => window.getComputedStyle(el).color);
    expect(color).toBe('rgb(255, 0, 0)');

    const text = await r.getMessage();
    expect(text).toContain('Email inválido');
  });
});
```

### Como usar

1. **Instalar dependências**  
   ```bash
   npm init -y
   npm i -D @playwright/test
   npx playwright install
   ```

2. **Estrutura de pastas**  
   ```
   ├─ tests
   │   └─ pbank.spec.ts          <-- arquivo acima
   ├─ playwright.config.ts      <-- configuração padrão do Playwright
   ```

3. **Configuração (playwright.config.ts)**  
   ```ts
   import { defineConfig } from '@playwright/test';

   export default defineConfig({
     testDir: 'tests',
     retries: 1,
     use: {
       baseURL: 'https://example.com',   // Substitua pela URL real do sistema
       viewport: { width: 1280, height: 720 },
       actionTimeout: 10000,
       trace: 'on-first-retry',
     },
   });
   ```

4. **Executar os testes**  
   ```bash
   npx playwright test
   ```

> **Observações**  
> • Os seletores (`input[name="..."]`, `.alert`, etc.) são exemplos; ajuste para os **seus** atributos reais.  
> • Para testes que dependem de estado do servidor (saldo, histórico, etc.) você pode usar *fixtures* ou *mocking* de APIs.  
> • O script acima já inclui *esperas implícitas* (`waitFor`, `waitForURL`) para garantir estabilidade.  
> • Comentários explicam cada passo, mantendo o código legível e fácil de manter.  

Pronto! Agora você tem um conjunto completo de testes automatizados que traduzem exatamente os cenários BDD do Gherkin para Playwright.