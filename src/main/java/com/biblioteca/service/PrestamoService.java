package com.biblioteca.service;

import com.biblioteca.model.*;
import com.biblioteca.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class PrestamoService {

    @Autowired
    private PrestamoRepository prestamoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private LibroRepository libroRepository;

    @Autowired
    private AmonestacionRepository amonestacionRepository;

    // Crear un préstamo

    public String crearPrestamo(String correoUsuario, Long isbn, String fechaPrestamoStr) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findByCorreo(correoUsuario);
        if (usuarioOpt.isEmpty()) return "Usuario no registrado.";

        Usuario usuario = usuarioOpt.get();
        if (!"USUARIO".equals(usuario.getRol())) return "Solo se pueden asociar préstamos a usuarios con rol USUARIO.";

        long prestamosActivos = prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuario.getId());
        if (prestamosActivos >= 2) return "El usuario ya tiene 2 préstamos activos.";

        boolean tieneAmonestaciones = amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuario.getId());
        if (tieneAmonestaciones) return "El usuario tiene amonestaciones activas.";

        Optional<Libro> libroOpt = libroRepository.findByIsbn(isbn);
        if (libroOpt.isEmpty()) return "Libro no encontrado.";
        Libro libro = libroOpt.get();
        if (libro.getCantidad() < 1) return "Libro no disponible para préstamo.";

        LocalDate fechaPrestamo = LocalDate.parse(fechaPrestamoStr);
        LocalDate fechaDevolucion = fechaPrestamo.plusDays(7);

        Prestamo prestamo = new Prestamo();
        prestamo.setUsuario(usuario);
        prestamo.setLibro(libro);
        prestamo.setFechaPrestamo(fechaPrestamo);
        prestamo.setFechaDevolucion(fechaDevolucion);
        prestamo.setEstado("activo");

        prestamoRepository.save(prestamo);

        libro.setCantidad(libro.getCantidad() - 1);
        libroRepository.save(libro);

        return "Préstamo registrado con éxito.";
    }

    /* public String crearPrestamo(Integer usuarioId, Long isbn) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(usuarioId);
        if (usuarioOpt.isEmpty()) return "Usuario no registrado.";

        Usuario usuario = usuarioOpt.get();
        if (!"USUARIO".equals(usuario.getRol())) return "Solo se pueden asociar préstamos a usuarios con rol USUARIO.";

        long prestamosActivos = prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuarioId);
        if (prestamosActivos >= 2) return "El usuario ya tiene 2 préstamos activos.";

        Optional<Libro> libroOpt = libroRepository.findByIsbn(isbn);
        if (libroOpt.isEmpty()) return "Libro no encontrado.";
        Libro libro = libroOpt.get();
        if (libro.getCantidad() < 1) return "Libro no disponible para préstamo.";

        // Registrar el préstamo
        Prestamo prestamo = new Prestamo();
        prestamo.setUsuario(usuario);
        prestamo.setLibro(libro);
        prestamo.setFechaPrestamo(LocalDate.now());
        prestamo.setFechaDevolucion(LocalDate.now().plusDays(7));

        prestamoRepository.save(prestamo);

        // Disminuir la cantidad de libros disponibles
        libro.setCantidad(libro.getCantidad() - 1);
        libroRepository.save(libro);

        return "Préstamo registrado con éxito.";
    } */

    // Devolver un préstamo
    public String devolverPrestamo(Integer prestamoId) {
        Optional<Prestamo> prestamoOpt = prestamoRepository.findById(prestamoId);
        if (prestamoOpt.isEmpty()) return "Préstamo no encontrado.";

        Prestamo prestamo = prestamoOpt.get();
        if (prestamo.getFechaDevolucion() != null && prestamo.getFechaDevolucion().isBefore(LocalDate.now())) {
            // Ya fue devuelto
            return "El préstamo ya fue devuelto.";
        }

        // Actualiza la fecha de devolución al día de hoy
        prestamo.setFechaDevolucion(LocalDate.now());
        prestamoRepository.save(prestamo);

        // Aumenta la cantidad de libros disponibles
        Libro libro = prestamo.getLibro();
        libro.setCantidad(libro.getCantidad() + 1);
        libroRepository.save(libro);

        return "Préstamo devuelto con éxito.";
    }

    // Listar todos los préstamos
    public List<Prestamo> obtenerPrestamos() {
        return prestamoRepository.findAll();
    }

    // Listar préstamos activos
    public List<Prestamo> obtenerPrestamosActivos() {
        return prestamoRepository.findByFechaDevolucionIsNull();
    }

    // Listar préstamos de un usuario
    public List<Prestamo> obtenerPrestamosPorUsuario(Integer usuarioId) {
        return prestamoRepository.findByUsuarioIdAndFechaDevolucionIsNull(usuarioId);
    }
}