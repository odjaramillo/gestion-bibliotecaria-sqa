package com.biblioteca.repository;

import com.biblioteca.model.ComentarioResena;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ComentarioResenaRepository extends JpaRepository<ComentarioResena, Integer> {
    List<ComentarioResena> findByResenaId(Integer resenaId);

    List<ComentarioResena> findByUsuarioId(Integer usuarioId);
}