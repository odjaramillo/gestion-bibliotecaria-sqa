package com.biblioteca.repository;

import com.biblioteca.model.Resena;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ResenaRepository extends JpaRepository<Resena, Integer> {
    List<Resena> findByLibroId(Integer libroId);

    List<Resena> findByUsuarioId(Integer usuarioId);
}