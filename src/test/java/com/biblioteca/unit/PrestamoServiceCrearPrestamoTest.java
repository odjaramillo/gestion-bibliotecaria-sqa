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

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-004 — Cobertura de las guardas de {@code crearPrestamo} (TCI-M1.1..M1.7).
 *
 * @see com.biblioteca.service.PrestamoService#crearPrestamo(String, Long, String)
 */
@ExtendWith(MockitoExtension.class)
@Tag("regresion")
class PrestamoServiceCrearPrestamoTest {

    private static final String FECHA_VALIDA = "2026-06-24";

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private LibroRepository libroRepository;
    @Mock private PrestamoRepository prestamoRepository;
    @Mock private AmonestacionRepository amonestacionRepository;

    @InjectMocks
    private PrestamoService prestamoService;

    private Usuario stubUsuarioSinBloqueos() {
        Usuario usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(0L);
        when(amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId())).thenReturn(false);
        return usuario;
    }

    @Test
    @DisplayName("TCI-M1.1 — correo de usuario inexistente rechaza sin tocar el resto de repositorios")
    void correoUsuarioInexistente_rechazaConMensaje() {
        String correoDesconocido = "desconocido@biblioteca.test";
        when(usuarioRepository.findByCorreo(correoDesconocido)).thenReturn(Optional.empty());

        String resultado = prestamoService.crearPrestamo(correoDesconocido, TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("Usuario no registrado.", resultado);
        verifyNoInteractions(libroRepository, prestamoRepository, amonestacionRepository);
    }

    @Test
    @DisplayName("TCI-M1.2 — usuario con rol BIBLIOTECARIO no puede tener préstamos asociados")
    void usuarioRolBibliotecario_rechazaConMensaje() {
        Usuario bibliotecario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_BIBLIOTECARIO);
        when(usuarioRepository.findByCorreo(bibliotecario.getCorreo())).thenReturn(Optional.of(bibliotecario));

        String resultado = prestamoService.crearPrestamo(bibliotecario.getCorreo(), TestDataFactory.ISBN_DEFAULT,
                FECHA_VALIDA);

        assertEquals("Solo se pueden asociar préstamos a usuarios con rol USUARIO.", resultado);
    }

    @Test
    @DisplayName("TCI-M1.3 — usuario con 2 préstamos activos alcanza el tope")
    void usuarioConDosPrestamosActivos_rechazaConMensaje() {
        Usuario usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(2L);

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("El usuario ya tiene 2 préstamos activos.", resultado);
    }

    @Test
    @DisplayName("TCI-M1.4 — usuario con amonestación no verificada rechaza el préstamo")
    void usuarioConAmonestacionNoVerificada_rechazaConMensaje() {
        Usuario usuario = TestDataFactory.usuarioConRol(TestDataFactory.ROL_USUARIO);
        when(usuarioRepository.findByCorreo(usuario.getCorreo())).thenReturn(Optional.of(usuario));
        when(prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId())).thenReturn(0L);
        when(amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId())).thenReturn(true);

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("El usuario tiene amonestaciones activas.", resultado);
    }

    @Test
    @DisplayName("TCI-M1.5 — isbn inexistente rechaza el préstamo")
    void isbnInexistente_rechazaConMensaje() {
        Usuario usuario = stubUsuarioSinBloqueos();
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.empty());

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("Libro no encontrado.", resultado);
    }

    @Test
    @DisplayName("TCI-M1.6 — libro con cantidad 0 no está disponible para préstamo")
    void libroSinCantidadDisponible_rechazaConMensaje() {
        Usuario usuario = stubUsuarioSinBloqueos();
        Libro libro = TestDataFactory.libroConCantidad(0);
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("Libro no disponible para préstamo.", resultado);
    }

    @Test
    @DisplayName("TCI-M1.7 — datos válidos registra el préstamo y decrementa el inventario")
    void datosValidos_registraPrestamoYDecrementaInventario() {
        Usuario usuario = stubUsuarioSinBloqueos();
        Libro libro = TestDataFactory.libroConCantidad(3);
        when(libroRepository.findByIsbn(TestDataFactory.ISBN_DEFAULT)).thenReturn(Optional.of(libro));

        String resultado = prestamoService.crearPrestamo(usuario.getCorreo(), TestDataFactory.ISBN_DEFAULT, FECHA_VALIDA);

        assertEquals("Préstamo registrado con éxito.", resultado);
        assertEquals(2, libro.getCantidad());
        verify(prestamoRepository).save(any(Prestamo.class));
        verify(libroRepository).save(libro);
    }
}
