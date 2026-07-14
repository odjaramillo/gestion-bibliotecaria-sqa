// @ts-check
const { expect } = require('@playwright/test');

/**
 * Logs a user in through the UI (not the API): opens the login screen from the
 * header, fills the form and submits it. Waits for the authenticated header to
 * appear so callers can act on role-specific navigation right away.
 *
 * The app has no router; screens are swapped by a `currentComponent` ref, so
 * navigation is done by clicking header buttons, not by visiting URLs.
 */
async function login(page, { correo, contrasena }) {
  await page.goto('/');
  // Header button — unambiguous while the main screen is shown.
  await page.getByRole('button', { name: 'Iniciar Sesión' }).click();
  await page.locator('#email-address').fill(correo);
  await page.locator('#password').fill(contrasena);
  // The only type=submit button on the page is the login form's.
  await page.locator('button[type="submit"]').click();
  // The authenticated header greets every role with "Hola, <nombre>".
  await expect(page.getByText(/Hola,/)).toBeVisible();
}

module.exports = { login };
