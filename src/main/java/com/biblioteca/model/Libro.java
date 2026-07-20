package com.biblioteca.model;
import java.util.ArrayList;
import java.util.List;
import jakarta.persistence.*;
import java.util.Base64;

@Entity
@Table(name = "libros")
public class Libro {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String titulo;

    @Column(nullable = false)
    private String autor;

    @Column(nullable = false)
    private String editorial;

    @Column(nullable = false)
    private String genero;

    @Column(unique = true, nullable = false)
    private Long isbn;

    @Column(nullable = false)
    private int anio;

    @Column(nullable = false)
    private int cantidad;

    @Column(length = 1000)
    private String sinopsis;

    @Column(columnDefinition = "LONGBLOB")
    private byte[] imagen;


    public Libro() {
    }

    public Libro(String titulo, String autor, String editorial, String genero, Long isbn, int anio, int cantidad, String sinopsis, byte[] imagen) {
        this.titulo = titulo;
        this.autor = autor;
        this.editorial = editorial;
        this.genero = genero;
        this.isbn = isbn;
        this.anio = anio;
        this.cantidad = cantidad;
        this.sinopsis = sinopsis;
        this.imagen = imagen;
    }

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getTitulo() { return titulo; }
    public void setTitulo(String titulo) { this.titulo = titulo; }

    public String getAutor() { return autor; }
    public void setAutor(String autor) { this.autor = autor; }

    public String getEditorial() { return editorial; }
    public void setEditorial(String editorial) { this.editorial = editorial; }

    public String getGenero() { return genero; }
    public void setGenero(String genero) { this.genero = genero; }

    public Long getIsbn() { return isbn; }
    public void setIsbn(Long isbn) { this.isbn = isbn; }

    public int getAnio() { return anio; }
    public void setAnio(int anio) { this.anio = anio; }

    public int getCantidad() { return cantidad; }
    public void setCantidad(int cantidad) { this.cantidad = cantidad; }

    public String getSinopsis() { return sinopsis; }
    public void setSinopsis(String sinopsis) { this.sinopsis = sinopsis; }

    public byte[] getImagen() { return imagen; }
    public void setImagen(byte[] imagen) { this.imagen = imagen; }

    @Transient
    public String getImagenBase64() {
        if (imagen != null && imagen.length > 0) {
            return "data:image/jpeg;base64," + Base64.getEncoder().encodeToString(imagen);
        }
        return null;
    }
    @OneToMany(mappedBy = "libro", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Resena> resenas = new ArrayList<>();
}