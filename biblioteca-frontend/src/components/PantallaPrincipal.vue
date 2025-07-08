<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <h2 class="text-4xl font-bold text-slate-700 mb-6 text-center">Bienvenido a la Biblioteca Digital</h2>
    <p class="text-gray-600 text-lg mb-10 text-center">Explora nuestra vasta colección de libros y encuentra tu próxima lectura.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="libro in libros" :key="libro.id"
        class="bg-gray-50 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
        <img :src="libro.imagenBase64 || libro.portadaUrl || 'https://placehold.co/300x400/A9A9A9/FFF?text=Sin+Imagen'" alt="Portada del libro" class="w-full h-64 object-cover">
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const libros = ref([])

const emit = defineEmits(['ver-libro'])

const cargarLibros = async () => {
  try {
    const res = await axios.get('/api/libros')
    libros.value = res.data
  } catch (e) {
    libros.value = []
  }
}

const verDetalles = (libro) => {
  emit('ver-libro', { ...libro })
}


onMounted(() => {
  cargarLibros()
  window.addEventListener('libro-registrado', cargarLibros)
})

</script>