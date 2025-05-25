<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-gray-700 text-white p-6 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
        <h1 class="text-3xl font-bold">Gestión Bibliotecaria</h1>
        <div>
          <button @click="irAPantallaPrincipal"
            class="px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Inicio</button>
          
          <!-- Menú dinámico según tipo de usuario -->
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
      <!-- Renderizado condicional simplificado -->
      <component 
        :is="activeComponent" 
        @login="handleLogin"
        @ver-libro="mostrarPantallaLibro"
        @volver="irAPantallaPrincipal"
        :libro="libroSeleccionado"
      />
    </main>

    <footer class="bg-gray-700 text-white text-center p-6 shadow-md mt-12">
      <p>&copy; 2025 GestiónBiblio. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import PantallaPrincipal from './components/PantallaPrincipal.vue';
import InicioSesion from './components/InicioSesion.vue';
import Registro from './components/RegistroUsuario.vue';
import RegistroLibro from './components/RegistroLibro.vue';
import PantallaUsuario from './components/PantallaUsuario.vue';
import PantallaBibliotecario from './components/PantallaBibliotecario.vue';
import EditarDatosPersonales from './components/EditarDatosPersonales.vue';
import PantallaLibro from './components/PantallaLibro.vue';
import SolicitudVerificacionPago from './components/SolicitudVerificacionPago.vue';
import VerificarPago from './components/VerificarPago.vue';
import AnadirPrestamo from './components/AnadirPrestamo.vue';
import DevolverPrestamo from './components/DevolverPrestamo.vue';

// Estado del usuario
const user = ref(null);
const currentComponent = ref('PantallaPrincipal');
const libroSeleccionado = ref(null);

// Mapeo de componentes
const components = {
  PantallaPrincipal,
  InicioSesion,
  Registro,
  RegistroLibro,
  PantallaUsuario,
  PantallaBibliotecario,
  EditarDatosPersonales,
  PantallaLibro,  // Asegúrate que está incluido
  SolicitudVerificacionPago,
  VerificarPago,
  AnadirPrestamo,
  DevolverPrestamo
};

const activeComponent = computed(() => {
  if (currentComponent.value === 'PantallaLibro') {
    return {
      ...components.PantallaLibro,
      props: { libro: libroSeleccionado.value }
    };
  }
  return components[currentComponent.value];
});

const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
};

const handleLogin = (userData) => {
  user.value = userData;
  currentComponent.value = 'PantallaPrincipal';
};

/* const handleLogin = (userData) => {
  user.value = userData;
  if (userData.role === 'bibliotecario') {
    currentComponent.value = 'PantallaPrincipal';
  } else {
    currentComponent.value = 'PantallaPrincipal';
  }
}; */

const logout = () => {
  user.value = null;
  currentComponent.value = 'PantallaPrincipal';
};
</script>


<!--<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-gray-700 text-white p-6 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
        <h1 class="text-3xl font-bold">Gestion Bibliotecaria</h1>
        <div>
          <button @click="irAPantallaPrincipal"
            class="px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Principal</button>
          <button @click="currentComponent = 'PantallaPrincipal'"
            class="px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Principal</button>
          <button @click="currentComponent = 'InicioSesion'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Iniciar Sesión</button>
          <button @click="currentComponent = 'Registro'" 
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Registro</button>
          <button @click="currentComponent = 'RegistroLibro'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Registrar Libro (Biblio)</button>
          <button @click="currentComponent = 'PantallaUsuario'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Pantalla Usuario</button>
          <button @click="currentComponent = 'PantallaBibliotecario'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Pantalla Bibliotecario</button>
          <button @click="currentComponent = 'EditarDatosPersonales'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Configuración</button>
          <button @click="currentComponent = 'PantallaLibro'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Consultar libro</button>
          <button @click="currentComponent = 'SolicitudVerificacionPago'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Solicitud Verificacion Pago</button>
            <button @click="currentComponent = 'VerificarPago'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Verificar Pago</button>
          <button @click="currentComponent = 'AnadirPrestamo'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Añadir prestamo</button>
          <button @click="currentComponent = 'DevolverPrestamo'"
            class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Devolver prestamo</button>

        </div>
      </nav>
    </header>

    <main class="container mx-auto p-8">
      <component 
        :is="activeComponent" 
        @ver-libro="mostrarPantallaLibro"
        :libro="libroSeleccionado"
        v-if="currentComponent !== 'PantallaLibro'"
      />
      <PantallaLibro 
        v-else
        :libro="libroSeleccionado"
        @volver="irAPantallaPrincipal"
      />
    </main>

    <footer class="bg-gray-700 text-white text-center p-6 shadow-md mt-12">
      <p>&copy; 2025 GestionBiblio. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import PantallaPrincipal from './components/PantallaPrincipal.vue';
import InicioSesion from './components/InicioSesion.vue';
import Registro from './components/RegistroUsuario.vue';
import RegistroLibro from './components/RegistroLibro.vue';
import PantallaUsuario from './components/PantallaUsuario.vue';
import PantallaBibliotecario from './components/PantallaBibliotecario.vue';
import EditarDatosPersonales from './components/EditarDatosPersonales.vue';
import PantallaLibro from './components/PantallaLibro.vue';
import SolicitudVerificacionPago from './components/SolicitudVerificacionPago.vue';
import VerificarPago from './components/VerificarPago.vue';
import AnadirPrestamo from './components/AnadirPrestamo.vue';
import DevolverPrestamo from './components/DevolverPrestamo.vue';

const currentComponent = ref('PantallaPrincipal');
const libroSeleccionado = ref(null);

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
  libroSeleccionado.value = null;
};

const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const components = {
  PantallaPrincipal,
  InicioSesion,
  Registro,
  RegistroLibro,
  PantallaUsuario,
  PantallaBibliotecario,
  EditarDatosPersonales,
  PantallaLibro,
  SolicitudVerificacionPago,
  VerificarPago,
  AnadirPrestamo,
  DevolverPrestamo
};

const activeComponent = computed(() => components[currentComponent.value]);
</script>

<style>
/* Tailwind CSS se importa globalmente a través de un CDN en index.html o se configura con PostCSS */
/* Estilos adicionales si son necesarios */
body {
  font-family: 'Inter', sans-serif; /* Asegúrate de tener esta fuente o cámbiala */
}
</style>

----->