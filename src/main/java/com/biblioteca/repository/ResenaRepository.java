package com.biblioteca.repository;

import com.biblioteca.model.Resena;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResenaRepository extends JpaRepository<Resena, Long> {
}