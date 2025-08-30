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
    <div class="toggle-wrapper">
      <button @click="$emit('toggle-view')" class="toggle-button">
        Switch to {{ isFloorMapView ? 'Dashboard View' : 'Map View' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from "vue"
import FilterDropdown from "./FilterDropdown.vue"

const props = defineProps({
	factoryOptions: { type: Array, required: true },
	selectedFactory: { type: String, required: true },
	isFloorMapView: { type: Boolean, required: true },
})

const emit = defineEmits(["filter-selected", "toggle-view"])

function emitFactorySelection(value) {
	emit("filter-selected", value)
}
</script>

<style scoped>
.controls-bar {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
  padding: 12px 16px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

/* Desktop layout */
@media (min-width: 768px) {
  .controls-bar {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }
}

.filters {
  display: flex;
  align-items: center;
  width: 100%;
}

.toggle-wrapper {
  display: flex;
  width: 100%;
}

/* Desktop: align toggle button to the right */
@media (min-width: 768px) {
  .filters {
    width: auto;
  }
  
  .toggle-wrapper {
    width: auto;
    justify-content: flex-end;
  }
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
  white-space: nowrap;
  width: 100%;
}

/* Desktop: reset button width */
@media (min-width: 768px) {
  .toggle-button {
    width: auto;
    min-width: fit-content;
  }
}

.toggle-button:hover {
  background-color: #1d4ed8; /* Darker blue */
}

.toggle-button:active {
  background-color: #1e40af; /* Even darker */
}

.loading-placeholder {
  color: #6b7280;
  font-style: italic;
}
</style>
