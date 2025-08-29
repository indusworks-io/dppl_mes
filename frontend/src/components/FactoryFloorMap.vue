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
        @click="handleBackgroundClick"
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
          ></div>
        </div>
      </div>
    </div>

    <!-- Machine Details Overlay -->
    <div v-if="selectedMachine && showOverlay" class="machine-overlay" @click="closeOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h3>{{ selectedMachine.machine_name || selectedMachine.name }}</h3>
          <button @click="closeOverlay" class="close-btn">×</button>
        </div>
        
        <div class="overlay-body">
          <div v-if="selectedMachineMetrics" class="job-details">
            <div class="detail-item">
              <label>Job Name:</label>
              <span>{{ selectedMachineMetrics.job_name || 'No Job Running' }}</span>
            </div>
            <div class="detail-item">
              <label>Job Number:</label>
              <span>{{ selectedMachineMetrics.job_number || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <label>Target Quantity:</label>
              <span>{{ selectedMachineMetrics.target_quantity || 0 }}</span>
            </div>
            <div class="detail-item">
              <label>Completed Quantity:</label>
              <span>{{ selectedMachineMetrics.completed_quantity || 0 }}</span>
            </div>
            <div class="detail-item">
              <label>Performance:</label>
              <span 
                :class="selectedMachineMetrics.run_rate_indicator === 1 ? 'status-good' : 'status-poor'"
              >
                {{ selectedMachineMetrics.run_rate_indicator === 1 ? 'On Track' : 'Behind Schedule' }}
              </span>
            </div>
          </div>
          
          <div v-else class="no-job-info">
            <p>No job information available</p>
          </div>
        </div>
        
        <div class="overlay-footer">
          <button @click="goToMachineDetails" class="details-btn">
            View Machine Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui"
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { useRouter } from "vue-router"
import { initSocket, useSocket } from "../socket.js"

const props = defineProps({
	selectedFactory: String,
	factoryData: Object,
	machines: Array,
})

const emit = defineEmits(["machine-selected"])

const router = useRouter()

// ✅ State
const isLoading = ref(false)
const error = ref("")
const svgContent = ref("")
const floorPlanContainer = ref(null)
const machineStates = ref({})

// Machine overlay state
const selectedMachine = ref(null)
const selectedMachineMetrics = ref(null)
const showOverlay = ref(false)
const machineJobMetrics = ref({})

// ✅ Zoom and Pan
const zoomLevel = ref(1)
const panX = ref(0)
const panY = ref(0)
const isDragging = ref(false)
const lastMouseX = ref(0)
const lastMouseY = ref(0)

// ✅ Computed
const floorPlanUrl = computed(() => {
	const url = props.factoryData?.floor_plan || null
	console.log(`🔍 floorPlanUrl computed:`, url)
	console.log(`🔍 props.factoryData:`, props.factoryData)
	console.log(`🔍 props.selectedFactory:`, props.selectedFactory)
	return url
})

// ✅ Load Floor Plan
const loadFloorPlan = async (floorPlanPath) => {
	console.log(`🔄 loadFloorPlan called with path:`, floorPlanPath)
	console.trace(`📍 loadFloorPlan call stack`)
	
	if (!floorPlanPath) {
		console.log(`❌ No floor plan path provided`)
		return
	}

	console.log(`🔄 Starting floor plan load process`)
	isLoading.value = true
	error.value = ""

	try {
		const baseUrl = window.location.origin
		const fullUrl = floorPlanPath.startsWith("http")
			? floorPlanPath
			: `${baseUrl}${floorPlanPath}`

		const response = await fetch(fullUrl)
		if (!response.ok)
			throw new Error(`Failed to load floor plan: ${response.statusText}`)

		const svgText = await response.text()
		if (!svgText.includes("<svg")) throw new Error("Invalid SVG file format")

		svgContent.value = svgText

		// Wait for DOM to update with new SVG content
		await nextTick()
		
		// Wait a bit more to ensure DOM is fully rendered
		await new Promise(resolve => setTimeout(resolve, 100))
		
		resetZoom()
		
		// Only setup machines if container is actually available
		// This will be called by nextTick after DOM renders
		nextTick(() => {
			console.log(`🔄 Checking if container exists after DOM update...`)
			if (floorPlanContainer.value) {
				console.log(`✅ Container found! Setting up machines.`)
				setupMachineElements()
				updateMachineColors()
			} else {
				console.log(`❌ Container still not found, will retry when DOM is ready`)
				// Try once more after a short delay
				setTimeout(() => {
					if (floorPlanContainer.value) {
						console.log(`✅ Container found on retry! Setting up machines.`)
						setupMachineElements()
						updateMachineColors()
					} else {
						console.error(`❌ Container never became available`)
					}
				}, 500)
			}
		})
	} catch (err) {
		console.error("Error loading floor plan:", err)
		error.value = err.message || "Failed to load floor plan"
		svgContent.value = ""
	} finally {
		isLoading.value = false
	}
}

// ✅ Setup machine elements mapping  
const setupMachineElements = async (retryCount = 0) => {
	if (!floorPlanContainer.value) {
		if (retryCount < 3) {
			await new Promise(resolve => setTimeout(resolve, 200))
			return setupMachineElements(retryCount + 1)
		} else {
			console.error(`❌ Floor plan container not found after retries`)
			return
		}
	}

	const svgElement = floorPlanContainer.value.querySelector("svg")
	if (!svgElement) {
		console.warn(`❌ No SVG element found in floor plan`)
		return
	}

	const paths = svgElement.querySelectorAll("path[id]")
	const machines = {}

	paths.forEach((path) => {
		const machineName = path.id
		machines[machineName] = {
			element: path,
			originalColor: path.style.fill || path.getAttribute("fill") || "#808080",
		}

		// Add interactivity
		path.style.cursor = "pointer"
		path.addEventListener("click", (event) => {
			event.stopPropagation()
			handleMachinePathClick(machineName, event)
		})
		path.addEventListener(
			"mouseenter",
			() => (path.style.filter = "brightness(1.2)"),
		)
		path.addEventListener("mouseleave", () => (path.style.filter = ""))
	})

	machineStates.value = machines
	console.log(`🏗️ Floor plan loaded with ${Object.keys(machines).length} machines`)
	
	// Apply any stored job metrics that arrived before floor plan was loaded
	updateMachineColors()
}

// ✅ Update machine color
const updateMachineColor = (machineName, color) => {
	if (machineStates.value[machineName]) {
		machineStates.value[machineName].element.style.fill = color
	} else {
		console.warn(`❌ Machine ${machineName} not found in floor plan`)
	}
}

// ✅ Update all machine colors based on current machine data
const updateMachineColors = () => {
	if (!Object.keys(machineStates.value).length) {
		return
	}

	// Reset all to gray first (no machine data)
	for (const machineName in machineStates.value) {
		const machine = machineStates.value[machineName]
		machine.element.style.fill = "#808080" // Gray for no data
	}

	// Update colors based on machine data and job metrics
	if (props.machines && props.machines.length) {
		props.machines.forEach((machine) => {
			const machineMetrics = machineJobMetrics.value[machine.name]
			let color

			if (machine.is_active === 0) {
				color = "#FFFFFF" // White for inactive
			} else if (machineMetrics && machineMetrics.run_rate_indicator === 1) {
				color = "#00FF00" // Green for running efficiently
			} else if (machineMetrics) {
				color = "#FF0000" // Red for behind schedule
			} else {
				color = "#808080" // Gray for no job data
			}

			updateMachineColor(machine.name, color)
		})
	}
}

// Function to handle job metrics update (moved to component scope)
const handleJobMetricsUpdate = (data) => {
	// Handle different data structures that Frappe might send
	let actualData = data
	if (data && data.message) {
		actualData = data.message // Frappe sometimes wraps data in 'message'
	}
	
	if (actualData && actualData.machine && actualData.job_metrics) {
		const machineName = actualData.machine
		const jobMetrics = actualData.job_metrics
		
		console.log(`📊 Updating machine ${machineName} - run_rate: ${jobMetrics.run_rate_indicator}`)
		
		// Update machine job metrics (always store this even if floor plan isn't loaded yet)
		machineJobMetrics.value[machineName] = jobMetrics

		// Update the color for this specific machine
		let color
		if (jobMetrics.run_rate_indicator === 1) {
			color = "#00FF00" // Green for running efficiently
		} else {
			color = "#FF0000" // Red for behind schedule  
		}

		// Try to update color immediately
		updateMachineColor(machineName, color)
		
		// If floor plan isn't loaded yet, the above will fail but data is stored
		if (Object.keys(machineStates.value).length === 0) {
			console.log(`⏰ Floor plan not loaded yet. Job metrics stored for later application.`)
		}

		// If this machine is currently selected, update the overlay
		if (selectedMachine.value && selectedMachine.value.name === machineName) {
			selectedMachineMetrics.value = jobMetrics
		}
	} else {
		console.warn(`❌ Invalid job metrics data received`)
	}
}

// ✅ Socket Integration
const setupSocketListener = () => {
	const socketInstance = useSocket() || initSocket()

	// Listen for any socket event that contains job metrics data
	socketInstance.onAny((...args) => {
		// Check if any event contains our job metrics data
		args.forEach((arg) => {
			if (arg && typeof arg === 'object') {
				// Check for direct machine/job_metrics structure
				if (arg.machine && arg.job_metrics) {
					handleJobMetricsUpdate(arg)
				}
				// Check for nested message structure
				else if (arg.message && arg.message.machine && arg.message.job_metrics) {
					handleJobMetricsUpdate(arg.message)
				}
				// Check for event-specific structure
				else if (arg.event === 'job_metrics_update' && arg.data) {
					handleJobMetricsUpdate(arg.data)
				}
			}
		})
	})

	// Primary listener for direct job_metrics_update events
	socketInstance.on('job_metrics_update', (data) => {
		handleJobMetricsUpdate(data)
	})

	// Listen for Frappe's default realtime event structure
	socketInstance.on('msgprint', (data) => {
		if (data && data.message && typeof data.message === 'object') {
			if (data.message.machine && data.message.job_metrics) {
				handleJobMetricsUpdate(data.message)
			}
		}
	})

	// Verify socket connection
	if (socketInstance.connected) {
		console.log("✅ Socket connected for realtime updates")
	}

}


// ✅ Machine Click Handlers
const handleMachinePathClick = (machineName, event) => {
	event.stopPropagation()

	// Find machine data
	const machineData = props.machines?.find((m) => m.name === machineName)
	if (!machineData) {
		console.warn(`Machine ${machineName} not found in props.machines`)
		return
	}

	selectedMachine.value = machineData

	// Use already stored job metrics from socket events (no API call)
	const existingMetrics = machineJobMetrics.value[machineName]
	if (existingMetrics) {
		selectedMachineMetrics.value = existingMetrics
	} else {
		selectedMachineMetrics.value = null
	}

	showOverlay.value = true
	emit("machine-selected", machineName)
}

const handleBackgroundClick = () => {
	// Only close overlay if clicking on background, not during pan/drag
	if (!isDragging.value && showOverlay.value) {
		closeOverlay()
	}
}

const closeOverlay = () => {
	showOverlay.value = false
	selectedMachine.value = null
	selectedMachineMetrics.value = null
}

const goToMachineDetails = () => {
	if (selectedMachine.value) {
		router.push(`/machine/${selectedMachine.value.name}`)
	}
}

// ✅ Watch for changes in machines prop
watch(
	() => props.machines,
	() => {
		if (svgContent.value) {
			updateMachineColors()
		}
	},
	{ deep: true, immediate: true },
)

// ✅ Watch for factory changes to load new floor plan
watch(
	() => props.factoryData?.floor_plan,
	(newFloorPlan) => {
		if (newFloorPlan) {
			loadFloorPlan(newFloorPlan)
		}
	},
	{ immediate: true },
)


// ✅ Zoom & Pan
const zoomIn = () => (zoomLevel.value = Math.min(zoomLevel.value * 1.2, 5))
const zoomOut = () => (zoomLevel.value = Math.max(zoomLevel.value / 1.2, 0.1))
const resetZoom = () => {
	zoomLevel.value = 1
	panX.value = 0
	panY.value = 0
}

const toggleFullscreen = () => {
	if (!document.fullscreenElement) {
		floorPlanContainer.value?.requestFullscreen()
	} else {
		document.exitFullscreen()
	}
}

// ✅ Wheel zoom
const handleWheel = (event) => {
	event.preventDefault()
	const delta = event.deltaY > 0 ? 0.9 : 1.1
	zoomLevel.value = Math.max(0.1, Math.min(5, zoomLevel.value * delta))
}

// ✅ Mouse drag
const handleMouseDown = (event) => {
	if (event.button === 0) {
		isDragging.value = true
		lastMouseX.value = event.clientX
		lastMouseY.value = event.clientY
		event.preventDefault()
	}
}

const handleMouseMove = (event) => {
	if (isDragging.value) {
		const deltaX = event.clientX - lastMouseX.value
		const deltaY = event.clientY - lastMouseY.value
		panX.value += deltaX
		panY.value += deltaY
		lastMouseX.value = event.clientX
		lastMouseY.value = event.clientY
	}
}

const handleMouseUp = () => (isDragging.value = false)


onMounted(() => {
	// Setup socket listeners first
	setupSocketListener()
	
	// Then load floor plan if available
	if (floorPlanUrl.value) {
		loadFloorPlan(floorPlanUrl.value)
	}
})

onUnmounted(() => {
	const socketInstance = useSocket()
	if (socketInstance) {
		socketInstance.off("job_metrics_update")
	}
})
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

/* Machine Overlay Styles */
.machine-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.overlay-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  animation: overlayFadeIn 0.2s ease-out;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.overlay-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.overlay-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.overlay-body {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.job-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.detail-item label {
  font-weight: 600;
  color: #495057;
}

.detail-item span {
  font-weight: 500;
  color: #212529;
}

.status-good {
  color: #28a745;
  font-weight: 600;
}

.status-poor {
  color: #dc3545;
  font-weight: 600;
}

.no-job-info {
  text-align: center;
  color: #6c757d;
  padding: 20px;
}

.overlay-footer {
  padding: 20px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.details-btn {
  width: 100%;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.details-btn:hover {
  background-color: #0056b3;
}

.details-btn:active {
  background-color: #004085;
}
</style>