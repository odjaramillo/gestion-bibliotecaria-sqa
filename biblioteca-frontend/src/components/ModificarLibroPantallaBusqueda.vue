<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg mx-auto animate-fadeIn">
    <h2 class="text-3xl font-bold text-slate-700 mb-6 text-center">Modificar Libro</h2>
    
    <div class="space-y-5">
      <div>
        <h3 class="text-xl font-semibold text-slate-600 mb-4 text-center">Escriba el ISBN del libro que desea modificar</h3>

        <div class="mb-4">
          <label for="isbnSearch" class="block text-sm font-medium text-gray-700">ISBN del Libro</label>
          <input 
            type="text" 
            id="isbnSearch" 
            v-model="searchISBN" 
            @keyup.enter="buscarLibro"
            placeholder="Ingrese el ISBN del libro..."
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm"
          >
        </div>
      </div>

      <button 
        type="button" 
        @click="buscarLibro"
        class="w-full bg-fuchsia-700 text-white py-3 rounded-md hover:bg-fuchsia-900 transition-colors font-semibold"
      >
        Buscar Libro
      </button>

      <div v-if="loading" class="text-center text-gray-500 mt-4">Cargando...</div>
      <div v-if="errorMessage" class="text-center text-red-500 mt-4">{{ errorMessage }}</div>
      
      <button type="button" @click="emit('volver')"
              class="w-full bg-gray-400 text-white py-3 rounded-md hover:bg-gray-500 transition-colors font-semibold mt-3">
        Volver a Inicio
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const searchISBN = ref('');
const loading = ref(false);
const errorMessage = ref('');

const emit = defineEmits(['seleccionar-libro-para-modificar', 'volver']);

const buscarLibro = async () => {
  if (!searchISBN.value.trim()) {
    errorMessage.value = 'Por favor, ingrese un ISBN para buscar.';
    return;
  }

  // Validación básica para asegurar que sea un número (si tu ISBN es Long)
  if (isNaN(searchISBN.value.trim())) {
    errorMessage.value = 'El ISBN debe ser un número.';
    return;
  }

  loading.value = true;
  errorMessage.value = ''; // Limpiar mensaje de error anterior

  try {
    // Llama al endpoint GET /api/libros/isbn/{isbn}
    const res = await axios.get(`/api/libros/isbn/${searchISBN.value.trim()}`, { 
      withCredentials: true // Esto es importante para tu autenticación
    });
    
    if (res.data) {
      // Si el libro se encuentra, lo emitimos para que App.vue lo use en el siguiente componente
      emit('seleccionar-libro-para-modificar', res.data); 
    } else {
      // Aunque el 404 del backend ya lo manejaría, esto es un fallback
      errorMessage.value = 'No se encontró ningún libro con ese ISBN.';
    }
  } catch (e) {
    console.error('Error al buscar libro por ISBN:', e);
    if (e.response && e.response.status === 404) {
      errorMessage.value = 'No se encontró ningún libro con ese ISBN.';
    } else {
      errorMessage.value = 'Ocurrió un error al buscar el libro. Intente de nuevo.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>