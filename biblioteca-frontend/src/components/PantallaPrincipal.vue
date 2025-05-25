<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <h2 class="text-4xl font-bold text-slate-700 mb-6 text-center">Bienvenido a la Biblioteca Digital</h2>
    <p class="text-gray-600 text-lg mb-10 text-center">Explora nuestra vasta colección de libros y encuentra tu próxima lectura.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="libro in librosDeEjemplo" :key="libro.id"
        class="bg-gray-50 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
        <img :src="libro.portadaUrl" alt="Portada del libro" class="w-full h-64 object-cover">
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-700">{{ libro.titulo }}</h3>
          <p class="text-sm text-gray-500">{{ libro.autor }}</p>
          <button 
            @click="verDetalles(libro)"
            class="mt-3 w-full bg-fuchsia-700 text-white py-2 rounded-md hover:bg-fuchsia-900 transition-colors text-sm"
          >
            Ver Detalles
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref , defineEmits} from 'vue';



const librosDeEjemplo = ref([
  { 
    id: 1, 
    titulo: 'El Señor de los Anillos', 
    autor: 'J.R.R. Tolkien',
    genero: 'Fantasía épica', 
    anio: 1954,
    isbn: '978-84-666-3768-9',
    descripcion: 'Una épica historia de aventuras en la Tierra Media...',
    portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+1',
    disponible: true
  },
  { 
    id: 2, 
    titulo: 'Cien Años de Soledad', 
    autor: 'Gabriel García Márquez', 
    portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+2',
    genero: 'Realismo mágico',
    anio: 1967,
    descripcion: 'La historia de la familia Buendía en el pueblo de Macondo...',
    isbn: '978-84-376-0494-7',
    disponible: true
  },
  { 
    id: 3, 
    titulo: '1984', 
    autor: 'George Orwell', 
    portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+3',
    genero: 'Distopía',
    anio: 1949,
    descripcion: 'Una visión futurista de un estado totalitario...',
    isbn: '978-84-206-7267-1',
    disponible: false
  }
]);

const emit = defineEmits(['ver-libro']);

const verDetalles = (libro) => {
  emit('ver-libro', { ...libro }); // Asegúrate de emitir un nuevo objeto
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>