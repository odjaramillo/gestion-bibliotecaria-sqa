<!-- <template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-md mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Solicitud de Pago</h1>
    
  
    <div class="mb-6 p-4 border border-gray-200 rounded-lg">
      <h2 class="text-lg font-semibold text-gray-800 mb-2">Información del Usuario</h2>
      <div class="space-y-2">
        <p><span class="font-medium">Nombre:</span> {{ usuario.nombre }}</p>
        <p><span class="font-medium">Deuda Total:</span>  {{ usuario.deuda.toFixed(2) }} Bs</p>
      </div>
    </div>

    
    <form @submit.prevent="enviarSolicitud" class="space-y-4">
      <div class="border border-purple-200 rounded-lg p-4 bg-fuchsia-50">
        <h2 class="text-lg font-semibold text-slate-700 mb-3">Datos del Pago Móvil</h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Banco</label>
          <select 
            v-model="pago.banco"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          >
            <option value="">Seleccionar banco</option>
            <option value="bcp">(0102) Banco de Venezuela</option>
            <option value="bcp">(0104) Banco Venezolano de Crédito</option>
            <option value="bcp">(0105) Banco Mercantil C.A.</option>
            <option value="bcp">(0108) BBVA Provincial</option>
            <option value="bcp">(0114) Bancaribe</option>
            <option value="bcp">(0115) Banco Exterior</option>
            <option value="bcp">(0128) Banco Caroní</option>
            <option value="bcp">(0134) Banesco Banco Universal</option>
            <option value="bcp">(0137) Banco Sofitasa</option>
            <option value="bcp">(0138) Banco Plaza</option>
            <option value="bcp">(0172) Bancamiga</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Número de celular</label>
          <input
            type="tel"
            v-model="pago.celular"
            placeholder="987 654 321"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Monto a pagar (Bs)</label>
          <input
            type="number"
            v-model="pago.monto"
            :max="usuario.deuda"
            min="0.01"
            step="0.01"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          >
          <p class="text-xs text-gray-500 mt-1">Máximo: Bs {{ usuario.deuda.toFixed(2) }}</p>
        </div>
      </div>

      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Comprobante de pago</label>
        <div class="flex items-center justify-center w-full">
          <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <p class="text-sm text-gray-500">
                <span class="font-semibold">Haz clic para subir</span> o arrastra el archivo
              </p>
            </div>
            <input 
              type="file" 
              @change="handleFileUpload"
              accept="image/*,.pdf"
              required
              class="hidden"
            >
          </label>
        </div>
        <p v-if="pago.comprobante" class="mt-2 text-sm text-green-600">
          Archivo seleccionado: {{ pago.comprobante.name }}
        </p>
      </div>

      
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="procesando"
          class="px-4 py-2 bg-fuchsia-700 text-white rounded-md shadow-sm text-sm font-medium hover:bg-fuchsia-700 focus:outline-none disabled:opacity-50"
        >
          {{ procesando ? 'Enviando...' : 'Enviar Solicitud' }}
        </button>
      </div>
    </form>
  </div>
</template> -->

<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-md mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Amonestaciones</h1>
    <div v-if="cargando" class="text-gray-500">Cargando...</div>
    <div v-else>
      <div v-if="!tieneAmonestacion" class="text-green-700 font-semibold">
        No tienes amonestaciones pendientes.
      </div>
      <div v-else>
        <div v-for="amon in amonestaciones" :key="amon.id" class="border p-4 rounded-lg mb-4 bg-red-50">
          <div class="mb-2">
            <span class="font-bold">Monto:</span> {{ amon.monto }} Bs
          </div>
          <div class="mb-2">
            <span class="font-bold">Estado:</span>
            <span v-if="amon.pagada" class="text-green-700">Pagada</span>
            <span v-else class="text-red-700">Pendiente</span>
          </div>
          <form v-if="!amon.pagada" @submit.prevent="pagarAmonestacion(amon.id)">
            <div class="mb-2">
              <label class="block font-medium">Método de pago</label>
              <input v-model="form.metodoPago" required class="border rounded px-2 py-1 w-full" />
            </div>
            <div class="mb-2">
              <label class="block font-medium">Comprobante de pago</label>
              <input v-model="form.comprobantePago" required class="border rounded px-2 py-1 w-full" />
            </div>
            <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Registrar Pago</button>
          </form>
          <div v-else class="text-green-700 mt-2">Pago registrado</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Datos simulados del usuario (en producción vendrían de una API)
/* const usuario = ref({
  nombre: 'Juan Pérez',
  deuda: 150.50
});

const pago = ref({
  banco: '',
  celular: '',
  monto: '',
  comprobante: null
}); */

// const procesando = ref(false);

const tieneAmonestacion = ref(false);
const amonestaciones = ref([]);
const form = ref({
  metodoPago: '',
  comprobantePago: ''
});
const cargando = ref(true);

const cargarAmonestaciones = async () => {
  cargando.value = true;
  try {
    const res = await fetch('/api/amonestaciones-usuario/mis-amonestaciones', { credentials: 'include' });
    const data = await res.json();
    tieneAmonestacion.value = !!(data.amonestaciones && data.amonestaciones.length > 0);
    amonestaciones.value = data.amonestaciones || [];
  } finally {
    cargando.value = false;
  }
};

const pagarAmonestacion = async (amonestacionId) => {
  await fetch('/api/amonestaciones-usuario/pagar', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      amonestacionId,
      metodoPago: form.value.metodoPago,
      comprobantePago: form.value.comprobantePago
    })
  });
  await cargarAmonestaciones();
  form.value.metodoPago = '';
  form.value.comprobantePago = '';
};

onMounted(() => {
  cargarAmonestaciones();
});

/* const handleFileUpload = (event) => {
  pago.value.comprobante = event.target.files[0];
};

const enviarSolicitud = async () => {
  procesando.value = true;
  
  try {
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const solicitud = {
      usuario: usuario.value,
      pago: pago.value,
      fecha: new Date().toISOString(),
      estado: 'pendiente'
    };
    
    console.log('Solicitud creada:', solicitud);
    alert('Solicitud enviada para aprobación');
    
    
    pago.value = {
      banco: '',
      celular: '',
      monto: '',
      comprobante: null
    };
    
  } finally {
    procesando.value = false;
  }
}; */
</script>

<style scoped>
/* Estilos opcionales para animación de entrada */
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>