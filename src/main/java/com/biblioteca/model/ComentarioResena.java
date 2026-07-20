package com.biblioteca.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "comentario_resena")
public class ComentarioResena {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "resena_id")
    private Resena resena;

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

    public ComentarioResena() {
    }

    public ComentarioResena(Resena resena, Usuario usuario, String texto, LocalDateTime fecha) {
        this.resena = resena;
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

    @Override
    public String toString() {
        return "ComentarioResena{" +
                "id=" + id +
                ", resena=" + (resena != null ? resena.getId() : null) +
                ", usuario=" + (usuario != null ? usuario.getNombre() : null) +
                ", texto='" + texto + '\'' +
                ", fecha=" + fecha +
                '}';
    }
}