<template>
  <div>
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Welcome Back</h1>
      <p class="text-sm text-gray-500 mt-1">Sign in to your account</p>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-4">
      <Input
        v-model="email"
        type="email"
        label="Email Address"
        placeholder="you@example.com"
        required
        :error="errors.email"
      />

      <Input
        v-model="password"
        type="password"
        label="Password"
        placeholder="••••••••"
        required
        :error="errors.password"
      />

      <div class="flex items-center justify-between">
        <label class="flex items-center">
          <input type="checkbox" v-model="remember" class="w-4 h-4 text-primary-600 rounded border-gray-300" />
          <span class="ml-2 text-sm text-gray-600">Remember me</span>
        </label>
        <router-link to="/forgot-password" class="text-sm text-primary-600 hover:underline">
          Forgot password?
        </router-link>
      </div>

      <div v-if="generalError" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
        {{ generalError }}
      </div>

      <Button type="submit" :loading="loading" full-width>
        Sign In
      </Button>
    </form>

    <p class="text-center text-sm text-gray-500 mt-6">
      Don't have an account?
      <router-link to="/signup" class="text-primary-600 hover:underline font-medium">Sign up</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()

const email = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)
const generalError = ref('')
const errors = ref({})

async function handleLogin() {
  errors.value = {}
  generalError.value = ''
  
  if (!email.value) {
    errors.value.email = 'Email is required'
    return
  }
  if (!password.value) {
    errors.value.password = 'Password is required'
    return
  }
  
  loading.value = true
  
  const success = await authStore.login(email.value, password.value)
  
  if (success) {
    uiStore.showSuccess('Welcome back!', 'Login Successful')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } else {
    generalError.value = 'Invalid email or password. Please try again.'
  }
  
  loading.value = false
}
</script>