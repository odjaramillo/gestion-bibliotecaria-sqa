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
        @libro-modificado="irAPantallaPrincipal" 
        @libro-eliminado="irAPantallaPrincipal" 
        :libro="libroSeleccionado"
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
// Importaciones de tus componentes
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
import EliminarLibro from './components/EliminarLibroPantallaBusqueda.vue'; // Confirmado que este es el nombre que usas

// Importa los dos componentes del flujo de modificación
import ModificarLibroPantallaBusqueda from './components/ModificarLibroPantallaBusqueda.vue';
import ModificarLibroFormulario from './components/ModificarLibroFormulario.vue';


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
  EliminarLibro, // Asegúrate de que la clave aquí coincide con el currentComponent.value que usas
  ModificarLibroFormulario,
  ModificarLibroPantallaBusqueda,
};

// Modificamos esta computed property para manejar el flujo de modificación y eliminación
const getComponentToRender = computed(() => {
  if (currentComponent.value === 'PantallaLibro') {
    return PantallaLibro;
  }
  // Si estamos en el formulario de modificación Y tenemos un libro para modificar
  if (currentComponent.value === 'ModificarLibroFormulario' && libroParaModificar.value) {
    return ModificarLibroFormulario;
  }
  // Si estamos en la pantalla de búsqueda de modificación
  if (currentComponent.value === 'ModificarLibroPantallaBusqueda') {
    return ModificarLibroPantallaBusqueda;
  }
  // AÑADIDO: Lógica para el componente de eliminación
  if (currentComponent.value === 'EliminarLibro') { // <--- CORRECCIÓN: Añadir esta condición
    return EliminarLibro;
  }
  // Para el resto de componentes (fallback)
  return components[currentComponent.value];
});


const mostrarPantallaLibro = (libro) => {
  libroSeleccionado.value = libro;
  currentComponent.value = 'PantallaLibro';
};

const irAPantallaPrincipal = () => {
  currentComponent.value = 'PantallaPrincipal';
  libroSeleccionado.value = null;
  libroParaModificar.value = null; // Limpiar también el libro de modificación al ir a inicio
};

// FUNCIÓN: Inicia el proceso de modificación desde el botón de navegación
const iniciarProcesoModificacion = () => {
  libroParaModificar.value = null; // Asegurarse de que no haya un libro cargado previamente
  currentComponent.value = 'ModificarLibroPantallaBusqueda'; // Ir directamente a la pantalla de búsqueda
};

// FUNCIÓN: Se llama desde ModificarLibroPantallaBusqueda.vue cuando un libro es seleccionado
const iniciarModificacionLibro = (libro) => {
  libroParaModificar.value = libro; // Almacena el libro encontrado
  currentComponent.value = 'ModificarLibroFormulario'; // Cambia a la pantalla del formulario de modificación
};

// AÑADIDO: Función para iniciar el proceso de eliminación (para consistencia con iniciarProcesoModificacion)
const iniciarProcesoEliminacion = () => {
  currentComponent.value = 'EliminarLibro'; // Asegúrate de que 'EliminarLibro' es la clave en el objeto 'components'
};


// Funciones de login/logout usando fetch (como lo tienes actualmente)
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
        role: userData.rol.toLowerCase() // Asegura que el rol siempre sea minúsculas
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
            // También limpia los estados relacionados con libros al cerrar sesión
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
</script>