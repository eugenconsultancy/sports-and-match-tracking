import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

// Create app
const app = createApp(App)

// Plugins
app.use(createPinia())
app.use(router)

// Global error handler
app.config.errorHandler = (err, vm, info) => {
    console.error('Vue Error:', err)
    console.error('Component:', vm)
    console.error('Info:', info)
}

// Mount
app.mount('#app')