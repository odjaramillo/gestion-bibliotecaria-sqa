// @ts-check
/**
 * Shared test data for the acceptance suite.
 *
 * The backend seeds nothing (src/main/resources/sql/data.sql is empty and the
 * default profile does not run it), so the tests create every entity they need
 * through the API in global-setup. These constants are the single source of
 * truth for both the seeding and the assertions.
 */

const BACKEND = 'http://localhost:8080';

const BIBLIOTECARIO = {
  nombre: 'Bibliotecario E2E',
  correo: 'bibliotecario.e2e@biblioteca.local',
  contrasena: 'Passw0rd!e2e',
  // The public registration endpoint honours the rol field from the body
  // (a known privilege-escalation weakness). The acceptance suite relies on
  // it purely as a seeding vehicle; the flow under test is the loan, not the
  // registration.
  rol: 'BIBLIOTECARIO',
};

const LECTOR = {
  nombre: 'Lector E2E',
  correo: 'lector.e2e@biblioteca.local',
  contrasena: 'Passw0rd!e2e',
  // rol omitted on purpose: the backend defaults an empty rol to USUARIO.
};

const LIBRO = {
  titulo: 'El nombre del viento',
  autor: 'Patrick Rothfuss',
  editorial: 'DAW Books',
  genero: 'Fantasia',
  isbn: 9788401352836, // exactly 13 digits — enforced by frontend and backend
  anio: 2007,
  cantidad: 5,
};

module.exports = { BACKEND, BIBLIOTECARIO, LECTOR, LIBRO };
