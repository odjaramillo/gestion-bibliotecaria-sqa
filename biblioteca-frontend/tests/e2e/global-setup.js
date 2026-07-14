// @ts-check
const { request } = require('@playwright/test');
const { BACKEND, BIBLIOTECARIO, LECTOR, LIBRO } = require('./fixtures');

/**
 * Seeds the backend before the acceptance suite runs.
 *
 * Order matters: the book endpoint (POST /api/libros) looks up correoUsuario
 * and rejects it unless that user has the BIBLIOTECARIO role, so the
 * bibliotecario must exist before the book is created.
 *
 * Registration is idempotent from the suite's point of view: the backend
 * answers "Correo ya registrado." on a repeat, which is harmless when the
 * MySQL volume survives between local runs. In CI the database is fresh.
 */
async function globalSetup() {
  const api = await request.newContext({ baseURL: BACKEND });

  await waitForBackend(api);

  await api.post('/api/usuarios/registro', { data: BIBLIOTECARIO });
  await api.post('/api/usuarios/registro', { data: LECTOR });

  // POST /api/libros is multipart: a JSON "libro" part plus a correoUsuario
  // field naming the acting bibliotecario. Mirrors RegistroLibro.vue.
  const libroResponse = await api.post('/api/libros', {
    multipart: {
      libro: {
        name: 'libro.json',
        mimeType: 'application/json',
        buffer: Buffer.from(JSON.stringify(LIBRO)),
      },
      correoUsuario: BIBLIOTECARIO.correo,
    },
  });

  const body = await libroResponse.text();
  const alreadyExists = body.includes('ya existe');
  if (!libroResponse.ok() && !alreadyExists) {
    throw new Error(
      `Seeding del libro falló (HTTP ${libroResponse.status()}): ${body}`,
    );
  }

  await api.dispose();
}

/**
 * Polls the backend health endpoint until it answers, independently of the
 * order in which Playwright brings up webServer and globalSetup.
 */
async function waitForBackend(api, attempts = 60, delayMs = 2000) {
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await api.get('/api/libros');
      if (res.ok()) return;
    } catch {
      // backend not up yet — keep polling
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }
  throw new Error('El backend no respondió en /api/libros dentro del tiempo de espera.');
}

module.exports = globalSetup;
