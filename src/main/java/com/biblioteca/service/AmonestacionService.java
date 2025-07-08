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

    // Eliminar amonestación (solo bibliotecarios)
    public String eliminarAmonestacion(Integer amonestacionId, String usuarioRol) {
        // Verificar que el usuario sea bibliotecario
        if (!"BIBLIOTECARIO".equals(usuarioRol)) {
            return "Solo los bibliotecarios pueden eliminar amonestaciones.";
        }

        if (!amonestacionRepository.existsById(amonestacionId)) {
            return "Amonestación no encontrada.";
        }

        amonestacionRepository.deleteById(amonestacionId);
        return "Amonestación eliminada con éxito.";
    }
}