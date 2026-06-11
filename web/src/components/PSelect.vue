<script setup lang="ts">

const props = defineProps<{
  options: Option[]
}>()

type Option = {
  label: string
  value: string
}
const selectedDuration = defineModel<string>('selected')

</script>
<template>
  <div class="select-wrapper">
    <select v-model="selectedDuration"
      class="block w-full p-2 px-4 truncate border bg-btn-primary border-gray-300 hover:brightness-95 rounded-md h-12 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
      <option disabled value="">
        <slot></slot>
      </option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>
<style scoped>
select {
  -webkit-appearance: none;
  appearance: none;
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: "⌄";
  font-size: 1.2rem;
  top: 12%;
  right: 15px;
  position: absolute;
}
</style>
