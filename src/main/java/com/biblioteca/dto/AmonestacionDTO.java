package com.biblioteca.dto;

import com.biblioteca.model.Amonestacion;

import java.time.LocalDateTime;

public class AmonestacionDTO {
    private Integer usuarioId;
    private Integer prestamoId;
    private Double monto;
    private boolean pagada;
    private String metodoPago;
    private String comprobantePago;
    private boolean verificada;
    private LocalDateTime fecha;

    public Integer getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Integer usuarioId) { this.usuarioId = usuarioId; }

    public Integer getPrestamoId() { return prestamoId; }
    public void setPrestamoId(Integer prestamoId) { this.prestamoId = prestamoId; }

    public Double getMonto() { return monto; }
    public void setMonto(Double monto) { this.monto = monto; }

    public boolean isPagada() { return pagada; }
    public void setPagada(boolean pagada) { this.pagada = pagada; }

    public String getMetodoPago() { return metodoPago; }
    public void setMetodoPago(String metodoPago) { this.metodoPago = metodoPago; }

    public String getComprobantePago() { return comprobantePago; }
    public void setComprobantePago(String comprobantePago) { this.comprobantePago = comprobantePago; }

    public boolean isVerificada() { return verificada; }
    public void setVerificada(boolean verificada) { this.verificada = verificada; }

    public LocalDateTime getFecha() { return fecha; }
    public void setFecha(LocalDateTime fecha) { this.fecha = fecha; }

    public Amonestacion toAmonestacion() {
        Amonestacion a = new Amonestacion();
        a.setMonto(monto);
        a.setPagada(pagada);
        a.setMetodoPago(metodoPago);
        a.setComprobantePago(comprobantePago);
        a.setVerificada(verificada);
        a.setFecha(fecha != null ? fecha : LocalDateTime.now());
        return a;
    }
}