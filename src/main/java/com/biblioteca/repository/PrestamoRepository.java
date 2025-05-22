package com.biblioteca.repository;

import com.biblioteca.model.Prestamo;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PrestamoRepository extends JpaRepository<Prestamo, Long> {
    long countByUsuarioIdAndFechaDevolucionIsNull(Long usuarioId);
}

//countByUsuarioIdAndFechaDevolucionIsNull sirve para contar los préstamos activos de un usuario (que no ha devuelto aún los libros).