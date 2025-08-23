<template>
  <div id="app">
      <NavBar :title="appTitle" />
      <HomePageControls
      :is-floor-map-view="isFloorMapView"
      :is-machine-details-view="isMachineDetailsView"
      :factory-options="factoryOptions"
      :area-options="areaOptions"
      @toggle-view="toggleView"
      
      @filter-selected="handleFilterSelected"
    />
    <!-- <router-view class="view-content" v-slot="{ Component }">
      <component :is="Component" :selected-filters="selectedFilters" />
    </router-view> -->
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { ref, watch } from 'vue';
import { createListResource } from 'frappe-ui';
import FilterDropdown from '../components/FilterDropdown.vue';

const router = useRouter();
const route = useRoute();

const isFloorMapView = ref(false);
const isMachineDetailsView = ref(false);

watch(() => route.name, (newName) => {
  isFloorMapView.value = newName === 'FactoryFloorMap';
  isMachineDetailsView.value = newName === 'MachineDetails';
}, { immediate: true });

const toggleView = () => {
  if (route.name === 'FactoryFloorMap') {
    router.push({ name: 'Dashboard' });
  } else {
    router.push({ name: 'FactoryFloorMap' });
  }
};


const goBackToDashboard = () => {
  router.push({ name: 'Dashboard' });
};

// Fetch factory and area options
const factoryResource = createListResource({
  doctype: 'Factory',
  fields: ['factory_name'],
  orderBy: 'factory_name',
  auto: true,
});

const areaResource = createListResource({
  doctype: 'Area',
  fields: ['area_name'],
  orderBy: 'area_name',
  auto: true,
});

// console.log('Factory Resource:', factoryResource);
// console.log('Area Resource:', areaResource);

const factoryOptions = ref([]);
const areaOptions = ref([]);

// Map fetched data to filter options
watch(() => factoryResource.data, (data) => {
  if (data) {
    factoryOptions.value = data.map(f => ({ value: f.factory_name, text: f.factory_name }));
  }
}, { immediate: true });

watch(() => areaResource.data, (data) => {
  if (data) {
    areaOptions.value = data.map(a => ({ value: a.area_name, text: a.area_name }));
  }
}, { immediate: true });

const selectedFilters = ref({
  factory: '',
  area: '',
});

const handleFilterSelected = (filterName, value) => {
  selectedFilters.value[filterName] = value;
};
</script>


<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
}


.controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 40px;
  background: #f7f8fa;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(60, 72, 88, 0.08);
  border: 1px solid #e5e7eb;
  margin: 18px 32px 0 32px;
  position: relative;
  z-index: 10;
}

.controls-bar button {
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

.controls-bar button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.4s;
}

.controls-bar button:hover::before {
  left: 100%;
}

.controls-bar button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.controls-bar button:active {
  transform: translateY(0px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.filters {
  display: flex;
  gap: 3rem;
  align-items: center;
  padding-left: 8px;
  padding-right: 8px;
}

.filters :deep(label) {
  font-size: 3rem;
  font-weight: 900;
  color: #334155;
  margin-bottom: 4px;
  letter-spacing: 0.2px;
  display: block;
}

.filters.disabled {
  opacity: 0.5;
  pointer-events: none;
  filter: grayscale(50%);
  transition: all 0.2s ease;
}

.view-content {
  flex-grow: 1;
  overflow: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}
</style>