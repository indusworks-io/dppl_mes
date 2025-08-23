<!-- src/components/HomePageControls.vue -->
<template>
    <div class="controls-bar">
            <button @click="$emit('toggle-view')" class="toggle-button">
                Switch to {{ isFloorMapView ? 'Dashboard' : 'Floor Map' }}
            </button>
            <div class="filters">
                <FilterDropdown
                    id="factory-filter"
                    label="Factory"
                    :options="factoryOptions"
                    @filter-selected="filterSelected('factory', $event)"
                />
                
                <FilterDropdown
                    id="area-filter"
                    label="Area"
                    :options="areaOptions"
                    @filter-selected="filterSelected('area', $event)"
                />
                
            </div>
    </div>

</template>

<script setup>
import FilterDropdown from './FilterDropdown.vue';

const props = defineProps({
  isFloorMapView: Boolean,
  isMachineDetailsView: Boolean,
  factoryOptions: Array,
  areaOptions: Array
});

const emit = defineEmits(['go-back', 'toggle-view', 'filter-selected']);

const filterSelected = (filterName, value) => {
  emit('filter-selected', { filterName, value });
};
</script>

<style scoped>
.controls-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: #f7f8fa;
  border-radius: 0px;
  box-shadow: 0 2px 16px rgba(60, 72, 88, 0.08);
  margin: 0px 0;
  position: relative;
  z-index: 10;
  gap: 10px;
}

.toggle-button {
  /* Ensure button doesn't shrink */
  flex-shrink: 0;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  padding: 0;
}

.filters :deep(.filter-dropdown) {
  min-width: 400px; /* Set consistent minimum width */
}

/* Alternative: Make filters equal width */
.filters :deep(.filter-dropdown select) {
  width: 400px;
  box-sizing: border-box;
}

/* Desktop: filters align to the right */
@media (min-width: 769px) {
  .filters {
    flex-grow: 1;
    justify-content: flex-end;
  }
}

/* Mobile: filters start from left when wrapped */
@media (max-width: 768px) {
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .toggle-button {
    align-self: flex-start;
  }
  
  .filters {
    justify-content: flex-start;
    width: 100%;
  }

  .filters :deep(.filter-dropdown) {
    max-width: 100%;
    flex: 1;
    }

    .filters :deep(.filter-dropdown select) {
    max-width: 100%;
    box-sizing: border-box;
    }
}

/* Alternative: Keep everything in rows but stack on very small screens */
@media (max-width: 480px) {
  .filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
</style>