package com.biblioteca.controller;

import com.biblioteca.model.Libro;
import com.biblioteca.repository.LibroRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/libros")
public class LibroController {

    @Autowired
    private LibroRepository libroRepository;

    @GetMapping
    public List<Libro> obtenerTodos() {
        return libroRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<?> registrarLibro(@RequestBody Libro libro) {
        if (libroRepository.findByIsbn(libro.getIsbn()).isPresent()) {
            return ResponseEntity.badRequest().body("El libro con ese ISBN ya existe.");
        }
        if (libro.getCantidad() <= 0) {
            return ResponseEntity.badRequest().body("Debe haber al menos una copia física del libro.");
        }
        libroRepository.save(libro);
        return ResponseEntity.ok("Libro registrado exitosamente.");
    }
}