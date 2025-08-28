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

// ✅ Zoom and Pan
const zoomLevel = ref(1);
const panX = ref(0);
const panY = ref(0);
const isDragging = ref(false);
const lastMouseX = ref(0);
const lastMouseY = ref(0);

// ✅ Computed
const floorPlanUrl = computed(() => props.factoryData?.floor_plan || null);

const machineElements = ref({});

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

    console.log('Loading floor plan from:', fullUrl);

    const response = await fetch(fullUrl);
    if (!response.ok) throw new Error(`Failed to load floor plan: ${response.statusText}`);

    const svgText = await response.text();
    if (!svgText.includes('<svg')) throw new Error('Invalid SVG file format');

    svgContent.value = svgText;

    await nextTick();
    resetZoom();
    setupMachineElements();
    setupMachineClickHandlers();
    
    // Apply machine colors after SVG is loaded and elements are mapped
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

  const elementsWithIds = svgElement.querySelectorAll('[id]');
  const machines = {};
  
  elementsWithIds.forEach(element => {
    machines[element.id] = {
      element,
      originalColor: element.style.fill || element.getAttribute('fill') || '#000000'
    };
  });
  
  machineElements.value = machines;
  console.log('Machine elements mapped:', Object.keys(machines));
  console.log('Available machine IDs in SVG:', Object.keys(machines));
  
  // Log machine names from props for comparison
  if (props.machines) {
    console.log('Machine names from props:', props.machines.map(m => m.name));
  }
};

// ✅ Update machine color
const updateMachineColor = (machineName, color) => {
  if (machineElements.value[machineName]) {
    const element = machineElements.value[machineName].element;
    element.style.fill = color;
    console.log(`Updated machine ${machineName} to color ${color}`);
  } else {
    console.warn(`Machine element not found: ${machineName}`);
  }
};

// ✅ Update all machine colors based on current machine data
const updateMachineColors = () => {
  if (!props.machines || !props.machines.length) {
    console.log('No machines data available');
    return;
  }
  
  console.log('Updating machine colors...');
  console.log('Available SVG elements:', Object.keys(machineElements.value));
  console.log('Machine data:', props.machines.map(m => ({ name: m.name, is_active: m.is_active })));
  
  props.machines.forEach(machine => {
    const color = machine.is_active === 1 ? '#22c55e' : '#6b7280'; // green if active, gray if not
    
    // Try exact match first
    if (machineElements.value[machine.name]) {
      updateMachineColor(machine.name, color);
    } else {
      // Try to find a partial match or transformed name
      const svgIds = Object.keys(machineElements.value);
      const possibleMatch = svgIds.find(id => 
        id.toLowerCase().includes(machine.name.toLowerCase()) ||
        machine.name.toLowerCase().includes(id.toLowerCase()) ||
        id.replace(/[-_\s]/g, '') === machine.name.replace(/[-_\s]/g, '')
      );
      
      if (possibleMatch) {
        console.log(`Found possible match: ${machine.name} -> ${possibleMatch}`);
        updateMachineColor(possibleMatch, color);
      } else {
        console.warn(`No SVG element found for machine: "${machine.name}"`);
      }
    }
  });
};

// ✅ Watch for changes in machines prop
watch(() => props.machines, (newMachines) => {
  console.log('Machines updated:', newMachines);
  if (newMachines && newMachines.length > 0) {
    // Only update colors if SVG is loaded and elements are mapped
    if (Object.keys(machineElements.value).length > 0) {
      updateMachineColors();
    }
  }
}, { deep: true, immediate: true });

// ✅ Watch for factory changes to load new floor plan
watch(() => props.factoryData?.floor_plan, (newFloorPlan) => {
  if (newFloorPlan) {
    loadFloorPlan(newFloorPlan);
  }
}, { immediate: true });

// ✅ Setup machine click handlers
const setupMachineClickHandlers = () => {
  if (!floorPlanContainer.value) return;
  const svgElement = floorPlanContainer.value.querySelector('svg');
  if (!svgElement) return;

  const machineElements = svgElement.querySelectorAll('[id]');
  
  machineElements.forEach(element => {
    element.style.cursor = 'pointer';

    element.addEventListener('click', (event) => {
      event.stopPropagation();
      const machineId = element.id;
      console.log('Machine clicked:', machineId);
      emit('machine-selected', machineId);
      highlightMachine(element);
    });

    element.addEventListener('mouseenter', () => {
      element.style.filter = 'brightness(1.2)';
    });

    element.addEventListener('mouseleave', () => {
      element.style.filter = '';
    });
  });
};

// ✅ Highlight machine
const highlightMachine = (element) => {
  const prev = floorPlanContainer.value?.querySelectorAll('.machine-highlighted');
  prev?.forEach(el => el.classList.remove('machine-highlighted'));
  element.classList.add('machine-highlighted');
};

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
  // Component is ready
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  padding: 20px;
  box-sizing: border-box;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
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

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #dc3545;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* No Floor Plan State */
.no-floor-plan {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
  padding: 40px;
}

.no-plan-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.no-floor-plan h3 {
  margin: 0 0 12px 0;
  color: #495057;
}

.no-floor-plan p {
  margin: 0;
  font-size: 14px;
}

/* Floor Plan Display */
.floor-plan-container {
  height: calc(100vh - 40px);
  display: flex;
  flex-direction: column;
}

.floor-plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

.control-btn:active {
  background: #e9ecef;
}

/* Floor Plan Wrapper */
.floor-plan-wrapper {
  flex: 1;
  overflow: hidden;
  position: relative;
  background: white;
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
  padding: 20px;
  box-sizing: border-box;
}

.floor-map {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* SVG Styling - Make SVG take full width with padding */
:deep(svg) {
  width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
}

/* Machine highlighting */
:deep(.machine-highlighted) {
  filter: brightness(1.3) drop-shadow(0 0 8px #3b82f6) !important;
  stroke: #3b82f6 !important;
  stroke-width: 3 !important;
}

/* Machine hover effects */
:deep([id]:hover) {
  filter: brightness(1.2);
  transition: filter 0.2s ease;
}

/* Responsive */
@media (max-width: 768px) {
  .map-container {
    padding: 10px;
  }
  
  .floor-plan-header {
    padding: 8px 12px;
  }

  .floor-plan-header h3 {
    font-size: 16px;
  }

  .control-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  .floor-plan-content {
    padding: 10px;
  }
}
</style>