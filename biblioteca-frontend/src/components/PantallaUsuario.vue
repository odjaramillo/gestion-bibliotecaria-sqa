. <template>
  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold text-slate-700">Bienvenido,
NombreUsuario</h2>


      <div class="relative">
        <button @click="toggleDropdown" class="bg-fuchsia-700
text-white px-4 py-2 rounded-md hover:fuchsia-900 transition-colors
flex items-center">
          Mi Perfil
          <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor"
viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path
stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19
9l-7 7-7-7"></path></svg>
        </button>
        <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-48
bg-white rounded-md shadow-lg py-1 z-10">
          <a href="#" class="block px-4 py-2 text-sm text-gray-700
hover:bg-gray-100">Ver Perfil</a>
          <a href="#" class="block px-4 py-2 text-sm text-gray-700
hover:bg-gray-100">Mis Préstamos</a>
          <a href="#" class="block px-4 py-2 text-sm text-gray-700
hover:bg-gray-100">Configuración</a>
          <a href="#" class="block px-4 py-2 text-sm text-red-600
hover:bg-gray-100">Cerrar Sesión</a>
        </div>
      </div>
    </div>

    <p class="text-gray-600 text-lg mb-10 ">Explora nuestra vasta colección de libros y encuentra tu próxima lectura.</p>


      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="libro in librosDeEjemplo" :key="libro.id"
        class="bg-gray-50 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
        <img :src="libro.portadaUrl" alt="Portada del libro" class="w-full h-64 object-cover">
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-700">{{ libro.titulo }}</h3>
          <p class="text-sm text-gray-500">{{ libro.autor }}</p>
          <button class="mt-3 w-full bg-fuchsia-700 text-white py-2 rounded-md hover:bg-fuchsia-900 transition-colors text-sm">
            Ver Detalles
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';

const dropdownOpen = ref(false);

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const librosDeEjemplo = ref([
  { id: 1, titulo: 'El Señor de los Anillos', autor: 'J.R.R. Tolkien', portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+1' },
  { id: 2, titulo: 'Cien Años de Soledad', autor: 'Gabriel García Márquez', portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+2' },
  { id: 3, titulo: '1984', autor: 'George Orwell', portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+3' },
  { id: 4, titulo: 'Don Quijote de la Mancha', autor: 'Miguel de Cervantes', portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+4' },
  { id: 5, titulo: 'Orgullo y Prejuicio', autor: 'Jane Austen', portadaUrl: 'https://placehold.co/300x400/A9A9A9/FFF?text=Libro+5' },
]);
// Lógica para cerrar el dropdown si se hace clic fuera
// Se podría implementar con un event listener global
</script>
<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>