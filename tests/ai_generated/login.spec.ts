import { test, expect } from '@playwright/test';

const HOME = '/parabank/index.htm';

export const LoginLocators = {
  usernameInput: '#loginPanel > form > div:nth-child(2) > input',
  passwordInput: '#loginPanel > form > div:nth-child(4) > input',
  loginButton: 'input[value="Log In"]',
  welcomeMessage: '#leftPanel > p',
};

async function openHome(page) {
  await page.goto(HOME);
  await expect(page.getByRole('heading', { name: 'ParaBank' })).toBeVisible();
}

test.describe('Login no Parabank', () => {
  test('Login inválido', async ({ page }) => {
    await openHome(page);

    await page.locator(LoginLocators.usernameInput).fill('invalid');
    await page.locator(LoginLocators.passwordInput).fill('invalid');
    await page.locator(LoginLocators.loginButton).click();

    await expect(page.getByText('could not be verified')).toBeVisible();
  });

  test('Login válido', async ({ page }) => {
    const user = 'john';
    const pass = 'demo';

    await openHome(page);

    await page.locator(LoginLocators.usernameInput).fill(user);
    await page.locator(LoginLocators.passwordInput).fill(pass);
    await page.locator(LoginLocators.loginButton).click();
  });
});
