package com.biblioteca.service;

import com.biblioteca.model.Libro;
import com.biblioteca.repository.LibroRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LibroService {

    @Autowired
    private LibroRepository libroRepository;

    public List<Libro> listarLibros() {
        return libroRepository.findAll();
    }

    public Optional<Libro> buscarPorIsbn(String isbn) {
        return libroRepository.findByIsbn(isbn);
    }

    public String registrarLibro(Libro libro) {
        if (libroRepository.findByIsbn(libro.getIsbn()).isPresent()) {
            return "El libro con ese ISBN ya existe.";
        }
        if (libro.getCantidad() <= 0) {
            return "Debe haber al menos una copia física del libro.";
        }
        libroRepository.save(libro);
        return "Libro registrado exitosamente.";
    }
}