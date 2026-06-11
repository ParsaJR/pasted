<script setup lang="ts">
defineProps(['text'])
</script>

<template>
  <button
    type="button"
    class="p-2 px-4 border border-gray-300 rounded-md hover:brightness-95 h-12 shadow-sm focus:outline-none focus:ring-2 bg-btn-primary focus:ring-blue-500 focus:border-blue-500 flex items-center gap-2"
  >
  <slot name="icon" ></slot>
    <span>{{ text }}</span>
  </button>
</template>
