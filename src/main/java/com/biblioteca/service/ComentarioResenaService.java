package com.biblioteca.service;

import com.biblioteca.model.ComentarioResena;
import com.biblioteca.model.Resena;
import com.biblioteca.model.Usuario;
import com.biblioteca.repository.ComentarioResenaRepository;
import com.biblioteca.repository.ResenaRepository;
import com.biblioteca.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ComentarioResenaService {

    @Autowired
    private ComentarioResenaRepository comentarioResenaRepository;

    @Autowired
    private ResenaRepository resenaRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    public List<ComentarioResena> findByResena(Integer resenaId) {
        return comentarioResenaRepository.findByResenaId(resenaId);
    }

    public ComentarioResena findById(Integer id) {
        return comentarioResenaRepository.findById(id).orElse(null);
    }

    public ComentarioResena save(Integer resenaId, Integer usuarioId, String texto) {
        Optional<Resena> resenaOpt = resenaRepository.findById(resenaId);
        Optional<Usuario> usuarioOpt = usuarioRepository.findById(usuarioId);
        if (resenaOpt.isEmpty() || usuarioOpt.isEmpty()) {
            throw new RuntimeException("Reseña o usuario no encontrado");
        }
        ComentarioResena comentario = new ComentarioResena();
        comentario.setResena(resenaOpt.get());
        comentario.setUsuario(usuarioOpt.get());
        comentario.setTexto(texto);
        comentario.setFecha(java.time.LocalDateTime.now());
        return comentarioResenaRepository.save(comentario);
    }

    public ComentarioResena guardar(ComentarioResena comentario) {
        return comentarioResenaRepository.save(comentario);
    }

    public void eliminar(ComentarioResena comentario) {
        comentarioResenaRepository.delete(comentario);
    }

    public void eliminarPorResena(Resena resena) {
        List<ComentarioResena> comentarios = comentarioResenaRepository.findByResenaId(resena.getId());
        comentarioResenaRepository.deleteAll(comentarios);
    }
}