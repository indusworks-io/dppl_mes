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
      <DashboardComponent v-if="!isFloorMapView" />
      <FactoryFloorMap
        v-else
        :selected-factory="selectedFactory"
        :factory-data="selectedFactoryData"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import DashboardComponent from '../components/DashboardComponent.vue';
import FactoryFloorMap from '../components/FactoryFloorMap.vue';
import HomePageControls from '../components/HomePageControls.vue';

const isFloorMapView = ref(false);
const isMachineDetailsView = ref(false);
const selectedFactory = ref('');
const selectedFactoryData = ref(null);

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
