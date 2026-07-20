<template>
  <div class="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-2xl">

    <!-- Titulo-->

    <h2 class="text-3xl font-bold text-slate-700 mb-8 text-center">Registro de Nuevo Libro</h2>

    <div v-if="!registroExitoso">

      <!-- Form pagina 1-->

      <form @submit.prevent="handleBookRegistration" class="space-y-6">
        <div v-if="currentStep === 1" class="animate-fadeIn">
          <h3 class="text-xl font-semibold text-gray-700 mb-4">1. Detalles del Libro</h3>
          <div>
            <label for="titulo" class="block text-sm font-medium text-gray-700">Título</label>
            <input type="text" id="titulo" v-model="libro.titulo" required
                   :class="{'border-red-500': errors.titulo}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.titulo" class="text-red-500 text-xs mt-1">{{ errors.titulo }}</p>
          </div>
          <div>
            <label for="genero" class="block text-sm font-medium text-gray-700 mt-4">Género</label>
            <input type="text" id="genero" v-model="libro.genero" required
                   :class="{'border-red-500': errors.genero}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.genero" class="text-red-500 text-xs mt-1">{{ errors.genero }}</p>
          </div>
          <div>
            <label for="editorial" class="block text-sm font-medium text-gray-700 mt-4">Editorial</label>
            <input type="text" id="editorial" v-model="libro.editorial"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
          </div>
          <div>
            <label for="autor" class="block text-sm font-medium text-gray-700 mt-4">Autor</label>
            <input type="text" id="autor" v-model="libro.autor" required
                   :class="{'border-red-500': errors.autor}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.autor" class="text-red-500 text-xs mt-1">{{ errors.autor }}</p>
          </div>
          <div>
            <label for="isbn" class="block text-sm font-medium text-gray-700 mt-4">ISBN</label>
            <input type="number" id="isbn" v-model="libro.isbn" required
                   :class="{'border-red-500': errors.isbn}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.isbn" class="text-red-500 text-xs mt-1">{{ errors.isbn }}</p>
          </div>
          <div>
            <label for="anio" class="block text-sm font-medium text-gray-700 mt-4">Año</label>
            <input type="number" id="anio" v-model="libro.anio" required
                   :class="{'border-red-500': errors.anio}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.anio" class="text-red-500 text-xs mt-1">{{ errors.anio }}</p>
          </div>
          <div>
            <label for="cantidad" class="block text-sm font-medium text-gray-700 mt-4">Cantidad</label>
            <input type="number" id="cantidad" v-model="libro.cantidad" required
                   :class="{'border-red-500': errors.cantidad}"
                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm">
            <p v-if="errors.cantidad" class="text-red-500 text-xs mt-1">{{ errors.cantidad }}</p>
          </div>
          <div>
            <label for="sinopsis" class="block text-sm font-medium text-gray-700 mt-4">Sinopsis</label>
            <textarea id="sinopsis" v-model="libro.sinopsis" required
                      :class="{'border-red-500': errors.sinopsis}"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900 sm:text-sm"></textarea>
            <p v-if="errors.sinopsis" class="text-red-500 text-xs mt-1">{{ errors.sinopsis }}</p>
          </div>
        </div>

        <!-- Form pagina 2-->

        <div v-if="currentStep === 2" class="animate-fadeIn">
          <h3 class="text-xl font-semibold text-gray-700 mb-4">2. Imagen de libro</h3>
          <div>
            <label for="imagen" class="block text-sm font-medium text-gray-700">Añadir imagen</label>
            <input type="file" id="imagen" @change="handleImageUpload" accept="image/*"
                   class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-fuchsia-700 file:text-white hover:file:bg-fuchsia-800">
            <p v-if="errors.imagen" class="text-red-500 text-xs mt-1">{{ errors.imagen }}</p>
          </div>
          <div v-if="libro.imagenPreviewUrl" class="mt-4">
            <p class="text-sm font-medium text-gray-700">Vista previa:</p>
            <img :src="libro.imagenPreviewUrl" alt="Vista previa de la portada" class="mt-2 rounded-md max-h-60 border border-gray-300">
          </div>
        </div>

        <div v-if="currentStep === 3" class="animate-fadeIn">
          <h3 class="text-xl font-semibold text-gray-700 mb-4">3. Revisar y Crear</h3>
          <div class="bg-gray-50 p-6 rounded-lg shadow">
            <h4 class="text-lg font-semibold text-fuchsia-700 mb-2">{{ libro.titulo || 'Título del Libro' }}</h4>
            <p class="text-sm text-gray-600"><strong>Autor:</strong> {{ libro.autor || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>Género:</strong> {{ libro.genero || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>Editorial:</strong> {{ libro.editorial || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>ISBN:</strong> {{ libro.isbn || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>Año:</strong> {{ libro.anio || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>Cantidad:</strong> {{ libro.cantidad || 'N/A' }}</p>
            <p class="text-sm text-gray-600"><strong>Sinopsis:</strong> {{ libro.sinopsis || 'N/A' }}</p>
            <div v-if="libro.imagenPreviewUrl" class="mt-4">
              <img :src="libro.imagenPreviewUrl" alt="Portada" class="rounded-md max-h-48 border">
            </div>
            <div v-else class="mt-4 h-48 bg-gray-200 rounded-md flex items-center justify-center text-gray-400">
              Sin imagen de portada
            </div>
          </div>
          <p class="mt-6 text-sm text-gray-500">Revisa los detalles del libro. Al hacer clic en "Registrar libro", el libro se registrará en el sistema.</p>
        </div>

        <!-- Form Botones-->
        <div class="mt-10 flex justify-between items-center">
          <button type="button" v-if="currentStep > 1" @click="prevStep"
                  class="py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-fuchsia-700 transition-colors">
            Anterior
          </button>
          <div v-else></div>
          <button type="button" v-if="currentStep < 3" @click="nextStep"
                  class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-fuchsia-700 transition-colors">
            Siguiente
          </button>
          <button type="submit" v-if="currentStep === 3"
                  class="py-2 px-6 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-fuchsia-700 transition-colors">
            Registrar libro
          </button>
        </div>
        <p v-if="submissionStatus" :class="submissionStatus.type === 'success' ? 'text-green-500' : 'text-red-500'" class="text-center text-sm mt-4">{{ submissionStatus.message }}</p>
      </form>
    </div>

    <div v-if="registroExitoso" class="text-center py-10 animate-fadeIn">
      <svg class="w-16 h-16 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3 class="text-2xl font-semibold text-gray-800">¡Éxito!</h3>
      <p class="text-gray-600 mt-2">"Se ha añadido el libro al catálogo exitosamente."</p>
      <button @click="resetForm"
              class="mt-6 py-2 px-6 bg-fuchsia-700 text-white rounded-md hover:bg-fuchsia-900 transition-colors">
        Registrar Otro Libro
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
// import { inject } from 'vue';

const props = defineProps({
  usuario: {
    type: Object,
    required: true
  }
});

// const user = inject('user', null);

const currentStep = ref(1);
const totalSteps = 3;
const registroExitoso = ref(false);
const submissionStatus = ref(null);

const libro = reactive({
  titulo: '',
  genero: '',
  editorial: '',
  autor: '',
  isbn: '',
  anio: '',
  cantidad: '',
  sinopsis: '',
  imagenFile: null,
  imagenPreviewUrl: ''
});

const errors = reactive({
  titulo: '',
  genero: '',
  autor: '',
  isbn: '',
  anio: '',
  cantidad: '',
  sinopsis: '',
  imagen: ''
});

const validateStep1 = () => {
  errors.titulo = !libro.titulo ? 'El título es obligatorio.' : '';
  errors.genero = !libro.genero ? 'El género es obligatorio.' : '';
  errors.autor = !libro.autor ? 'El autor es obligatorio.' : '';
  errors.isbn = !libro.isbn ? 'El ISBN es obligatorio.' : '';
  errors.anio = !libro.anio ? 'El año es obligatorio.' : '';
  errors.cantidad = !libro.cantidad ? 'La cantidad es obligatoria.' : '';
  errors.sinopsis = !libro.sinopsis ? 'La sinopsis es obligatoria.' : '';
  return !errors.titulo && !errors.genero && !errors.autor && !errors.isbn && !errors.anio && !errors.cantidad && !errors.sinopsis;
};

const validateStep2 = () => {
  errors.imagen = '';
  return true;
};

const nextStep = () => {
  let isValid = false;
  if (currentStep.value === 1) {
    isValid = validateStep1();
  } else if (currentStep.value === 2) {
    isValid = validateStep2();
  }
  if (isValid && currentStep.value < totalSteps) {
    currentStep.value++;
    submissionStatus.value = null;
  } else if (!isValid) {
    submissionStatus.value = { type: 'error', message: 'Por favor, corrige los errores del paso actual.' };
  }
};


const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
    submissionStatus.value = null;
  }
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    libro.imagenFile = file;
    libro.imagenPreviewUrl = URL.createObjectURL(file);
    errors.imagen = '';
  } else {
    libro.imagenFile = null;
    libro.imagenPreviewUrl = '';
  }
};

const handleBookRegistration = async () => {
  submissionStatus.value = null;
  if (!validateStep1() && currentStep.value === 1) {
    submissionStatus.value = { type: 'error', message: 'Faltan datos en el paso 1.' };
    currentStep.value = 1;
    return;
  }
  const formData = new FormData();
  formData.append('libro', new Blob([JSON.stringify({
    titulo: libro.titulo,
    genero: libro.genero,
    editorial: libro.editorial,
    autor: libro.autor,
    isbn: libro.isbn,
    anio: libro.anio,
    cantidad: libro.cantidad,
    sinopsis: libro.sinopsis
  })], { type: 'application/json' }));
  if (libro.imagenFile) {
    formData.append('imagen', libro.imagenFile);
  }
  formData.append('correoUsuario', props.usuario.correo);

  try {
    const res = await fetch('/api/libros', {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      throw new Error('Error al registrar libro');
    }
    const msg = await res.text();
    submissionStatus.value = { type: 'success', message: msg };
    registroExitoso.value = true;
    // Actualizar libros en la pantalla principal
    window.dispatchEvent(new Event('libro-registrado'));
  } catch (e) {
    submissionStatus.value = { type: 'error', message: 'No se pudo registrar el libro.' };
  }
};

const resetForm = () => {
  currentStep.value = 1;
  registroExitoso.value = false;
  submissionStatus.value = null;
  libro.titulo = '';
  libro.genero = '';
  libro.editorial = '';
  libro.autor = '';
  libro.isbn = '';
  libro.anio = '';
  libro.cantidad = '';
  libro.sinopsis = '';
  libro.imagenFile = null;
  libro.imagenPreviewUrl = '';
  Object.keys(errors).forEach(key => errors[key] = '');
  const inputFile = document.getElementById('imagen');
  if (inputFile) {
    inputFile.value = '';
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>