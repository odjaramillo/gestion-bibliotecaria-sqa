<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg mx-auto animate-fadeIn">
    <h2 class="text-3xl font-bold text-slate-700 mb-6 text-center">Eliminar Libro</h2>
    
    <div class="space-y-5">
      <div>
        <h3 class="text-xl font-semibold text-slate-600 mb-4 text-center">Inserta el ISBN del libro que desea eliminar</h3>

        <div class="mb-4">
          <label for="isbnDelete" class="block text-sm font-medium text-gray-700">ISBN del Libro</label>
          <input 
            type="text" 
            id="isbnDelete" 
            v-model="deleteISBN" 
            @keyup.enter="eliminarLibro"
            placeholder="Ingrese el ISBN del libro..."
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm"
          >
        </div>
      </div>

      <button 
        type="button" 
        @click="eliminarLibro"
        class="w-full bg-red-600 text-white py-3 rounded-md hover:bg-red-700 transition-colors font-semibold"
      >
        Eliminar Libro
      </button>

      <div v-if="loading" class="text-center text-gray-500 mt-4">Cargando...</div>
      <div v-if="message" :class="{'text-green-600': !errorMessage, 'text-red-500': errorMessage}" class="text-center mt-4">{{ message }}</div>
      
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

const deleteISBN = ref('');
const loading = ref(false);
const message = ref('');
const errorMessage = ref(false); // Para controlar el color del mensaje

const emit = defineEmits(['volver', 'libro-eliminado']); // Nuevo evento 'libro-eliminado'

const eliminarLibro = async () => {
  if (!deleteISBN.value.trim()) {
    message.value = 'Por favor, ingrese el ISBN del libro a eliminar.';
    errorMessage.value = true;
    return;
  }

  // Validación básica para asegurar que sea un número (si tu ISBN es Long)
  if (isNaN(deleteISBN.value.trim())) {
    message.value = 'El ISBN debe ser un número.';
    errorMessage.value = true;
    return;
  }

  // Confirmación antes de eliminar
  if (!confirm(`¿Estás seguro de que quieres eliminar el libro con ISBN ${deleteISBN.value.trim()}? Esta acción es irreversible.`)) {
    return; // Si el usuario cancela, no hacemos nada
  }

  loading.value = true;
  message.value = ''; // Limpiar mensaje anterior
  errorMessage.value = false;

  try {
    // Llama al endpoint DELETE /api/libros/isbn/{isbn}
    const res = await axios.delete(`/api/libros/isbn/${deleteISBN.value.trim()}`, { 
      withCredentials: true // Esto es importante para tu autenticación
    });
    
    if (res.status === 200) {
      message.value = res.data || 'Libro eliminado exitosamente.';
      errorMessage.value = false;
      emit('libro-eliminado'); // Notifica que el libro fue eliminado
      deleteISBN.value = ''; // Limpiar el campo después de la eliminación
    } else {
      message.value = res.data || 'Ocurrió un error al eliminar el libro.';
      errorMessage.value = true;
    }
  } catch (e) {
    console.error('Error al eliminar libro por ISBN:', e);
    if (e.response) {
      if (e.response.status === 404) {
        message.value = 'No se encontró ningún libro con ese ISBN para eliminar.';
      } else if (e.response.status === 403) {
        message.value = 'No tienes permisos para eliminar libros.';
      } else {
        message.value = e.response.data || 'Ocurrió un error al eliminar el libro. Intente de nuevo.';
      }
    } else {
      message.value = 'Ocurrió un error de red o inesperado al eliminar el libro.';
    }
    errorMessage.value = true;
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