<template>
  <div class="bg-gray-100 min-h-screen font-sans">
    <header class="bg-gray-700 text-white p-6 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
<<<<<<< HEAD
        <h1 class="text-3xl font-bold">Gestión Bibliotecaria</h1>
=======
        <h1 class="text-2xl font-bold">Gestión Bibliotecaria</h1>
>>>>>>> EliminarAmonestacion-RenovarPrestamo
        <div>
          <button @click="irAPantallaPrincipal"
            class="px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Inicio</button>
          
<<<<<<< HEAD
=======
          <!-- Menú dinámico según tipo de usuario -->
>>>>>>> EliminarAmonestacion-RenovarPrestamo
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
<<<<<<< HEAD
            <span class="ml-4 font-semibold">Hola, {{ user.nombre }}</span>
            <button @click="currentComponent = 'RegistroLibro'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Registrar nuevo libro</button>
            
            <button @click="iniciarProcesoModificacion"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Modificar libro</button>
            
            <button @click="iniciarProcesoEliminacion" 
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Eliminar libro</button>
            
            <button @click="currentComponent = 'VerificarPago'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Verificar Pagos</button>
            <button @click="currentComponent = 'AnadirPrestamo'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Añadir Préstamo</button>
            <button @click="currentComponent = 'DevolverPrestamo'"
              class="ml-4 px-4 py-2 hover:bg-gray-800 rounded-md transition-colors">Devolver Préstamo</button>
            <button @click="logout"
              class="ml-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-md transition-colors">Cerrar Sesión</button>
=======
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
>>>>>>> EliminarAmonestacion-RenovarPrestamo
          </template>
        </div>
      </nav>
    </header>

    <main class="container mx-auto p-8">
<<<<<<< HEAD
      <component 
        :is="getComponentToRender" 
        @login="handleLogin"
        @ver-libro="mostrarPantallaLibro"
        @volver="irAPantallaPrincipal"
        @seleccionar-libro-para-modificar="iniciarModificacionLibro"
        @libro-modificado="irAPantallaPrincipal" 
        @libro-eliminado="irAPantallaPrincipal" 
        :libro="libroSeleccionado"
        :libro-a-modificar="libroParaModificar"
=======
      <!-- Renderizado condicional simplificado -->
      <component 
        :is="currentComponent === 'PantallaLibro' ? PantallaLibro : activeComponent" 
        @login="handleLogin"
        @ver-libro="mostrarPantallaLibro"
        @volver="irAPantallaPrincipal"
        :libro="libroSeleccionado"
>>>>>>> EliminarAmonestacion-RenovarPrestamo
        :usuario="user"
      />
    </main>

    <footer class="bg-gray-700 text-white text-center p-6 shadow-md mt-12">
      <p>&copy; 2025 GestiónBiblio. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
<<<<<<< HEAD
import { ref, computed, onMounted } from 'vue';
=======
import { ref, computed } from 'vue';
>>>>>>> EliminarAmonestacion-RenovarPrestamo
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
<<<<<<< HEAD
import EliminarLibro from './components/EliminarLibroPantallaBusqueda.vue'; 
import ModificarLibroPantallaBusqueda from './components/ModificarLibroPantallaBusqueda.vue';
import ModificarLibroFormulario from './components/ModificarLibroFormulario.vue';

const user = ref(null);
const currentComponent = ref('PantallaPrincipal');
const libroSeleccionado = ref(null); 
const libroParaModificar = ref(null); 

=======
import RenovarPrestamo from './components/RenovarPrestamo.vue';

// Estado del usuario
const user = ref(null);
const currentComponent = ref('PantallaPrincipal');
const libroSeleccionado = ref(null);

// Mapeo de componentes
>>>>>>> EliminarAmonestacion-RenovarPrestamo
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
<<<<<<< HEAD
  EliminarLibro, 
  ModificarLibroFormulario,
  ModificarLibroPantallaBusqueda,
};

const getComponentToRender = computed(() => {
  if (currentComponent.value === 'PantallaLibro') {
    return PantallaLibro;
  }
  if (currentComponent.value === 'ModificarLibroFormulario' && libroParaModificar.value) {
    return ModificarLibroFormulario;
  }
  if (currentComponent.value === 'ModificarLibroPantallaBusqueda') {
    return ModificarLibroPantallaBusqueda;
  }
  if (currentComponent.value === 'EliminarLibro') { 
    return EliminarLibro;
  }
  return components[currentComponent.value];
});
=======
  RenovarPrestamo
};

const activeComponent = computed(() => components[currentComponent.value]);
>>>>>>> EliminarAmonestacion-RenovarPrestamo

const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
  libroSeleccionado.value = null;
<<<<<<< HEAD
  libroParaModificar.value = null; 
};

const iniciarProcesoModificacion = () => {
  libroParaModificar.value = null; 
  currentComponent.value = 'ModificarLibroPantallaBusqueda'; 
};

const iniciarModificacionLibro = (libro) => {
  libroParaModificar.value = libro; 
  currentComponent.value = 'ModificarLibroFormulario'; 
};

const iniciarProcesoEliminacion = () => {
  currentComponent.value = 'EliminarLibro'; 
=======
>>>>>>> EliminarAmonestacion-RenovarPrestamo
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
<<<<<<< HEAD
        role: userData.rol.toLowerCase() 
=======
        role: userData.rol.toLowerCase()
>>>>>>> EliminarAmonestacion-RenovarPrestamo
      }
      currentComponent.value = 'PantallaPrincipal'
    } else {
      user.value = null
    }
  } catch (e) {
    user.value = null
  }
}

<<<<<<< HEAD
const logout = async () => {
    try {
        const res = await fetch('/api/logout', {
            method: 'POST',
            credentials: 'include'
        });
        if (res.ok) {
            user.value = null;
            currentComponent.value = 'InicioSesion';
            libroSeleccionado.value = null;
            libroParaModificar.value = null; 
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
=======
const logout = () => {
  user.value = null;
  currentComponent.value = 'PantallaPrincipal';
};
>>>>>>> EliminarAmonestacion-RenovarPrestamo
</script>