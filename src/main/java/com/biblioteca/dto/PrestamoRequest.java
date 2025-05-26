package com.biblioteca.dto;

public class PrestamoRequest {
    private String correoUsuario;
    private Long isbn;
    private String fechaPrestamo;

    public String getCorreoUsuario() { return correoUsuario; }
    public void setCorreoUsuario(String correoUsuario) { this.correoUsuario = correoUsuario; }
    public Long getIsbn() { return isbn; }
    public void setIsbn(Long isbn) { this.isbn = isbn; }
    public String getFechaPrestamo() { return fechaPrestamo; }
    public void setFechaPrestamo(String fechaPrestamo) { this.fechaPrestamo = fechaPrestamo; }
}