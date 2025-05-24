<template>
    <div class="container">
        <header class="background">
            <h1 class="title">Gestión Bibliotecaria</h1>
            <div class="search-bar">
                <input type="text" placeholder="Buscar...">
                <button>Buscar</button>
            </div>
        </header>

        <div class="tool-bar">
            <button class="loggin">Iniciar Sesion</button>
        </div>

        <section class="welcome-section">
            <h2>Bienvenido...</h2>
            <p class="welcome-message">Mensaje blablabla</p>
            
            <div class="book-list">
                <div class="book-item">
                    <h3>REYES CAÍDOS</h3>
                    <p class="author">NAIBA CAMBOA</p>
                    <button class="see-more">Ver más</button>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Datos de libros (podrían venir de una API en un proyecto real)
    const booksData = {
        "welcome": [
            { title: "REYES CAÍDOS", author: "JULIAN ALONSO" },
            { title: "El Bosque Mágico", author: "NAIBA CAMBOA" },
            { title: "El Secreto del Río", author: "MARÍA LÓPEZ" },
            { title: "La Ciudad Perdida", author: "CARLOS RUIZ" },
            { title: "Noche Estrellada", author: "ANA GARCÍA" }
        ]
    };

    // Función para renderizar libros
    function renderBooks(section, books) {
        const container = document.querySelector(`.${section}-section .book-list`);
        
        // Limpiar contenedor (excepto el primer libro que está en el HTML)
        while (container.children.length > 1) {
            container.removeChild(container.lastChild);
        }
        
        // Agregar libros (empezamos desde el índice 1 porque el primero ya está)
        for (let i = 1; i < books.length; i++) {
            const book = books[i];
            const bookElement = document.createElement('div');
            bookElement.className = 'book-item';
            
            bookElement.innerHTML = `
                <h3>${book.title}</h3>
                ${book.author ? `<p class="author">${book.author}</p>` : ''}
                <button class="see-more">Ver más</button>
            `;
            
            container.appendChild(bookElement);
        }
    }

    // Renderizar libros al cargar la página
    renderBooks('welcome', booksData.welcome);
    renderBooks('android', booksData.android);

    // Manejar el botón de búsqueda
    const searchButton = document.querySelector('.search-bar button');
    searchButton.addEventListener('click', function() {
        const searchTerm = document.querySelector('.search-bar input').value.toLowerCase();
        
        // Filtrar libros en ambas secciones
        const filteredWelcome = booksData.welcome.filter(book => 
            book.title.toLowerCase().includes(searchTerm) || 
            book.author.toLowerCase().includes(searchTerm)
        );
        
        const filteredAndroid = booksData.android.filter(book => 
            book.title.toLowerCase().includes(searchTerm) || 
            book.author.toLowerCase().includes(searchTerm)
        );
        
        // Renderizar libros filtrados
        renderBooks('welcome', filteredWelcome.length > 0 ? filteredWelcome : booksData.welcome);
        renderBooks('android', filteredAndroid.length > 0 ? filteredAndroid : booksData.android);
    });

    // Manejar clics en "Ver más" (delegación de eventos)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('see-more')) {
            const bookTitle = e.target.closest('.book-item').querySelector('h3').textContent;
            alert(`Has seleccionado ver más información sobre: ${bookTitle}`);
            // En una aplicación real, aquí podrías redirigir a una página de detalles
            // o mostrar un modal con más información del libro
        }
    });
});
</script>

<style>
body {
    font-family: Arial, sans-serif;
    background-color: #ECF0F1;
    color: #333;
    margin: 0px;
}

.title{
    padding: 30px 15px 5px;
    width: 200px;
    margin-bottom: 0px;
    margin-top: 0px;
}

.search-bar{
    display: flex;
    position: fixed;
    left: 80%;
    top: 5%;
}

.search-bar input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 1px 0 0 4px;
}

.search-bar button {
    padding: 10px 15px;
    background-color: #454F64;
    color: white;
    border: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
}

.search-bar button:hover {
    background-color: #2980b9;
}


.tool-bar{
    background-color: #454F64;
    padding: 10px;
    width: 1440;
    height: 102;
    top: 105px;
}

.loggin{
    background-color: #AC8FAF;
    border-radius: 5px;
    
}

h2 {
    color: #2c3e50;
    margin-bottom: 15px;
}

.welcome-message {
    margin-bottom: 20px;
    color: #7f8c8d;
}

.book-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.book-item {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #3498db;
}

.book-item h3 {
    margin-top: 0;
    color: #2c3e50;
}

.author {
    font-style: italic;
    color: #7f8c8d;
    margin: 10px 0;
}

.see-more {
    background-color: #34495E;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.see-more:hover {
    background-color: #27ae60;
}

.background{
    background-color: #ECF0F1;
    margin-top: 0px;
}
</style>
