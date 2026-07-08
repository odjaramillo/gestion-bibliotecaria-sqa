package com.biblioteca.unit;

import com.biblioteca.model.Libro;
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
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.format.DateTimeParseException;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-008 (parte 2/2) — Partición de la fecha en {@code crearPrestamo}: casos inválidos
 * (TCI-T1.2..T1.4). Suite {@code defecto-conocido}: documenta el comportamiento ACTUAL —
 * {@code LocalDate.parse} sin manejo de excepciones propaga
 * {@link DateTimeParseException}/{@link NullPointerException} en lugar de un HTTP 400
 * controlado (ERS). Clase separada de {@link ParseFechaValidaTest} por D1.
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@ExtendWith(MockitoExtension.class)
@Tag("defecto-conocido")
class ParseFechaInvalidaTest {

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private LibroRepository libroRepository;
    @Mock private PrestamoRepository prestamoRepository;
    @Mock private AmonestacionRepository amonestacionRepository;

    @InjectMocks
    private PrestamoService prestamoService;

    private Usuario usuario;

    @BeforeEach
    void arrangeUsuarioYLibroValidos() {
        usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        Libro libro = TestDataFactory.libroConCantidad(3);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(0L);
        when(amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId())).thenReturn(false);
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));
    }

    @Test
    @DisplayName("TCI-T1.2 — formato dd-MM-yyyy propaga DateTimeParseException no controlada [defecto WT-01/INC-WT-01]")
    void formatoDiaMesAnio_propagaDateTimeParseException() {
        assertThrows(DateTimeParseException.class, () ->
                prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, "24-06-2026"));
    }

    @Test
    @DisplayName("TCI-T1.3 — cadena sin formato de fecha propaga DateTimeParseException no controlada [defecto WT-01/INC-WT-01]")
    void cadenaSinFormatoDeFecha_propagaDateTimeParseException() {
        assertThrows(DateTimeParseException.class, () ->
                prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, "99/99/9999"));
    }

    @Test
    @DisplayName("TCI-T1.4 — fecha null propaga NullPointerException no controlada [defecto WT-01/INC-WT-01]")
    void fechaNull_propagaNullPointerException() {
        assertThrows(NullPointerException.class, () ->
                prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, null));
    }
}
