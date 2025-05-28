<template>
  <div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl">
      <div>
        
        <!-- Titulo-->

        <h2 class="mt-6 text-center text-3xl font-extrabold text-slate-700">
          Iniciar Sesión
        </h2>
      </div>

      <!-- Formulario inicio sesion-->

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <!-- Entradas texto-->

            <label for="email-address" class="sr-only">Correo electrónico</label>
            <input id="email-address" name="email" type="email" autocomplete="email" required
                   v-model="credentials.correo"
                   :class="{'border-red-500': errors.correo}"
                   class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-purple-500 focus:border-fuchsia-700 focus:z-10 sm:text-sm"
                   placeholder="Correo electrónico">
            <p v-if="errors.correo" class="text-red-500 text-xs mt-1">{{ errors.correo }}</p>
          </div>
          <div>
            <label for="password" class="sr-only">Contraseña</label>
            <input id="password" name="password" type="password" autocomplete="current-password" required
                   v-model="credentials.contrasena"
                   :class="{'border-red-500': errors.contrasena}"
                   class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-purple-500 focus:border-fuchsia-700 focus:z-10 sm:text-sm"
                   placeholder="Contraseña">
            <p v-if="errors.contrasena" class="text-red-500 text-xs mt-1">{{ errors.contrasena }}</p>
          </div>
        </div>

        <!-- Boton recordar -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
                   class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded">
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              Recordarme
            </label>
          </div>
      <!-- Boton recordar contraseña-->
          <div class="text-sm">
            <a href="#" class="font-medium text-purple-600 hover: text-fuchsia-900">
              ¿Olvidaste tu contraseña?
            </a>
          </div>
        </div>

        <!-- Boton Inicio sesion-->
        <div>
          <button type="submit"
                  class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors">
            Iniciar Sesión
          </button>
        </div>
        <p v-if="submissionStatus" :class="submissionStatus.type === 'success' ? 'text-green-500' : 'text-red-500'" class="text-center text-sm">{{ submissionStatus.message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const credentials = ref({
  correo: '',
  contrasena: ''
});

const errors = ref({
  correo: '',
  contrasena: ''
});

const submissionStatus = ref(null); // { type: 'success'/'error', message: '...' }

const emit = defineEmits(['login']);

const validateEmail = (correo) => {
  if (!correo) return "El correo electrónico es obligatorio.";
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(correo)) return "El formato del correo electrónico no es válido.";
  return "";
};

const validatePassword = (contrasena) => {
  if (!contrasena) return "La contraseña es obligatoria.";
  // if (contrasena.length < 6) return "La contraseña debe tener al menos 6 caracteres.";
  return "";
};

const validateForm = () => {
  errors.value.correo = validateEmail(credentials.value.correo);
  errors.value.contrasena = validatePassword(credentials.value.contrasena);
  return !errors.value.correo && !errors.value.contrasena;
};

const handleLogin = async () => {
  submissionStatus.value = null
  if (validateForm()) {
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: credentials.value.correo,
          password: credentials.value.contrasena
        }),
        credentials: 'include'
      })
      if (!res.ok) {
        throw new Error('Credenciales inválidas')
      }
      // Aquí puedes emitir el correo para que el menú se actualice
      emit('login', { correo: credentials.value.correo })
      submissionStatus.value = { type: 'success', message: 'Inicio de sesión exitoso.' }
    } catch (error) {
      submissionStatus.value = { type: 'error', message: 'Correo o contraseña incorrectos.' }
    }
  } else {
    submissionStatus.value = { type: 'error', message: 'Por favor, corrige los errores en el formulario.' }
  }
}
</script>