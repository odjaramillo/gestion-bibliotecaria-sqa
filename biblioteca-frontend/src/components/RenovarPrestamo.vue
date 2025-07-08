<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Renovación de Préstamos</h1>
    
    <!-- Filtros -->
    <div class="mb-6 flex flex-wrap gap-4 items-center">
      <div class="relative flex-grow max-w-md">
        <input
          type="text"
          v-model="busqueda"
          placeholder="Buscar por usuario o libro..."
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-900"
        >
      </div>
      
      <div class="px-4 py-2 border rounded-md bg-gray-100 text-gray-700 cursor-default">
        Préstamos Finalizados
      </div>
    </div>

    <!-- Mensaje -->
    <p v-if="mensaje" :class="mensajeTipo === 'error' ? 'text-red-600' : 'text-green-600'" class="mb-4 text-center">{{ mensaje }}</p>

    <!-- Lista de Préstamos -->
    <div class="space-y-4">
      <div 
        v-for="prestamo in prestamosFiltrados" 
        :key="prestamo.id"
        class="border rounded-lg p-4 border-red-200 bg-red-50"
      >
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
          <!-- Datos Usuario -->
          <div>
            <h3 class="font-semibold text-gray-800">{{ prestamo.usuario?.nombre }}</h3>
            <p class="text-sm text-gray-600">Correo: {{ prestamo.usuario?.correo }}</p>
            <p class="text-sm">Préstamo ID: {{ prestamo.id }}</p>
          </div>
          
          <!-- Datos Libro -->
          <div>
            <p class="font-medium">{{ prestamo.libro?.titulo }}</p>
            <p class="text-sm text-gray-600">ISBN: {{ prestamo.libro?.isbn }}</p>
          </div>
          
          <!-- Fechas -->
          <div>
            <p class="text-sm"><span class="font-medium">Préstamo:</span> {{ formatFecha(prestamo.fechaPrestamo) }}</p>
            <p class="text-sm"><span class="font-medium">Límite:</span> {{ formatFecha(prestamo.fechaLimite) }}</p>
            <p class="text-sm"><span class="font-medium">Devolución:</span> {{ formatFecha(prestamo.fechaDevolucion) }}</p>
            <p class="text-sm text-red-600">
              Finalizado (Vencido)
            </p>
            <span v-if="prestamo.amonestaciones && prestamo.amonestaciones.length > 0" class="ml-2 text-red-600 font-bold">(Amonestado)</span>
          </div>
        </div>
        
        <!-- Acción de renovación -->
        <div class="flex justify-end items-center pt-3 border-t border-gray-200">
          <button 
            @click="renovarPrestamo(prestamo)"
            :disabled="procesando"
            class="px-3 py-1 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600 disabled:opacity-50"
          >
            {{ procesando ? 'Procesando...' : 'Renovar' }}
          </button>
        </div>
      </div>
      
      <p v-if="prestamosFiltrados.length === 0" class="text-center text-gray-500 py-6">
        No hay préstamos finalizados para renovar
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Estado del componente
const prestamos = ref([])
const busqueda = ref('')
const procesando = ref(false)
const mensaje = ref('')
const mensajeTipo = ref('')

const cargarPrestamos = async () => {
  try {
    const res = await fetch('/api/prestamos/finalizados', { credentials: 'include' })
    if (res.ok) {
      prestamos.value = await res.json()
    } else {
      prestamos.value = []
    }
  } catch (e) {
    prestamos.value = []
  }
}

const prestamosFiltrados = computed(() => {
  const termino = busqueda.value.toLowerCase()
  let lista = prestamos.value

  // Solo préstamos finalizados (ya filtrados por el endpoint)
  // Filtro por búsqueda
  if (termino) {
    lista = lista.filter(p =>
      (p.usuario?.nombre?.toLowerCase() || '').includes(termino) ||
      (p.usuario?.correo?.toLowerCase() || '').includes(termino) ||
      (p.libro?.titulo?.toLowerCase() || '').includes(termino) ||
      (p.libro?.isbn?.toString() || '').includes(termino)
    )
  }
  return lista
})

// Métodos
const formatFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const renovarPrestamo = async (prestamo) => {
  if (!prestamo.id) return
  procesando.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch(`/api/prestamos/${prestamo.id}/renovar`, {
      method: 'PUT',
      credentials: 'include'
    })
    const msg = await res.text()
    if (res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'success'
      await cargarPrestamos()
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    }
  } catch (e) {
    mensaje.value = 'Error al renovar el préstamo'
    mensajeTipo.value = 'error'
  } finally {
    procesando.value = false
  }
}

onMounted(() => {
  cargarPrestamos()
})
</script>

<style scoped>
/* Estilos opcionales para animación */
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
