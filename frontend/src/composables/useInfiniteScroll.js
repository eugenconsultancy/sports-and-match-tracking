import { ref, onMounted, onUnmounted } from 'vue'

export function useInfiniteScroll(loadMore, options = {}) {
    const {
        threshold = 100,
        enabled = true,
        initialLoading = false,
    } = options

    const loading = ref(initialLoading)
    const hasMore = ref(true)
    const error = ref(null)
    let observer = null
    let sentinelRef = null

    const setSentinel = (el) => {
        if (!el || !enabled) return

        sentinelRef = el

        if (observer) {
            observer.disconnect()
        }

        observer = new IntersectionObserver(
            async (entries) => {
                const entry = entries[0]
                if (entry.isIntersecting && !loading.value && hasMore.value) {
                    loading.value = true
                    error.value = null

                    try {
                        const result = await loadMore()
                        if (result === false) {
                            hasMore.value = false
                        }
                    } catch (err) {
                        error.value = err
                        console.error('Failed to load more:', err)
                    } finally {
                        loading.value = false
                    }
                }
            },
            { rootMargin: `${threshold}px` }
        )

        observer.observe(el)
    }

    const reset = () => {
        hasMore.value = true
        loading.value = false
        error.value = null
    }

    onMounted(() => {
        if (!sentinelRef && enabled) {
            // Create a sentinel element if not provided
            const div = document.createElement('div')
            div.style.height = '1px'
            document.querySelector('main')?.appendChild(div)
            setSentinel(div)
        }
    })

    onUnmounted(() => {
        if (observer) {
            observer.disconnect()
            observer = null
        }
    })

    return {
        loading,
        hasMore,
        error,
        setSentinel,
        reset,
    }
}