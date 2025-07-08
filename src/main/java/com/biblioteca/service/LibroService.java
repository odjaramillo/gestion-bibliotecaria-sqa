package com.biblioteca.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.UsuarioRepository;

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
    public String registrarLibroConImagen(Libro libro, MultipartFile imagen, String correoUsuario) {
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
        if (imagen != null && !imagen.isEmpty()) {
        try {
            libro.setImagen(imagen.getBytes());
        } catch (Exception e) {
            return "Error al procesar la imagen.";
            }
        }
        libroRepository.save(libro);
        return "Libro registrado exitosamente.";
    }

        // === FUNCIONES CLAVE PARA BUSCAR Y MODIFICAR POR ISBN ===

    // 1. Función para BUSCAR un libro por su ISBN (para el GET)
    public Optional<Libro> buscarLibroPorIsbn(Long isbn) {
        return libroRepository.findByIsbn(isbn);
    }

    // 2. Función para MODIFICAR un libro por su ISBN (para el PUT)
    public String actualizarLibroPorIsbn(Long isbn, Libro datosActualizados, String correoUsuario) {
        Usuario usuario = usuarioRepository.findByCorreo(correoUsuario).orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        if (!"BIBLIOTECARIO".equals(usuario.getRol())) {
            throw new AccessDeniedException("No tienes permisos para esta acción.");
        }

        Libro libroExistente = libroRepository.findByIsbn(isbn)
            .orElseThrow(() -> new RuntimeException("Libro no encontrado por ISBN"));

        // Actualiza solo los campos que deberían ser modificables
        libroExistente.setTitulo(datosActualizados.getTitulo());
        libroExistente.setAutor(datosActualizados.getAutor());
        libroExistente.setGenero(datosActualizados.getGenero());
        libroExistente.setEditorial(datosActualizados.getEditorial()); // ¡Asegúrate de incluir todos los campos que quieres que se puedan modificar!
        libroExistente.setAnio(datosActualizados.getAnio());
        libroExistente.setCantidad(datosActualizados.getCantidad());
        libroExistente.setSinopsis(datosActualizados.getSinopsis());

        libroRepository.save(libroExistente);
        return "Libro actualizado exitosamente.";
    }

    public String eliminarLibroPorIsbn(Long isbn, String correoUsuario) {
        Usuario usuario = usuarioRepository.findByCorreo(correoUsuario)
            .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        if (!"BIBLIOTECARIO".equals(usuario.getRol())) {
            throw new AccessDeniedException("No tienes permisos para esta acción.");
        }

        Libro libro = libroRepository.findByIsbn(isbn)
            .orElseThrow(() -> new RuntimeException("Libro no encontrado por ISBN"));

        libroRepository.delete(libro);
        return "Libro eliminado correctamente.";
    }
}