package com.biblioteca.integration;

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
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * TC-FIAB-019 — Transición de estado e inventario (TCI-M3.1, TCI-M3.2): verifica
 * que {@code crearPrestamo}/{@code devolverPrestamo} mantienen sincronía entre
 * el estado del préstamo y la cantidad disponible del libro, sobre H2 real
 * (sin mocks de repositorio).
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 * @see com.biblioteca.service.PrestamoService#devolverPrestamo(Integer)
 */
@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("regresion")
class PrestamoEstadoInventarioTest {

    /** Fecha fija en el futuro: garantiza fechaLimite posterior a "hoy" en cualquier ejecución (hasta 2030). */
    private static final String FECHA_PRESTAMO_A_TIEMPO = "2030-01-01";

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
        libro = libroRepository.save(TestDataFactory.libroConCantidadParaPersistir(5));
    }

    @Test
    @DisplayName("TCI-M3.1 — crear préstamo pasa el libro a activo y decrementa la cantidad")
    void crearPrestamo_pasaAEstadoActivoYDecrementaCantidad() {
        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), libro.getIsbn(), FECHA_PRESTAMO_A_TIEMPO);

        assertEquals("Préstamo registrado con éxito.", resultado);

        Libro libroActualizado = libroRepository.findByIsbn(libro.getIsbn()).orElseThrow();
        assertEquals(4, libroActualizado.getCantidad());

        List<Prestamo> activos = prestamoRepository.findByUsuarioIdAndFechaDevolucionIsNull(usuario.getId());
        assertEquals(1, activos.size());
        assertEquals("activo", activos.get(0).getEstado());
    }

    @Test
    @DisplayName("TCI-M3.2 — devolver a tiempo pasa a finalizado, repone inventario y no genera amonestación")
    void devolverATiempo_pasaAFinalizadoYReponeInventarioSinAmonestacion() {
        prestamoService.crearPrestamo(usuario.getCorreo(), libro.getIsbn(), FECHA_PRESTAMO_A_TIEMPO);
        Prestamo prestamoActivo = prestamoRepository.findByUsuarioIdAndFechaDevolucionIsNull(usuario.getId()).get(0);

        String resultado = prestamoService.devolverPrestamo(prestamoActivo.getId());

        assertEquals("Préstamo devuelto con éxito.", resultado);

        Prestamo prestamoActualizado = prestamoRepository.findById(prestamoActivo.getId()).orElseThrow();
        assertEquals("finalizado", prestamoActualizado.getEstado());

        Libro libroActualizado = libroRepository.findByIsbn(libro.getIsbn()).orElseThrow();
        assertEquals(5, libroActualizado.getCantidad());

        assertTrue(amonestacionRepository.findByUsuarioId(usuario.getId()).isEmpty());
    }
}
