package com.biblioteca.controller;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.Optional;

@RestController
@RequestMapping("/api/prestamos")
public class PrestamoController {

    @Autowired
    private PrestamoRepository prestamoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private LibroRepository libroRepository;

    @PostMapping
    public ResponseEntity<?> crearPrestamo(@RequestParam Long usuarioId, @RequestParam String isbn) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) return ResponseEntity.badRequest().body("Usuario no registrado.");

        long prestamosActivos = prestamoRepository.countByUsuarioIdAndFechaDevolucionIsNull(usuarioId);
        if (prestamosActivos >= 2) return ResponseEntity.badRequest().body("El usuario ya tiene 2 préstamos activos.");

        Optional<Libro> libro = libroRepository.findByIsbn(isbn);
        if (libro.isEmpty() || libro.get().getCantidad() <= 1) {
            return ResponseEntity.badRequest().body("Libro no disponible para préstamo.");
        }

        Prestamo prestamo = new Prestamo();
        prestamo.setUsuario(usuario.get());
        prestamo.setLibro(libro.get());
        prestamo.setFechaPrestamo(LocalDate.now());
        prestamo.setFechaDevolucion(LocalDate.now().plusDays(7));

        prestamoRepository.save(prestamo);
        return ResponseEntity.ok("Préstamo registrado con éxito.");
    }
}