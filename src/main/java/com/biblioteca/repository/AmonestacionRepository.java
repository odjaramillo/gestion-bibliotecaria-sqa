package com.biblioteca.repository;

import com.biblioteca.model.Amonestacion;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AmonestacionRepository extends JpaRepository<Amonestacion, Long> {
}