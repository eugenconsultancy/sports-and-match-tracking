import axios from '@/axios'

class AuthService {
    constructor() {
        this.baseURL = '/api/v1/auth'
    }

    async login(email, password) {
        const response = await axios.post(`${this.baseURL}/login/`, { email, password })
        const { access, refresh, user } = response.data

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

        return { user, access, refresh }
    }

    async register(email, password, firstName, lastName) {
        const response = await axios.post(`${this.baseURL}/register/`, {
            email,
            password,
            password_confirm: password,
            first_name: firstName,
            last_name: lastName,
        })
        return response.data
    }

    async logout() {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
            try {
                await axios.post(`${this.baseURL}/logout/`, { refresh: refreshToken })
            } catch (error) {
                console.error('Logout error:', error)
            }
        }

        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete axios.defaults.headers.common['Authorization']
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) throw new Error('No refresh token')

        const response = await axios.post(`${this.baseURL}/token/refresh/`, { refresh: refreshToken })
        const { access } = response.data

        localStorage.setItem('access_token', access)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

        return access
    }

    async getCurrentUser() {
        const response = await axios.get(`${this.baseURL}/users/me/`)
        return response.data
    }

    async updateProfile(data) {
        const response = await axios.patch(`${this.baseURL}/users/me/`, data)
        return response.data
    }

    async changePassword(oldPassword, newPassword) {
        const response = await axios.post(`${this.baseURL}/users/change_password/`, {
            old_password: oldPassword,
            new_password: newPassword,
        })
        return response.data
    }

    isAuthenticated() {
        return !!localStorage.getItem('access_token')
    }

    setupAxiosInterceptor() {
        axios.interceptors.response.use(
            response => response,
            async error => {
                const originalRequest = error.config

                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true

                    try {
                        const newToken = await this.refreshToken()
                        originalRequest.headers.Authorization = `Bearer ${newToken}`
                        return axios(originalRequest)
                    } catch (refreshError) {
                        localStorage.removeItem('access_token')
                        localStorage.removeItem('refresh_token')
                        window.location.href = '/login'
                        return Promise.reject(refreshError)
                    }
                }

                return Promise.reject(error)
            }
        )
    }
}

export const authService = new AuthService()
export default authService