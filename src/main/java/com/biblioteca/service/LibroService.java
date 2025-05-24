package com.biblioteca.service;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LibroService {

    @Autowired
    private LibroRepository libroRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    // Listar todos los libros
    public List<Libro> listarLibros() {
        return libroRepository.findAll();
    }

    // Registrar un libro (solo bibliotecario)
    public String registrarLibro(Libro libro, String correoUsuario) {
        Usuario usuario = usuarioRepository.findByCorreo(correoUsuario)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));
        if (!"BIBLIOTECARIO".equals(usuario.getRol())) {
            throw new AccessDeniedException("No tienes permisos para esta acción.");
        }
        if (libroRepository.findByIsbn(libro.getIsbn()).isPresent()) {
            return "El libro con ese ISBN ya existe.";
        }
        // Validación de 13 dígitos
        if (libro.getIsbn() == null || String.valueOf(libro.getIsbn()).length() != 13) {
            return "El ISBN debe tener exactamente 13 dígitos.";
        }
        if (libro.getCantidad() <= 0) {
            return "Debe haber al menos una copia física del libro.";
        }
        libroRepository.save(libro);
        return "Libro registrado exitosamente.";
    }
}