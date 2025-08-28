<template>
  <div class="controls-bar">
    <!-- Factory Filter -->
    <div class="filters">
      <FilterDropdown
        v-if="factoryOptions.length > 0 && selectedFactory"
        :id="'factory-filter'"
        label="Factory"
        :options="factoryOptions"
        :model-value="selectedFactory"
        placeholder="Select Factory"
        @update:modelValue="emitFactorySelection"
      />
      <div v-else class="loading-placeholder">Loading factories...</div>
    </div>

    <!-- Toggle Button -->
    <button @click="$emit('toggle-view')" class="toggle-button">
      Switch to {{ isFloorMapView ? 'Dashboard View' : 'Map View' }}
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import FilterDropdown from './FilterDropdown.vue';

const props = defineProps({
  factoryOptions: { type: Array, required: true },
  selectedFactory: { type: String, required: true },
  isFloorMapView: { type: Boolean, required: true }
});

const emit = defineEmits(['filter-selected', 'toggle-view']);

function emitFactorySelection(value) {
  emit('filter-selected', value);
}
</script>

<style scoped>
.controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.filters {
  display: flex;
  align-items: center;
}

.toggle-button {
  background-color: #2563eb; /* Blue 600 */
  color: white;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.toggle-button:hover {
  background-color: #1d4ed8; /* Darker blue */
}

.toggle-button:active {
  background-color: #1e40af; /* Even darker */
}
</style>
