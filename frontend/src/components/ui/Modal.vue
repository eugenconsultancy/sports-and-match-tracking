<template>
  <!-- Teleport to body so stacking context doesn't clip the modal -->
  <Teleport to="body">
    <Transition name="backdrop-fade">
      <div
        v-if="modelValue"
        class="modal-backdrop"
        :class="{ 'dark-theme': isDark }"
        @click.self="closeIfAllowed"
        aria-modal="true"
        role="dialog"
        :aria-label="title || 'Dialog'"
      >
        <Transition :name="isMobile ? 'sheet-slide' : 'modal-spring'">
          <div
            v-if="modelValue"
            ref="modalRef"
            class="modal-content"
            :class="[
              sizeClasses[size],
              typeClass,
              { 'is-loading': loading },
            ]"
            tabindex="-1"
            @keydown.esc="closeIfAllowed"
          >
            <!-- ── Header ──────────────────────────────────── -->
            <div v-if="$slots.header || title" class="modal-header">
              <slot name="header">
                <h2 class="modal-title">{{ title }}</h2>
              </slot>
              <button
                v-if="showClose"
                class="modal-close-btn"
                aria-label="Close"
                @click="emit('close')"
                @keydown.enter="emit('close')"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- ── Body ───────────────────────────────────── -->
            <div class="modal-body" :class="{ 'modal-body--noPad': noPadding }">
              <!-- Loading overlay -->
              <div v-if="loading" class="modal-loading">
                <svg class="modal-spinner" viewBox="0 0 50 50">
                  <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" />
                </svg>
              </div>
              <slot v-else />
            </div>

            <!-- ── Footer ─────────────────────────────────── -->
            <div v-if="$slots.footer" class="modal-footer">
              <slot name="footer" />
            </div>

            <!-- Mobile drag handle for bottom-sheet -->
            <div v-if="isMobile" class="drag-handle" aria-hidden="true"></div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

// ──────────────────────────────────────────────────────────
// Props & Emits
// ──────────────────────────────────────────────────────────
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title:      { type: String,  default: '' },
  size:       { type: String,  default: 'md', validator: v => ['sm','md','lg','xl','full'].includes(v) },
  /** dialog | drawer | fullscreen */
  type:       { type: String,  default: 'dialog' },
  showClose:  { type: Boolean, default: true },
  /** Prevent closing by clicking backdrop or ESC */
  persistent: { type: Boolean, default: false },
  loading:    { type: Boolean, default: false },
  noPadding:  { type: Boolean, default: false },
  dark:       { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'close'])

// ──────────────────────────────────────────────────────────
// Refs & state
// ──────────────────────────────────────────────────────────
const modalRef = ref(null)
const isMobile = ref(false)

const isDark = computed(() => {
  if (props.dark) return true
  return typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches
})

const sizeClasses = {
  sm:   'max-w-sm',
  md:   'max-w-lg',
  lg:   'max-w-2xl',
  xl:   'max-w-4xl',
  full: 'max-w-6xl',
}

const typeClass = computed(() => ({
  'modal--dialog':     props.type === 'dialog',
  'modal--drawer':     props.type === 'drawer',
  'modal--fullscreen': props.type === 'fullscreen',
}))

// ──────────────────────────────────────────────────────────
// Close logic
// ──────────────────────────────────────────────────────────
function closeIfAllowed() {
  if (!props.persistent) emit('close')
}

// ──────────────────────────────────────────────────────────
// Scroll lock
// ──────────────────────────────────────────────────────────
watch(() => props.modelValue, async (open) => {
  document.body.style.overflow = open ? 'hidden' : ''

  if (open) {
    await nextTick()
    // Focus trap – focus the modal container so ESC works immediately
    modalRef.value?.focus()
  }
})

// ──────────────────────────────────────────────────────────
// Focus trap (keyboard users stay inside modal)
// ──────────────────────────────────────────────────────────
function trapFocus(e) {
  if (!props.modelValue || !modalRef.value) return
  const focusable = modalRef.value.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  const first = focusable[0]
  const last  = focusable[focusable.length - 1]

  if (e.key === 'Tab') {
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last?.focus() }
    } else {
      if (document.activeElement === last)  { e.preventDefault(); first?.focus() }
    }
  }
  if (e.key === 'Escape') closeIfAllowed()
}

// ──────────────────────────────────────────────────────────
// Responsive
// ──────────────────────────────────────────────────────────
function checkMobile() {
  isMobile.value = window.innerWidth < 640
}

onMounted(() => {
  document.addEventListener('keydown', trapFocus)
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  document.removeEventListener('keydown', trapFocus)
  window.removeEventListener('resize', checkMobile)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ─────────────────────────────────────────────────────────
   BACKDROP
───────────────────────────────────────────────────────── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(10px) saturate(150%);
  -webkit-backdrop-filter: blur(10px) saturate(150%);
}

/* Bottom-sheet on mobile */
@media (max-width: 639px) {
  .modal-backdrop {
    align-items: flex-end;
    padding: 0;
  }
}

/* ─────────────────────────────────────────────────────────
   MODAL CONTENT BOX
───────────────────────────────────────────────────────── */
.modal-content {
  position: relative;
  width: 100%;
  background: #fff;
  border-radius: 1.25rem;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.18),
    0 4px 16px  rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
  outline: none;
  overscroll-behavior: contain;
}

/* Fade edges on scroll */
.modal-content::after {
  content: '';
  position: sticky;
  bottom: 0;
  display: block;
  height: 1.5rem;
  background: linear-gradient(to top, #fff, transparent);
  pointer-events: none;
}

/* Mobile: full-width bottom sheet */
@media (max-width: 639px) {
  .modal-content {
    border-radius: 1.5rem 1.5rem 0 0;
    max-height: 92vh;
  }
}

/* ─────────────────────────────────────────────────────────
   HEADER
───────────────────────────────────────────────────────── */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(to right, rgba(249,250,251,0.8), rgba(255,255,255,0.6));
  border-bottom: 1px solid rgba(229,231,235,0.7);
  position: sticky;
  top: 0;
  backdrop-filter: blur(8px);
  border-radius: 1.25rem 1.25rem 0 0;
  z-index: 1;
}

@media (max-width: 639px) {
  .modal-header {
    border-radius: 1.5rem 1.5rem 0 0;
  }
}

.modal-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.01em;
}

/* ─────────────────────────────────────────────────────────
   CLOSE BUTTON
───────────────────────────────────────────────────────── */
.modal-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.625rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #6b7280;
  transition: background 0.15s ease, color 0.15s ease, transform 0.1s ease;
}

.modal-close-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-close-btn:active {
  transform: scale(0.88);
}

/* ─────────────────────────────────────────────────────────
   BODY
───────────────────────────────────────────────────────── */
.modal-body {
  padding: 1.5rem;
}

.modal-body--noPad {
  padding: 0;
}

/* ─────────────────────────────────────────────────────────
   FOOTER
───────────────────────────────────────────────────────── */
.modal-footer {
  padding: 1rem 1.5rem 1.25rem;
  border-top: 1px solid rgba(229,231,235,0.6);
  background: rgba(249,250,251,0.5);
  border-radius: 0 0 1.25rem 1.25rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* ─────────────────────────────────────────────────────────
   LOADING OVERLAY
───────────────────────────────────────────────────────── */
.modal-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem;
}

.modal-spinner {
  width: 2.5rem;
  height: 2.5rem;
  color: #6366f1;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ─────────────────────────────────────────────────────────
   DRAG HANDLE (mobile bottom-sheet)
───────────────────────────────────────────────────────── */
.drag-handle {
  position: absolute;
  top: 0.625rem;
  left: 50%;
  transform: translateX(-50%);
  width: 2.5rem;
  height: 4px;
  background: #d1d5db;
  border-radius: 2px;
}

/* ─────────────────────────────────────────────────────────
   ANIMATIONS – backdrop
───────────────────────────────────────────────────────── */
.backdrop-fade-enter-active,
.backdrop-fade-leave-active {
  transition: opacity 0.22s ease;
}
.backdrop-fade-enter-from,
.backdrop-fade-leave-to {
  opacity: 0;
}

/* ─────────────────────────────────────────────────────────
   ANIMATIONS – modal (spring-physics feel)
───────────────────────────────────────────────────────── */
.modal-spring-enter-active {
  transition:
    transform 0.38s cubic-bezier(0.22, 1, 0.36, 1),
    opacity   0.25s ease;
}
.modal-spring-leave-active {
  transition:
    transform 0.2s ease,
    opacity   0.18s ease;
}
.modal-spring-enter-from {
  transform: translateY(24px) scale(0.95);
  opacity: 0;
}
.modal-spring-leave-to {
  transform: translateY(12px) scale(0.98);
  opacity: 0;
}

/* ─────────────────────────────────────────────────────────
   ANIMATIONS – bottom sheet (mobile)
───────────────────────────────────────────────────────── */
.sheet-slide-enter-active {
  transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.25s ease;
}
.sheet-slide-leave-active {
  transition: transform 0.22s ease, opacity 0.18s ease;
}
.sheet-slide-enter-from {
  transform: translateY(100%);
  opacity: 0;
}
.sheet-slide-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

/* ─────────────────────────────────────────────────────────
   DARK THEME
───────────────────────────────────────────────────────── */
.dark-theme .modal-content {
  background: #1f2937;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.5),
    0 4px 16px  rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.dark-theme .modal-content::after {
  background: linear-gradient(to top, #1f2937, transparent);
}

.dark-theme .modal-header {
  background: linear-gradient(to right, rgba(31,41,55,0.9), rgba(31,41,55,0.7));
  border-bottom-color: rgba(75,85,99,0.5);
}

.dark-theme .modal-title {
  color: #f9fafb;
}

.dark-theme .modal-close-btn {
  color: #9ca3af;
}

.dark-theme .modal-close-btn:hover {
  background: #374151;
  color: #f3f4f6;
}

.dark-theme .modal-footer {
  border-top-color: rgba(75,85,99,0.4);
  background: rgba(31,41,55,0.5);
}

.dark-theme .modal-backdrop {
  background: rgba(0, 0, 0, 0.7);
}

.dark-theme .drag-handle {
  background: #4b5563;
}
</style>