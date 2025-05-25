<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <h2 class="text-2xl font-bold text-slate-700 mb-6">Editar Perfil</h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Nombre Completo -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700">Nombre Completo</label>
        <input
          type="text"
          id="name"
          v-model="form.name"
          @blur="validateField('name')"
          :class="{'border-red-500': errors.name}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-fuchsia-900 "
          placeholder="Ej: Juan Pérez"
        >
        <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
      </div>

      <!-- Correo Electrónico -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          @blur="validateField('email')"
          :class="{'border-red-500': errors.email}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900"
          placeholder="ejemplo@correo.com"
        >
        <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
      </div>

      <!-- Contraseña -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Nueva Contraseña</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          @blur="validateField('password')"
          :class="{'border-red-500': errors.password}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900"
          placeholder="••••••••"
        >
        <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
        <p class="mt-1 text-xs text-gray-500">Mínimo 8 caracteres, 1 mayúscula y 1 número</p>
      </div>

      <!-- Confirmar Contraseña -->
      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmar Contraseña</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="form.confirmPassword"
          @blur="validateField('confirmPassword')"
          :class="{'border-red-500': errors.confirmPassword}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-fuchsia-900"
          placeholder="••••••••"
        >
        <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">{{ errors.confirmPassword }}</p>
      </div>

      <!-- Botones -->
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="resetForm"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-fuchsia-700 hover:bg-fuchsia-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
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

const isSubmitting = ref(false);

const validateField = (field) => {
  switch(field) {
    case 'name': {
      errors.value.name = form.value.name.trim() === '' 
        ? 'El nombre es requerido' 
        : form.value.name.length < 3 
          ? 'Mínimo 3 caracteres' 
          : '';
      break;
    }
      
    case 'email': {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      errors.value.email = !emailRegex.test(form.value.email) 
        ? 'Ingrese un correo válido' 
        : '';
      break;
    }
      
    case 'password': {
      const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
      errors.value.password = form.value.password && !passwordRegex.test(form.value.password) 
        ? 'La contraseña debe tener al menos 8 caracteres, 1 mayúscula y 1 número' 
        : '';
      break;
    }
      
    case 'confirmPassword': {
      errors.value.confirmPassword = form.value.password !== form.value.confirmPassword 
        ? 'Las contraseñas no coinciden' 
        : '';
      break;
    }
  }
};

const validateForm = () => {
  Object.keys(form.value).forEach(field => validateField(field));
  return !Object.values(errors.value).some(error => error !== '');
};

const handleSubmit = async () => {
  if (validateForm()) {
    isSubmitting.value = true;
    try {
      // Simulación de envío a API
      await new Promise(resolve => setTimeout(resolve, 1500));
      console.log('Datos actualizados:', form.value);
      alert('¡Perfil actualizado con éxito!');
      resetForm();
    } finally {
      isSubmitting.value = false;
    }
  }
};

const resetForm = () => {
  form.value = {
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  };
  Object.keys(errors.value).forEach(key => errors.value[key] = '');
};
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>