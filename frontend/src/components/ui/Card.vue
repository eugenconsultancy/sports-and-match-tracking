<template>
  <div
    class="ls-card"
    :class="[
      `ls-card--${variant}`,
      { 'ls-card--clickable': clickable, 'ls-card--elevated': elevated, 'ls-card--glass': glass }
    ]"
    @click="clickable && $emit('click')"
  >
    <!-- Header Slot -->
    <div v-if="$slots.header" class="ls-card__header">
      <slot name="header" />
    </div>

    <!-- Image Slot -->
    <div v-if="$slots.image" class="ls-card__image">
      <slot name="image" />
    </div>

    <!-- Body -->
    <div class="ls-card__body" :class="`ls-card__body--${padding}`">
      <slot />
    </div>

    <!-- Footer Slot -->
    <div v-if="$slots.footer" class="ls-card__footer">
      <slot name="footer" />
    </div>

    <!-- Hover shimmer line -->
    <div v-if="clickable" class="ls-card__shimmer" />
  </div>
</template>

<script setup>
defineProps({
  clickable: { type: Boolean, default: false },
  elevated:  { type: Boolean, default: false },
  glass:     { type: Boolean, default: false },
  padding:   { type: String, default: 'md', validator: v => ['none','sm','md','lg'].includes(v) },
  variant:   { type: String, default: 'default', validator: v => ['default','accent','live','ghost'].includes(v) },
})
defineEmits(['click'])
</script>

<style scoped>
.ls-card {
  position: relative;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition);
}

/* Variants */
.ls-card--accent {
  border-color: rgba(0,230,118,0.2);
  background: linear-gradient(145deg, var(--c-surface), rgba(0,230,118,0.04));
}

.ls-card--live {
  border-color: rgba(255,61,87,0.2);
  background: linear-gradient(145deg, var(--c-surface), rgba(255,61,87,0.04));
}

.ls-card--ghost {
  background: transparent;
  border-color: var(--c-border);
}

.ls-card--glass {
  background: rgba(14, 20, 32, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}

/* Clickable */
.ls-card--clickable {
  cursor: pointer;
  user-select: none;
}

.ls-card--clickable:hover {
  border-color: var(--c-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}

.ls-card--clickable:active {
  transform: translateY(0) scale(0.99);
}

/* Elevated */
.ls-card--elevated {
  box-shadow: var(--shadow-card);
}

.ls-card--elevated:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-3px);
}

/* Header */
.ls-card__header {
  padding: 14px 18px;
  border-bottom: 1px solid var(--c-border);
  background: linear-gradient(to right, var(--c-surface-2), var(--c-surface));
}

/* Image */
.ls-card__image {
  overflow: hidden;
  line-height: 0;
}

.ls-card__image img {
  width: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.ls-card--clickable:hover .ls-card__image img {
  transform: scale(1.04);
}

/* Body padding variants */
.ls-card__body--sm  { padding: 12px; }
.ls-card__body--md  { padding: 18px; }
.ls-card__body--lg  { padding: 24px; }

/* Footer */
.ls-card__footer {
  padding: 12px 18px;
  border-top: 1px solid var(--c-border);
  background: rgba(0,0,0,0.1);
}

/* Shimmer on hover */
.ls-card__shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(
    105deg,
    transparent,
    rgba(255,255,255,0.03) 50%,
    transparent
  );
  pointer-events: none;
  transition: left 0.5s ease;
}

.ls-card--clickable:hover .ls-card__shimmer {
  left: 140%;
}
</style>