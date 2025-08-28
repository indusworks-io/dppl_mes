<template>
  <div id="app">
    <NavBar />
    <HomePageControls
      :is-floor-map-view="isFloorMapView"
      :is-machine-details-view="isMachineDetailsView"
      @toggle-view="toggleView"
      @filter-selected="handleFactorySelection"
      @factory-data-updated="handleFactoryDataUpdate"
    />

    <div id="HomePageView">
      <DashboardComponent v-if="!isFloorMapView" :areas="areas" :machines="machines" />
      <FactoryFloorMap
        v-else
        :selected-factory="selectedFactory"
        :factory-data="selectedFactoryData"
        :machines="machines"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { createListResource } from 'frappe-ui';
import DashboardComponent from '../components/DashboardComponent.vue';
import FactoryFloorMap from '../components/FactoryFloorMap.vue';
import HomePageControls from '../components/HomePageControls.vue';

const isFloorMapView = ref(false);
const isMachineDetailsView = ref(false);
const selectedFactory = ref('');
const selectedFactoryData = ref(null);
const areas = ref([]);
const machines = ref([]);

// Resources
const areaResource = createListResource({
  doctype: 'Area',
  fields: ['name', 'area_name', 'factory', 'sequence_number'],
  auto: true,
});

const machineResource = createListResource({
  doctype: 'Machine',
  fields: ['name', 'machine_name', 'is_active', 'area', 'factory','sequence_number', 'machine_image'],
  auto: true,
});

watch(() => areaResource.data, (newAreas) => {
  if (newAreas) {
    areas.value = newAreas;
  }
});

watch(() => machineResource.data, (newMachines) => {
  if (newMachines) {
    console.log('Fetched machines in Home.vue:', newMachines);
    machines.value = newMachines;
  }
});

// Toggle view
const toggleView = () => {
  isFloorMapView.value = !isFloorMapView.value;
};

// Handle factory selection
const handleFactorySelection = (factoryName) => {
  selectedFactory.value = factoryName;
  console.log('Selected factory in Home.vue:', factoryName);
};

// Handle factory data update
const handleFactoryDataUpdate = (data) => {
  selectedFactoryData.value = data;
  console.log('Factory data in Home.vue:', data);
};

// Initialize view based on device size
const initializeView = () => {
  isFloorMapView.value = window.innerWidth > 1024;
};

onMounted(() => {
  initializeView();
  window.addEventListener('resize', initializeView);
});

onUnmounted(() => {
  window.removeEventListener('resize', initializeView);
});
</script>
