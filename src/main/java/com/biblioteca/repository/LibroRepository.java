package com.biblioteca.repository;

import com.biblioteca.model.Libro;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface LibroRepository extends JpaRepository<Libro, Integer> {
    Optional<Libro> findByIsbn(Long isbn);
}

//findByIsbn es para buscar libros únicos por código.

//Optional se usa para evitar null y manejar el resultado de forma segura.