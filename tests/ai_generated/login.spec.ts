import { test, expect } from '../helpers/fixtures';
import * as fs from 'fs';

const HOME = 'https://parabank.parasoft.com/parabank/index.htm';

const LoginLocators = {
  usernameInput: 'input[name="username"]',
  passwordInput: 'input[name="password"]',
  loginButton: 'input[value="Log In"]',
  welcomeMessage: '#leftPanel > p',
  errorMessage: '.error',
};

async function openHome(page) {
  await page.goto(HOME, { waitUntil: 'domcontentloaded' });
  await expect(page.locator(LoginLocators.usernameInput)).toBeVisible();
}

test.afterEach(async ({}, testInfo) => {
  if (testInfo.status !== 'passed') {
    fs.appendFileSync('erros.txt', `${new Date().toISOString()} - ${testInfo.title} falhou\n`);
    if (testInfo.error) {
      fs.appendFileSync('erros.txt', `${testInfo.error.message}\n\n`);
    }
  }
});

test.describe('Login no Parabank', () => {
  test('Login inválido', async ({ page }) => {
    await openHome(page);

    await page.locator(LoginLocators.usernameInput).fill('john');
    await page.locator(LoginLocators.passwordInput).fill('senhaErrada');
    await page.locator(LoginLocators.loginButton).click();

    await expect(page.locator(LoginLocators.errorMessage)).toContainText(
      'An internal error has occurred and has been logged.'
    );
  });

  test('Login válido', async ({ page }) => {
    await openHome(page);

    await page.locator(LoginLocators.usernameInput).fill('john');
    await page.locator(LoginLocators.passwordInput).fill('demo');
    await page.locator(LoginLocators.loginButton).click();

    await expect(page.locator(LoginLocators.welcomeMessage)).toContainText('Welcome');
  });
});
