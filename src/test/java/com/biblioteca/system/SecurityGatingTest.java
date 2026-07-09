package com.biblioteca.system;

import com.biblioteca.dto.PrestamoRequest;
import com.biblioteca.model.Amonestacion;
import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.support.TestDataFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * SC-SEC-01 — Gating de seguridad (issue #15, REQ-DYN-SEC): {@code /api/prestar} exige
 * {@code hasAuthority("BIBLIOTECARIO")} ({@code SecurityConfig.java:28-29}); sin autoridad
 * la petición es rechazada, con la autoridad correcta el gating se supera y la petición
 * llega a la lógica de negocio.
 *
 * <p>También cubre las ramas de autorización EN el propio método
 * {@code Controller.pagarAmonestacion} ({@code Controller.java:372-380}, no delegadas al
 * filtro de seguridad porque el endpoint solo exige {@code authenticated()}): 401 cuando el
 * correo autenticado no resuelve ningún {@code Usuario}, 403 cuando la amonestación no
 * pertenece al usuario autenticado. Estas ramas quedaron explícitamente diferidas a esta
 * fase por {@code PagarAmonestacionTest} (Fase 3, TC-FIAB-025).
 *
 * <p>Requiere {@code properties = "spring.autoconfigure.exclude="} para reactivar
 * {@code SecurityAutoConfiguration} (excluida globalmente por {@code application-test.properties})
 * — sin esto {@code SecurityConfig.filterChain(HttpSecurity)} no puede resolver el bean
 * {@code HttpSecurity} y el contexto de Spring falla al levantar.
 *
 * @see com.biblioteca.controller.Controller#registrarPrestamo(PrestamoRequest)
 * @see com.biblioteca.controller.Controller#pagarAmonestacion(org.springframework.security.core.Authentication, Map)
 */
@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Tag("regresion")
class SecurityGatingTest {

    private static final String CORREO_DUENIO = "duenio-amonestacion@biblioteca.test";
    private static final String CORREO_OTRO_USUARIO = "otro-usuario@biblioteca.test";
    private static final String CORREO_INEXISTENTE = "nadie-registrado@biblioteca.test";
    private static final String CORREO_USUARIO_SIN_AMONESTACIONES = "usuario-sin-amonestaciones@biblioteca.test";
    private static final String FECHA_PRESTAMO_VENCIDA = "2020-01-01";
    private static final String FECHA_PRESTAMO_FUTURA = LocalDate.now().plusYears(1).toString();

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private LibroRepository libroRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;

    private Usuario duenio;
    private Libro libro;
    private Amonestacion amonestacionDelDuenio;

    @BeforeEach
    void limpiarYSembrarDatos() {
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        libroRepository.deleteAll();
        usuarioRepository.deleteAll();

        duenio = usuarioRepository.save(
                TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO, CORREO_DUENIO));
        libro = libroRepository.save(TestDataFactory.libroConCantidadParaPersistir(3));
        Prestamo prestamo = prestamoRepository.save(
                TestDataFactory.prestamoActivo(duenio, libro, LocalDate.parse(FECHA_PRESTAMO_VENCIDA)));
        amonestacionDelDuenio = amonestacionRepository.save(
                TestDataFactory.amonestacion(duenio, prestamo, false, false));
    }

    @Test
    @DisplayName("SC-SEC-01 — POST /api/prestar sin autoridad BIBLIOTECARIO es rechazado")
    void crearPrestamo_sinAutoridadBibliotecario_esRechazado() throws Exception {
        // Comportamiento REAL documentado (no el asumido literalmente 401/403 por SC-SEC-01):
        // SecurityConfig configura .formLogin() sin .loginPage() propia, así que Spring
        // Security instala un LoginUrlAuthenticationEntryPoint por defecto. Una petición sin
        // autenticar a un recurso protegido no recibe 401/403 sino un 302 hacia "/login" — la
        // petición SIGUE siendo rechazada (nunca llega a PrestamoService.crearPrestamo), solo
        // que el mecanismo de rechazo es una redirección, no un código 4xx puro.
        mockMvc.perform(post("/api/prestar")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(cuerpoPrestamoValido())))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("http://localhost/login"));
    }

    @Test
    @WithMockUser(authorities = "BIBLIOTECARIO")
    @DisplayName("SC-SEC-01 — POST /api/prestar con autoridad BIBLIOTECARIO supera el gating de seguridad")
    void crearPrestamo_conAutoridadBibliotecario_superaElGating() throws Exception {
        // Usuario sin amonestaciones ni préstamos activos: la petición debe alcanzar la
        // lógica de negocio y completarse con éxito, no solo "no ser 401/403".
        Usuario usuarioSinAmonestaciones = usuarioRepository.save(TestDataFactory.usuarioConRolParaPersistir(
                TestDataFactory.ROL_USUARIO, CORREO_USUARIO_SIN_AMONESTACIONES));

        PrestamoRequest request = new PrestamoRequest();
        request.setCorreoUsuario(usuarioSinAmonestaciones.getCorreo());
        request.setIsbn(libro.getIsbn());
        request.setFechaPrestamo(FECHA_PRESTAMO_FUTURA);

        mockMvc.perform(post("/api/prestar")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(username = CORREO_INEXISTENTE)
    @DisplayName("Controller.pagarAmonestacion — correo autenticado sin Usuario asociado retorna 401")
    void pagarAmonestacion_usuarioNoResuelto_retorna401() throws Exception {
        mockMvc.perform(put("/api/amonestaciones-usuario/pagar")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(cuerpoPago(amonestacionDelDuenio.getId()))))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = CORREO_OTRO_USUARIO)
    @DisplayName("Controller.pagarAmonestacion — amonestación de otro usuario retorna 403")
    void pagarAmonestacion_amonestacionDeOtroUsuario_retorna403() throws Exception {
        usuarioRepository.save(
                TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO, CORREO_OTRO_USUARIO));

        mockMvc.perform(put("/api/amonestaciones-usuario/pagar")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(cuerpoPago(amonestacionDelDuenio.getId()))))
                .andExpect(status().isForbidden())
                .andExpect(content().string("No autorizado"));
    }

    private PrestamoRequest cuerpoPrestamoValido() {
        PrestamoRequest request = new PrestamoRequest();
        request.setCorreoUsuario(duenio.getCorreo());
        request.setIsbn(libro.getIsbn());
        request.setFechaPrestamo(FECHA_PRESTAMO_FUTURA);
        return request;
    }

    private Map<String, Object> cuerpoPago(Integer amonestacionId) {
        Map<String, Object> body = new HashMap<>();
        body.put("amonestacionId", amonestacionId);
        body.put("metodoPago", "tarjeta");
        body.put("comprobantePago", "REF-123");
        return body;
    }
}
