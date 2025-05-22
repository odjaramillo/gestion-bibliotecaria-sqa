package com.biblioteca.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class ComentarioResena {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Resena resena;

    @ManyToOne(optional = false)
    private Usuario usuario;

    @Column(nullable = false, length = 1000)
    private String texto;

    private LocalDateTime fecha = LocalDateTime.now();

    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }   
    public Resena getResena() {
        return resena;
    }
    public void setResena(Resena resena) {
        this.resena = resena;
    }
    public Usuario getUsuario() {
        return usuario;
    }
    public void setUsuario(Usuario usuario) {
        this.usuario = usuario;
    }
    public String getTexto() {
        return texto;
    }
    public void setTexto(String texto) {
        this.texto = texto;
    }
    public LocalDateTime getFecha() {
        return fecha;
    }
    public void setFecha(LocalDateTime fecha) {
        this.fecha = fecha;
    }

    public ComentarioResena() {
    }

    public ComentarioResena(Resena resena, Usuario usuario, String texto, LocalDateTime fecha) {
        this.resena = resena;
        this.usuario = usuario;
        this.texto = texto;
        this.fecha = fecha;
    }

    @Override
    public String toString() {
        return "ComentarioResena{" +
                "id=" + id +
                ", resena=" + resena +
                ", usuario=" + usuario +
                ", texto='" + texto + '\'' +
                ", fecha=" + fecha +
                '}';
    }
}