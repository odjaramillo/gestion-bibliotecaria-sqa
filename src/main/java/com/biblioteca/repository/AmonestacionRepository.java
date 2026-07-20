package com.biblioteca.repository;

import com.biblioteca.model.Amonestacion;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AmonestacionRepository extends JpaRepository<Amonestacion, Integer> {
    List<Amonestacion> findByUsuarioId(Integer usuarioId);
    List<Amonestacion> findByPrestamoId(Integer prestamoId);
    boolean existsByUsuarioIdAndVerificadaFalse(Integer usuarioId);

    boolean existsByUsuarioIdAndPagadaFalse(Integer usuarioId);
}