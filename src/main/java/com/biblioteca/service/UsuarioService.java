package com.biblioteca.service;

import com.biblioteca.model.Usuario;
import com.biblioteca.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UsuarioService {

    @Autowired
    private UsuarioRepository usuarioRepository;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    // Registro de usuario
    public String registrarUsuario(Usuario usuario) {
        if (usuarioRepository.existsByCorreo(usuario.getCorreo())) {
            return "Correo ya registrado.";
        }
        // Encripta la contraseña antes de guardar
        usuario.setContrasena(passwordEncoder.encode(usuario.getContrasena()));
        // Asigna rol USUARIO
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
        System.out.println("Contraseña recibida: " + contrasena);
        System.out.println("Contraseña en BD: " + usuario.getContrasena());
        System.out.println("BCrypt match: " + passwordEncoder.matches(contrasena, usuario.getContrasena()));
        if (passwordEncoder.matches(contrasena, usuario.getContrasena())) {
            return usuario;
        }
    }
    return null;

    }

    public Usuario buscarPorCorreo(String correo) {
            return usuarioRepository.findByCorreo(correo).orElse(null);
        }

   /*  public String autenticarUsuario(String correo, String contrasena) {
        return usuarioRepository.findByCorreo(correo)
                .map(usuario -> {
                    if (passwordEncoder.matches(contrasena, usuario.getContrasena())) {
                        return "Login exitoso. Rol: " + usuario.getRol();
                    } else {
                        return "Contraseña incorrecta.";
                    }
                })
                .orElse("Usuario no encontrado.");
                
    } */
}