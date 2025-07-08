<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-gray-700 text-white p-6 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold">Gestión Bibliotecaria</h1>
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
            <span class="ml-3 font-semibold">Hola, {{ user.nombre }}</span>
            <button @click="currentComponent = 'RegistroLibro'"
              class="ml-3 px-3 py-2 hover:bg-gray-800 rounded-md transition-colors text-sm">Registrar nuevo libro</button>
            <button @click="currentComponent = 'VerificarPago'"
              class="ml-3 px-3 py-2 hover:bg-gray-800 rounded-md transition-colors text-sm">Verificar Pagos</button>
            <button @click="currentComponent = 'AnadirPrestamo'"
              class="ml-3 px-3 py-2 hover:bg-gray-800 rounded-md transition-colors text-sm">Añadir Préstamo</button>
            <button @click="currentComponent = 'DevolverPrestamo'"
              class="ml-3 px-3 py-2 hover:bg-gray-800 rounded-md transition-colors text-sm">Devolver Préstamo</button>
            <button @click="currentComponent = 'RenovarPrestamo'"
              class="ml-3 px-3 py-2 hover:bg-gray-800 rounded-md transition-colors text-sm">Renovar Préstamo</button>
            <button @click="logout"
              class="ml-3 px-3 py-2 bg-red-600 hover:bg-red-700 rounded-md transition-colors text-sm">Cerrar Sesión</button>
          </template>
        </div>
      </nav>
    </header>

    <main class="container mx-auto p-8">
      <!-- Renderizado condicional simplificado -->
      <component 
        :is="currentComponent === 'PantallaLibro' ? PantallaLibro : activeComponent" 
        @login="handleLogin"
        @ver-libro="mostrarPantallaLibro"
        @volver="irAPantallaPrincipal"
        :libro="libroSeleccionado"
        :usuario="user"
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
import EditarDatosPersonales from './components/EditarDatosPersonales.vue';
import PantallaLibro from './components/PantallaLibro.vue';
import SolicitudVerificacionPago from './components/SolicitudVerificacionPago.vue';
import VerificarPago from './components/VerificarPago.vue';
import AnadirPrestamo from './components/AnadirPrestamo.vue';
import DevolverPrestamo from './components/DevolverPrestamo.vue';
import RenovarPrestamo from './components/RenovarPrestamo.vue';

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
  EditarDatosPersonales,
  PantallaLibro,
  SolicitudVerificacionPago,
  VerificarPago,
  AnadirPrestamo,
  DevolverPrestamo,
  RenovarPrestamo
};

const activeComponent = computed(() => components[currentComponent.value]);

const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
  libroSeleccionado.value = null;
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

const logout = () => {
  user.value = null;
  currentComponent.value = 'PantallaPrincipal';
};
</script>