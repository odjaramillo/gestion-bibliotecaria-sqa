package com.biblioteca.integration;

import com.biblioteca.model.Amonestacion;
import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.service.PrestamoService;
import com.biblioteca.support.TestDataFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

/**
 * TC-FIAB-020 — Escenario operativo end-to-end (TCI-M4.1, TCI-M4.2): préstamo →
 * devolución tardía → amonestación por mora, ejercitando el flujo completo
 * (Controller → Service → Repository) sin fallas de integración sobre H2 real.
 *
 * @see com.biblioteca.service.PrestamoService#devolverPrestamo(Integer)
 */
@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("regresion")
class PrestamoMoraAmonestacionTest {

    /** Fecha fija en el pasado: garantiza fechaLimite anterior a "hoy" en cualquier ejecución. */
    private static final String FECHA_PRESTAMO_VENCIDA = "2020-01-01";

    @Autowired private PrestamoService prestamoService;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private LibroRepository libroRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;

    private Usuario usuario;
    private Libro libro;

    @BeforeEach
    void limpiarYSembrarDatos() {
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        libroRepository.deleteAll();
        usuarioRepository.deleteAll();

        usuario = usuarioRepository.save(TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO));
        libro = libroRepository.save(TestDataFactory.libroConCantidadParaPersistir(3));
    }

    @Test
    @DisplayName("TCI-M4.1/M4.2 — devolución tardía genera amonestación de mora (monto=100.0, pagada=false)")
    void devolverPrestamoVencido_generaAmonestacionDeMora() {
        String creado = prestamoService.crearPrestamo(usuario.getCorreo(), libro.getIsbn(), FECHA_PRESTAMO_VENCIDA);
        assertEquals("Préstamo registrado con éxito.", creado);

        Prestamo prestamoActivo = prestamoRepository.findByUsuarioIdAndFechaDevolucionIsNull(usuario.getId()).get(0);

        String devuelto = prestamoService.devolverPrestamo(prestamoActivo.getId());
        assertEquals("Préstamo devuelto con éxito.", devuelto);

        List<Amonestacion> amonestaciones = amonestacionRepository.findByUsuarioId(usuario.getId());
        assertEquals(1, amonestaciones.size());

        Amonestacion amonestacion = amonestaciones.get(0);
        assertEquals(100.0, amonestacion.getMonto());
        assertFalse(amonestacion.isPagada());
        assertFalse(amonestacion.isVerificada());
    }
}
