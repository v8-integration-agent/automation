import { test, expect } from '@playwright/test';

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
