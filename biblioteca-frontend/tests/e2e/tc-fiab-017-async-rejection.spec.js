// @ts-check
const { test, expect } = require('@playwright/test');
const { login } = require('./helpers');
const { LECTOR } = require('./fixtures');

/**
 * TC-FIAB-017 — Transición de promesa async en frontend [defecto-conocido]
 *
 * Sub-característica (ISO/IEC 25010): Tolerancia a Fallos.
 * Métrica: M-05 (manejo de fallos de red). Suite: defecto-conocido (informativa).
 * Técnica (29119): transición de estados sobre una promesa async.
 * Trazabilidad: TCI-T4.1 · WT-03 / INC-WT-03. Especificación: TCS-FIAB-001 §5.
 *
 * Automatiza el caso que hasta ahora se ejecutaba a mano con DevTools
 * (sqa/fase2/dinamicas/tc-fiab-017-evidencia.md). `cargarAmonestaciones` en
 * SolicitudVerificacionPago.vue no tiene bloque catch y `onMounted` la invoca
 * sin await ni .catch: cuando la petición de red falla, el rechazo queda sin
 * manejar y el usuario no recibe ningún mensaje. Este test DOCUMENTA ese
 * defecto observando exactamente ese comportamiento; no lo corrige.
 */
test('TC-FIAB-017: el rechazo de promesa por fallo de red queda sin manejar', async ({ page }) => {
  const rechazosSinManejar = [];
  page.on('pageerror', (error) => rechazosSinManejar.push(error.message));

  await login(page, LECTOR);

  // Simula la pérdida de red durante la promesa: la petición se aborta.
  await page.route('**/api/amonestaciones-usuario/mis-amonestaciones', (route) =>
    route.abort(),
  );

  await page.getByRole('button', { name: 'Solicitar verificar Pago' }).click();

  // Comportamiento documentado (defecto): el rechazo aflora como error no
  // capturado en la página.
  await expect
    .poll(() => rechazosSinManejar.length, {
      message: 'Se esperaba un rechazo de promesa sin manejar tras el fallo de red',
    })
    .toBeGreaterThan(0);

  // Y el usuario no recibe ninguna señal del fallo: no hay texto de error rojo.
  await expect(page.locator('p.text-red-600')).toHaveCount(0);
});
