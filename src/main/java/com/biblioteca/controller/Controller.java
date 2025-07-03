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
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Map;

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
            @RequestParam String correoUsuario) {
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
    public ResponseEntity<Usuario> getUsuarioAutenticado(
            org.springframework.security.core.Authentication authentication) {
        String correo = authentication.getName();
        Usuario usuario = usuarioService.buscarPorCorreo(correo);
        usuario.setContrasena(null);
        return ResponseEntity.ok(usuario);
    }

    // Login de usuario

    @PostMapping("/login")
    public ResponseEntity<?> loginUsuario(@RequestBody Usuario usuario) {
        Usuario usuarioAutenticado = usuarioService.autenticarYObtenerUsuario(usuario.getCorreo(),
                usuario.getContrasena());
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

    @PutMapping("/usuarios/nombre")
    public ResponseEntity<?> actualizarNombreUsuario(
            org.springframework.security.core.Authentication authentication,
            @RequestBody Map<String, String> body) {
        String correo = authentication.getName();
        Usuario usuario = usuarioService.buscarPorCorreo(correo);
        if (usuario == null) {
            return ResponseEntity.status(404).body("Usuario no encontrado");
        }
        String nuevoNombre = body.get("nombre");
        usuario.setNombre(nuevoNombre);
        usuarioService.guardar(usuario);
        return ResponseEntity.ok("Nombre actualizado correctamente");
    }

    // Cambiar contraseña
    @PutMapping("/usuarios/contrasena")
    public ResponseEntity<String> cambiarContrasena(
            org.springframework.security.core.Authentication authentication,
            @RequestBody Map<String, String> body) {
        String correo = authentication.getName();
        String contrasenaActual = body.get("contrasenaActual");
        String contrasenaNueva = body.get("contrasenaNueva");

        String resultado = usuarioService.cambiarContrasena(correo, contrasenaActual, contrasenaNueva);
        if (resultado.equals("Contraseña actualizada correctamente.")) {
            return ResponseEntity.ok(resultado);
        } else {
            return ResponseEntity.status(400).body(resultado);
        }
    }

    // Eliminar perfil
    @DeleteMapping("/usuarios")
    public ResponseEntity<String> eliminarPerfil(
            org.springframework.security.core.Authentication authentication) {
        String correo = authentication.getName();
        usuarioService.eliminarUsuario(correo);
        return ResponseEntity.ok("Perfil eliminado correctamente.");
    }

    // Préstamos

    // Crear préstamo
    @PostMapping("/prestar")
    public ResponseEntity<String> registrarPrestamo(@RequestBody PrestamoRequest request) {
        String respuesta = prestamoService.crearPrestamo(request.getCorreoUsuario(), request.getIsbn(),
                request.getFechaPrestamo());
        if (respuesta.startsWith("Préstamo registrado")) {
            return ResponseEntity.ok(respuesta);
        } else {
            return ResponseEntity.badRequest().body(respuesta);
        }
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

    // Reseñas

    // Crear reseña
    @PostMapping("/resenas")
    public ResponseEntity<Resena> crearResena(@RequestBody ResenaRequest request) {
        Resena resena = resenaService.save(request.getLibroId(), request.getUsuarioId(), request.getTexto());
        return ResponseEntity.ok(resena);
    }

    @GetMapping("/resenas/libro/{libroId}")
    public List<Resena> listarResenasPorLibro(@PathVariable Integer libroId) {
        return resenaService.findByLibro(libroId);
    }

    @PostMapping("/comentarios-resena")
    public ResponseEntity<ComentarioResena> crearComentarioResena(@RequestBody ComentarioResenaRequest request) {
        ComentarioResena comentario = comentarioResenaService.save(request.getResenaId(), request.getUsuarioId(),
                request.getTexto());
        return ResponseEntity.ok(comentario);
    }

    @GetMapping("/comentarios-resena/resena/{resenaId}")
    public List<ComentarioResena> listarComentariosPorResena(@PathVariable Integer resenaId) {
        return comentarioResenaService.findByResena(resenaId);
    }

    // Amonestaciones
    @GetMapping("/amonestaciones-usuario/mis-amonestaciones")
    public ResponseEntity<?> getAmonestacionesUsuario(Authentication authentication) {
        String correo = authentication.getName();
        Usuario usuario = usuarioService.buscarPorCorreo(correo);
        if (usuario == null) {
            return ResponseEntity.status(401).body("Usuario no autenticado");
        }
        List<Amonestacion> amonestaciones = amonestacionService.findByUsuario(usuario.getId());
        return ResponseEntity.ok(Map.of(
                "tieneAmonestacion", amonestaciones != null && !amonestaciones.isEmpty(),
                "amonestaciones", amonestaciones));
    }

    @PutMapping("/amonestaciones-usuario/pagar")
    public ResponseEntity<?> pagarAmonestacion(
            Authentication authentication,
            @RequestBody Map<String, Object> body) {
        String correo = authentication.getName();
        Usuario usuario = usuarioService.buscarPorCorreo(correo);
        if (usuario == null) {
            return ResponseEntity.status(401).body("Usuario no autenticado");
        }
        Integer amonestacionId = (Integer) body.get("amonestacionId");
        String metodoPago = (String) body.get("metodoPago");
        String comprobantePago = (String) body.get("comprobantePago");
        Amonestacion amonestacion = amonestacionService.findById(amonestacionId);
        if (amonestacion == null || !amonestacion.getUsuario().getId().equals(usuario.getId())) {
            return ResponseEntity.status(403).body("No autorizado");
        }
        amonestacion.setMetodoPago(metodoPago);
        amonestacion.setComprobantePago(comprobantePago);
        amonestacion.setPagada(true);
        amonestacionService.guardar(amonestacion);
        return ResponseEntity.ok("Amonestación pagada correctamente");
    }

    @GetMapping("/amonestaciones-usuario/todas")
    public List<Amonestacion> getTodasAmonestaciones() {
        return amonestacionService.findAll();
    }

    @PutMapping("/amonestaciones-usuario/verificar/{id}")
    public ResponseEntity<?> verificarAmonestacion(@PathVariable Integer id) {
        Amonestacion amonestacion = amonestacionService.findById(id);
        if (amonestacion == null) {
            return ResponseEntity.status(404).body("Amonestación no encontrada");
        }
        amonestacion.setVerificada(true);
        amonestacionService.guardar(amonestacion);
        return ResponseEntity.ok("Amonestación verificada");
    }
}
