// @ts-check
const { test, expect } = require('@playwright/test');
const { login } = require('./helpers');
const { BIBLIOTECARIO, LECTOR, LIBRO } = require('./fixtures');

/**
 * TC-FIAB-043 — Ciclo operativo de préstamo por interfaz (camino feliz)
 *
 * Sub-característica (ISO/IEC 25010): Madurez.
 * Métrica: M-01 (densidad de fallas en operación normal), M-03.
 * Suite: regresion (gate). Técnica (29119): escenario operativo end-to-end.
 * Especificación: TCS-FIAB-001 §5.
 *
 * Verifica que un BIBLIOTECARIO puede registrar y luego devolver un préstamo
 * accionando la interfaz Vue contra el backend real, sin fallas de integración.
 * Es el equivalente por UI de TC-FIAB-020 (que cubre el mismo flujo a nivel
 * sistema con MockMvc): aquí lo que se prueba es que el frontend efectivamente
 * se conecta al backend y completa el ciclo — nivel de aceptación.
 */
test('TC-FIAB-043: registrar y devolver un préstamo desde la interfaz', async ({ page }) => {
  await login(page, BIBLIOTECARIO);

  // --- Registrar el préstamo -------------------------------------------------
  await page.getByRole('button', { name: 'Añadir Préstamo' }).click();
  await expect(page.getByRole('heading', { name: 'Registrar Nuevo Préstamo' })).toBeVisible();

  await page.getByPlaceholder('usuario@email.com').fill(LECTOR.correo);
  await page.getByPlaceholder('ISBN').fill(String(LIBRO.isbn));
  await page.getByRole('button', { name: 'Registrar Préstamo' }).click();

  // El backend responde "Préstamo registrado..." y el componente lo pinta en verde.
  const mensajePrestamo = page.getByText(/Préstamo registrado/i);
  await expect(mensajePrestamo).toBeVisible();
  await expect(mensajePrestamo).toHaveClass(/text-green-600/);

  // --- Devolver el préstamo --------------------------------------------------
  await page.getByRole('button', { name: 'Devolver Préstamo' }).click();
  await expect(page.getByRole('heading', { name: 'Devolución de Préstamos' })).toBeVisible();

  // El préstamo recién creado aparece como activo, con su botón de devolución.
  const tarjeta = page.locator('div', { hasText: LIBRO.titulo }).filter({
    has: page.getByRole('button', { name: 'Registrar Devolución' }),
  }).last();
  await expect(tarjeta).toBeVisible();
  await tarjeta.getByRole('button', { name: 'Registrar Devolución' }).click();

  // Devolución dentro del plazo: éxito, sin amonestación por mora.
  const mensajeDevolucion = page.locator('p.text-green-600');
  await expect(mensajeDevolucion).toBeVisible();
});
