import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/axios'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const accessToken = ref(localStorage.getItem('access_token'))
    const refreshToken = ref(localStorage.getItem('refresh_token'))

    const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

    function setTokens(access, refresh) {
        accessToken.value = access
        refreshToken.value = refresh
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)

        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
    }

    function clearAuth() {
        user.value = null
        accessToken.value = null
        refreshToken.value = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete axios.defaults.headers.common['Authorization']
    }

    async function login(email, password) {
        try {
            const response = await axios.post('/api/v1/auth/login/', { email, password })
            const { access, refresh } = response.data
            setTokens(access, refresh)
            await fetchUser()
            return true
        } catch (error) {
            console.error('Login failed:', error)
            return false
        }
    }

    async function register(email, password, firstName, lastName) {
        try {
            await axios.post('/api/v1/auth/register/', {
                email,
                password,
                password_confirm: password,
                first_name: firstName,
                last_name: lastName,
            })
            return await login(email, password)
        } catch (error) {
            console.error('Registration failed:', error)
            return false
        }
    }

    async function fetchUser() {
        try {
            const response = await axios.get('/api/v1/auth/users/me/')
            user.value = response.data
            return response.data
        } catch (error) {
            console.error('Failed to fetch user:', error)
            return null
        }
    }

    async function checkAuth() {
        if (accessToken.value) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
            await fetchUser()
        }
    }

    function logout() {
        clearAuth()
        window.location.href = '/'
    }

    return {
        user,
        accessToken,
        refreshToken,
        isAuthenticated,
        login,
        register,
        logout,
        fetchUser,
        checkAuth,
    }
})