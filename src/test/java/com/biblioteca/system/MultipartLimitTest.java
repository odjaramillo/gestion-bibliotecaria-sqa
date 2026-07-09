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
import org.springframework.core.io.ByteArrayResource;
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
 * TC-FIAB-021 — Valor límite del tamaño multipart [defecto-conocido] (TCI-T3.1, TCI-T3.3,
 * {@code Controller.java:66-73}): {@code POST /api/libros} no configura
 * {@code spring.servlet.multipart.max-file-size}, así que rige el límite por defecto de
 * Spring Boot (1MB por archivo).
 *
 * <p><b>Hallazgo 1</b>: la especificación original asumía que, sin {@code @RestControllerAdvice}
 * (grep = 0 en el proyecto), {@code MaxUploadSizeExceededException} se traduciría en un HTTP
 * 500 genérico en vez del HTTP 413 correcto. En la práctica, {@code DefaultHandlerExceptionResolver}
 * de Spring MVC ya mapea esta excepción específica a HTTP 413 automáticamente desde Spring
 * Framework 5.1 — SIN necesitar ningún {@code @RestControllerAdvice} propio.
 *
 * <p><b>Hallazgo 2</b>: aunque {@code /api/libros} es {@code permitAll}, la respuesta 413 se
 * envía vía {@code HttpServletResponse.sendError(413)}, lo que dispara un reenvío interno del
 * contenedor a {@code /error} (el mismo mecanismo de página de error visto en
 * {@code PrestarJsonMalformadoTest}). Ese reenvío SÍ pasa por {@code anyRequest().authenticated()};
 * sin sesión, Spring Security lo redirige a {@code /login} y el cliente nunca ve el 413 real
 * (termina viendo un 200 de la página de login tras seguir la redirección). Por eso esta clase
 * inicia sesión real antes de subir, igual que {@code PrestarJsonMalformadoTest}.
 *
 * <p>Requiere {@code webEnvironment = RANDOM_PORT} + {@code TestRestTemplate} (D7): MockMvc
 * NO aplica el límite multipart real (lo impone el contenedor Tomcat embebido, no el
 * {@code DispatcherServlet} simulado).
 *
 * @see com.biblioteca.controller.Controller#registrarLibro(
 *         com.biblioteca.model.Libro, org.springframework.web.multipart.MultipartFile, String)
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("defecto-conocido")
class MultipartLimitTest {

    private static final String CORREO_BIBLIOTECARIO = "bibliotecario-multipart@biblioteca.test";
    private static final String CONTRASENA_PLANA = "clave-de-prueba";
    private static final long ISBN_DENTRO_DEL_LIMITE = 9780000000010L;
    private static final int UN_MEGABYTE = 1024 * 1024;

    @Autowired private TestRestTemplate restTemplate;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private LibroRepository libroRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;
    @Autowired private PasswordEncoder passwordEncoder;

    @BeforeEach
    void limpiarYSembrarDatos() {
        // Limpieza defensiva en orden de dependencia FK (riesgo de contexto Spring compartido
        // documentado en apply-progress de la Fase 3): esta clase no persiste Prestamo, pero
        // comparte cache de contexto (RANDOM_PORT + mismo property override) con otras clases
        // de este paquete.
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        libroRepository.deleteAll();
        usuarioRepository.deleteAll();
        Usuario bibliotecario = new Usuario("Bibliotecario Test", CORREO_BIBLIOTECARIO,
                passwordEncoder.encode(CONTRASENA_PLANA), TestDataFactory.ROL_BIBLIOTECARIO);
        usuarioRepository.save(bibliotecario);
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

    @Test
    @DisplayName("TCI-T3.1 — imagen de 0.9MB (dentro del límite) se registra sin excepción")
    void imagenDentroDelLimite_registraElLibroConExito() {
        String cookie = iniciarSesionYObtenerCookie();

        ResponseEntity<String> respuesta = registrarLibroConImagen(cookie, ISBN_DENTRO_DEL_LIMITE,
                (int) (0.9 * UN_MEGABYTE));

        assertEquals(HttpStatus.OK, respuesta.getStatusCode());
        assertEquals("Libro registrado exitosamente.", respuesta.getBody());
    }

    @Test
    @DisplayName("TCI-T3.3 — imagen de 1.1MB (sobre el límite) dispara MaxUploadSizeExceededException, "
            + "que Spring ya traduce a HTTP 413 sin necesitar @RestControllerAdvice")
    void imagenSobreElLimite_disparaMaxUploadSizeExceededYSpringResponde413() {
        String cookie = iniciarSesionYObtenerCookie();

        ResponseEntity<String> respuesta = registrarLibroConImagen(cookie, TestDataFactory.ISBN_DEFAULT,
                (int) (1.1 * UN_MEGABYTE));

        assertEquals(HttpStatus.PAYLOAD_TOO_LARGE, respuesta.getStatusCode());
    }

    private ResponseEntity<String> registrarLibroConImagen(String cookieSesion, long isbn, int tamanoImagenBytes) {
        String libroJson = "{\"titulo\":\"Titulo Test\",\"autor\":\"Autor Test\",\"editorial\":\"Editorial Test\","
                + "\"genero\":\"Genero Test\",\"isbn\":" + isbn + ",\"anio\":2024,\"cantidad\":3,"
                + "\"sinopsis\":\"Sinopsis de prueba\"}";

        HttpHeaders libroPartHeaders = new HttpHeaders();
        libroPartHeaders.setContentType(MediaType.APPLICATION_JSON);

        byte[] contenidoImagen = new byte[tamanoImagenBytes];

        MultiValueMap<String, Object> multipartBody = new LinkedMultiValueMap<>();
        multipartBody.add("libro", new HttpEntity<>(libroJson, libroPartHeaders));
        multipartBody.add("imagen", new ByteArrayResource(contenidoImagen) {
            @Override
            public String getFilename() {
                return "imagen.png";
            }
        });

        HttpHeaders requestHeaders = new HttpHeaders();
        requestHeaders.setContentType(MediaType.MULTIPART_FORM_DATA);
        requestHeaders.add(HttpHeaders.COOKIE, cookieSesion);

        return restTemplate.postForEntity(
                "/api/libros?correoUsuario=" + CORREO_BIBLIOTECARIO,
                new HttpEntity<>(multipartBody, requestHeaders), String.class);
    }
}
