<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn max-w-4xl mx-auto">
    <!-- Encabezado -->
    <div class="flex justify-between items-start mb-6">
      <h1 class="text-3xl font-bold text-slate-700">{{ libro.titulo }}</h1>
      <button 
        @click="$router.go(-1)"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
      >
        Volver
      </button>
    </div>

    <!-- Contenido principal -->
    <div class="flex flex-col md:flex-row gap-8">
      <!-- Portada y detalles básicos -->
      <div class="md:w-1/3">
        <img 
          :src="libro.portadaUrl" 
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
            <span :class="libro.disponible ? 'text-green-600' : 'text-red-600'">
              {{ libro.disponible ? 'Disponible' : 'Prestado' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Descripción y comentarios -->
      <div class="md:w-2/3">
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-slate-700 mb-2">Descripción</h2>
          <p class="text-gray-700">{{ libro.descripcion }}</p>
        </div>

        <!-- Sección de comentarios -->
        <div>
          <h2 class="text-xl font-semibold text-slate-700 mb-4">Comentarios ({{ comentarios.length }})</h2>
          
          <!-- Formulario nuevo comentario -->
          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <textarea
              v-model="nuevoComentario"
              placeholder="Escribe tu comentario..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-fuchsia-900"
              rows="3"
            ></textarea>
            <button
              @click="agregarComentario"
              class="mt-2 px-4 py-2 bg-fuchsia-700 text-white rounded-md hover:bg-fuchsia-900 transition-colors"
              :disabled="!nuevoComentario.trim()"
            >
              Publicar comentario
            </button>
          </div>

          <!-- Lista de comentarios -->
          <div class="space-y-4">
            <div 
              v-for="comentario in comentarios" 
              :key="comentario.id"
              class="p-4 border border-gray-200 rounded-lg"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <span class="font-semibold">{{ comentario.usuario }}</span>
                  <span class="text-gray-500 text-sm ml-2">{{ formatFecha(comentario.fecha) }}</span>
                </div>
                <button 
                  v-if="comentario.usuarioId === usuarioActual.id"
                  @click="eliminarComentario(comentario.id)"
                  class="text-red-500 hover:text-red-700"
                >
                  Eliminar
                </button>
              </div>
              <p class="text-gray-700 mb-2">{{ comentario.texto }}</p>
              
              <!-- Respuestas -->
              <div 
                v-if="comentario.respuestas.length"
                class="ml-6 mt-3 space-y-3 border-l-2 border-gray-200 pl-4"
              >
                <div 
                  v-for="respuesta in comentario.respuestas" 
                  :key="respuesta.id"
                  class="text-sm"
                >
                  <div class="flex justify-between">
                    <span class="font-semibold">{{ respuesta.usuario }}</span>
                    <span class="text-gray-500">{{ formatFecha(respuesta.fecha) }}</span>
                  </div>
                  <p class="text-gray-600">{{ respuesta.texto }}</p>
                </div>
              </div>

              <!-- Formulario respuesta -->
              <div class="mt-3 flex items-center">
                <input
                  v-model="respuestasTemporales[comentario.id]"
                  type="text"
                  placeholder="Escribe una respuesta..."
                  class="flex-1 px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-fuchsia-900"
                >
                <button
                  @click="agregarRespuesta(comentario.id)"
                  class="ml-2 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm transition-colors"
                  :disabled="!respuestasTemporales[comentario.id]?.trim()"
                >
                  Responder
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';


// Datos del libro (simulados)
const libro = reactive({
  titulo: 'El nombre del viento',
  autor: 'Patrick Rothfuss',
  genero: 'Fantasía épica',
  anio: 2007,
  isbn: '978-84-666-3768-9',
  descripcion: 'La historia de Kvothe, un personaje legendario que relata su propia biografía. Una obra maestra de la fantasía contemporánea que ha cautivado a millones de lectores.',
  portadaUrl: 'https://m.media-amazon.com/images/I/81iqZ+tL2ZL._AC_UF1000,1000_QL80_.jpg',
  disponible: true
});

// Comentarios y respuestas (simulados)
const comentarios = ref([
  {
    id: 1,
    usuario: 'María González',
    usuarioId: 2,
    texto: 'Una de las mejores novelas de fantasía que he leído. La prosa de Rothfuss es simplemente mágica.',
    fecha: new Date(2023, 5, 15),
    respuestas: [
      {
        id: 1,
        usuario: 'Carlos Méndez',
        texto: 'Totalmente de acuerdo, especialmente la construcción del sistema de magia.',
        fecha: new Date(2023, 5, 16)
      }
    ]
  },
  {
    id: 2,
    usuario: 'Juan Pérez',
    usuarioId: 1,
    texto: '¿Alguien sabe cuándo saldrá la tercera parte? Llevo años esperando...',
    fecha: new Date(2023, 4, 22),
    respuestas: []
  }
]);

// Usuario actual (simulado)
const usuarioActual = reactive({
  id: 1,
  nombre: 'Juan Pérez'
});

// Nuevo comentario
const nuevoComentario = ref('');
const respuestasTemporales = reactive({});

// Funciones
const agregarComentario = () => {
  if (!nuevoComentario.value.trim()) return;
  
  comentarios.value.push({
    id: Date.now(),
    usuario: usuarioActual.nombre,
    usuarioId: usuarioActual.id,
    texto: nuevoComentario.value,
    fecha: new Date(),
    respuestas: []
  });
  
  nuevoComentario.value = '';
};

const agregarRespuesta = (comentarioId) => {
  const respuestaTexto = respuestasTemporales[comentarioId];
  if (!respuestaTexto?.trim()) return;
  
  const comentario = comentarios.value.find(c => c.id === comentarioId);
  if (comentario) {
    comentario.respuestas.push({
      id: Date.now(),
      usuario: usuarioActual.nombre,
      texto: respuestaTexto,
      fecha: new Date()
    });
    respuestasTemporales[comentarioId] = '';
  }
};

const eliminarComentario = (id) => {
  comentarios.value = comentarios.value.filter(c => c.id !== id);
};

const formatFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
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