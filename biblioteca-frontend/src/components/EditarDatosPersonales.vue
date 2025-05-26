<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-2xl animate-fadeIn">
    <h2 class="text-2xl font-bold text-slate-700 mb-6">Editar Perfil</h2>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Nombre Completo -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700">Nombre Completo</label>
        <input
          type="text"
          id="nombre"
          v-model="nombre"
          :class="{'border-red-500': error}"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-fuchsia-900 "
          placeholder="Ej: Juan Pérez"
        >
        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
      </div>

      <!-- Correo Electrónico -->
      <!-- <div>
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
      </div> -->

      <!-- Contraseña -->
      <!-- <div>
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
      </div> -->

      <!-- Confirmar Contraseña -->
      <!-- <div>
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
      </div> -->

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
      <p v-if="mensaje" :class="mensajeTipo === 'error' ? 'text-red-600' : 'text-green-600'" class="mt-2 text-center">{{ mensaje }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

/* const form = ref({
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
}); */

const nombre = ref('')
const error = ref('')
const isSubmitting = ref(false)
const mensaje = ref('')
const mensajeTipo = ref('')

const cargarNombre = async () => {
  try {
    const res = await fetch('/api/usuarios/me', { credentials: 'include' })
    if (res.ok) {
      const user = await res.json()
      nombre.value = user.nombre || ''
    }
  } catch (e) {
    nombre.value = ''
  }
}

/* const validateField = (field) => {
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
}; */

const validate = () => {
  if (!nombre.value.trim()) {
    error.value = 'El nombre es requerido'
    return false
  }
  if (nombre.value.length < 3) {
    error.value = 'Mínimo 3 caracteres'
    return false
  }
  error.value = ''
  return true
}

/* const validateForm = () => {
  Object.keys(form.value).forEach(field => validateField(field));
  return !Object.values(errors.value).some(error => error !== '');
};
 */

/* const handleSubmit = async () => {
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
}; */

const handleSubmit = async () => {
  if (!validate()) return
  isSubmitting.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  try {
    const res = await fetch('/api/usuarios/nombre', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ nombre: nombre.value })
    })
    const msg = await res.text()
    if (res.ok) {
      mensaje.value = msg
      mensajeTipo.value = 'success'
    } else {
      mensaje.value = msg
      mensajeTipo.value = 'error'
    }
  } catch (e) {
    mensaje.value = 'Error al actualizar el nombre'
    mensajeTipo.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}

/* const resetForm = () => {
  form.value = {
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  };
  Object.keys(errors.value).forEach(key => errors.value[key] = '');
}; */

const resetForm = () => {
  cargarNombre()
  error.value = ''
  mensaje.value = ''
  mensajeTipo.value = ''
}

onMounted(() => {
  cargarNombre()
})

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