<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Verificar Pagos de Amonestaciones</h1>
    <div class="space-y-4">
      <div v-for="amon in amonestaciones" :key="amon.id" class="border rounded-lg p-4 bg-yellow-50">
        <div class="mb-2">
          <span class="font-bold">Usuario:</span> {{ amon.usuario.nombre }} ({{ amon.usuario.correo }})
        </div>
        <div class="mb-2">
          <span class="font-bold">Monto:</span> {{ amon.monto }} Bs
        </div>
        <div class="mb-2">
          <span class="font-bold">Método de pago:</span> {{ amon.metodoPago }}
        </div>
        <div class="mb-2">
          <span class="font-bold">Comprobante:</span> {{ amon.comprobantePago }}
        </div>
        <div class="mb-2">
          <span class="font-bold">Estado:</span>
          <span v-if="amon.verificada" class="text-green-700">Verificada</span>
          <span v-else class="text-yellow-700">Pendiente</span>
        </div>
        <div class="flex gap-2">
          <button v-if="!amon.verificada" @click="verificarAmonestacion(amon.id)" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Comprobar</button>
          <button v-if="!amon.verificada" @click="eliminarAmonestacion(amon.id)" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">Eliminar Amonestación</button>
          <span v-if="amon.verificada" class="text-green-700 font-semibold">Pago verificado</span>
        </div>
      </div>
      <p v-if="amonestaciones.length === 0" class="text-center text-gray-500 py-6">
        No hay pagos pendientes de verificación
      </p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';


const amonestaciones = ref([]);

const cargarAmonestaciones = async () => {
  const res = await fetch('/api/amonestaciones-usuario/todas', { credentials: 'include' });
  const data = await res.json();
  amonestaciones.value = data || [];
};

const verificarAmonestacion = async (amonestacionId) => {
  await fetch(`/api/amonestaciones-usuario/verificar/${amonestacionId}`, {
    method: 'PUT',
    credentials: 'include'
  });
  await cargarAmonestaciones();
};

const eliminarAmonestacion = async (amonestacionId) => {
  if (confirm('¿Está seguro de que desea eliminar esta amonestación?')) {
    try {
      const res = await fetch(`/api/amonestaciones/${amonestacionId}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (res.ok) {
        await cargarAmonestaciones();
      } else {
        const error = await res.text();
        alert('Error al eliminar amonestación: ' + error);
      }
    } catch (e) {
      alert('Error al eliminar amonestación');
    }
  }
};

onMounted(() => {
  cargarAmonestaciones();
});

</script>

<style scoped>
</style>