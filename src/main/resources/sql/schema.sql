CREATE DATABASE IF NOT EXISTS biblioteca_db;

USE biblioteca_db;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL, -- Aquí se almacena la contraseña hasheada
    rol ENUM('USUARIO', 'BIBLIOTECARIO') NOT NULL
);


CREATE TABLE IF NOT EXISTS libros (
    
);


CREATE TABLE IF NOT EXISTS prestamos (
    
);