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
        LocalDate fechaLimite = fechaPrestamo.plusDays(7);

        Prestamo prestamo = new Prestamo();
        prestamo.setUsuario(usuario);
        prestamo.setLibro(libro);
        prestamo.setFechaPrestamo(fechaPrestamo);
        prestamo.setFechaDevolucion(null);
        prestamo.setFechaLimite(fechaLimite); 
        prestamo.setEstado("activo");

        prestamoRepository.save(prestamo);

        libro.setCantidad(libro.getCantidad() - 1);
        libroRepository.save(libro);

        return "Préstamo registrado con éxito.";
    }

    // Devolver un préstamo
    public String devolverPrestamo(Integer prestamoId) {
    Optional<Prestamo> prestamoOpt = prestamoRepository.findById(prestamoId);
    if (prestamoOpt.isEmpty()) return "Préstamo no encontrado.";

    Prestamo prestamo = prestamoOpt.get();
    if (prestamo.getFechaDevolucion() != null) {
        return "El préstamo ya fue devuelto.";
    }

    LocalDate hoy = LocalDate.now();
    prestamo.setFechaDevolucion(hoy);
    prestamo.setEstado("finalizado"); // Marcar como finalizado
    prestamoRepository.save(prestamo);

    Libro libro = prestamo.getLibro();
    libro.setCantidad(libro.getCantidad() + 1);
    libroRepository.save(libro);

    // Si la devolución es después de la fecha límite, genera amonestación
    if (prestamo.getFechaLimite() != null && hoy.isAfter(prestamo.getFechaLimite())) {
        Amonestacion amonestacion = new Amonestacion();
        amonestacion.setUsuario(prestamo.getUsuario());
        amonestacion.setPrestamo(prestamo);
        amonestacion.setMonto(100.0);
        amonestacion.setPagada(false);
        amonestacion.setMetodoPago(null);
        amonestacion.setComprobantePago(null);
        amonestacion.setVerificada(false);
        amonestacion.setFecha(java.time.LocalDateTime.now());
        amonestacionRepository.save(amonestacion);
    }

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

    // Renovar un préstamo finalizado (solo bibliotecarios)
    public String renovarPrestamo(Integer prestamoId, String usuarioRol) {
        // Verificar que el usuario sea bibliotecario
        if (!"BIBLIOTECARIO".equals(usuarioRol)) {
            return "Solo los bibliotecarios pueden renovar préstamos.";
        }

        Optional<Prestamo> prestamoOpt = prestamoRepository.findById(prestamoId);
        if (prestamoOpt.isEmpty()) {
            return "Préstamo no encontrado.";
        }

        Prestamo prestamo = prestamoOpt.get();
        
        // Verificar que el préstamo tenga fecha de devolución (esté finalizado)
        if (prestamo.getFechaDevolucion() == null) {
            return "Solo se pueden renovar préstamos finalizados.";
        }

        LocalDate hoy = LocalDate.now();
        
        // Renovar: nueva fecha límite 7 días desde hoy
        prestamo.setFechaLimite(hoy.plusDays(7));
        prestamo.setEstado("activo");
        prestamo.setFechaDevolucion(null); // Resetear fecha de devolución
        
        prestamoRepository.save(prestamo);

        // Reducir cantidad disponible del libro
        Libro libro = prestamo.getLibro();
        libro.setCantidad(libro.getCantidad() - 1);
        libroRepository.save(libro);

        return "Préstamo renovado con éxito. Nueva fecha límite: " + prestamo.getFechaLimite();
    }

    // Listar préstamos finalizados (para renovar)
    public List<Prestamo> obtenerPrestamosFinalizados() {
        return prestamoRepository.findByFechaDevolucionIsNotNull();
    }
}