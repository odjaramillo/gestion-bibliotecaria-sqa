package com.biblioteca.unit;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.service.PrestamoService;
import com.biblioteca.support.TestDataFactory;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-018 — Valor límite del tope de préstamos activos ({@code prestamosActivos >= 2}),
 * TCI-M2.1..M2.3. Frontera esperada: 1 permite, 2 y 3 rechazan.
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@ExtendWith(MockitoExtension.class)
@Tag("regresion")
class PrestamosActivosLimiteTest {

    private static final String FECHA_VALIDA = "2026-06-24";

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private LibroRepository libroRepository;
    @Mock private PrestamoRepository prestamoRepository;
    @Mock private AmonestacionRepository amonestacionRepository;

    @InjectMocks
    private PrestamoService prestamoService;

    @ParameterizedTest(name = "TCI-M2.{index} — prestamosActivos={0} -> rechaza={1}")
    @CsvSource({
            "1, false",
            "2, true",
            "3, true"
    })
    @DisplayName("Frontera prestamosActivos >= 2: 1 permite, 2 y 3 rechazan")
    void fronteraPrestamosActivos_determinaAceptacionORechazo(long prestamosActivos, boolean debeRechazar) {
        Usuario usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        Libro libro = TestDataFactory.libroConCantidad(3);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(prestamosActivos);
        lenient().when(amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId())).thenReturn(false);
        lenient().when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        if (debeRechazar) {
            assertEquals("El usuario ya tiene 2 préstamos activos.", resultado);
        } else {
            assertEquals("Préstamo registrado con éxito.", resultado);
        }
    }
}
