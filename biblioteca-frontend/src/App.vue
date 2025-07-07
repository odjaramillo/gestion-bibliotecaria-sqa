<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-gray-700 text-white p-6 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
        <h1 class="text-3xl font-bold">Gestión Bibliotecaria</h1>
        <div>
          <button @click="irAPantallaPrincipal"
            class="px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Inicio</button>
          
          <template v-if="!user">
            <button @click="currentComponent = 'InicioSesion'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Iniciar Sesión</button>
            <button @click="currentComponent = 'Registro'" 
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Registro</button>
          </template>
          
          <template v-if="user && user.role === 'usuario'">
            <span class="ml-4 font-semibold">Hola, {{ user.nombre }}</span>
            <button @click="currentComponent = 'SolicitudVerificacionPago'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Solicitar verificar Pago</button>
            <button @click="currentComponent = 'EditarDatosPersonales'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Configuración</button>
            <button @click="logout"
              class="ml-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-md transition-colors">Cerrar Sesión</button>
          </template>
          
          <template v-if="user && user.role === 'bibliotecario'">
            <span class="ml-4 font-semibold">Hola, {{ user.nombre }}</span>
            <button @click="currentComponent = 'RegistroLibro'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Registrar nuevo libro</button>
            
            <button @click="iniciarProcesoModificacion"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Modificar libro</button>
            
            <button @click="currentComponent = 'EliminarLibro'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Eliminar libro</button>
            
            <button @click="currentComponent = 'VerificarPago'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Verificar Pagos</button>
            <button @click="currentComponent = 'AnadirPrestamo'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Añadir Préstamo</button>
            <button @click="currentComponent = 'DevolverPrestamo'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Devolver Préstamo</button>
            <button @click="logout"
              class="ml-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-md transition-colors">Cerrar Sesión</button>
          </template>
        </div>
      </nav>
    </header>

    <main class="container mx-auto p-8">
      <component 
        :is="getComponentToRender" 
        @login="handleLogin"
        @ver-libro="mostrarPantallaLibro"
        @volver="irAPantallaPrincipal"
        @seleccionar-libro-para-modificar="iniciarModificacionLibro"
        @libro-modificado="irAPantallaPrincipal" :libro="libroSeleccionado"
        :libro-a-modificar="libroParaModificar"
        :usuario="user"
      />
    </main>

    <footer class="bg-gray-700 text-white text-center p-6 shadow-md mt-12">
      <p>&copy; 2025 GestiónBiblio. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import PantallaPrincipal from './components/PantallaPrincipal.vue';
import InicioSesion from './components/InicioSesion.vue';
import Registro from './components/RegistroUsuario.vue';
import RegistroLibro from './components/RegistroLibro.vue';
import EditarDatosPersonales from './components/EditarDatosPersonales.vue';
import PantallaLibro from './components/PantallaLibro.vue';
import SolicitudVerificacionPago from './components/SolicitudVerificacionPago.vue';
import VerificarPago from './components/VerificarPago.vue';
import AnadirPrestamo from './components/AnadirPrestamo.vue';
import DevolverPrestamo from './components/DevolverPrestamo.vue';
import EliminarLibro from './components/EliminarLibro.vue';

// Importa los componentes para el flujo de modificación
import ModificarLibroPantallaBusqueda from './components/ModificarLibroPantallaBusqueda.vue';
import ModificarLibroFormulario from './components/ModificarLibroFormulario.vue';


// Estado del usuario
const user = ref(null);
const currentComponent = ref('PantallaPrincipal');
const libroSeleccionado = ref(null); // Usado para 'Ver Detalles' en PantallaPrincipal
const libroParaModificar = ref(null); // Almacena el libro seleccionado para modificar

// Mapeo de componentes disponibles
const components = {
  PantallaPrincipal,
  InicioSesion,
  Registro,
  RegistroLibro,
  EditarDatosPersonales,
  PantallaLibro,
  SolicitudVerificacionPago,
  VerificarPago,
  AnadirPrestamo,
  DevolverPrestamo,
  EliminarLibro,
  ModificarLibroPantallaBusqueda, // La primera pantalla de búsqueda
  ModificarLibroFormulario // La segunda pantalla, el formulario de edición
};

// Computed property para determinar qué componente renderizar dinámicamente
const getComponentToRender = computed(() => {
  if (currentComponent.value === 'PantallaLibro') {
    return PantallaLibro;
  }
  // Si currentComponent es 'ModificarLibroFormulario' y ya hay un libro seleccionado
  if (currentComponent.value === 'ModificarLibroFormulario' && libroParaModificar.value) {
    return ModificarLibroFormulario;
  }
  // Si currentComponent es 'ModificarLibroPantallaBusqueda'
  if (currentComponent.value === 'ModificarLibroPantallaBusqueda') {
    return ModificarLibroPantallaBusqueda;
  }
  // Para el resto de componentes
  return components[currentComponent.value];
});


const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
  libroSeleccionado.value = null;
  libroParaModificar.value = null; // Limpiar también el libro de modificación
};

// Función para iniciar el proceso de modificación desde la navegación (limpia estado y va a la búsqueda)
const iniciarProcesoModificacion = () => {
  libroParaModificar.value = null; // Muy importante: asegúrate de que no haya un libro precargado
  currentComponent.value = 'ModificarLibroPantallaBusqueda';
};


// Función llamada por ModificarLibroPantallaBusqueda.vue cuando encuentra y selecciona un libro
const iniciarModificacionLibro = (libro) => {
  libroParaModificar.value = libro; // Guarda los datos del libro encontrado
  currentComponent.value = 'ModificarLibroFormulario'; // Cambia la vista al formulario de modificación
};

const handleLogin = async () => {
  try {
    const res = await fetch('/api/usuarios/me', {
      credentials: 'include'
    })
    if (res.ok) {
      const userData = await res.json()
      user.value = {
        id: userData.id,
        nombre: userData.nombre,
        correo: userData.correo,
        role: userData.rol.toLowerCase()
      }
      currentComponent.value = 'PantallaPrincipal'
    } else {
      user.value = null
    }
  } catch (e) {
    user.value = null
  }
}

const logout = async () => {
    try {
        const res = await fetch('/api/logout', {
            method: 'POST',
            credentials: 'include'
        });
        if (res.ok) {
            user.value = null;
            currentComponent.value = 'InicioSesion';
        } else {
            console.error("Error al cerrar sesión en el servidor.");
        }
    } catch (e) {
        console.error("Error de red al cerrar sesión:", e);
    }
};

onMounted(() => {
    handleLogin();
});
</script>