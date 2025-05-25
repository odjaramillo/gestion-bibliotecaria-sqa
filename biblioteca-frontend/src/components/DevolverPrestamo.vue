<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Finalización de Préstamos</h1>
    
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

    <!-- Lista de Préstamos -->
    <div class="space-y-4">
      <div 
        v-for="prestamo in prestamosFiltrados" 
        :key="prestamo.id"
        class="border rounded-lg p-4"
        :class="{
          'border-blue-200 bg-blue-50': !prestamoVencido(prestamo),
          'border-red-200 bg-red-50': prestamoVencido(prestamo)
        }"
      >
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
          <!-- Datos Usuario -->
          <div>
            <h3 class="font-semibold text-gray-800">{{ prestamo.usuario.nombre }}</h3>
            <p class="text-sm text-gray-600">Código: {{ prestamo.usuario.codigo }}</p>
            <p class="text-sm">Préstamo ID: {{ prestamo.id }}</p>
          </div>
          
          <!-- Datos Libro -->
          <div>
            <p class="font-medium">{{ prestamo.libro.titulo }}</p>
            <p class="text-sm text-gray-600">{{ prestamo.libro.autor }}</p>
            <p class="text-sm">ISBN: {{ prestamo.libro.isbn }}</p>
          </div>
          
          <!-- Fechas -->
          <div>
            <p class="text-sm"><span class="font-medium">Préstamo:</span> {{ formatFecha(prestamo.fechaPrestamo) }}</p>
            <p class="text-sm"><span class="font-medium">Devolución:</span> {{ formatFecha(prestamo.fechaDevolucion) }}</p>
            <p class="text-sm" :class="prestamoVencido(prestamo) ? 'text-red-600' : 'text-green-600'">
              {{ estadoPrestamo(prestamo) }}
            </p>
          </div>
        </div>
        
        <!-- Observaciones y acciones -->
        <div class="flex justify-between items-center pt-3 border-t border-gray-200">
          <div>
            <p v-if="prestamo.observaciones" class="text-sm text-gray-600">
              <span class="font-medium">Obs:</span> {{ prestamo.observaciones }}
            </p>
          </div>
          
          <div class="space-x-2">
            <button 
              v-if="!prestamo.fechaDevolucionReal"
              @click="mostrarModalDevolucion(prestamo)"
              class="px-3 py-1 bg-green-500 text-white rounded-md text-sm hover:bg-green-600"
            >
              Registrar Devolución
            </button>
            <span v-else class="text-sm text-green-600">
              Devuelto el {{ formatFecha(prestamo.fechaDevolucionReal) }}
            </span>
          </div>
        </div>
      </div>
      
      <p v-if="prestamosFiltrados.length === 0" class="text-center text-gray-500 py-6">
        No hay préstamos que coincidan con los filtros
      </p>
    </div>
    
    <!-- Modal de Devolución -->
    <div v-if="modalVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Datos simulados de préstamos
const prestamos = ref([
  {
    id: 'PREST-001',
    usuario: {
      id: 1,
      codigo: 'USR-001',
      nombre: 'María González'
    },
    libro: {
      id: 1,
      titulo: 'El nombre del viento',
      autor: 'Patrick Rothfuss',
      isbn: '978-84-666-3768-9'
    },
    fechaPrestamo: new Date(2023, 5, 1),
    fechaDevolucion: new Date(2023, 5, 15),
    fechaDevolucionReal: null,
    observaciones: 'Libro con daño leve en portada',
    estado: 'activo'
  },
  {
    id: 'PREST-002',
    usuario: {
      id: 2,
      codigo: 'USR-002',
      nombre: 'Carlos Méndez'
    },
    libro: {
      id: 2,
      titulo: 'Cien años de soledad',
      autor: 'Gabriel García Márquez',
      isbn: '978-84-376-0494-7'
    },
    fechaPrestamo: new Date(2023, 5, 5),
    fechaDevolucion: new Date(2023, 5, 19),
    fechaDevolucionReal: new Date(2023, 5, 18),
    observaciones: '',
    estado: 'completado'
  }
]);

// Estado del componente
const busqueda = ref('');
const filtroEstado = ref('activos');
const modalVisible = ref(false);
const prestamoActual = ref(null);

const devolucion = ref({
  estadoLibro: 'bueno',
  observaciones: ''
});

// Filtros computados
const prestamosFiltrados = computed(() => {
  const termino = busqueda.value.toLowerCase();
  const hoy = new Date();
  
  return prestamos.value.filter(p => {
    // Filtro por búsqueda
    const coincideBusqueda = 
      p.usuario.nombre.toLowerCase().includes(termino) ||
      p.usuario.codigo.toLowerCase().includes(termino) ||
      p.libro.titulo.toLowerCase().includes(termino) ||
      p.libro.isbn.includes(termino);
    
    // Filtro por estado
    let coincideEstado = true;
    if (filtroEstado.value === 'activos') {
      coincideEstado = !p.fechaDevolucionReal;
    } else if (filtroEstado.value === 'vencidos') {
      coincideEstado = !p.fechaDevolucionReal && new Date(p.fechaDevolucion) < hoy;
    }
    
    return coincideBusqueda && coincideEstado;
  });
});

// Métodos
const formatFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

const prestamoVencido = (prestamo) => {
  if (prestamo.fechaDevolucionReal) return false;
  return new Date(prestamo.fechaDevolucion) < new Date();
};

const estadoPrestamo = (prestamo) => {
  if (prestamo.fechaDevolucionReal) return 'Devuelto';
  if (prestamoVencido(prestamo)) return 'Vencido';
  return 'En curso';
};

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

// Cargar datos iniciales (simular llamada API)
onMounted(() => {
  // En una app real, aquí harías una llamada a tu API
});
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