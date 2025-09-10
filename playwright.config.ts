import { defineConfig, devices } from '@playwright/test';
import fs from "fs";

export default defineConfig({
  testDir: './tests',
  timeout: 10_000,
  retries: 0,
  reporter: [
    ['list'],
    ['json', { outputFile: 'report.json' }],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  use: {
    headless: true,
    baseURL: process.env.BASE_URL || 'https://parabank.parasoft.com/parabank',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } }
  ]
});
