<script setup lang="ts">
const checked = defineModel<boolean>()

withDefaults(
  defineProps<{
    scaleBy?: string
  }>(),
  {
    scaleBy: '1',
  },
)
</script>

<template>
  <label class="flex items-center gap-2 cursor-pointer">
    <input
      v-model="checked"
      type="checkbox"
      :style="{
	  transform: `scale(${scaleBy})`
      }"
    />

    <slot />
  </label>
</template>
