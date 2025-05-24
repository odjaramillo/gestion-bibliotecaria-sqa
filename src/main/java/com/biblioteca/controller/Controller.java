package com.biblioteca.controller;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.model.Prestamo;
import com.biblioteca.service.LibroService;
import com.biblioteca.service.UsuarioService;
import com.biblioteca.service.PrestamoService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")

public class Controller {
    

    @Autowired
    private UsuarioService usuarioService;

    @Autowired
    private LibroService libroService;

    @Autowired
    private PrestamoService prestamoService;

    // Libros

    // Consultar todos los libros (acceso público)
    @GetMapping("/libros")
    public List<Libro> obtenerLibros() {
        return libroService.listarLibros();
    }

    // Registrar libro (solo bibliotecario)
    @PostMapping("/libros")
    public ResponseEntity<?> registrarLibro(@RequestBody Libro libro, @RequestParam String correoUsuario) {
        String respuesta = libroService.registrarLibro(libro, correoUsuario);
        return ResponseEntity.ok(respuesta);
    }

    // Usuarios

    // Registro de usuario
    @PostMapping("/usuarios/registro")
    public ResponseEntity<String> registrarUsuario(@RequestBody Usuario usuario) {
        String respuesta = usuarioService.registrarUsuario(usuario);
        return ResponseEntity.ok(respuesta);
    }

    // Login de usuario
    @PostMapping("/usuarios/login")
    public ResponseEntity<String> loginUsuario(@RequestBody Usuario usuario) {
        String respuesta = usuarioService.autenticarUsuario(usuario.getCorreo(), usuario.getContrasena());
        return ResponseEntity.ok(respuesta);
    }

    /* // Préstamos
    @PostMapping("/prestamos")
    public ResponseEntity<?> crearPrestamo(@RequestParam Long usuarioId, @RequestParam String isbn) {
        return prestamoService.crearPrestamo(usuarioId, isbn);
    }

    @GetMapping("/prestamos")
    public List<Prestamo> obtenerPrestamos() {
        return prestamoService.obtenerPrestamos();
    }

    @PostMapping("/prestamos/devolver")
    public ResponseEntity<?> devolverPrestamo(@RequestParam Long prestamoId) {
        return prestamoService.devolverPrestamo(prestamoId);
    }

    @GetMapping("/prestamos/usuario/{usuarioId}")
    public List<Prestamo> obtenerPrestamosPorUsuario(@PathVariable Long usuarioId) {
        return prestamoService.obtenerPrestamosPorUsuario(usuarioId);
    } */
}
