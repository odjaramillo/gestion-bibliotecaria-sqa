package com.biblioteca.service;

import com.biblioteca.model.Resena;
import com.biblioteca.repository.ResenaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ResenaService {

    @Autowired
    private ResenaRepository resenaRepository;

    public List<Resena> findAll() {
        return resenaRepository.findAll();
    }

    public Resena save(Resena resena) {
        return resenaRepository.save(resena);
    }

    // Otros métodos según tu lógica de negocio
}