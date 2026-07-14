// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Acceptance test configuration for the reliability layer (TCS-FIAB-001).
 *
 * These tests exercise the application from the end-user's perspective:
 * the Vue frontend driving the real Spring Boot backend, not the API in
 * isolation. This is the only test level that crosses the frontend/backend
 * boundary — see PACS.md §5.1.
 *
 * Ports:
 *   - Backend (Spring Boot)      : 8080  (its own default)
 *   - Frontend (vue-cli-service) : 5173  (pinned to avoid colliding with 8080,
 *                                         since vue-cli-service also defaults
 *                                         to 8080 and would silently shift)
 * The dev server proxies /api to the backend (see vue.config.js).
 *
 * Backend database: the tests expect MySQL reachable on localhost:3306 with
 * the credentials in src/main/resources/application.properties. In CI this is
 * a service container; locally it is a documented precondition.
 */

const FRONTEND_PORT = 5173;
const BACKEND_HEALTHCHECK = 'http://localhost:8080/api/libros';

module.exports = defineConfig({
  testDir: './tests/e2e',
  // Acceptance flows share seeded backend state, so run serially.
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { open: 'never' }]],

  // Seeds the BIBLIOTECARIO, the borrower and a book before any test runs.
  globalSetup: require.resolve('./tests/e2e/global-setup.js'),

  use: {
    baseURL: `http://localhost:${FRONTEND_PORT}`,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],

  webServer: [
    {
      // The repo carries two @SpringBootApplication classes; only
      // com.biblioteca.* wires the controllers and services. The stray
      // __1.spring_boot one makes spring-boot:run ambiguous, so the main class
      // is pinned here (test infra — the SUT is left untouched).
      command:
        './mvnw spring-boot:run -Dspring-boot.run.main-class=com.biblioteca.GestionBibliotecariaApplication',
      cwd: '..',
      url: BACKEND_HEALTHCHECK,
      reuseExistingServer: !process.env.CI,
      timeout: 180_000,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      command: `npm run serve -- --port ${FRONTEND_PORT}`,
      url: `http://localhost:${FRONTEND_PORT}`,
      reuseExistingServer: !process.env.CI,
      timeout: 180_000,
    },
  ],
});
