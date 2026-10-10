export const validators = {
    required: (value, message = 'This field is required') => {
        if (value === null || value === undefined || value === '') {
            return message
        }
        return null
    },

    email: (value, message = 'Invalid email address') => {
        if (!value) return null
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) {
            return message
        }
        return null
    },

    minLength: (min, message) => (value) => {
        if (!value) return null
        if (value.length < min) {
            return message || `Must be at least ${min} characters`
        }
        return null
    },

    maxLength: (max, message) => (value) => {
        if (!value) return null
        if (value.length > max) {
            return message || `Must be at most ${max} characters`
        }
        return null
    },

    min: (min, message) => (value) => {
        if (value === null || value === undefined) return null
        if (Number(value) < min) {
            return message || `Must be at least ${min}`
        }
        return null
    },

    max: (max, message) => (value) => {
        if (value === null || value === undefined) return null
        if (Number(value) > max) {
            return message || `Must be at most ${max}`
        }
        return null
    },

    pattern: (regex, message) => (value) => {
        if (!value) return null
        if (!regex.test(value)) {
            return message || 'Invalid format'
        }
        return null
    },

    match: (field, message) => (value, formData) => {
        if (value !== formData[field]) {
            return message || `Does not match ${field}`
        }
        return null
    },

    url: (value, message = 'Invalid URL') => {
        if (!value) return null
        try {
            new URL(value)
            return null
        } catch {
            return message
        }
    },

    phone: (value, message = 'Invalid phone number') => {
        if (!value) return null
        const phoneRegex = /^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$/
        if (!phoneRegex.test(value)) {
            return message
        }
        return null
    },

    number: (value, message = 'Must be a number') => {
        if (value === null || value === undefined || value === '') return null
        if (isNaN(Number(value))) {
            return message
        }
        return null
    },

    integer: (value, message = 'Must be an integer') => {
        if (value === null || value === undefined || value === '') return null
        if (!Number.isInteger(Number(value))) {
            return message
        }
        return null
    },

    positive: (value, message = 'Must be positive') => {
        if (value === null || value === undefined || value === '') return null
        if (Number(value) <= 0) {
            return message
        }
        return null
    },
}

export function validate(formData, rules) {
    const errors = {}

    for (const [field, fieldRules] of Object.entries(rules)) {
        for (const rule of fieldRules) {
            const error = rule(formData[field], formData)
            if (error) {
                errors[field] = error
                break
            }
        }
    }

    return errors
}

export function isValidEmail(email) {
    return validators.email(email) === null
}

export function isValidPassword(password) {
    return password && password.length >= 8
}