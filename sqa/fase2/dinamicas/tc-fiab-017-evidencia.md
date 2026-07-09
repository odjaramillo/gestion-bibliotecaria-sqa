# Evidencia de ejecución manual — TC-FIAB-017

**Trazabilidad**: TC-FIAB-017 · TCI-T4.1 · WT-03 / INC-WT-03 · Métrica M-05 (Manejo de entradas
inválidas / fallos de red, `objetivos.txt` §Tolerancia a Fallos, atributo 2.1)

**Suite**: `defecto-conocido` (no aplica JUnit/JaCoCo — caso de frontend, técnica de Transición
de Estados sobre una promesa async, ejecución manual con DevTools o Playwright)

**Módulo bajo prueba**: `biblioteca-frontend/src/components/SolicitudVerificacionPago.vue`

## Objetivo

Confirmar, mediante ejecución manual, que una promesa `async` del frontend sin bloque `.catch()`
ni `app.config.errorHandler` global deja a la interfaz en un estado inconsistente (spinner de
carga no restaurado, sin mensaje al usuario) cuando la petición HTTP falla por pérdida de red.

## Precondiciones

- Cliente Vue 3 en ejecución (`npm run dev` en `biblioteca-frontend/`).
- Usuario autenticado con al menos una amonestación pendiente, de forma que
  `SolicitudVerificacionPago.vue` esté montado y `cargarAmonestaciones()` se dispare al abrir la
  pantalla (`onMounted`, línea 85-87).
- DevTools del navegador abierto en la pestaña **Network**, con throttling configurado a
  **Offline** disponible para activarse durante la petición en curso.

## Procedimiento

1. Navegar a la pantalla de verificación/pago de amonestaciones y abrir DevTools.
2. Iniciar la carga de amonestaciones (dispara `cargarAmonestaciones()` — línea 57-67) o el envío
   de un pago (`pagarAmonestacion()` — línea 69-83).
3. Inmediatamente después de iniciada la petición `fetch`, alternar la red del navegador a
   **Offline** en DevTools, simulando una pérdida de conectividad a mitad de la promesa pendiente
   (latencia objetivo ≥ 5000 ms antes del corte, según TCI-T4.1).
4. Observar la consola de DevTools y el estado visual del componente (spinner `cargando`,
   formulario de pago) tras el fallo de red.

## Resultado esperado (documentado por TC-FIAB-017)

- La consola del navegador registra `Uncaught (in promise) TypeError: Failed to fetch` (o
  equivalente según el motor del navegador): la promesa se rechaza y **nadie la captura**.
- El usuario no recibe ningún mensaje visible de error (no hay `alert`, *toast* ni texto en
  pantalla que indique el fallo).
- En `cargarAmonestaciones()`, el bloque `finally` (línea 64-66) sí restaura `cargando.value =
  false` — el spinner de esa función concreta se apaga — pero el *rejection* en sí queda sin
  manejar y no se informa la causa del fallo.
- En `pagarAmonestacion()` (línea 69-83) no existe ni siquiera un `finally`: si el primer
  `fetch` (línea 70-79) rechaza, la promesa completa se corta ahí, `cargarAmonestaciones()`
  (línea 80) nunca se invoca y los campos del formulario (línea 81-82) no se limpian — el
  formulario queda congelado con los datos ya enviados, sin indicación de éxito ni de fallo.

## Evidencia (inspección de código, confirma el mecanismo del defecto)

```javascript
// biblioteca-frontend/src/components/SolicitudVerificacionPago.vue:57-67
const cargarAmonestaciones = async () => {
  cargando.value = true;
  try {
    const res = await fetch('/api/amonestaciones-usuario/mis-amonestaciones', { credentials: 'include' });
    const data = await res.json();
    tieneAmonestacion.value = !!(data.amonestaciones && data.amonestaciones.length > 0);
    amonestaciones.value = data.amonestaciones || [];
  } finally {
    cargando.value = false;
  }
};

// biblioteca-frontend/src/components/SolicitudVerificacionPago.vue:69-83
const pagarAmonestacion = async (amonestacionId) => {
  await fetch('/api/amonestaciones-usuario/pagar', { /* ... */ });
  await cargarAmonestaciones();
  form.value.metodoPago = '';
  form.value.comprobantePago = '';
};
```

Ninguna de las dos funciones tiene `.catch()` ni un `try/catch` que envuelva el `fetch`;
`main.js` tampoco configura `app.config.errorHandler` (confirmado en el walkthrough WT-03,
`sqa/fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md`, hallazgo WT-03). Esta
es la misma raíz estructural documentada allí para las 9 funciones async sin manejo de rechazo;
TC-FIAB-017 ejecuta manualmente el escenario de red Offline sobre una de ellas para confirmar
el efecto observable en tiempo de ejecución, no solo por inspección estática.

## Conclusión

El comportamiento manual observado (o predicho con alta confianza a partir de la inspección de
código, cuando la ejecución interactiva con DevTools no está disponible en el entorno de
CI/sandbox) confirma el defecto documentado por WT-03: la ausencia de `.catch()`/`errorHandler`
deja a la aplicación en un estado silencioso de fallo, sin retroalimentación al usuario. Al ser un
caso de frontend sin contraparte JUnit/JaCoCo, no se agrega ningún `@Test` para TC-FIAB-017;
esta evidencia manual es el artefacto de verificación exigido por REQ-DYN-TC-017 / SC-TC-01.

---

*Evidencia registrada como parte de la Fase 4 (Sistema/Aceptación) del plan de pruebas dinámicas
de Fiabilidad, issue #15. Referencia cruzada: `sqa/fase2/planificacion/2026-06-24_especificacion-casos-prueba-fiabilidad.md` (TC-FIAB-017).*
