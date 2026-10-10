import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue = null) {
    const storedValue = localStorage.getItem(key)
    const initial = storedValue !== null ? JSON.parse(storedValue) : defaultValue

    const data = ref(initial)

    watch(data, (newValue) => {
        if (newValue === null || newValue === undefined) {
            localStorage.removeItem(key)
        } else {
            localStorage.setItem(key, JSON.stringify(newValue))
        }
    }, { deep: true })

    const remove = () => {
        localStorage.removeItem(key)
        data.value = defaultValue
    }

    return { data, remove }
}

export function useLocalStorageObject(key, defaultObject = {}) {
    const stored = localStorage.getItem(key)
    const initial = stored ? JSON.parse(stored) : defaultObject

    const data = ref(initial)

    const update = (updates) => {
        data.value = { ...data.value, ...updates }
    }

    const set = (value) => {
        data.value = value
    }

    const reset = () => {
        data.value = defaultObject
    }

    watch(data, (newValue) => {
        if (newValue === null || Object.keys(newValue).length === 0) {
            localStorage.removeItem(key)
        } else {
            localStorage.setItem(key, JSON.stringify(newValue))
        }
    }, { deep: true })

    return { data, update, set, reset }
}