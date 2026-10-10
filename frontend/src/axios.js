import axios from 'axios'

const instance = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor
instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor
instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                const refreshToken = localStorage.getItem('refresh_token')
                if (refreshToken) {
                    const response = await axios.post('/api/v1/auth/token/refresh/', {
                        refresh: refreshToken,
                    })

                    const { access } = response.data
                    localStorage.setItem('access_token', access)
                    originalRequest.headers.Authorization = `Bearer ${access}`

                    return instance(originalRequest)
                }
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

export default instance