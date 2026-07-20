<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Registrar Nuevo Préstamo</h1>
    <form @submit.prevent="registrarPrestamo" class="space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Correo del Usuario</label>
        <input
          type="email"
          v-model="correoUsuario"
          placeholder="usuario@email.com"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-900"
        >
        <p v-if="errores.usuario" class="mt-1 text-sm text-red-600">{{ errores.usuario }}</p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">ISBN del Libro</label>
        <input
          type="number"
          v-model="isbnLibro"
          placeholder="ISBN"
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-900"
        >
        <p v-if="errores.libro" class="mt-1 text-sm text-red-600">{{ errores.libro }}</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="fechaPrestamo" class="block text-sm font-medium text-gray-700">Fecha de Préstamo</label>
          <input
            type="date"
            id="fechaPrestamo"
            v-model="fechaPrestamo"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
            :max="fechaPrestamo"
          >
        </div>
        <div>
          <label for="fechaDevolucion" class="block text-sm font-medium text-gray-700">Fecha de Devolución</label>
          <input
            type="date"
            id="fechaDevolucion"
            :value="fechaDevolucion"
            disabled
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900 bg-gray-100"
          >
        </div>
      </div>
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="cancelar"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="procesando"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
        >
          {{ procesando ? 'Registrando...' : 'Registrar Préstamo' }}
        </button>
      </div>
      <p v-if="mensaje" :class="mensajeTipo === 'error' ? 'text-red-600' : 'text-green-600'" class="mt-4 text-center">{{ mensaje }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const correoUsuario = ref('')
const isbnLibro = ref('')
const fechaPrestamo = ref(new Date().toISOString().split('T')[0])
const fechaDevolucion = ref(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
const procesando = ref(false)
const errores = ref({ usuario: '', libro: '' })
const mensaje = ref('')
const mensajeTipo = ref('')

const validar = () => {
  let valido = true
  errores.value.usuario = ''
  errores.value.libro = ''
  if (!correoUsuario.value || !correoUsuario.value.includes('@')) {
    errores.value.usuario = 'Debe ingresar un correo válido'
    valido = false
  }
  if (!isbnLibro.value || isbnLibro.value.toString().length !== 13) {
    errores.value.libro = 'Debe ingresar un ISBN válido de 13 dígitos'
    valido = false
  }
  return valido
}

const registrarPrestamo = async () => {
  mensaje.value = ''
  mensajeTipo.value = ''
  if (!validar()) return
  procesando.value = true
  try {
    const res = await fetch('/api/prestar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        correoUsuario: correoUsuario.value,
        isbn: isbnLibro.value,
        fechaPrestamo: fechaPrestamo.value
      })
    })
    const msg = await res.text()
    if (!res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'success'
      correoUsuario.value = ''
      isbnLibro.value = ''
      fechaPrestamo.value = new Date().toISOString().split('T')[0]
    }
  } catch (e) {
    mensaje.value = 'Error al registrar el préstamo'
    mensajeTipo.value = 'error'
  } finally {
    procesando.value = false
  }
}

const cancelar = () => {
  correoUsuario.value = ''
  isbnLibro.value = ''
  mensaje.value = ''
  mensajeTipo.value = ''
}
</script>