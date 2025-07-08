package com.biblioteca.repository;

import com.biblioteca.model.Prestamo;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PrestamoRepository extends JpaRepository<Prestamo, Integer> {
    long countByUsuarioIdAndFechaDevolucionIsNull(Integer usuarioId);
    List<Prestamo> findByUsuarioIdAndFechaDevolucionIsNull(Integer usuarioId);
    List<Prestamo> findByFechaDevolucionIsNull();

    boolean existsByUsuarioIdAndFechaDevolucionIsNull(Integer usuarioId);

}