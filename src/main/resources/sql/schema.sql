CREATE DATABASE IF NOT EXISTS biblioteca_db;

USE biblioteca_db;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('USUARIO', 'BIBLIOTECARIO') NOT NULL
);


CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    editorial VARCHAR(255) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    isbn BIGINT NOT NULL UNIQUE,
    anio INT NOT NULL,
    cantidad INT NOT NULL,
    sinopsis VARCHAR(1000),
    imagen VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    libro_id INT NOT NULL,
    fecha_prestamo DATETIME NOT NULL,
    fecha_devolucion DATETIME,
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);


CREATE TABLE IF NOT EXISTS amonestaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    prestamo_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    pagada BOOLEAN NOT NULL DEFAULT FALSE,
    metodo_pago VARCHAR(50),
    comprobante_pago VARCHAR(100),
    verificada BOOLEAN NOT NULL DEFAULT FALSE,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id)
);


CREATE TABLE IF NOT EXISTS resenas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    texto VARCHAR(1000) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (libro_id) REFERENCES libros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);


CREATE TABLE IF NOT EXISTS comentario_resena (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resena_id INT NOT NULL,
    usuario_id INT NOT NULL,
    texto VARCHAR(1000) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resena_id) REFERENCES resenas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
); 