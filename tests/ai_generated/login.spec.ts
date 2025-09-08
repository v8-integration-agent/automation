import { test, expect } from '@playwright/test';

const HOME = 'parabank.parasoft.com';

async function openHome(page) {
  await page.goto(HOME);
  await expect(page.getByRole('heading', { name: 'ParaBank' })).toBeVisible();
}

test.describe('Login no Parabank', () => {
  test('Login inválido', async ({ page, baseURL }) => {
    await openHome(page);
    await page.getByLabel('Username').fill('invalid');
    await page.getByLabel('Password').fill('invalid');
    await page.getByRole('button', { name: 'Log In' }).click();
    await expect(page.getByText('could not be verified')).toBeVisible();
  });

  test('Login válido', async ({ page }) => {
    const user = "john";
    const pass = "demo";
    await openHome(page);
    await page.getByLabel('Username').fill(user);
    await page.getByLabel('Password').fill(pass);
    await page.getByRole('button', { name: 'Log In' }).click();
    await expect(page.getByRole('heading', { name: 'Accounts Overview' })).toBeVisible();
  });
});