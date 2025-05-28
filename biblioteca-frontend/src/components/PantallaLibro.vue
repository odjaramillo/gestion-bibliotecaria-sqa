<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn max-w-4xl mx-auto">
    <div class="flex justify-between items-start mb-6">
      <h1 class="text-3xl font-bold text-slate-700">{{ libro.titulo }}</h1>
      <button 
        @click="$emit('volver')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
      >
        Volver
      </button>
    </div>
    <div class="flex flex-col md:flex-row gap-8">
      <div class="md:w-1/3">
        <img 
          :src="libro.imagenBase64 || libro.portadaUrl || 'https://placehold.co/300x400/A9A9A9/FFF?text=Sin+Imagen'" 
          :alt="'Portada de ' + libro.titulo"
          class="w-full rounded-lg shadow-md"
        >
        <div class="mt-4 space-y-2">
          <p><span class="font-semibold">Autor:</span> {{ libro.autor }}</p>
          <p><span class="font-semibold">Género:</span> {{ libro.genero }}</p>
          <p><span class="font-semibold">Año:</span> {{ libro.anio }}</p>
          <p><span class="font-semibold">ISBN:</span> {{ libro.isbn }}</p>
          <div class="flex items-center mt-2">
            <span class="font-semibold mr-2">Estado:</span>
            <span :class="(libro.cantidad && libro.cantidad >= 1) ? 'text-green-600' : 'text-red-600'">
              {{ (libro.cantidad && libro.cantidad >= 1) ? 'Disponible' : 'Prestado' }}
            </span>
          </div>
        </div>
      </div>
      <div class="md:w-2/3">
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-slate-700 mb-2">Descripción</h2>
          <p class="text-gray-700">{{ libro.sinopsis }}</p>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-slate-700 mb-4">Comentarios ({{ resenas.length }})</h2>
          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <textarea
              v-model="nuevaResena"
              placeholder="Escribe tu reseña..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-fuchsia-900"
              rows="3"
            ></textarea>
            <button
              @click="agregarResena"
              class="mt-2 px-4 py-2 bg-fuchsia-700 text-white rounded-md hover:bg-fuchsia-900 transition-colors"
              :disabled="!nuevaResena.trim()"
            >
              Publicar comentario
            </button>
          </div>
          <div class="space-y-6">
            <div 
              v-for="resena in resenas" 
              :key="resena.id"
              class="p-4 border border-gray-200 rounded-lg"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-semibold">{{ resena.usuarioNombre }}</span>
                  <span class="text-gray-500 text-sm ml-2">{{ formatFecha(resena.fecha) }}</span>
                </div>
                <button 
                  v-if="resena.usuarioId === usuarioActual.id"
                  @click="eliminarResena(resena.id)"
                  class="text-red-500 hover:text-red-700"
                >
                  Eliminar
                </button>
              </div>
              <p class="text-gray-700 mb-2">{{ resena.texto }}</p>
              <div>
                <h3 class="font-semibold text-sm mb-1">Comentarios ({{ resena.comentarios.length }})</h3>
                <div class="mb-2">
                  <input
                    v-model="comentariosTemporales[resena.id]"
                    type="text"
                    placeholder="Escribe un comentario..."
                    class="w-full px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-fuchsia-900"
                  >
                  <button
                    @click="agregarComentarioResena(resena.id)"
                    class="mt-2 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm transition-colors"
                    :disabled="!comentariosTemporales[resena.id]?.trim()"
                  >
                    Comentar
                  </button>
                </div>
                <div class="space-y-2">
                  <div 
                    v-for="comentario in resena.comentarios"
                    :key="comentario.id"
                    class="pl-2 border-l-2 border-gray-200"
                  >
                    <div class="flex justify-between">
                      <span class="font-semibold">{{ comentario.usuarioNombre }}</span>
                      <span class="text-gray-500 text-xs">{{ formatFecha(comentario.fecha) }}</span>
                      <button 
                        v-if="comentario.usuarioId === usuarioActual.id"
                        @click="eliminarComentarioResena(comentario.id)"
                        class="text-red-500 hover:text-red-700 text-xs ml-2"
                      >
                        Eliminar
                      </button>
                    </div>
                    <p class="text-gray-600 text-sm">{{ comentario.texto }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed} from 'vue'
import axios from 'axios'

const props = defineProps({
  libro: {
    type: Object,
    required: true
  },
  usuario: {
    type: Object,
    required: true
  }
})

const usuarioActual = computed(() => props.usuario || {})

const resenas = ref([])
const nuevaResena = ref('')
const comentariosTemporales = reactive({})

const cargarResenas = async () => {
  try {
    const res = await axios.get(`/api/resenas/libro/${props.libro.id}`)
    resenas.value = res.data.map(r => ({
      id: r.id,
      usuarioId: r.usuario.id,
      usuarioNombre: r.usuario.nombre,
      texto: r.texto,
      fecha: r.fecha,
      comentarios: []
    }))
    for (const resena of resenas.value) {
      const resp = await axios.get(`/api/comentarios-resena/resena/${resena.id}`)
      resena.comentarios = resp.data.map(c => ({
        id: c.id,
        usuarioId: c.usuario.id,
        usuarioNombre: c.usuario.nombre,
        texto: c.texto,
        fecha: c.fecha
      }))
    }
  } catch (e) {
    resenas.value = []
  }
}

const agregarResena = async () => {
  if (!usuarioActual.value.id) {
    window.location.href = '/'; // Redirige a inicio de sesión
    return;
  }
  if (!nuevaResena.value.trim() || !usuarioActual.value.id) return
  await axios.post('/api/resenas', {
    libroId: props.libro.id,
    usuarioId: usuarioActual.value.id,
    texto: nuevaResena.value
  })
  nuevaResena.value = ''
  await cargarResenas()
}

const eliminarResena = async (resenaId) => {}

const agregarComentarioResena = async (resenaId) => {
  if (!usuarioActual.value.id) {
    window.location.href = '/'; // Redirige a inicio de sesión
    return;
  }
  const texto = comentariosTemporales[resenaId]
  if (!texto?.trim() || !usuarioActual.value.id) return
  await axios.post('/api/comentarios-resena', {
    resenaId,
    usuarioId: usuarioActual.value.id,
    texto
  })
  comentariosTemporales[resenaId] = ''
  await cargarResenas()
}

const eliminarComentarioResena = async (comentarioId) => {}

const formatFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  cargarResenas()
})
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