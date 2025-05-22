package com.biblioteca.controller;

import com.biblioteca.model.Resena;
import com.biblioteca.repository.ResenaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/resenas")
public class ResenaController {

    @Autowired
    private ResenaRepository resenaRepository;

    @GetMapping
    public List<Resena> getAll() {
        return resenaRepository.findAll();
    }

    @PostMapping
    public Resena create(@RequestBody Resena resena) {
        return resenaRepository.save(resena);
    }
}