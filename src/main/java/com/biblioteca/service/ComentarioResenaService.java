package com.biblioteca.service;

import com.biblioteca.model.ComentarioResena;
import com.biblioteca.repository.ComentarioResenaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ComentarioResenaService {

    @Autowired
    private ComentarioResenaRepository comentarioResenaRepository;

    public List<ComentarioResena> findAll() {
        return comentarioResenaRepository.findAll();
    }

    public ComentarioResena save(ComentarioResena comentarioResena) {
        return comentarioResenaRepository.save(comentarioResena);
    }

    // Otros métodos según tu lógica de negocio
}