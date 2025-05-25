<template>


  <div class="bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">

    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold text-slate-700">Bienvenido, NombreBibliotecario</h2>
       <div class="relative">
      </div>
    </div>

    <p class="text-gray-600 text-lg mb-6">Panel de administración de libro de la biblioteca.
    </p>
    <h3 class="text-xl font-bold text-slate-700">¿Qué desea hacer?</h3>
    <br>
    

    <div class=" grid grid-cols-5 md:grid-cols-2SS lg:grid-cols-2 gap-5 mb-10">
      
        
        <button class="bg-fuchsia-700 p-6 rounded-lg shadow-md text-xl font-semibold text-white rounded-lgshadow-md hover:bg-fuchsia-900 transition-colors ">
          Registrar nuevo libro
        </button>
          
        <button class="bg-fuchsia-700 p-6 rounded-lg shadow-md text-xl font-semibold text-white rounded-lgshadow-md hover:bg-fuchsia-900 transition-colors ">
          Añadir prestamo a Usuario
        </button>

        <button class="bg-fuchsia-700 p-6 rounded-lg shadow-md text-xl font-semibold text-white rounded-lgshadow-md hover:bg-fuchsia-900 transition-colors ">
          Devolver prestamo de libro
        </button>

        <button class="bg-fuchsia-700 p-6 rounded-lg shadow-md text-xl font-semibold text-white rounded-lgshadow-md hover:bg-fuchsia-900 transition-colors ">
          Verificar pago de amonestaciones
        </button>
        
        
    </div>

    </div>
</template>

<script setup>

</script>
