package com.biblioteca.dto;

public class ComentarioResenaRequest {
    private Integer resenaId;
    private Integer usuarioId;
    private String texto;

    public Integer getResenaId() { return resenaId; }
    public void setResenaId(Integer resenaId) { this.resenaId = resenaId; }
    public Integer getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Integer usuarioId) { this.usuarioId = usuarioId; }
    public String getTexto() { return texto; }
    public void setTexto(String texto) { this.texto = texto; }
}