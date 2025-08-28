<template>
  <div class="map-container">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading floor plan...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
    </div>

    <!-- No Floor Plan State -->
    <div v-else-if="!floorPlanUrl" class="no-floor-plan">
      <div class="no-plan-icon">🏭</div>
      <h3>No Floor Plan Available</h3>
      <p>{{ selectedFactory ? `No floor plan uploaded for ${selectedFactory}` : 'Please select a factory to view floor plan' }}</p>
    </div>

    <!-- Floor Plan Display -->
    <div v-else class="floor-plan-container">
      <div class="floor-plan-header">
        <h3>{{ selectedFactory }} - Floor Plan</h3>
        <div class="floor-plan-controls">
          <button @click="zoomIn" class="control-btn" title="Zoom In">🔍+</button>
          <button @click="zoomOut" class="control-btn" title="Zoom Out">🔍-</button>
          <button @click="resetZoom" class="control-btn" title="Reset Zoom">⌂</button>
          <button @click="toggleFullscreen" class="control-btn" title="Toggle Fullscreen">⛶</button>
        </div>
      </div>
      
      <div 
        ref="floorPlanContainer" 
        class="floor-plan-wrapper"
        @wheel="handleWheel"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @mouseleave="handleMouseUp"
      >
        <div 
          class="floor-plan-content"
          :style="{
            transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})`,
            transformOrigin: 'center center'
          }"
        >
          <div 
            v-html="svgContent" 
            class="floor-map"
            @click="handleMachineClick"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, nextTick } from 'vue';

const props = defineProps({
  selectedFactory: String,
  factoryData: Object,
  machines: Array,
});

const emit = defineEmits(['machine-selected']);

// ✅ State
const isLoading = ref(false);
const error = ref('');
const svgContent = ref('');
const floorPlanContainer = ref(null);
const machineStates = ref({});

// ✅ Zoom and Pan
const zoomLevel = ref(1);
const panX = ref(0);
const panY = ref(0);
const isDragging = ref(false);
const lastMouseX = ref(0);
const lastMouseY = ref(0);

// ✅ Computed
const floorPlanUrl = computed(() => props.factoryData?.floor_plan || null);

// ✅ Load Floor Plan
const loadFloorPlan = async (floorPlanPath) => {
  if (!floorPlanPath) return;

  isLoading.value = true;
  error.value = '';

  try {
    const baseUrl = window.location.origin;
    const fullUrl = floorPlanPath.startsWith('http')
      ? floorPlanPath
      : `${baseUrl}${floorPlanPath}`;

    const response = await fetch(fullUrl);
    if (!response.ok) throw new Error(`Failed to load floor plan: ${response.statusText}`);

    const svgText = await response.text();
    if (!svgText.includes('<svg')) throw new Error('Invalid SVG file format');

    svgContent.value = svgText;

    await nextTick();
    resetZoom();
    setupMachineElements();
    
    updateMachineColors();

  } catch (err) {
    console.error('Error loading floor plan:', err);
    error.value = err.message || 'Failed to load floor plan';
    svgContent.value = '';
  } finally {
    isLoading.value = false;
  }
};

// ✅ Setup machine elements mapping
const setupMachineElements = () => {
  if (!floorPlanContainer.value) return;
  
  const svgElement = floorPlanContainer.value.querySelector('svg');
  if (!svgElement) return;

  const paths = svgElement.querySelectorAll('path[id]');
  const machines = {};
  
  paths.forEach(path => {
    const machineName = path.id;
    console.log('Machine Name:', machineName);
    machines[machineName] = {
      element: path,
      originalColor: path.style.fill || path.getAttribute('fill') || '#808080'
    };
    path.style.fill = machineStates.value[machineName] || machines[machineName].originalColor;

    // Add interactivity
    path.style.cursor = 'pointer';
    path.addEventListener('click', (event) => {
      event.stopPropagation();
      emit('machine-selected', machineName);
      highlightMachine(path);
    });
    path.addEventListener('mouseenter', () => path.style.filter = 'brightness(1.2)');
    path.addEventListener('mouseleave', () => path.style.filter = '');
  });
  
  machineStates.value = machines;
};

// ✅ Update machine color
const updateMachineColor = (machineName, color) => {
  if (machineStates.value[machineName]) {
    const machine = machineStates.value[machineName];
    machine.element.style.fill = color;
  }
};

// ✅ Update all machine colors based on current machine data
const updateMachineColors = () => {
  if (!props.machines || !props.machines.length || !Object.keys(machineStates.value).length) {
    return;
  }
  
  // Reset all to original color first
  for (const machineName in machineStates.value) {
    const machine = machineStates.value[machineName];
    machine.element.style.fill = machine.originalColor;
  }

  props.machines.forEach(machine => {
    let color;
    if (machine.is_active === 0) {
      color = '#FFFFFF'; // Inactive
    } else {
      // Example logic for other states, assuming you have them
      // For now, just green for active
      color = '#00FF00'; // Active
    }
    updateMachineColor(machine.name, color);
  });
};

// ✅ Watch for changes in machines prop
watch(() => props.machines, () => {
  if (svgContent.value) {
    updateMachineColors();
  }
}, { deep: true, immediate: true });

// ✅ Watch for factory changes to load new floor plan
watch(() => props.factoryData?.floor_plan, (newFloorPlan) => {
  if (newFloorPlan) {
    loadFloorPlan(newFloorPlan);
  }
}, { immediate: true });


// // ✅ Highlight machine
// const highlightMachine = (element) => {
//   const prev = floorPlanContainer.value?.querySelectorAll('.machine-highlighted');
//   prev?.forEach(el => el.classList.remove('machine-highlighted'));
//   element.classList.add('machine-highlighted');
// };

// ✅ Zoom & Pan
const zoomIn = () => zoomLevel.value = Math.min(zoomLevel.value * 1.2, 5);
const zoomOut = () => zoomLevel.value = Math.max(zoomLevel.value / 1.2, 0.1);
const resetZoom = () => { zoomLevel.value = 1; panX.value = 0; panY.value = 0; };

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    floorPlanContainer.value?.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};

// ✅ Wheel zoom
const handleWheel = (event) => {
  event.preventDefault();
  const delta = event.deltaY > 0 ? 0.9 : 1.1;
  zoomLevel.value = Math.max(0.1, Math.min(5, zoomLevel.value * delta));
};

// ✅ Mouse drag
const handleMouseDown = (event) => {
  if (event.button === 0) {
    isDragging.value = true;
    lastMouseX.value = event.clientX;
    lastMouseY.value = event.clientY;
    event.preventDefault();
  }
};

const handleMouseMove = (event) => {
  if (isDragging.value) {
    const deltaX = event.clientX - lastMouseX.value;
    const deltaY = event.clientY - lastMouseY.value;
    panX.value += deltaX;
    panY.value += deltaY;
    lastMouseX.value = event.clientX;
    lastMouseY.value = event.clientY;
  }
};

const handleMouseUp = () => isDragging.value = false;

// ✅ Machine click placeholder
const handleMachineClick = () => {};

onMounted(() => {
  if (floorPlanUrl.value) {
    loadFloorPlan(floorPlanUrl.value);
  }
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  padding: 1rem;
  box-sizing: border-box;
}

/* Loading State */
.loading-state, .error-state, .no-floor-plan {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon, .no-plan-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* Floor Plan Display */
.floor-plan-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.floor-plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e9ecef;
  border-radius: 8px 8px 0 0;
}

.floor-plan-header h3 {
  margin: 0;
  color: #495057;
  font-size: 18px;
}

.floor-plan-controls {
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #dee2e6;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

/* Floor Plan Wrapper */
.floor-plan-wrapper {
  flex: 1;
  overflow: hidden;
  position: relative;
  background: #fff;
  cursor: grab;
  border-radius: 0 0 8px 8px;
}

.floor-plan-wrapper:active {
  cursor: grabbing;
}

.floor-plan-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s ease;
}

.floor-map {
  width: 100%;
  height: 100%;
  padding: 1rem;
  box-sizing: border-box;
}

:deep(svg) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

:deep(.machine-highlighted) {
  filter: brightness(1.3) drop-shadow(0 0 8px #3b82f6) !important;
  stroke: #3b82f6 !important;
  stroke-width: 3 !important;
}
</style>