package com.biblioteca.dto;

public class ResenaRequest {
    private Integer libroId;
    private Integer usuarioId;
    private String texto;

    public Integer getLibroId() { return libroId; }
    public void setLibroId(Integer libroId) { this.libroId = libroId; }
    public Integer getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Integer usuarioId) { this.usuarioId = usuarioId; }
    public String getTexto() { return texto; }
    public void setTexto(String texto) { this.texto = texto; }
}