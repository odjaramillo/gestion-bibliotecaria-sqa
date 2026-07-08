package com.biblioteca.integration;

import com.biblioteca.controller.Controller;
import com.biblioteca.model.Amonestacion;
import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.support.TestDataFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-025 — Pago de amonestación sin validación [defecto-conocido] (TCI-M6.1..M6.3):
 * {@code Controller.pagarAmonestacion} persiste {@code metodoPago}/{@code comprobantePago}
 * sin validar formato ni contenido (comportamiento ACTUAL, no el ERS). Se invoca el
 * método directamente (sin MockMvc); el gating de seguridad se cubre aparte en TC-FIAB-011.
 *
 * @see com.biblioteca.controller.Controller#pagarAmonestacion(Authentication, Map)
 */
@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("defecto-conocido")
class PagarAmonestacionTest {

    private static final String FECHA_PRESTAMO_VENCIDA = "2020-01-01";

    @Autowired private Controller controller;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private LibroRepository libroRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;

    private Usuario usuario;

    @BeforeEach
    void limpiarYSembrarDatos() {
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        libroRepository.deleteAll();
        usuarioRepository.deleteAll();

        usuario = usuarioRepository.save(TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO));
    }

    private static Stream<Arguments> combinacionesMetodoPagoSinValidar() {
        return Stream.of(
                Arguments.of("TCI-M6.1 — metodoPago vacío persiste sin rechazo", "", "REF-000"),
                Arguments.of("TCI-M6.2 — metodoPago/comprobantePago null marcan pagada=true", null, null),
                Arguments.of("TCI-M6.3 — inyección SQL persiste tal cual sin sanitizar",
                        "'; DROP TABLE amonestaciones; --", "REF-999"));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("combinacionesMetodoPagoSinValidar")
    void pagarAmonestacion_persisteSinValidar(String descripcion, String metodoPago, String comprobantePago) {
        Libro libro = libroRepository.save(TestDataFactory.libroConCantidadParaPersistir(1));
        Prestamo prestamo = prestamoRepository.save(
                TestDataFactory.prestamoActivo(usuario, libro, LocalDate.parse(FECHA_PRESTAMO_VENCIDA)));
        Amonestacion amonestacion = amonestacionRepository.save(
                TestDataFactory.amonestacion(usuario, prestamo, false, false));

        Authentication authentication = mock(Authentication.class);
        when(authentication.getName()).thenReturn(usuario.getCorreo());
        Map<String, Object> body = new HashMap<>();
        body.put("amonestacionId", amonestacion.getId());
        body.put("metodoPago", metodoPago);
        body.put("comprobantePago", comprobantePago);

        ResponseEntity<?> respuesta = controller.pagarAmonestacion(authentication, body);

        assertEquals(200, respuesta.getStatusCode().value());
        Amonestacion actualizada = amonestacionRepository.findById(amonestacion.getId()).orElseThrow();
        assertTrue(actualizada.isPagada());
        assertEquals(metodoPago, actualizada.getMetodoPago());
    }
}
