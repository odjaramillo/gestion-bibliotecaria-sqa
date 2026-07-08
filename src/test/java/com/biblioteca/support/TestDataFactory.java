package com.biblioteca.support;

import com.biblioteca.model.Amonestacion;
import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Builders reutilizables para pruebas dinámicas de Fiabilidad (issue #15, D6).
 * Los builders originales fijan {@code id=1} para pruebas unitarias con Mockito
 * (Fase 2, sin persistencia real); los {@code *ParaPersistir} (Fase 3) omiten el
 * {@code id} para que JPA lo genere vía {@code IDENTITY} al persistir de verdad.
 */
public final class TestDataFactory {

    public static final String ROL_USUARIO = "USUARIO";
    public static final String ROL_BIBLIOTECARIO = "BIBLIOTECARIO";
    public static final String CORREO_USUARIO_DEFAULT = "usuario@biblioteca.test";
    public static final Long ISBN_DEFAULT = 9780000000001L;
    public static final LocalDateTime FECHA_AMONESTACION_DEFAULT = LocalDateTime.of(2026, 6, 24, 10, 0);

    private TestDataFactory() {
    }

    public static Usuario usuario(Integer id, String correo, String rol) {
        Usuario usuario = new Usuario("Usuario Test", correo, "clave-hash", rol);
        usuario.setId(id);
        return usuario;
    }

    public static Usuario usuarioConRol(String rol) {
        return usuario(1, CORREO_USUARIO_DEFAULT, rol);
    }

    /** Sin {@code id}: {@code usuarioRepository.save(...)} hace {@code persist} real, no {@code merge}. */
    public static Usuario usuarioConRolParaPersistir(String rol) {
        return new Usuario("Usuario Test", CORREO_USUARIO_DEFAULT, "clave-hash", rol);
    }

    public static Libro libro(Integer id, Long isbn, int cantidad) {
        Libro libro = new Libro("Titulo Test", "Autor Test", "Editorial Test", "Genero Test", isbn, 2024, cantidad,
                "Sinopsis de prueba", null);
        libro.setId(id);
        return libro;
    }

    public static Libro libroConCantidad(int cantidad) {
        return libro(1, ISBN_DEFAULT, cantidad);
    }

    /** Sin {@code id}: {@code libroRepository.save(...)} hace {@code persist} real, no {@code merge}. */
    public static Libro libroConCantidadParaPersistir(int cantidad) {
        return new Libro("Titulo Test", "Autor Test", "Editorial Test", "Genero Test", ISBN_DEFAULT, 2024, cantidad,
                "Sinopsis de prueba", null);
    }

    public static Prestamo prestamoActivo(Usuario usuario, Libro libro, LocalDate fechaPrestamo) {
        Prestamo prestamo = new Prestamo(usuario, libro, fechaPrestamo, null, "activo");
        prestamo.setFechaLimite(fechaPrestamo.plusDays(7));
        return prestamo;
    }

    public static Amonestacion amonestacion(Usuario usuario, Prestamo prestamo, boolean pagada, boolean verificada,
            LocalDateTime fecha) {
        return new Amonestacion(usuario, prestamo, 100.0, pagada, null, null, verificada, fecha);
    }

    /** Convenience overload: usa {@link #FECHA_AMONESTACION_DEFAULT} en lugar de la hora actual del reloj. */
    public static Amonestacion amonestacion(Usuario usuario, Prestamo prestamo, boolean pagada, boolean verificada) {
        return amonestacion(usuario, prestamo, pagada, verificada, FECHA_AMONESTACION_DEFAULT);
    }
}
