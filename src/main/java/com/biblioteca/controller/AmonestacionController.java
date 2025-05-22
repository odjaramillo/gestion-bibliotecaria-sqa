package com.biblioteca.controller;

import com.biblioteca.model.Amonestacion;
import com.biblioteca.repository.AmonestacionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/amonestaciones")
public class AmonestacionController {

    @Autowired
    private AmonestacionRepository amonestacionRepository;

    @GetMapping
    public List<Amonestacion> getAll() {
        return amonestacionRepository.findAll();
    }

    @PostMapping
    public Amonestacion create(@RequestBody Amonestacion amonestacion) {
        return amonestacionRepository.save(amonestacion);
    }

    // Puedes agregar métodos para actualizar/verificar pagos, etc.
}