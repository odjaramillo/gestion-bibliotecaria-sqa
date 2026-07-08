package com.biblioteca.unit;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.service.PrestamoService;
import com.biblioteca.support.TestDataFactory;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-008 (parte 1/2) — Partición de la fecha en {@code crearPrestamo}: caso válido
 * (TCI-T1.1). Suite {@code regresion}. El caso inválido (TCI-T1.2..T1.4) vive en
 * {@link ParseFechaInvalidaTest} (clase separada, D1) para no compartir el mismo XML de
 * Surefire entre los pasos {@code regresion}/{@code defecto-conocido} de CI.
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@ExtendWith(MockitoExtension.class)
@Tag("regresion")
class ParseFechaValidaTest {

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private LibroRepository libroRepository;
    @Mock private PrestamoRepository prestamoRepository;
    @Mock private AmonestacionRepository amonestacionRepository;

    @InjectMocks
    private PrestamoService prestamoService;

    @Test
    @DisplayName("TCI-T1.1 — fecha ISO-8601 válida procesa el préstamo y calcula la fecha límite")
    void fechaValidaIso8601_procesaPrestamoYCalculaFechaLimite() {
        Usuario usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        Libro libro = TestDataFactory.libroConCantidad(3);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(0L);
        when(amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId())).thenReturn(false);
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT,
                "2026-06-24");

        assertEquals("Préstamo registrado con éxito.", resultado);
        verify(prestamoRepository).save(argThat((Prestamo p) ->
                LocalDate.of(2026, 6, 24).equals(p.getFechaPrestamo())
                        && LocalDate.of(2026, 7, 1).equals(p.getFechaLimite())));
    }
}
