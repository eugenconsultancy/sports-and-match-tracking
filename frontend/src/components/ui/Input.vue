<template>
  <div class="space-y-1">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
      :class="inputClasses"
    />
    
    <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
    <p v-if="hint" class="text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  label: String,
  id: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  disabled: Boolean,
  required: Boolean,
  error: String,
  hint: String,
  variant: { type: String, default: 'default' },
})
defineEmits(['update:modelValue'])

const inputClasses = computed(() => {
  if (props.error) {
    return 'border-red-300 focus:ring-red-500'
  }
  return 'border-gray-300 focus:ring-primary-500'
})
</script>