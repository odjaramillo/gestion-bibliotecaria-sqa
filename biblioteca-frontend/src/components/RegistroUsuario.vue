<template>
  <div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl">
      <div>

        <!-- Titulo-->

        <h2 class="mt-6 text-center text-3xl font-extrabold text-slate-700">
          Regístrate
        </h2>
      </div>

      <!-- fORMULARIO ENTRADAS-->
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Nombre Completo:</label>
            <label for="register-name" class="sr-only">Nombre</label>
            <input id="register-name" name="name" type="text" autocomplete="name" required
                   v-model="userData.name"
                   :class="{'border-red-500': errors.name}"
                   class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-fuchsia-700 focus:border-fuchsia-700 sm:text-sm"
                   placeholder="Nombre completo">
            <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
          </div>
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Correo Electronico:</label>
            <label for="register-email" class="sr-only">Correo electrónico</label>
            <input id="register-email" name="email" type="email" autocomplete="email" required
                   v-model="userData.email"
                   :class="{'border-red-500': errors.email}"
                   class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-fuchsia-700 sm:text-sm"
                   placeholder="Correo electrónico">
            <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
          </div>
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Contraseña: </label>
            <label for="register-password" class="sr-only">Contraseña</label>
            <input id="register-password" name="password" type="password" autocomplete="new-password" required
                   v-model="userData.password"
                   :class="{'border-red-500': errors.password}"
                   class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-fuchsia-700 sm:text-sm"
                   placeholder="Contraseña">
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
          </div>
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Confirmacion de contraseña:</label>
            <label for="confirm-password" class="sr-only">Confirmar Contraseña</label>
            <input id="confirm-password" name="confirm-password" type="password" autocomplete="new-password" required
                   v-model="userData.confirmPassword"
                   :class="{'border-red-500': errors.confirmPassword}"
                   class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-fuchsia-700 sm:text-sm"
                   placeholder="Confirmar Contraseña">
            <p v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</p>
          </div>
        </div>

        <!-- Boton crear cuenta-->
        <div>
          <button type="submit"
                  class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors">
            Crear Cuenta
          </button>
        </div>
        <p v-if="submissionStatus" :class="submissionStatus.type === 'success' ? 'text-green-500' : 'text-red-500'" class="text-center text-sm">{{ submissionStatus.message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const userData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const errors = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const submissionStatus = ref(null);

const validateName = (name) => {
  if (!name) return "El nombre es obligatorio.";
  return "";
};

const validateEmail = (email) => {
  if (!email) return "El correo electrónico es obligatorio.";
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) return "El formato del correo electrónico no es válido.";
  return "";
};

const validatePassword = (password) => {
  if (!password) return "La contraseña es obligatoria.";
  if (password.length < 8) return "La contraseña debe tener al menos 8 caracteres.";
  return "";
};

const validateConfirmPassword = (password, confirmPassword) => {
  if (!confirmPassword) return "Debes confirmar la contraseña.";
  if (password !== confirmPassword) return "Las contraseñas no coinciden.";
  return "";
};

const validateForm = () => {
  errors.value.name = validateName(userData.value.name);
  errors.value.email = validateEmail(userData.value.email);
  errors.value.password = validatePassword(userData.value.password);
  errors.value.confirmPassword = validateConfirmPassword(userData.value.password, userData.value.confirmPassword);
  return !errors.value.name && !errors.value.email && !errors.value.password && !errors.value.confirmPassword;
};

const handleRegister = async () => {
  submissionStatus.value = null;
  if (validateForm()) {
    const dataToSend = {
      name: userData.value.name,
      email: userData.value.email,
      password: userData.value.password
    };
    console.log('Datos de registro para enviar al backend:', dataToSend);
    submissionStatus.value = { type: 'success', message: 'Simulación: Registro enviado (ver consola).' };
  } else {
    console.log('Errores de validación:', errors.value);
    submissionStatus.value = { type: 'error', message: 'Por favor, corrige los errores en el formulario.' };
  }
};
</script>