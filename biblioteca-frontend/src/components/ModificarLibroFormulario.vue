<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg mx-auto animate-fadeIn">
    <h2 class="text-3xl font-bold text-slate-700 mb-6 text-center">Modificar Libro</h2>

    <div v-if="!libroAModificar" class="text-center text-red-500 mb-4">
      No se ha seleccionado un libro para modificar. Por favor, vuelve a la pantalla anterior y selecciona uno.
      <button @click="emit('volver')" class="mt-4 bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">Volver</button>
    </div>

    <form v-else @submit.prevent="guardarCambios" class="space-y-5">
      <div>
        <h3 class="text-xl font-semibold text-slate-600 mb-4">1. Detalles del Libro</h3>

        <div class="mb-4">
          <label for="titulo" class="block text-sm font-medium text-gray-700">Título</label>
          <input type="text" id="titulo" v-model="libroEditado.titulo" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="genero" class="block text-sm font-medium text-gray-700">Género</label>
          <input type="text" id="genero" v-model="libroEditado.genero" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="editorial" class="block text-sm font-medium text-gray-700">Editorial</label>
          <input type="text" id="editorial" v-model="libroEditado.editorial" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="autor" class="block text-sm font-medium text-gray-700">Autor</label>
          <input type="text" id="autor" v-model="libroEditado.autor" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="isbn" class="block text-sm font-medium text-gray-700">ISBN (No Editable)</label>
          <input type="text" id="isbn" v-model="libroEditado.isbn" readonly
            class="mt-1 block w-full px-3 py-2 border border-gray-300 bg-gray-100 rounded-md shadow-sm sm:text-sm cursor-not-allowed">
        </div>

        <div class="mb-4">
          <label for="ano" class="block text-sm font-medium text-gray-700">Año</label>
          <input type="number" id="ano" v-model="libroEditado.anio" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="cantidad" class="block text-sm font-medium text-gray-700">Cantidad Disponible</label>
          <input type="number" id="cantidad" v-model="libroEditado.cantidad" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm">
        </div>

        <div class="mb-4">
          <label for="sinopsis" class="block text-sm font-medium text-gray-700">Sinopsis</label>
          <textarea id="sinopsis" v-model="libroEditado.sinopsis" rows="4" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm"></textarea>
        </div>
      </div>

      <button type="submit"
        class="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition-colors font-semibold">
        Guardar Cambios
      </button>
      <button type="button" @click="emit('volver')"
        class="w-full bg-gray-400 text-white py-3 rounded-md hover:bg-gray-500 transition-colors font-semibold mt-3">
        Cancelar
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  libroAModificar: Object
})

const emit = defineEmits(['volver', 'libro-modificado'])

const libroEditado = ref({
  id: null,
  titulo: '',
  genero: '',
  editorial: '',
  autor: '',
  isbn: '',
  anio: null,
  cantidad: null,
  sinopsis: ''
})

watch(() => props.libroAModificar, (newVal) => {
  if (newVal) {
    libroEditado.value = { ...newVal }
  } else {
    libroEditado.value = {
      id: null, titulo: '', genero: '', editorial: '', autor: '',
      isbn: '', anio: '', cantidad: '', sinopsis: ''
    }
  }
}, { immediate: true })

const guardarCambios = async () => {
  if (!libroEditado.value.isbn) {
    alert('Error: El ISBN del libro es necesario para la modificación.')
    return
  }

  try {
    const res = await axios.put(`/api/libros/isbn/${libroEditado.value.isbn}`, libroEditado.value, {
      withCredentials: true
    })

    if (res.status === 200) {
      alert('Libro modificado exitosamente.')
      emit('libro-modificado')
      emit('volver')
    } else {
      alert(`Error al modificar el libro: ${res.statusText}`)
    }
  } catch (error) {
    console.error('Error al enviar la solicitud de modificación:', error)
    if (error.response) {
      alert(`Error del servidor: ${error.response.data.message || error.response.statusText}`)
    } else {
      alert('Ocurrió un error inesperado al modificar el libro.')
    }
  }
}
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