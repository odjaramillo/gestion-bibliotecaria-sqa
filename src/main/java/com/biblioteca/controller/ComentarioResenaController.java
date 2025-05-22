package com.biblioteca.controller;

import com.biblioteca.model.ComentarioResena;
import com.biblioteca.repository.ComentarioResenaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/comentarios-resena")
public class ComentarioResenaController {

    @Autowired
    private ComentarioResenaRepository comentarioResenaRepository;

    @GetMapping
    public List<ComentarioResena> getAll() {
        return comentarioResenaRepository.findAll();
    }

    @PostMapping
    public ComentarioResena create(@RequestBody ComentarioResena comentarioResena) {
        return comentarioResenaRepository.save(comentarioResena);
    }
}