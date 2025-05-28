<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Devolución de Préstamos</h1>
    
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
      
      <select v-model="filtroEstado" class="px-4 py-2 border rounded-md">
        <option value="activos">Préstamos Activos</option>
        <option value="vencidos">Préstamos Vencidos</option>
        <option value="todos">Todos los Préstamos</option>
      </select>
    </div>

    <!-- Mensaje -->
    <p v-if="mensaje" :class="mensajeTipo === 'error' ? 'text-red-600' : 'text-green-600'" class="mb-4 text-center">{{ mensaje }}</p>

    <!-- Lista de Préstamos -->
    <div class="space-y-4">
      <div 
        v-for="prestamo in prestamosFiltrados" 
        :key="prestamo.id"
        class="border rounded-lg p-4"
        :class="prestamo.fechaDevolucion ? 'border-green-200 bg-green-50' : 'border-blue-200 bg-blue-50'"
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
            <p class="text-sm" :class="prestamoVencido(prestamo) ? 'text-red-600' : 'text-green-600'">
              {{ estadoPrestamo(prestamo) }}
            </p>
            <span v-if="prestamo.amonestaciones && prestamo.amonestaciones.length > 0" class="ml-2 text-red-600 font-bold">(Amonestado)</span>
          </div>
        </div>
        
        <!-- Acción de devolución -->
        <div class="flex justify-end items-center pt-3 border-t border-gray-200">
          <button 
            v-if="!prestamo.fechaDevolucion"
            @click="devolverPrestamo(prestamo)"
            :disabled="procesando"
            class="px-3 py-1 bg-green-500 text-white rounded-md text-sm hover:bg-green-600 disabled:opacity-50"
          >
            {{ procesando ? 'Procesando...' : 'Registrar Devolución' }}
          </button>
          <span v-else class="text-sm text-green-600">
            Devuelto el {{ formatFecha(prestamo.fechaDevolucion) }}
          </span>
        </div>
      </div>
      
      <p v-if="prestamosFiltrados.length === 0" class="text-center text-gray-500 py-6">
        No hay préstamos que coincidan con los filtros
      </p>
    </div>
    
    <!-- Modal de Devolución -->
    <!-- <div v-if="modalVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Registrar Devolución</h3>
          <button @click="modalVisible = false" class="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>
        
        <div v-if="prestamoActual">
          <p class="mb-2"><span class="font-medium">Libro:</span> {{ prestamoActual.libro.titulo }}</p>
          <p class="mb-4"><span class="font-medium">Usuario:</span> {{ prestamoActual.usuario.nombre }}</p>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Estado del Libro</label>
            <select 
              v-model="devolucion.estadoLibro"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="bueno">Buen estado</option>
              <option value="danado">Dañado</option>
              <option value="perdido">Perdido</option>
            </select>
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Observaciones</label>
            <textarea
              v-model="devolucion.observaciones"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500"
              placeholder="Detalles del estado del libro..."
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              @click="modalVisible = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              @click="registrarDevolucion"
              class="px-4 py-2 bg-purple-600 text-white rounded-md text-sm font-medium hover:bg-purple-700"
            >
              Confirmar Devolución
            </button>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Estado del componente
const prestamos = ref([])
const busqueda = ref('')
const filtroEstado = ref('todos')
const procesando = ref(false)
const mensaje = ref('')
const mensajeTipo = ref('')

/* const devolucion = ref({
  estadoLibro: 'bueno',
  observaciones: ''
}); */

const cargarPrestamos = async () => {
  try {
    const res = await fetch('/api/prestamos', { credentials: 'include' })
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

  // Filtro por estado
  if (filtroEstado.value === 'activos') {
    lista = lista.filter(p => p.fechaDevolucion == null)
  } else if (filtroEstado.value === 'finalizados') {
    lista = lista.filter(p => p.fechaDevolucion != null)
  }

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

/* const prestamosFiltrados = computed(() => {
  const termino = busqueda.value.toLowerCase();
  const hoy = new Date();
  
  return prestamos.value.filter(p => {
   
    const coincideBusqueda = 
      p.usuario.nombre.toLowerCase().includes(termino) ||
      p.usuario.codigo.toLowerCase().includes(termino) ||
      p.libro.titulo.toLowerCase().includes(termino) ||
      p.libro.isbn.includes(termino);
    
    
    let coincideEstado = true;
    if (filtroEstado.value === 'activos') {
      coincideEstado = !p.fechaDevolucionReal;
    } else if (filtroEstado.value === 'vencidos') {
      coincideEstado = !p.fechaDevolucionReal && new Date(p.fechaDevolucion) < hoy;
    }
    
    return coincideBusqueda && coincideEstado;
  });
}); */

// Métodos
const formatFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

/* const prestamoVencido = (prestamo) => {
  if (prestamo.fechaDevolucionReal) return false;
  return new Date(prestamo.fechaDevolucion) < new Date();
}; */

const estadoPrestamo = (prestamo) => {
  if (prestamo.fechaDevolucion) return 'Finalizado'
  return 'Activo'
}

const devolverPrestamo = async (prestamo) => {
  if (!prestamo.id) return
  procesando.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch(`/api/prestamos/devolver?prestamoId=${prestamo.id}`, {
      method: 'POST',
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
    mensaje.value = 'Error al devolver el préstamo'
    mensajeTipo.value = 'error'
  } finally {
    procesando.value = false
  }
}

const prestamoVencido = (prestamo) => {
  if (!prestamo.fechaDevolucion && prestamo.fechaLimite) {
    const hoy = new Date()
    const limite = new Date(prestamo.fechaLimite)
    return hoy > limite
  }
  return false
}

const mostrarModalDevolucion = (prestamo) => {
  prestamoActual.value = prestamo;
  devolucion.value = {
    estadoLibro: 'bueno',
    observaciones: ''
  };
  modalVisible.value = true;
};

const registrarDevolucion = async () => {
  try {
    // Simular llamada a API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Actualizar el préstamo
    const index = prestamos.value.findIndex(p => p.id === prestamoActual.value.id);
    if (index !== -1) {
      prestamos.value[index] = {
        ...prestamos.value[index],
        fechaDevolucionReal: new Date(),
        estado: 'completado',
        observaciones: devolucion.value.observaciones || prestamos.value[index].observaciones
      };
    }
    
    // Cerrar modal y resetear
    modalVisible.value = false;
    prestamoActual.value = null;
    
    alert('Devolución registrada exitosamente!');
    
  } catch (error) {
    console.error('Error al registrar devolución:', error);
    alert('Ocurrió un error al registrar la devolución');
  }
};

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