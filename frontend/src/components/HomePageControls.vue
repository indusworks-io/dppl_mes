<template>
  <div class="controls-bar">
    <!-- Factory Filter -->
    <div class="filters">
      <FilterDropdown
        v-if="factoryOptions.length > 0 && selectedFactory"
        :key="`factory-${selectedFactory}-${factoryOptions.length}`"
        id="factory-filter"
        label="Factory"
        :options="factoryOptions"
        :model-value="selectedFactory"
        placeholder="Select Factory"
        @filter-selected="handleFilterChange"
      />
      <div v-else class="loading-placeholder">
        Loading factories...
      </div>
    </div>
    
    <!-- Toggle Button -->
    <button @click="$emit('toggle-view')" class="toggle-button">
      Switch to {{ isFloorMapView ? 'Dashboard View' : 'Map View' }}
    </button>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { createListResource, createDocumentResource } from 'frappe-ui';
import FilterDropdown from './FilterDropdown.vue';

const props = defineProps({
  isFloorMapView: Boolean,
  isMachineDetailsView: Boolean,
});

const emit = defineEmits(['go-back', 'toggle-view', 'filter-selected', 'factory-data-updated']);

// ✅ Reactive state
const factoryOptions = ref([]);
const selectedFactory = ref('');

// ✅ Fetch list of factories
const factoryResource = createListResource({
  doctype: 'Factory',
  fields: ['name', 'factory_name', 'floor_plan'], // Include factory_name for display
  filters: {
    is_active: 1 // Only fetch active factories
  },
  auto: true,
});

// ✅ Fetch organization settings (single doctype)
const organizationSettings = createDocumentResource({
  doctype: 'Organization Settings',
  name: 'Organization Settings', // For single doctypes, name is usually the doctype name
  auto: true,
});

// ✅ Get current factory data
const currentFactoryData = computed(() => {
  if (!selectedFactory.value || !factoryResource.data) return null;
  
  return factoryResource.data.find(f => f.name === selectedFactory.value);
});

// ✅ Watch for data updates and build dropdown options
watch([() => factoryResource.data, () => organizationSettings.doc], ([factories, orgSettings]) => {
  console.log('Factories data:', factories);
  console.log('Organization settings:', orgSettings);
  
  if (!factories || !Array.isArray(factories)) return;

  const defaultFactory = orgSettings?.default_factory || '';
  console.log('Default factory from settings:', defaultFactory);

  // Build options list using factory_name for display and name for value
  let options = factories.map(f => ({
    value: f.name,
    text: f.factory_name || f.name, // Use factory_name if available, fallback to name
  }));

  console.log('All factory options before reordering:', options);

  // Put default factory first if it exists and reorder the array
  if (defaultFactory) {
    const defaultOptionIndex = options.findIndex(opt => opt.value === defaultFactory);
    console.log('Default factory index found:', defaultOptionIndex);
    
    if (defaultOptionIndex !== -1) {
      // Remove default factory from its current position
      const [defaultOption] = options.splice(defaultOptionIndex, 1);
      // Add it to the beginning
      options.unshift(defaultOption);
      
      console.log('Reordered options with default first:', options);
      
      // Set as selected (always set the default factory as selected)
      selectedFactory.value = defaultFactory;
      console.log('Selected factory set to:', defaultFactory);
    }
  }

  // If no default factory but we have options, select the first one
  if (!defaultFactory && options.length > 0) {
    selectedFactory.value = options[0].value;
    console.log('No default factory, selected first option:', options[0].value);
  }

  factoryOptions.value = options;
  console.log('Final factoryOptions:', factoryOptions.value);
  console.log('Final selectedFactory:', selectedFactory.value);
}, { immediate: true });

// ✅ Watch for current factory data changes and emit to parent
watch(currentFactoryData, (newData) => {
  console.log('Current factory data changed:', newData);
  emit('factory-data-updated', newData);
}, { immediate: true });

// ✅ Handle selection
const handleFilterChange = (value) => {
  console.log('Filter changed to:', value);
  selectedFactory.value = value;
  emit('filter-selected', value);
};

// ✅ Emit initial selection when component mounts and default factory is loaded
watch(() => selectedFactory.value, (newValue) => {
  console.log('selectedFactory watcher triggered with:', newValue);
  if (newValue) {
    emit('filter-selected', newValue);
  }
});

// ✅ Force update the dropdown when both data and selection are ready
const isReady = computed(() => {
  const ready = factoryOptions.value.length > 0 && selectedFactory.value;
  console.log('Component ready state:', ready, {
    optionsCount: factoryOptions.value.length,
    selectedValue: selectedFactory.value
  });
  return ready;
});
</script>

<style scoped>
.controls-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  padding: 10px 20px;
  background: #f7f8fa;
  box-shadow: 0 2px 16px rgba(60, 72, 88, 0.08);
  gap: 10px;
  position: relative;
  z-index: 10;
}

/* Filters Section */
.filters {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-grow: 1;
}

/* Loading placeholder */
.loading-placeholder {
  padding: 10px 15px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  color: #6c757d;
  font-size: 14px;
}

/* Toggle Button Style */
.toggle-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.25px;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  position: relative;
  overflow: hidden;
}

.toggle-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.4s;
}

.toggle-button:hover::before {
  left: 100%;
}

.toggle-button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.toggle-button:active {
  transform: translateY(0px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

/* Responsive Layout */
@media (max-width: 768px) {
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .filters {
    justify-content: flex-start;
    width: 100%;
  }
}
</style>