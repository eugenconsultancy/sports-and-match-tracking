<template>
  <div>
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Create Account</h1>
      <p class="text-sm text-gray-500 mt-1">Join LiveScore to follow your favorite teams</p>
    </div>

    <form @submit.prevent="handleSignup" class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <Input
          v-model="form.first_name"
          label="First Name"
          placeholder="John"
          :error="errors.first_name"
        />
        <Input
          v-model="form.last_name"
          label="Last Name"
          placeholder="Doe"
          :error="errors.last_name"
        />
      </div>

      <Input
        v-model="form.email"
        type="email"
        label="Email Address"
        placeholder="you@example.com"
        required
        :error="errors.email"
      />

      <Input
        v-model="form.password"
        type="password"
        label="Password"
        placeholder="Create a strong password"
        required
        :error="errors.password"
      />

      <Input
        v-model="form.confirmPassword"
        type="password"
        label="Confirm Password"
        placeholder="Confirm your password"
        required
        :error="errors.confirmPassword"
      />

      <div v-if="generalError" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
        {{ generalError }}
      </div>

      <div class="text-xs text-gray-500">
        By signing up, you agree to our 
        <a href="#" class="text-primary-600 hover:underline">Terms of Service</a> and 
        <a href="#" class="text-primary-600 hover:underline">Privacy Policy</a>.
      </div>

      <Button type="submit" :loading="loading" full-width>
        Create Account
      </Button>
    </form>

    <p class="text-center text-sm text-gray-500 mt-6">
      Already have an account?
      <router-link to="/login" class="text-primary-600 hover:underline font-medium">Sign in</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'
import { validators } from '@/validators'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const loading = ref(false)
const generalError = ref('')
const errors = ref({})

function validateForm() {
  const newErrors = {}
  
  if (!form.value.email) {
    newErrors.email = 'Email is required'
  } else if (!validators.email(form.value.email)) {
    newErrors.email = 'Invalid email address'
  }
  
  if (!form.value.password) {
    newErrors.password = 'Password is required'
  } else if (form.value.password.length < 8) {
    newErrors.password = 'Password must be at least 8 characters'
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    newErrors.confirmPassword = 'Passwords do not match'
  }
  
  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

async function handleSignup() {
  errors.value = {}
  generalError.value = ''
  
  if (!validateForm()) return
  
  loading.value = true
  
  const success = await authStore.register(
    form.value.email,
    form.value.password,
    form.value.first_name,
    form.value.last_name
  )
  
  if (success) {
    uiStore.showSuccess('Welcome to LiveScore!', 'Account Created')
    router.push('/')
  } else {
    generalError.value = 'Registration failed. Please try a different email.'
  }
  
  loading.value = false
}
</script>