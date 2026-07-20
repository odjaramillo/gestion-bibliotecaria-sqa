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
            <span class="font-bold">Datos pago móvil</span>
            <br>
            <span>Número télefono: 0416-0000000</span>
            <br>
            <span>Rif: J-12345678</span>
            <br>
            <span>Bancamiga</span>
          </div>
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
              <label class="block font-medium">Número de Teléfono</label>
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