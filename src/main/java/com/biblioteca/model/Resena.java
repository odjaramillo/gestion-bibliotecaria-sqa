package com.biblioteca.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "resenas")
public class Resena {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "libro_id")
    private Libro libro;

    @ManyToOne(optional = false)
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    @Column(nullable = false, length = 1000)
    private String texto;

    @Column(nullable = false)
    private LocalDateTime fecha;

    @PrePersist
    public void prePersist() {
        this.fecha = LocalDateTime.now();
    }

    public Resena() {
    }

    public Resena(Libro libro, Usuario usuario, String texto, LocalDateTime fecha) {
        this.libro = libro;
        this.usuario = usuario;
        this.texto = texto;
        this.fecha = fecha;
    }

    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
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

    @Override
    public String toString() {
        return "Resena{" +
                "id=" + id +
                ", libro=" + (libro != null ? libro.getTitulo() : null) +
                ", usuario=" + (usuario != null ? usuario.getNombre() : null) +
                ", texto='" + texto + '\'' +
                ", fecha=" + fecha +
                '}';
    }
}