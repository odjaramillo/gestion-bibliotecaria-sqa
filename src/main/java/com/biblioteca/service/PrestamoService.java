package com.biblioteca.service;

import com.biblioteca.model.*;
import com.biblioteca.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.Optional;

import java.util.List;

@Service
public class PrestamoService {

    @Autowired
    private PrestamoRepository prestamoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private LibroRepository libroRepository;

    /* public String crearPrestamo(Integer usuarioId, String isbn) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) return "Usuario no registrado.";

        long prestamosActivos = prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuarioId);
        if (prestamosActivos >= 2) return "El usuario ya tiene 2 préstamos activos.";

        Optional<Libro> libro = libroRepository.findByIsbn(isbn);
        if (libro.isEmpty() || libro.get().getCantidad() <= 1) {
            return "Libro no disponible para préstamo.";
        }

        Prestamo prestamo = new Prestamo();
        prestamo.setUsuario(usuario.get());
        prestamo.setLibro(libro.get());
        prestamo.setFechaPrestamo(LocalDate.now());
        prestamo.setFechaDevolucion(LocalDate.now().plusDays(7));

        prestamoRepository.save(prestamo);
        return "Préstamo registrado con éxito.";
    } */

    public List<Prestamo> obtenerPrestamos() {
    return prestamoRepository.findAll();
}
}