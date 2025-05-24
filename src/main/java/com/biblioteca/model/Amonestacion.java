package com.biblioteca.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "amonestaciones")
public class Amonestacion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(optional = false)
    private Usuario usuario;

    @ManyToOne(optional = false)
    private Prestamo prestamo;

    @Column(nullable = false)
    private Double monto;

    @Column(nullable = false)
    private boolean pagada = false;

    private String metodoPago;
    private String comprobantePago;
    private boolean verificada = false;
    private LocalDateTime fecha = LocalDateTime.now();

    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public Usuario getUsuario() {
        return usuario;
    }
    public void setUsuario(Usuario usuario) {
        this.usuario = usuario;
    }
    public Prestamo getPrestamo() {
        return prestamo;
    }
    public void setPrestamo(Prestamo prestamo) {
        this.prestamo = prestamo;
    }
    public Double getMonto() {
        return monto;
    }
    public void setMonto(Double monto) {
        this.monto = monto;
    }
    public boolean isPagada() {
        return pagada;
    }
    public void setPagada(boolean pagada) {
        this.pagada = pagada;
    }
    public String getMetodoPago() {
        return metodoPago;
    }
    public void setMetodoPago(String metodoPago) {
        this.metodoPago = metodoPago;
    }
    public String getComprobantePago() {
        return comprobantePago;
    }
    public void setComprobantePago(String comprobantePago) {
        this.comprobantePago = comprobantePago;
    }
    public boolean isVerificada() {
        return verificada;
    }
    public void setVerificada(boolean verificada) {
        this.verificada = verificada;
    }
    public LocalDateTime getFecha() {
        return fecha;
    }

    public void setFecha(LocalDateTime fecha) {
        this.fecha = fecha;
    }

    public Amonestacion() {
    }

    public Amonestacion(Usuario usuario, Prestamo prestamo, Double monto, boolean pagada, String metodoPago, String comprobantePago, boolean verificada, LocalDateTime fecha) {
        this.usuario = usuario;
        this.prestamo = prestamo;
        this.monto = monto;
        this.pagada = pagada;
        this.metodoPago = metodoPago;
        this.comprobantePago = comprobantePago;
        this.verificada = verificada;
        this.fecha = fecha;
    }

    @Override
    public String toString() {
        return "Amonestacion{" +
                "id=" + id +
                ", usuario=" + usuario.getNombre() +
                ", prestamo=" + prestamo.getId() +
                ", monto=" + monto +
                ", pagada=" + pagada +
                ", metodoPago='" + metodoPago + '\'' +
                ", comprobantePago='" + comprobantePago + '\'' +
                ", verificada=" + verificada +
                ", fecha=" + fecha +
                '}';
    }
}