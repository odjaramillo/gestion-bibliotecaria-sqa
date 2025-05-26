package com.biblioteca.controller;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.model.Prestamo;
import com.biblioteca.model.Resena;
import com.biblioteca.model.ComentarioResena;
import com.biblioteca.model.Amonestacion;

import com.biblioteca.dto.ResenaRequest;
import com.biblioteca.dto.ComentarioResenaRequest;
import com.biblioteca.dto.PrestamoRequest;
import com.biblioteca.dto.AmonestacionDTO;

import com.biblioteca.service.ComentarioResenaService;
import com.biblioteca.service.LibroService;
import com.biblioteca.service.UsuarioService;
import com.biblioteca.service.PrestamoService;
import com.biblioteca.service.ResenaService;
import com.biblioteca.service.AmonestacionService;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

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

     @Autowired
    private ResenaService resenaService;

    @Autowired
    private ComentarioResenaService comentarioResenaService;

    @Autowired
    private AmonestacionService amonestacionService;

    // Libros

    // Consultar todos los libros
    @GetMapping("/libros")
    public List<Libro> obtenerLibros() {
        return libroService.listarLibros();
    }

    // Registrar libro (solo bibliotecario)
    @PostMapping("/libros")
    public ResponseEntity<?> registrarLibro(
        @RequestPart("libro") Libro libro,
        @RequestPart(value = "imagen", required = false) MultipartFile imagen,
        @RequestParam String correoUsuario
    ) {
        String respuesta = libroService.registrarLibroConImagen(libro, imagen, correoUsuario);
        return ResponseEntity.ok(respuesta);
    }

    // Usuarios

    // Registro de usuario
    @PostMapping("/usuarios/registro")
    public ResponseEntity<String> registrarUsuario(@RequestBody Usuario usuario) {
        String respuesta = usuarioService.registrarUsuario(usuario);
        return ResponseEntity.ok(respuesta);
    }

    @GetMapping("/usuarios/me")
        public ResponseEntity<Usuario> getUsuarioAutenticado(org.springframework.security.core.Authentication authentication) {
            String correo = authentication.getName();
            Usuario usuario = usuarioService.buscarPorCorreo(correo);
            usuario.setContrasena(null);
            return ResponseEntity.ok(usuario);
        }

    // Login de usuario

    @PostMapping("/login")
    public ResponseEntity<?> loginUsuario(@RequestBody Usuario usuario) {
        Usuario usuarioAutenticado = usuarioService.autenticarYObtenerUsuario(usuario.getCorreo(), usuario.getContrasena());
        if (usuarioAutenticado != null) {
            // No devuelvas la contraseña
            Usuario respuesta = new Usuario();
            respuesta.setId(usuarioAutenticado.getId());
            respuesta.setNombre(usuarioAutenticado.getNombre());
            respuesta.setCorreo(usuarioAutenticado.getCorreo());
            respuesta.setRol(usuarioAutenticado.getRol());
            return ResponseEntity.ok(respuesta);
        } else {
            return ResponseEntity.status(401).body("Credenciales inválidas");
        }
    }

    /* @PostMapping("/login")
    public ResponseEntity<String> loginUsuario(@RequestBody Usuario usuario) {
        String respuesta = usuarioService.autenticarUsuario(usuario.getCorreo(), usuario.getContrasena());
        return ResponseEntity.ok(respuesta);
    } */

    // Préstamos

    // Crear préstamo

    @PostMapping("/prestar")
    public ResponseEntity<String> registrarPrestamo(@RequestBody PrestamoRequest request) {
        String respuesta = prestamoService.crearPrestamo(request.getCorreoUsuario(), request.getIsbn(), request.getFechaPrestamo());
        if (respuesta.startsWith("Préstamo registrado")) {
            return ResponseEntity.ok(respuesta);
        } else {
            return ResponseEntity.badRequest().body(respuesta);
        }
    }

    /* @PostMapping("/prestamos")
    public ResponseEntity<String> crearPrestamo(@RequestBody PrestamoRequest request) {
        String respuesta = prestamoService.crearPrestamo(request.getUsuarioId(), request.getIsbn());
        return ResponseEntity.ok(respuesta);
    } */

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

    // Reseñas

    // Crear reseña
    @PostMapping("/resenas")
    public ResponseEntity<Resena> crearResena(@RequestBody ResenaRequest request) {
        Resena resena = resenaService.save(request.getLibroId(), request.getUsuarioId(), request.getTexto());
        return ResponseEntity.ok(resena);
    }

    // Listar reseñas de un libro
    @GetMapping("/resenas/libro/{libroId}")
    public List<Resena> listarResenasPorLibro(@PathVariable Integer libroId) {
        return resenaService.findByLibro(libroId);
    }

    // Crear comentario en reseña
    @PostMapping("/comentarios-resena")
    public ResponseEntity<ComentarioResena> crearComentarioResena(@RequestBody ComentarioResenaRequest request) {
        ComentarioResena comentario = comentarioResenaService.save(request.getResenaId(), request.getUsuarioId(), request.getTexto());
        return ResponseEntity.ok(comentario);
    }

    // Listar comentarios de una reseña
    @GetMapping("/comentarios-resena/resena/{resenaId}")
    public List<ComentarioResena> listarComentariosPorResena(@PathVariable Integer resenaId) {
        return comentarioResenaService.findByResena(resenaId);
    }


    // Amonestaciones

    @GetMapping("/amonestaciones")
    public List<Amonestacion> listarAmonestaciones() {
        return amonestacionService.findAll();
    }

    @GetMapping("/amonestaciones/usuario/{usuarioId}")
    public List<Amonestacion> listarAmonestacionesPorUsuario(@PathVariable Integer usuarioId) {
        return amonestacionService.findByUsuario(usuarioId);
    }

    @GetMapping("/amonestaciones/prestamo/{prestamoId}")
    public List<Amonestacion> listarAmonestacionesPorPrestamo(@PathVariable Integer prestamoId) {
        return amonestacionService.findByPrestamo(prestamoId);
    }

    @PostMapping("/amonestaciones")
    public Amonestacion crearAmonestacion(@RequestBody AmonestacionDTO dto) {
        return amonestacionService.save(dto.toAmonestacion(), dto.getUsuarioId(), dto.getPrestamoId());
    }

    @DeleteMapping("/amonestaciones/{id}")
    public void eliminarAmonestacion(@PathVariable Integer id) {
        amonestacionService.eliminarAmonestacion(id);
    }
}
