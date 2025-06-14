package com.biblioteca.service;

import com.biblioteca.model.Amonestacion;
import com.biblioteca.repository.AmonestacionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AmonestacionService {

    @Autowired
    private AmonestacionRepository amonestacionRepository;

    public List<Amonestacion> findAll() {
        return amonestacionRepository.findAll();
    }

    public List<Amonestacion> findByUsuario(Integer usuarioId) {
        return amonestacionRepository.findByUsuarioId(usuarioId);
    }

    public Amonestacion findById(Integer id) {
        return amonestacionRepository.findById(id).orElse(null);
    }
    

    public Amonestacion guardar(Amonestacion amonestacion) {
        return amonestacionRepository.save(amonestacion);
    }

}