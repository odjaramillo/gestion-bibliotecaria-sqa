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
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-022 — Ausencia de frontera transaccional [defecto-conocido] (TCI-T5.1):
 * sin {@code @Transactional}, un fallo entre {@code prestamoRepository.save} (L58) y
 * {@code libroRepository.save} (L61) deja un {@code Prestamo} huérfano sin rollback.
 * Fallo forzado con {@code @MockitoBean LibroRepository}; la fila real de {@code libros}
 * se siembra por JDBC directo (fuera del mock) para que el {@code Prestamo} real
 * satisfaga su FK {@code libro_id}.
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("defecto-conocido")
class TransactionalGapTest {

    private static final String FECHA_VALIDA = "2026-06-24";

    @Autowired private PrestamoService prestamoService;
    @Autowired private UsuarioRepository usuarioRepository;
    @Autowired private PrestamoRepository prestamoRepository;
    @Autowired private AmonestacionRepository amonestacionRepository;
    @Autowired private JdbcTemplate jdbcTemplate;

    @MockitoBean
    private LibroRepository libroRepository;

    private Usuario usuario;
    private Integer libroIdReal;

    @BeforeEach
    void limpiarYSembrarDatos() {
        amonestacionRepository.deleteAll();
        prestamoRepository.deleteAll();
        jdbcTemplate.update("DELETE FROM libros");
        usuarioRepository.deleteAll();

        usuario = usuarioRepository.save(TestDataFactory.usuarioConRolParaPersistir(TestDataFactory.ROL_USUARIO));

        jdbcTemplate.update(
                "INSERT INTO libros (titulo, autor, editorial, genero, isbn, anio, cantidad, sinopsis) "
                        + "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                "Titulo Test", "Autor Test", "Editorial Test", "Genero Test", TestDataFactory.ISBN_DEFAULT, 2024, 3,
                "Sinopsis de prueba");
        libroIdReal = jdbcTemplate.queryForObject("SELECT id FROM libros WHERE isbn = ?", Integer.class,
                TestDataFactory.ISBN_DEFAULT);
    }

    @Test
    @DisplayName("TCI-T5.1 — fallo en libroRepository.save() deja un Prestamo huérfano sin rollback")
    void falloEntreSaves_dejaPrestamoHuerfanoSinDecrementarInventario() {
        Libro libro = TestDataFactory.libro(libroIdReal, TestDataFactory.ISBN_DEFAULT, 3);
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));
        when(libroRepository.save(any(Libro.class)))
                .thenThrow(new RuntimeException("Fallo simulado de persistencia (WT-04)"));

        assertThrows(RuntimeException.class,
                () -> prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA));

        // Prestamo ya confirmado en H2 (save() corre en su propia transacción) pese al
        // fallo posterior: huérfano sin @Transactional que revierta.
        List<Prestamo> huerfanos = prestamoRepository.findAll();
        assertEquals(1, huerfanos.size());
        assertEquals(usuario.getId(), huerfanos.get(0).getUsuario().getId());
        assertEquals(libroIdReal, huerfanos.get(0).getLibro().getId());

        // Decremento calculado en memoria (llegó al 2do save) pero nunca persistido:
        // "cantidad" real queda inconsistente con el Prestamo ya guardado (corrupción = 1).
        assertEquals(2, libro.getCantidad());
        verify(libroRepository).save(libro);

        Integer cantidadPersistida = jdbcTemplate.queryForObject("SELECT cantidad FROM libros WHERE id = ?",
                Integer.class, libroIdReal);
        assertEquals(3, cantidadPersistida);
    }
}
