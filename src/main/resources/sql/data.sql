-- Insertar usuario administrador inicial
INSERT IGNORE INTO usuarios (nombre, email, password, es_bibliotecario) 
VALUES ('Administrador', 'admin@biblioteca.com', 
        '$2a$10$zRtUyXNlQkYnqoLWwPvVH.7mOuM0rZiZkZjM0rZiZkZjM0rZiZkZjM0rZ',
        true);