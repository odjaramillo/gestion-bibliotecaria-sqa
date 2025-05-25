<template>
  <div class="bg-white p-8 rounded-xl shadow-2xl max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-slate-700 mb-6">Registrar Nuevo Préstamo</h1>
    
    <form @submit.prevent="registrarPrestamo" class="space-y-6">
      <!-- Búsqueda de Usuario -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Usuario</label>
        <div class="relative">
          <input
            type="text"
            v-model="busquedaUsuario"
            @input="buscarUsuarios"
            placeholder="Buscar por nombre"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-900"
          >
          <ul v-if="resultadosUsuarios.length > 0 && busquedaUsuario" 
              class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
            <li v-for="usuario in resultadosUsuarios" 
                :key="usuario.id"
                @click="seleccionarUsuario(usuario)"
                class="px-4 py-2 hover:bg-purple-50 cursor-pointer">
              {{ usuario.nombre }} ({{ usuario.codigo }})
            </li>
          </ul>
        </div>
        <div v-if="usuarioSeleccionado" class="mt-2 p-2 bg-gray-50 rounded-md flex justify-between items-center">
          <span>{{ usuarioSeleccionado.nombre }} - {{ usuarioSeleccionado.codigo }}</span>
          <button @click="usuarioSeleccionado = null" class="text-red-500 hover:text-red-700">
            ✕
          </button>
        </div>
        <p v-if="errores.usuario" class="mt-1 text-sm text-red-600">{{ errores.usuario }}</p>
      </div>

      <!-- Búsqueda de Libro -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Libro</label>
        <div class="relative">
          <input
            type="text"
            v-model="busquedaLibro"
            @input="buscarLibros"
            placeholder="Buscar por título, autor o ISBN"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-900"
          >
          <ul v-if="resultadosLibros.length > 0 && busquedaLibro" 
              class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
            <li v-for="libro in resultadosLibros" 
                :key="libro.id"
                @click="seleccionarLibro(libro)"
                class="px-4 py-2 hover:bg-purple-50 cursor-pointer flex justify-between">
              <span>{{ libro.titulo }} ({{ libro.autor }})</span>
              <span :class="libro.disponible ? 'text-green-600' : 'text-red-600'" class="text-xs">
                {{ libro.disponible ? 'Disponible' : 'Prestado' }}
              </span>
            </li>
          </ul>
        </div>
        <div v-if="libroSeleccionado" class="mt-2 p-2 bg-gray-50 rounded-md flex justify-between items-center">
          <span>{{ libroSeleccionado.titulo }} ({{ libroSeleccionado.autor }})</span>
          <button @click="libroSeleccionado = null" class="text-red-500 hover:text-red-700">
            ✕
          </button>
        </div>
        <p v-if="errores.libro" class="mt-1 text-sm text-red-600">{{ errores.libro }}</p>
      </div>

      <!-- Fechas -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="fechaPrestamo" class="block text-sm font-medium text-gray-700">Fecha de Préstamo</label>
          <input
            type="date"
            id="fechaPrestamo"
            v-model="prestamo.fechaPrestamo"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          >
        </div>
        <div>
          <label for="fechaDevolucion" class="block text-sm font-medium text-gray-700">Fecha de Devolución</label>
          <input
            type="date"
            id="fechaDevolucion"
            v-model="prestamo.fechaDevolucion"
            :min="prestamo.fechaPrestamo"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          >
        </div>
      </div>

      <!-- Observaciones -->
      <div>
        <label for="observaciones" class="block text-sm font-medium text-gray-700">Observaciones</label>
        <textarea
          id="observaciones"
          v-model="prestamo.observaciones"
          rows="2"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-fuchsia-900 focus:border-fuchsia-900"
          placeholder="Ej: Libro con daño leve en portada"
        ></textarea>
      </div>

      <!-- Botones -->
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="cancelar"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="procesando"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
        >
          {{ procesando ? 'Registrando...' : 'Registrar Préstamo' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Datos simulados - en producción vendrían de una API
const usuarios = ref([
  { id: 1, codigo: 'USR-001', nombre: 'María González', email: 'maria@example.com' },
  { id: 2, codigo: 'USR-002', nombre: 'Juan Pérez', email: 'juan@example.com' },
  { id: 3, codigo: 'USR-003', nombre: 'Carlos Méndez', email: 'carlos@example.com' }
]);

const libros = ref([
  { id: 1, titulo: 'El nombre del viento', autor: 'Patrick Rothfuss', isbn: '978-84-666-3768-9', disponible: true },
  { id: 2, titulo: 'Cien años de soledad', autor: 'Gabriel García Márquez', isbn: '978-84-376-0494-7', disponible: false },
  { id: 3, titulo: '1984', autor: 'George Orwell', isbn: '978-84-9759-227-7', disponible: true }
]);

// Estado del componente
const busquedaUsuario = ref('');
const busquedaLibro = ref('');
const resultadosUsuarios = ref([]);
const resultadosLibros = ref([]);
const usuarioSeleccionado = ref(null);
const libroSeleccionado = ref(null);
const procesando = ref(false);

const prestamo = reactive({
  fechaPrestamo: new Date().toISOString().split('T')[0],
  fechaDevolucion: '',
  observaciones: ''
});

const errores = reactive({
  usuario: '',
  libro: ''
});

// Métodos
const buscarUsuarios = () => {
  if (!busquedaUsuario.value.trim()) {
    resultadosUsuarios.value = [];
    return;
  }
  const termino = busquedaUsuario.value.toLowerCase();
  resultadosUsuarios.value = usuarios.value.filter(u => 
    u.nombre.toLowerCase().includes(termino) || 
    u.codigo.toLowerCase().includes(termino)
  );
};

const buscarLibros = () => {
  if (!busquedaLibro.value.trim()) {
    resultadosLibros.value = [];
    return;
  }
  const termino = busquedaLibro.value.toLowerCase();
  resultadosLibros.value = libros.value.filter(l => 
    l.titulo.toLowerCase().includes(termino) || 
    l.autor.toLowerCase().includes(termino) ||
    l.isbn.includes(termino)
  );
};

const seleccionarUsuario = (usuario) => {
  usuarioSeleccionado.value = usuario;
  busquedaUsuario.value = '';
  resultadosUsuarios.value = [];
  errores.usuario = '';
};

const seleccionarLibro = (libro) => {
  if (!libro.disponible) {
    errores.libro = 'Este libro no está disponible para préstamo';
    return;
  }
  libroSeleccionado.value = libro;
  busquedaLibro.value = '';
  resultadosLibros.value = [];
  errores.libro = '';
};

const validarFormulario = () => {
  let valido = true;
  
  if (!usuarioSeleccionado.value) {
    errores.usuario = 'Debe seleccionar un usuario';
    valido = false;
  } else {
    errores.usuario = '';
  }
  
  if (!libroSeleccionado.value) {
    errores.libro = 'Debe seleccionar un libro disponible';
    valido = false;
  } else {
    errores.libro = '';
  }
  
  return valido;
};

const registrarPrestamo = async () => {
  if (!validarFormulario()) return;
  
  procesando.value = true;
  
  try {
    // Simular llamada a API
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const nuevoPrestamo = {
      id: Date.now(),
      usuario: usuarioSeleccionado.value,
      libro: libroSeleccionado.value,
      fechaPrestamo: prestamo.fechaPrestamo,
      fechaDevolucion: prestamo.fechaDevolucion,
      observaciones: prestamo.observaciones,
      estado: 'activo'
    };
    
    console.log('Préstamo registrado:', nuevoPrestamo);
    alert('Préstamo registrado exitosamente!');
    
    // Resetear formulario
    usuarioSeleccionado.value = null;
    libroSeleccionado.value = null;
    prestamo.fechaDevolucion = '';
    prestamo.observaciones = '';
    
  } catch (error) {
    console.error('Error al registrar préstamo:', error);
    alert('Ocurrió un error al registrar el préstamo');
  } finally {
    procesando.value = false;
  }
};

const cancelar = () => {
  // Lógica para cancelar (puede emitir un evento o redirigir)
  console.log('Operación cancelada');
};
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