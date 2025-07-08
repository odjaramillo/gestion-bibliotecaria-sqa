<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <h2 class="text-2xl font-bold text-slate-700 mb-6">Editar Perfil</h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Nombre Completo -->
      <div>
        <label for="nombre" class="block text-sm font-medium text-gray-700">Nombre Completo</label>
        <input
          type="text"
          id="nombre"
          v-model="nombre"
          :class="{'border-red-500': error}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-fuchsia-900"
          placeholder="Ej: Juan Pérez"
        >
        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
      </div>

      <!-- Cambiar Contraseña -->
      <div>
        <label for="currentPassword" class="block text-sm font-medium text-gray-700">Contraseña Actual</label>
        <input
          type="password"
          id="currentPassword"
          v-model="contrasenaActual"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-fuchsia-900"
        >
      </div>
      <div>
        <label for="newPassword" class="block text-sm font-medium text-gray-700">Nueva Contraseña</label>
        <input
          type="password"
          id="newPassword"
          v-model="contrasenaNueva"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-fuchsia-900"
        >
      </div>

      <!-- Botones Guardar/Cancelar -->
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="resetForm"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>

            <div>
        <button
          type="button"
          @click="cambiarContrasena"
          :disabled="isSubmitting"
          class="mt-2 w-full px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 disabled:opacity-50"
        >
          Cambiar Contraseña
        </button>
      </div>

      <!-- Eliminar Perfil -->
      <div class="pt-4">
        <button
          type="button"
          @click="eliminarPerfil"
          class="w-full px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Eliminar Perfil
        </button>
      </div>

      <!-- Mensaje de feedback -->
      <p v-if="mensaje" :class="mensajeTipo === 'error' ? 'text-red-600' : 'text-green-600'" class="mt-2 text-center">
        {{ mensaje }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const nombre = ref('')
const error = ref('')
const isSubmitting = ref(false)
const mensaje = ref('')
const mensajeTipo = ref('')

const contrasenaActual = ref('')
const contrasenaNueva = ref('')

// Cargar nombre del usuario
const cargarNombre = async () => {
  try {
    const res = await fetch('/api/usuarios/me', { credentials: 'include' })
    if (res.ok) {
      const user = await res.json()
      nombre.value = user.nombre || ''
    }
  } catch (e) {
    nombre.value = ''
  }
}

// Validar nombre
const validate = () => {
  if (!nombre.value.trim()) {
    error.value = 'El nombre es requerido'
    return false
  }
  if (nombre.value.length < 3) {
    error.value = 'Mínimo 3 caracteres'
    return false
  }
  error.value = ''
  return true
}

// Guardar cambios de nombre
const handleSubmit = async () => {
  if (!validate()) return
  isSubmitting.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch('/api/usuarios/nombre', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ nombre: nombre.value })
    })
    const msg = await res.text()
    if (res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'success'
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    }
  } catch (e) {
    mensaje.value = 'Error al actualizar el nombre.'
    mensajeTipo.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

// Cambiar contraseña
const cambiarContrasena = async () => {
  if (!contrasenaActual.value || !contrasenaNueva.value) {
    mensaje.value = 'Debes completar ambas contraseñas.'
    mensajeTipo.value = 'error'
    return
  }
  isSubmitting.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch('/api/usuarios/contrasena', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        contrasenaActual: contrasenaActual.value,
        contrasenaNueva: contrasenaNueva.value
      })
    })
    const msg = await res.text()
    if (res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'success'
      contrasenaActual.value = ''
      contrasenaNueva.value = ''
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    }
  } catch (e) {
    mensaje.value = 'Error al cambiar la contraseña.'
    mensajeTipo.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

// Eliminar perfil
const eliminarPerfil = async () => {
  if (!confirm('¿Estás seguro que deseas eliminar tu perfil? Esta acción no se puede deshacer.')) {
    return
  }
  isSubmitting.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch('/api/usuarios', {
      method: 'DELETE',
      credentials: 'include'
    })
    const msg = await res.text()
    if (res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'success'
      window.location.href = '/login'
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    }
  } catch (e) {
    mensaje.value = 'Error al eliminar el perfil.'
    mensajeTipo.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

// Cancelar cambios
const resetForm = () => {
  cargarNombre()
  error.value = ''
  mensaje.value = ''
  mensajeTipo.value = ''
  contrasenaActual.value = ''
  contrasenaNueva.value = ''
}

onMounted(() => {
  cargarNombre()
})
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
