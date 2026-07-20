package com.biblioteca.system;

import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.support.TestDataFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * TC-FIAB-011 — Sintaxis: payload JSON malformado [defecto-conocido] (TCI-T2.1, TCI-T2.2):
 * {@code POST /api/prestar} sin {@code @RestControllerAdvice} (grep = 0 en el proyecto).
 *
 * <p>Requiere {@code webEnvironment = RANDOM_PORT} + {@code TestRestTemplate} (no MockMvc,
 * ver D7): con {@code MockMvc.perform(...)}, una excepción no controlada en el controlador
 * se propaga como {@code ServletException} directo AL TEST — {@code TestDispatcherServlet}
 * no invoca el mecanismo de página de error del contenedor. Solo un contenedor real
 * (Tomcat embebido vía {@code RANDOM_PORT}) enruta la excepción no controlada a través de
 * {@code ErrorPageFilter}/{@code BasicErrorController} y produce la respuesta HTTP 500 real
 * que documenta este caso — el mismo motivo por el que TC-FIAB-021 (D7) usa esa combinación.
 * {@code /api/prestar} exige {@code hasAuthority("BIBLIOTECARIO")}, así que la autenticación
 * se hace con un login real (formLogin, sesión con cookie) en lugar de {@code @WithMockUser}
 * (que solo aplica en el hilo de {@code MockMvc}, no a una llamada HTTP real de
 * {@code TestRestTemplate}).
 *
 * <p><b>Hallazgo</b>: el payload literal de la especificación (isbn con tipo incorrecto +
 * fecha inválida) NO reproduce un HTTP 500 — Jackson rechaza el tipo incorrecto de
 * {@code isbn} con {@code HttpMessageNotReadableException}, que Spring maneja de forma
 * automática (sin necesitar {@code @RestControllerAdvice}) devolviendo HTTP 400. El defecto
 * real (HTTP 500 sin control) solo aparece cuando el JSON es sintácticamente válido y los
 * tipos son correctos, pero el VALOR de {@code fechaPrestamo} no es parseable por
 * {@code LocalDate.parse} dentro de {@code PrestamoService.crearPrestamo}
 * ({@code PrestamoService.java:47}) — ahí sí no hay manejo de la excepción y el contenedor
 * responde 500. Ambos matices se documentan aquí en lugar de asumir ciegamente el escenario
 * combinado original de la especificación.
 *
 * @see com.biblioteca.controller.Controller#registrarPrestamo(com.biblioteca.dto.PrestamoRequest)
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("defecto-conocido")
class PrestarJsonMalformadoTest {

    private static final String CORREO_BIBLIOTECARIO = "bibliotecario-json-malformado@biblioteca.test";
    private static final String CONTRASENA_PLANA = "clave-de-prueba";

    @Autowired private TestRestTemplate restTemplate;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private LibroRepository libroRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;
    @Autowired private PasswordEncoder passwordEncoder;

    @BeforeEach
    void limpiarYSembrarDatos() {
        // Limpieza defensiva en orden de dependencia FK, aunque esta clase no cree Prestamo:
        // comparte el mismo contexto Spring cacheado (RANDOM_PORT + mismo property override)
        // con MultipartLimitTest y otras clases que sí persisten filas reales (riesgo de
        // contexto compartido documentado en apply-progress de la Fase 3).
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        libroRepository.deleteAll();
        usuarioRepository.deleteAll();

        Usuario bibliotecario = new Usuario("Bibliotecario Test", CORREO_BIBLIOTECARIO,
                passwordEncoder.encode(CONTRASENA_PLANA), TestDataFactory.ROL_BIBLIOTECARIO);
        usuarioRepository.save(bibliotecario);
        usuarioRepository.save(TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO));
        libroRepository.save(TestDataFactory.libroConCantidadParaPersistir(3));
    }

    /** Login real vía {@code formLogin}: devuelve la cookie {@code JSESSIONID} de la sesión autenticada. */
    private String iniciarSesionYObtenerCookie() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("username", CORREO_BIBLIOTECARIO);
        form.add("password", CONTRASENA_PLANA);

        ResponseEntity<String> respuestaLogin = restTemplate.postForEntity(
                "/api/login", new HttpEntity<>(form, headers), String.class);
        assertEquals(HttpStatus.OK, respuestaLogin.getStatusCode());

        String cookie = respuestaLogin.getHeaders().getFirst(HttpHeaders.SET_COOKIE);
        assertTrue(cookie != null && cookie.contains("JSESSIONID"), "Login no devolvió cookie de sesión");
        return cookie;
    }

    private ResponseEntity<String> enviarPrestar(String cookieSesion, String cuerpoJson) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.add(HttpHeaders.COOKIE, cookieSesion);
        return restTemplate.postForEntity("/api/prestar", new HttpEntity<>(cuerpoJson, headers), String.class);
    }

    @Test
    @DisplayName("TCI-T2.1 — isbn con tipo incorrecto: Spring maneja HttpMessageNotReadableException sin "
            + "@RestControllerAdvice (HTTP 400, sin defecto)")
    void isbnConTipoIncorrecto_devuelveHttp400SinNecesitarControllerAdvice() {
        String cookie = iniciarSesionYObtenerCookie();
        String cuerpoTipoIncorrecto = "{\"isbn\": \"no-es-isbn\", \"fechaPrestamo\": \"99/99/9999\", "
                + "\"correoUsuario\": \"x\"}";

        ResponseEntity<String> respuesta = enviarPrestar(cookie, cuerpoTipoIncorrecto);

        assertEquals(HttpStatus.BAD_REQUEST, respuesta.getStatusCode());
    }

    @Test
    @DisplayName("TCI-T2.2 — fechaPrestamo no parseable (JSON válido, tipos correctos): "
            + "DateTimeParseException no controlada llega al contenedor como HTTP 500")
    void fechaPrestamoNoParseable_devuelveHttp500SinControllerAdvice() {
        String cookie = iniciarSesionYObtenerCookie();
        String cuerpoFechaInvalida = "{\"isbn\": " + TestDataFactory.ISBN_DEFAULT + ", "
                + "\"fechaPrestamo\": \"99/99/9999\", \"correoUsuario\": \"" + TestDataFactory.CORREO_USUARIO_DEFAULT
                + "\"}";

        ResponseEntity<String> respuesta = enviarPrestar(cookie, cuerpoFechaInvalida);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, respuesta.getStatusCode());
        assertTrue(respuesta.getBody() != null && respuesta.getBody().contains("\"status\":500"),
                "El cuerpo debe reflejar el error 500 genérico del contenedor (sin @RestControllerAdvice)");
    }
}
