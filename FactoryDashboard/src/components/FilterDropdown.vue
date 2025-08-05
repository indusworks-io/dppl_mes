<template>
  <div class="filter-dropdown">
    <label :for="id">{{ label }}:</label>
    <select :id="id" @change="handleChange">
      <option value="">All</option>
      <option v-for="option in options" :key="option.value" :value="option.value">{{ option.text }}</option>
    </select>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  id: String,
  label: String,
  options: Array
});

const emit = defineEmits(['filter-selected']);

const handleChange = (event) => {
  emit('filter-selected', event.target.value);
};
</script>

<style scoped>
.filter-dropdown {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-dropdown label {
  font-weight: 600;
  font-size: 1rem;
  color: #343a40;
}

.filter-dropdown select {
  /* Resetting default appearance */
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  /* Custom Styles */
  padding: 10px 36px 10px 14px;
  border-radius: 6px;
  border: 1px solid #ced4da;
  background-color: #fff;
  font-size: 1.15rem;
  font-weight: 600;
  color: #212529;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  /* Custom Arrow */
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px 12px;
}

.filter-dropdown select:hover {
  border-color: #adb5bd;
}

.filter-dropdown select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>