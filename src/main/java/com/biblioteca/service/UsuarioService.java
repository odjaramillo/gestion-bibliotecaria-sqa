package com.biblioteca.service;

import com.biblioteca.model.Usuario;
import com.biblioteca.model.Resena;
import com.biblioteca.model.ComentarioResena;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.repository.PrestamoRepository;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.ResenaRepository;
import com.biblioteca.repository.ComentarioResenaRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import jakarta.transaction.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class UsuarioService {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private PrestamoRepository prestamoRepository;

    @Autowired
    private AmonestacionRepository amonestacionRepository;

    @Autowired
    private ResenaRepository resenaRepository;

    @Autowired
    private ComentarioResenaRepository comentarioResenaRepository;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    // Registro de usuario
    public String registrarUsuario(Usuario usuario) {
        if (usuarioRepository.existsByCorreo(usuario.getCorreo())) {
            return "Correo ya registrado.";
        }
        usuario.setContrasena(passwordEncoder.encode(usuario.getContrasena()));
        if (usuario.getRol() == null || usuario.getRol().isEmpty()) {
            usuario.setRol("USUARIO");
        }
        usuarioRepository.save(usuario);
        return "Usuario registrado con éxito.";
    }

    // Autenticación de usuario
    public Usuario autenticarYObtenerUsuario(String correo, String contrasena) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findByCorreo(correo);
        if (usuarioOpt.isPresent()) {
            Usuario usuario = usuarioOpt.get();
            if (passwordEncoder.matches(contrasena, usuario.getContrasena())) {
                return usuario;
            }
        }
        return null;
    }

    public Usuario buscarPorCorreo(String correo) {
        return usuarioRepository.findByCorreo(correo).orElse(null);
    }

    public void guardar(Usuario usuario) {
        usuarioRepository.save(usuario);
    }

    public String cambiarContrasena(String correo, String contrasenaActual, String contrasenaNueva) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findByCorreo(correo);
        if (usuarioOpt.isEmpty()) {
            return "Usuario no encontrado.";
        }
        Usuario usuario = usuarioOpt.get();

        if (!passwordEncoder.matches(contrasenaActual, usuario.getContrasena())) {
            return "La contraseña actual no es correcta.";
        }

        usuario.setContrasena(passwordEncoder.encode(contrasenaNueva));
        usuarioRepository.save(usuario);
        return "Contraseña actualizada correctamente.";
    }

   @Transactional
    public void eliminarUsuario(String correo) {
        Usuario usuario = usuarioRepository.findByCorreo(correo)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        // Verificar préstamos activos
        boolean tienePrestamos = prestamoRepository.existsByUsuarioIdAndFechaDevolucionIsNull(usuario.getId());
        if (tienePrestamos) {
            throw new RuntimeException("No puedes eliminar tu cuenta con préstamos activos.");
        }

        // Verificar amonestaciones no pagadas
        boolean tieneAmonestaciones = amonestacionRepository.existsByUsuarioIdAndPagadaFalse(usuario.getId());
        if (tieneAmonestaciones) {
            throw new RuntimeException("No puedes eliminar tu cuenta con amonestaciones pendientes.");
        }

        // Eliminar comentarios asociados
        List<ComentarioResena> comentarios = comentarioResenaRepository.findByUsuarioId(usuario.getId());
        comentarioResenaRepository.deleteAll(comentarios);

        // Eliminar reseñas asociadas
        List<Resena> resenas = resenaRepository.findByUsuarioId(usuario.getId());
        resenaRepository.deleteAll(resenas);

        // Eliminar usuario
        usuarioRepository.delete(usuario);
    }
}
