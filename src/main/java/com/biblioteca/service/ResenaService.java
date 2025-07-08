package com.biblioteca.service;

import com.biblioteca.model.Resena;
import com.biblioteca.model.Libro;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.ResenaRepository;
import com.biblioteca.repository.LibroRepository;
import com.biblioteca.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ResenaService {

    @Autowired
    private ResenaRepository resenaRepository;

    @Autowired
    private LibroRepository libroRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    public List<Resena> findByLibro(Integer libroId) {
        return resenaRepository.findByLibroId(libroId);
    }

    public Resena save(Integer libroId, Integer usuarioId, String texto) {
        Optional<Libro> libroOpt = libroRepository.findById(libroId.intValue());
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(usuarioId);
        if (libroOpt.isEmpty() || usuarioOpt.isEmpty()) {
            throw new RuntimeException("Libro o usuario no encontrado");
        }
        Resena resena = new Resena();
        resena.setLibro(libroOpt.get());
        resena.setUsuario(usuarioOpt.get());
        resena.setTexto(texto);
        resena.setFecha(java.time.LocalDateTime.now());
        return resenaRepository.save(resena);
    }

    public Resena findById(Integer id) {
        return resenaRepository.findById(id).orElse(null);
    }

    public Resena guardar(Resena resena) {
        return resenaRepository.save(resena);
    }

    public void eliminar(Resena resena) {
        resenaRepository.delete(resena);
    }
}