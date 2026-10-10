/**
 * Utility functions for formatting data across the application.
 */

/**
 * Format a date string into a human-readable format.
 * @param {string|Date} date - Date to format
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string}
 */
export function formatDate(date, options = {}) {
    if (!date) return ''

    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        ...options,
    }

    try {
        const dateObj = typeof date === 'string' ? new Date(date) : date
        return new Intl.DateTimeFormat('en-US', defaultOptions).format(dateObj)
    } catch (err) {
        console.warn('Invalid date:', date)
        return ''
    }
}

/**
 * Format a date string as relative time (e.g., "2 hours ago").
 * @param {string|Date} date
 * @returns {string}
 */
export function formatRelativeTime(date) {
    if (!date) return ''

    const now = new Date()
    const then = typeof date === 'string' ? new Date(date) : date
    const diffMs = now - then
    const diffSeconds = Math.floor(diffMs / 1000)
    const diffMinutes = Math.floor(diffSeconds / 60)
    const diffHours = Math.floor(diffMinutes / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffSeconds < 60) return 'Just now'
    if (diffMinutes < 60) return `${diffMinutes}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return formatDate(date)
}

/**
 * Format a time string (HH:MM).
 * @param {string|Date} date
 * @returns {string}
 */
export function formatTime(date) {
    if (!date) return ''

    try {
        const dateObj = typeof date === 'string' ? new Date(date) : date
        return dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } catch {
        return ''
    }
}

/**
 * Format a kickoff time with relative labeling.
 * @param {string} dateString
 * @returns {string}
 */
export function formatKickoffTime(dateString) {
    if (!dateString) return 'TBD'

    const now = new Date()
    const kickoff = new Date(dateString)
    const diffHours = (kickoff - now) / (1000 * 60 * 60)

    if (diffHours < 0) {
        // Past
        if (diffHours > -2) return 'Just finished'
        return formatDate(dateString)
    }

    if (diffHours < 1) return `In ${Math.round(diffHours * 60)} min`
    if (diffHours < 24) return `Today ${formatTime(dateString)}`
    if (diffHours < 48) return `Tomorrow ${formatTime(dateString)}`
    return formatDate(dateString) + ' ' + formatTime(dateString)
}

/**
 * Format a number with separators (e.g., 1,500,000).
 * @param {number} num
 * @returns {string}
 */
export function formatNumber(num) {
    if (num === null || num === undefined) return '0'
    return Number(num).toLocaleString()
}

/**
 * Format a large number with abbreviations (e.g., 1.5M).
 * @param {number} num
 * @returns {string}
 */
export function formatCompactNumber(num) {
    if (num === null || num === undefined) return '0'
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M'
    if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K'
    return num.toString()
}

/**
 * Format a score string.
 * @param {number} home
 * @param {number} away
 * @returns {string}
 */
export function formatScore(home, away) {
    if (home === null || home === undefined) return 'vs'
    return `${home} - ${away}`
}

/**
 * Get a human-readable match status label.
 * @param {string} status
 * @returns {string}
 */
export function getMatchStatusLabel(status) {
    const labels = {
        scheduled: 'Scheduled',
        live: 'Live',
        half_time: 'Half Time',
        finished: 'Full Time',
        postponed: 'Postponed',
        cancelled: 'Cancelled',
        suspended: 'Suspended',
    }
    return labels[status] || status || 'Unknown'
}

/**
 * Get CSS class for match status badge.
 * @param {string} status
 * @returns {string}
 */
export function getMatchStatusClass(status) {
    const classes = {
        scheduled: 'bg-blue-100 text-blue-800',
        live: 'bg-red-100 text-red-800',
        half_time: 'bg-orange-100 text-orange-800',
        finished: 'bg-gray-100 text-gray-800',
        postponed: 'bg-yellow-100 text-yellow-800',
        cancelled: 'bg-red-100 text-red-800',
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

/**
 * Get event icon emoji.
 * @param {string} eventType
 * @returns {string}
 */
export function getEventIcon(eventType) {
    const icons = {
        goal: '⚽',
        penalty_goal: '🥅',
        own_goal: '🔴',
        penalty_miss: '❌',
        yellow_card: '🟨',
        second_yellow: '🟨🟥',
        red_card: '🟥',
        substitution_in: '🟢',
        substitution_out: '🔴',
        assist: '🅰️',
        half_time: '⏸️',
        full_time: '⏹️',
    }
    return icons[eventType] || '📌'
}

/**
 * Format possession percentage string.
 * @param {Object} possession - { home: number, away: number }
 * @returns {string}
 */
export function formatPossession(possession) {
    if (!possession) return '50% - 50%'
    return `${possession.home || 50}% - ${possession.away || 50}%`
}

/**
 * Truncate text with ellipsis.
 * @param {string} text
 * @param {number} maxLength
 * @returns {string}
 */
export function truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text || ''
    return text.substring(0, maxLength).trim() + '...'
}

/**
 * Get country flag emoji from country name.
 * This is a simple mapping; production would use a proper library.
 * @param {string} country
 * @returns {string}
 */
export function getCountryFlag(country) {
    if (!country) return '🏳️'
    const flags = {
        England: '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        Spain: '🇪🇸',
        France: '🇫🇷',
        Germany: '🇩🇪',
        Italy: '🇮🇹',
        Portugal: '🇵🇹',
        Netherlands: '🇳🇱',
        Belgium: '🇧🇪',
        Brazil: '🇧🇷',
        Argentina: '🇦🇷',
        Norway: '🇳🇴',
        Egypt: '🇪🇬',
        USA: '🇺🇸',
        International: '🌍',
    }
    return flags[country] || '🏳️'
}

/**
 * Format a currency value.
 * @param {number} value
 * @param {string} currency
 * @returns {string}
 */
export function formatCurrency(value, currency = 'EUR') {
    if (!value) return '-'
    const symbols = { EUR: '€', GBP: '£', USD: '$' }
    const symbol = symbols[currency] || currency + ' '
    return `${symbol}${formatCompactNumber(value)}`
}