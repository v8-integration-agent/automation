import { test, expect } from '@playwright/test';
import * as fs from 'fs';

const HOME = 'https://parabank.parasoft.com/parabank/index.htm';

const LoginLocators = {
  usernameInput: 'input[name="username"]',
  passwordInput: 'input[name="password"]',
  loginButton: 'input[value="Log In"]',
 
};

const updateProfileLocators = {
  linkPerfil: '//*[@id="leftPanel"]/ul/li[6]/a',
  inputPhone: '//*[@id="customer.phoneNumber"]',
  botaoSalvar: '//*[@id="updateProfileForm"]/form/table/tbody/tr[8]/td[2]/input',
   phoneError: '//*[@id="phone-error"]'
};

test.afterEach(async ({}, testInfo) => {
  if (testInfo.status !== 'passed') {
    fs.appendFileSync('erros.txt', `${new Date().toISOString()} - ${testInfo.title} falhou\n`);
    if (testInfo.error) {
      fs.appendFileSync('erros.txt', `${testInfo.error.message}\n\n`);
    }
  }
});

async function acessarProfile(page) {
  await page.goto(HOME, { waitUntil: 'domcontentloaded' });
  await page.locator(LoginLocators.usernameInput).fill('john');   
  await page.locator(LoginLocators.passwordInput).fill('demo');
  await page.locator(LoginLocators.loginButton).click();
  await page.locator(updateProfileLocators.linkPerfil).click();
  await expect(page.locator(updateProfileLocators.inputPhone)).toBeVisible();
}

test.describe('Atualização de Telefone', () => {
  test('Usuário deve atualizar telefone com sucesso', async ({ page }) => {
    await acessarProfile(page);
    await page.fill(updateProfileLocators.inputPhone, "11999999999");
    const valorAtual = await page.inputValue(updateProfileLocators.inputPhone);
    expect(valorAtual).toBe("11999999999");
    await page.click(updateProfileLocators.botaoSalvar);;
  });

  test('Usuário deve atualizar telefone com campo vazio', async ({ page }) => {
    await acessarProfile(page);
    await page.fill(updateProfileLocators.inputPhone, "");
    await page.click(updateProfileLocators.botaoSalvar);
    await expect(page.locator(updateProfileLocators.phoneError)).toContainText('Phone is required.');
  });
});
