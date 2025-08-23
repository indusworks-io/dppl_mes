<template>
  <div id="app">
      <NavBar/>
      <HomePageControls
      :is-floor-map-view="isFloorMapView"
      :is-machine-details-view="isMachineDetailsView"
      @toggle-view="toggleView"
    />

    <div id="HomePageView">
      <!-- Conditionally render components based on current view -->
      <DashboardComponent v-if="!isFloorMapView" />
      <FactoryFloorMap v-else />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { createListResource } from 'frappe-ui';
import DashboardComponent from '../components/DashboardComponent.vue';
import FactoryFloorMap from '../components/FactoryFloorMap.vue';
import HomePageControls from '../components/HomePageControls.vue';

const isFloorMapView = ref(false);
const isMachineDetailsView = ref(false);

// Function to check if device is mobile/tablet (small screen)
const isMobileDevice = () => {
  return window.innerWidth <= 1024; // Consider anything <= 1024px as mobile/tablet
};

// Initialize view based on device size
const initializeView = () => {
  if (isMobileDevice()) {
    // Small devices: default to Dashboard
    isFloorMapView.value = false;
  } else {
    // Large devices: default to Factory Floor Map
    isFloorMapView.value = true;
  }
};

// Handle window resize to potentially adjust view
const handleResize = () => {
  // Optionally, you can uncomment the line below to auto-switch on resize
  // initializeView();
};

// Toggle between views
const toggleView = () => {
  isFloorMapView.value = !isFloorMapView.value;
};

// Set up event listeners and initialize
onMounted(() => {
  initializeView();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

</script>

<style>

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

#HomePageView {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Media queries for responsive behavior */
@media (max-width: 1024px) {
  #HomePageView {
    /* Styles optimized for mobile/tablet view */
    padding: 10px;
  }
}

@media (min-width: 1025px) {
  #HomePageView {
    /* Styles optimized for desktop/TV view */
    padding: 20px;
  }
}

</style>