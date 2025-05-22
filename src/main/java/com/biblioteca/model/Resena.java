package com.biblioteca.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class Resena {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    private Libro libro;

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
    public Libro getLibro() {
        return libro;
    }
    public void setLibro(Libro libro) {
        this.libro = libro;
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

    public Resena() {
    }
    public Resena(Libro libro, Usuario usuario, String texto, LocalDateTime fecha) {
        this.libro = libro;
        this.usuario = usuario;
        this.texto = texto;
        this.fecha = fecha;
    }

    @Override
    public String toString() {
        return "Resena{" +
                "id=" + id +
                ", libro=" + libro.getTitulo() +
                ", usuario=" + usuario.getNombre() +
                ", texto='" + texto + '\'' +
                ", fecha=" + fecha +
                '}';
    }

}