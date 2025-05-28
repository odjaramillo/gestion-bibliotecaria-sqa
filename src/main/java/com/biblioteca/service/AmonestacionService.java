package com.biblioteca.service;

import com.biblioteca.model.Amonestacion;
import com.biblioteca.model.Usuario;
import com.biblioteca.model.Prestamo;
import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.repository.UsuarioRepository;
import com.biblioteca.repository.PrestamoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AmonestacionService {

    @Autowired
    private AmonestacionRepository amonestacionRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private PrestamoRepository prestamoRepository;

    public List<Amonestacion> findAll() {
        return amonestacionRepository.findAll();
    }

    public List<Amonestacion> findByUsuario(Integer usuarioId) {
        return amonestacionRepository.findByUsuarioId(usuarioId);
    }

    public List<Amonestacion> findByPrestamo(Integer prestamoId) {
        return amonestacionRepository.findByPrestamoId(prestamoId);
    }

    public Amonestacion save(Amonestacion amonestacion, Integer usuarioId, Integer prestamoId) {
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(usuarioId);
        Optional<Prestamo> prestamoOpt = prestamoRepository.findById(prestamoId);
        if (usuarioOpt.isEmpty() || prestamoOpt.isEmpty()) {
            throw new RuntimeException("Usuario o préstamo no encontrado");
        }
        amonestacion.setUsuario(usuarioOpt.get());
        amonestacion.setPrestamo(prestamoOpt.get());
        return amonestacionRepository.save(amonestacion);
    }

    public void eliminarAmonestacion(Integer id) {
        amonestacionRepository.deleteById(id);
    }

    public boolean usuarioTieneAmonestacionesNoVerificadas(Integer usuarioId) {
        return amonestacionRepository.existsByUsuarioIdAndVerificadaFalse(usuarioId);
    }

    public Amonestacion findById(Integer id) {
        return amonestacionRepository.findById(id).orElse(null);
    }
    

    public Amonestacion guardar(Amonestacion amonestacion) {
        return amonestacionRepository.save(amonestacion);
    }

}