/**
 * WebSocket connection manager for real-time features.
 * Handles connection lifecycle, reconnection, and message routing.
 */

class WebSocketManager {
    constructor() {
        this.connections = new Map()
        this.listeners = new Map()
        this.reconnectTimers = new Map()
        this.defaultReconnectDelay = 3000
        this.maxReconnectAttempts = 10
    }

    /**
     * Get the WebSocket base URL based on current protocol.
     */
    getBaseUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const host = import.meta.env.VITE_WS_HOST || 'localhost:8001'
        return `${protocol}//${host}`
    }

    /**
     * Connect to a WebSocket endpoint.
     * @param {string} key - Unique identifier for this connection
     * @param {string} endpoint - WebSocket endpoint path (e.g., '/ws/match/123')
     * @param {Object} options - Connection options
     * @returns {WebSocket}
     */
    connect(key, endpoint, options = {}) {
        // Close existing connection for this key
        if (this.connections.has(key)) {
            this.disconnect(key)
        }

        const url = `${this.getBaseUrl()}${endpoint}`
        const ws = new WebSocket(url)
        const reconnectAttempts = { count: 0 }

        ws.onopen = () => {
            console.log(`[WS] Connected: ${key}`)
            reconnectAttempts.count = 0

            // Start ping interval
            if (options.pingInterval !== false) {
                const interval = options.pingInterval || 30000
                ws._pingTimer = setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({ type: 'ping' }))
                    }
                }, interval)
            }

            if (options.onOpen) options.onOpen()
        }

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)

                // Handle pong
                if (data.type === 'pong') return

                // Notify specific listeners
                if (this.listeners.has(key)) {
                    this.listeners.get(key).forEach(callback => callback(data))
                }

                if (options.onMessage) options.onMessage(data)
            } catch (err) {
                console.error(`[WS] Failed to parse message for ${key}:`, err)
            }
        }

        ws.onerror = (error) => {
            console.error(`[WS] Error on ${key}:`, error)
            if (options.onError) options.onError(error)
        }

        ws.onclose = (event) => {
            console.log(`[WS] Disconnected: ${key} (code: ${event.code})`)
            clearInterval(ws._pingTimer)

            // Auto-reconnect
            if (options.autoReconnect !== false && reconnectAttempts.count < this.maxReconnectAttempts) {
                const delay = options.reconnectDelay || this.defaultReconnectDelay
                reconnectAttempts.count++

                console.log(`[WS] Reconnecting ${key} in ${delay}ms (attempt ${reconnectAttempts.count})`)

                this.reconnectTimers.set(key, setTimeout(() => {
                    this.connect(key, endpoint, options)
                }, delay))
            }

            if (options.onClose) options.onClose(event)
            this.connections.delete(key)
        }

        this.connections.set(key, ws)
        return ws
    }

    /**
     * Disconnect a WebSocket connection.
     */
    disconnect(key) {
        const timer = this.reconnectTimers.get(key)
        if (timer) {
            clearTimeout(timer)
            this.reconnectTimers.delete(key)
        }

        const ws = this.connections.get(key)
        if (ws) {
            clearInterval(ws._pingTimer)
            ws.close()
            this.connections.delete(key)
        }
    }

    /**
     * Disconnect all WebSocket connections.
     */
    disconnectAll() {
        this.reconnectTimers.forEach(timer => clearTimeout(timer))
        this.reconnectTimers.clear()

        this.connections.forEach((ws, key) => {
            clearInterval(ws._pingTimer)
            ws.close()
        })
        this.connections.clear()
    }

    /**
     * Send a message through a connection.
     */
    send(key, data) {
        const ws = this.connections.get(key)
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(data))
            return true
        }
        return false
    }

    /**
     * Add a message listener for a connection.
     */
    addListener(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, new Set())
        }
        this.listeners.get(key).add(callback)

        // Return unsubscribe function
        return () => {
            const listeners = this.listeners.get(key)
            if (listeners) {
                listeners.delete(callback)
                if (listeners.size === 0) {
                    this.listeners.delete(key)
                }
            }
        }
    }

    /**
     * Check if a connection is active.
     */
    isConnected(key) {
        const ws = this.connections.get(key)
        return ws && ws.readyState === WebSocket.OPEN
    }

    /**
     * Get the ready state of a connection.
     */
    getState(key) {
        const ws = this.connections.get(key)
        if (!ws) return 'CLOSED'
        const states = ['CONNECTING', 'OPEN', 'CLOSING', 'CLOSED']
        return states[ws.readyState] || 'UNKNOWN'
    }

    // --- Convenience methods for common connections ---

    /**
     * Connect to a live match stream.
     */
    connectMatch(matchId, onUpdate, onEvent) {
        return this.connect(`match-${matchId}`, `/ws/match/${matchId}`, {
            autoReconnect: true,
            onMessage: (data) => {
                if ((data.type === 'match_state' || data.type === 'match_update') && onUpdate) {
                    onUpdate(data.data)
                }
                if (data.type === 'match_event' && onEvent) {
                    onEvent(data.data)
                }
                if (data.type === 'live_state_update' && onUpdate) {
                    onUpdate(data.data)
                }
            }
        })
    }

    /**
     * Connect to live matches summary.
     */
    connectLiveMatches(onUpdate) {
        return this.connect('live-matches', '/ws/matches/live', {
            autoReconnect: true,
            reconnectDelay: 5000,
            onMessage: (data) => {
                if ((data.type === 'initial_live_matches' || data.type === 'live_matches_update') && onUpdate) {
                    onUpdate(data.data)
                }
            }
        })
    }

    /**
     * Connect to a poll stream.
     */
    connectPoll(pollId, onUpdate) {
        return this.connect(`poll-${pollId}`, `/ws/poll/${pollId}`, {
            autoReconnect: true,
            onMessage: (data) => {
                if (data.type === 'poll_update' && onUpdate) {
                    onUpdate(data.data)
                }
            }
        })
    }

    /**
     * Connect to competition updates.
     */
    connectCompetition(competitionId, onUpdate) {
        return this.connect(`competition-${competitionId}`, `/ws/competition/${competitionId}`, {
            autoReconnect: true,
            onMessage: (data) => {
                if (onUpdate) onUpdate(data)
            }
        })
    }
}

// Singleton instance
export const wsManager = new WebSocketManager()

export default wsManager