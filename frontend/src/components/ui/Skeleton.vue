<template>
  <div
    class="skeleton-wrapper"
    :class="[
      heightClasses[height],
      variantClasses[variant],
      directionClass,
      { 'dark-mode': dark }
    ]"
    :style="{
      width,
      animationDelay: delay + 'ms',
      animationDuration: duration + 'ms',
      willChange: 'background-position, opacity',
    }"
    :aria-label="label || 'Loading...'"
    role="status"
    aria-busy="true"
  >
    <!-- Optional label beneath -->
    <span v-if="label" class="skeleton-label">{{ label }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** Visual height preset */
  height: {
    type: String,
    default: 'md',
    validator: (v) => ['xs', 'sm', 'md', 'lg', 'xl', '2xl'].includes(v),
  },
  /** Explicit width override */
  width: {
    type: String,
    default: '100%',
  },
  /** Shape variant */
  variant: {
    type: String,
    default: 'text',
    validator: (v) => ['text', 'avatar', 'card', 'button', 'default', 'circle', 'rounded'].includes(v),
  },
  /** Shimmer direction */
  direction: {
    type: String,
    default: 'horizontal',
    validator: (v) => ['horizontal', 'vertical'].includes(v),
  },
  /** Animation delay in ms – use for stagger effects */
  delay: {
    type: Number,
    default: 0,
  },
  /** Animation duration in ms */
  duration: {
    type: Number,
    default: 1400,
  },
  /** Optional descriptive label rendered below the skeleton */
  label: {
    type: String,
    default: '',
  },
  /** Force dark-mode colours regardless of OS preference */
  dark: {
    type: Boolean,
    default: false,
  },
})

const heightClasses = {
  xs:  'h-2',
  sm:  'h-4',
  md:  'h-8',
  lg:  'h-12',
  xl:  'h-16',
  '2xl': 'h-24',
}

const variantClasses = {
  text:    'rounded',
  avatar:  'rounded-full',
  card:    'rounded-2xl',
  button:  'rounded-lg',
  // legacy aliases kept for backward-compat
  default: 'rounded',
  circle:  'rounded-full',
  rounded: 'rounded-xl',
}

const directionClass = computed(() =>
  props.direction === 'vertical' ? 'shimmer-vertical' : 'shimmer-horizontal'
)
</script>

<style scoped>
/* ─────────────────────────────────────────────────────────
   CORE SKELETON WRAPPER
───────────────────────────────────────────────────────── */
.skeleton-wrapper {
  display: block;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.03);

  /* Pulse rhythm layered on top of shimmer */
  animation:
    shimmer-h var(--sk-duration, 1.4s) ease-in-out infinite,
    sk-pulse    2s                     ease-in-out infinite;

  animation-delay: var(--sk-delay, 0ms), var(--sk-delay, 0ms);
}

/* ─────────────────────────────────────────────────────────
   HORIZONTAL SHIMMER (default)
───────────────────────────────────────────────────────── */
.shimmer-horizontal {
  background-image: linear-gradient(
    90deg,
    rgba(229, 231, 235, 0.6)  0%,
    rgba(243, 244, 246, 0.95) 50%,
    rgba(229, 231, 235, 0.6)  100%
  );
  background-size: 200% 100%;
  animation-name: shimmer-h, sk-pulse;
}

@keyframes shimmer-h {
  0%   { background-position: 150% 0; }
  100% { background-position: -150% 0; }
}

/* ─────────────────────────────────────────────────────────
   VERTICAL SHIMMER
───────────────────────────────────────────────────────── */
.shimmer-vertical {
  background-image: linear-gradient(
    180deg,
    rgba(229, 231, 235, 0.6)  0%,
    rgba(243, 244, 246, 0.95) 50%,
    rgba(229, 231, 235, 0.6)  100%
  );
  background-size: 100% 200%;
  animation-name: shimmer-v, sk-pulse;
}

@keyframes shimmer-v {
  0%   { background-position: 0 150%; }
  100% { background-position: 0 -150%; }
}

/* ─────────────────────────────────────────────────────────
   PULSE (combined with shimmer for "alive" feel)
───────────────────────────────────────────────────────── */
@keyframes sk-pulse {
  0%, 100% { opacity: 0.9; }
  50%       { opacity: 1; }
}

/* ─────────────────────────────────────────────────────────
   DARK MODE – system preference
───────────────────────────────────────────────────────── */
@media (prefers-color-scheme: dark) {
  .skeleton-wrapper {
    border-color: rgba(255, 255, 255, 0.04);
  }

  .shimmer-horizontal {
    background-image: linear-gradient(
      90deg,
      rgba(55,  65, 81, 0.6)  0%,
      rgba(75,  85, 99, 0.95) 50%,
      rgba(55,  65, 81, 0.6)  100%
    );
  }

  .shimmer-vertical {
    background-image: linear-gradient(
      180deg,
      rgba(55,  65, 81, 0.6)  0%,
      rgba(75,  85, 99, 0.95) 50%,
      rgba(55,  65, 81, 0.6)  100%
    );
  }
}

/* ─────────────────────────────────────────────────────────
   FORCED DARK VIA PROP
───────────────────────────────────────────────────────── */
.dark-mode.shimmer-horizontal {
  background-image: linear-gradient(
    90deg,
    rgba(55,  65, 81, 0.6)  0%,
    rgba(75,  85, 99, 0.95) 50%,
    rgba(55,  65, 81, 0.6)  100%
  );
}

.dark-mode.shimmer-vertical {
  background-image: linear-gradient(
    180deg,
    rgba(55,  65, 81, 0.6)  0%,
    rgba(75,  85, 99, 0.95) 50%,
    rgba(55,  65, 81, 0.6)  100%
  );
}

/* ─────────────────────────────────────────────────────────
   OPTIONAL LABEL
───────────────────────────────────────────────────────── */
.skeleton-label {
  position: absolute;
  bottom: -1.25rem;
  left: 0;
  font-size: 0.65rem;
  color: #9ca3af;
  animation: sk-pulse 2s ease-in-out infinite;
}
</style>