<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Gestión de Pagos Pendientes</h1>
    
    <!-- Filtros -->
    <div class="mb-6 flex flex-wrap gap-4">
      <select v-model="filtroEstado" class="px-4 py-2 border rounded-lg">
        <option value="todos">Todos</option>
        <option value="pendiente">Pendientes</option>
        <option value="aprobado">Aprobados</option>
        <option value="rechazado">Rechazados</option>
      </select>
      
      <input 
        type="text" 
        v-model="busqueda" 
        placeholder="Buscar por usuario..." 
        class="px-4 py-2 border rounded-lg flex-grow max-w-md"
      >
    </div>

    <!-- Lista de Solicitudes -->
    <div class="space-y-4">
      <div 
        v-for="solicitud in solicitudesFiltradas" 
        :key="solicitud.id"
        class="border rounded-lg p-4"
        :class="{
          'border-yellow-200 bg-yellow-50': solicitud.estado === 'pendiente',
          'border-green-200 bg-green-50': solicitud.estado === 'aprobado',
          'border-red-200 bg-red-50': solicitud.estado === 'rechazado'
        }"
      >
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
          <!-- Datos Usuario -->
          <div>
            <h3 class="font-semibold text-gray-800">{{ solicitud.usuario.nombre }}</h3>
            <p class="text-sm">Deuda: <span class="font-medium">Bs {{ solicitud.usuario.deuda.toFixed(2) }}</span></p>
          </div>
          
          <!-- Datos Pago -->
          <div>
            <p class="text-sm"><span class="font-medium">Banco:</span> {{ formatBanco(solicitud.pago.banco) }}</p>
            <p class="text-sm"><span class="font-medium">Celular:</span> {{ solicitud.pago.celular }}</p>
            <p class="text-sm"><span class="font-medium">Monto:</span> Bs {{ solicitud.pago.monto }}</p>
          </div>
          
          <!-- Estado -->
          <div class="flex items-center">
            <span 
              class="px-2 py-1 rounded-full text-xs font-medium"
              :class="{
                'bg-yellow-100 text-yellow-800': solicitud.estado === 'pendiente',
                'bg-green-100 text-green-800': solicitud.estado === 'aprobado',
                'bg-red-100 text-red-800': solicitud.estado === 'rechazado'
              }"
            >
              {{ formatEstado(solicitud.estado) }}
            </span>
          </div>
        </div>
        
        <!-- Acciones -->
        <div class="flex justify-between items-center pt-3 border-t border-gray-200">
          <div>
            <button 
              @click="verComprobante(solicitud)"
              class="text-sm text-fuchsia-700 hover:text-fuchsia-900 mr-4"
            >
              Ver comprobante
            </button>
            <span class="text-sm fuchsia-900">{{ formatFecha(solicitud.fecha) }}</span>
          </div>
          
          <div v-if="solicitud.estado === 'pendiente'" class="space-x-2">
            <button 
              @click="aprobarPago(solicitud.id)"
              class="px-3 py-1 bg-green-500 text-white rounded-md text-sm hover:bg-green-600"
            >
              Aprobar
            </button>
            <button 
              @click="rechazarPago(solicitud.id)"
              class="px-3 py-1 bg-red-500 text-white rounded-md text-sm hover:bg-red-600"
            >
              Rechazar
            </button>
          </div>
        </div>
      </div>
      
      <p v-if="solicitudesFiltradas.length === 0" class="text-center text-gray-500 py-6">
        No hay solicitudes que coincidan con los filtros
      </p>
    </div>
    
    <!-- Modal Comprobante -->
    <div v-if="comprobanteVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-auto">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Comprobante de Pago</h3>
          <button @click="comprobanteVisible = false" class="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>
        
        <div v-if="comprobanteActual" class="text-center">
          <img 
            v-if="esImagen(comprobanteActual)"
            :src="URL.createObjectURL(comprobanteActual)" 
            alt="Comprobante de pago"
            class="max-h-[70vh] mx-auto"
          >
          <div v-else class="p-8 bg-gray-100 rounded-lg">
            <p class="text-gray-600 mb-4">Documento PDF: {{ comprobanteActual.name }}</p>
            <button 
              @click="descargarComprobante"
              class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Descargar PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Datos simulados
const solicitudes = ref([
  {
    id: 'SOL-001',
    usuario: {
      id: 'USR-001',
      nombre: 'María González',
      deuda: 120.00
    },
    pago: {
      banco: 'bcp',
      celular: '987654321',
      monto: 120.00,
      comprobante: new File([''], 'comprobante.jpg', { type: 'image/jpeg' })
    },
    fecha: new Date(2023, 5, 15),
    estado: 'pendiente'
  },
  {
    id: 'SOL-002',
    usuario: {
      id: 'USR-002',
      nombre: 'Carlos Méndez',
      deuda: 85.50
    },
    pago: {
      banco: 'bbva',
      celular: '987123456',
      monto: 85.50,
      comprobante: new File([''], 'recibo.pdf', { type: 'application/pdf' })
    },
    fecha: new Date(2023, 5, 16),
    estado: 'pendiente'
  }
]);

// Filtros
const filtroEstado = ref('pendiente');
const busqueda = ref('');

// Modal comprobante
const comprobanteVisible = ref(false);
const comprobanteActual = ref(null);

// Filtrar solicitudes
const solicitudesFiltradas = computed(() => {
  return solicitudes.value.filter(s => {
    const cumpleEstado = filtroEstado.value === 'todos' || s.estado === filtroEstado.value;
    const cumpleBusqueda = s.usuario.nombre.toLowerCase().includes(busqueda.value.toLowerCase());
    return cumpleEstado && cumpleBusqueda;
  });
});

// Formateadores
const formatEstado = (estado) => {
  const estados = {
    pendiente: 'Pendiente',
    aprobado: 'Aprobado',
    rechazado: 'Rechazado'
  };
  return estados[estado] || estado;
};

const formatBanco = (banco) => {
  const bancos = {
    bcp: 'BCP',
    bbva: 'BBVA',
    interbank: 'Interbank',
    scotiabank: 'Scotiabank'
  };
  return bancos[banco] || banco;
};

const formatFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

// Acciones
const verComprobante = (solicitud) => {
  comprobanteActual.value = solicitud.pago.comprobante;
  comprobanteVisible.value = true;
};

const esImagen = (archivo) => {
  return archivo.type.startsWith('image/');
};

const descargarComprobante = () => {
  // En una app real, esto descargaría el archivo
  alert(`Descargando ${comprobanteActual.value.name}`);
};

const aprobarPago = (id) => {
  const solicitud = solicitudes.value.find(s => s.id === id);
  if (solicitud) {
    solicitud.estado = 'aprobado';
    // Aquí iría la lógica para actualizar la deuda del usuario
  }
};

const rechazarPago = (id) => {
  const solicitud = solicitudes.value.find(s => s.id === id);
  if (solicitud) {
    solicitud.estado = 'rechazado';
  }
};
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>