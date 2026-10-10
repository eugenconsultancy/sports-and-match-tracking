import { ref, onUnmounted } from 'vue'
import wsManager from '@/utils/websocket'

export function useWebSocket(endpoint, options = {}) {
    const isConnected = ref(false)
    const lastMessage = ref(null)
    const error = ref(null)

    const key = options.key || endpoint

    const connect = () => {
        wsManager.connect(key, endpoint, {
            autoReconnect: options.autoReconnect !== false,
            reconnectDelay: options.reconnectDelay || 3000,
            onOpen: () => {
                isConnected.value = true
                error.value = null
                options.onOpen?.()
            },
            onMessage: (data) => {
                lastMessage.value = data
                options.onMessage?.(data)
            },
            onError: (err) => {
                error.value = err
                options.onError?.(err)
            },
            onClose: () => {
                isConnected.value = false
                options.onClose?.()
            },
        })
    }

    const disconnect = () => {
        wsManager.disconnect(key)
        isConnected.value = false
    }

    const send = (data) => {
        return wsManager.send(key, data)
    }

    const addListener = (callback) => {
        return wsManager.addListener(key, callback)
    }

    if (options.autoConnect !== false) {
        connect()
    }

    onUnmounted(() => {
        if (options.autoDisconnect !== false) {
            disconnect()
        }
    })

    return {
        isConnected,
        lastMessage,
        error,
        connect,
        disconnect,
        send,
        addListener,
    }
}

export function useMatchWebSocket(matchId, onUpdate, onEvent) {
    return useWebSocket(`/ws/match/${matchId}`, {
        key: `match-${matchId}`,
        onMessage: (data) => {
            if (data.type === 'match_state' || data.type === 'match_update') {
                onUpdate?.(data.data)
            }
            if (data.type === 'match_event') {
                onEvent?.(data.data)
            }
            if (data.type === 'live_state_update') {
                onUpdate?.(data.data)
            }
        },
    })
}

export function useLiveMatchesWebSocket(onUpdate) {
    return useWebSocket('/ws/matches/live', {
        key: 'live-matches',
        reconnectDelay: 5000,
        onMessage: (data) => {
            if (data.type === 'initial_live_matches' || data.type === 'live_matches_update') {
                onUpdate?.(data.data)
            }
        },
    })
}

export function usePollWebSocket(pollId, onUpdate) {
    // Only connect if pollId is provided
    if (!pollId) {
        return { isConnected: ref(false), lastMessage: ref(null), error: ref(null), connect: () => { }, disconnect: () => { }, send: () => { }, addListener: () => { } }
    }

    return useWebSocket(`/ws/poll/${pollId}`, {
        key: `poll-${pollId}`,
        onMessage: (data) => {
            if (data.type === 'poll_update' || data.type === 'initial_poll_results') {
                onUpdate?.(data.data)
            }
        },
    })
}