package com.biblioteca.dto;

public class PrestamoRequest {
    private Integer usuarioId;
    private Long isbn;

    public Integer getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Integer usuarioId) { this.usuarioId = usuarioId; }
    public Long getIsbn() { return isbn; }
    public void setIsbn(Long isbn) { this.isbn = isbn; }
}