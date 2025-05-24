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

    // Consultar todos los libros
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

    // Préstamos

    // Crear préstamo
    @PostMapping("/prestamos")
    public ResponseEntity<String> crearPrestamo(@RequestParam Integer usuarioId, @RequestParam Long isbn) {
        String respuesta = prestamoService.crearPrestamo(usuarioId, isbn);
        return ResponseEntity.ok(respuesta);
    }

    // Devolver préstamo
    @PostMapping("/prestamos/devolver")
    public ResponseEntity<String> devolverPrestamo(@RequestParam Integer prestamoId) {
        String respuesta = prestamoService.devolverPrestamo(prestamoId);
        return ResponseEntity.ok(respuesta);
    }

    // Listar todos los préstamos
    @GetMapping("/prestamos")
    public List<Prestamo> obtenerPrestamos() {
        return prestamoService.obtenerPrestamos();
    }

    // Listar préstamos activos
    @GetMapping("/prestamos/activos")
    public List<Prestamo> obtenerPrestamosActivos() {
        return prestamoService.obtenerPrestamosActivos();
    }

    // Listar préstamos activos de un usuario
    @GetMapping("/prestamos/usuario/{usuarioId}")
    public List<Prestamo> obtenerPrestamosPorUsuario(@PathVariable Integer usuarioId) {
        return prestamoService.obtenerPrestamosPorUsuario(usuarioId);
    }
}
