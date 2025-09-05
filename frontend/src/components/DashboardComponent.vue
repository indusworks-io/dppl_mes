<template>
  <div class="dashboard-container">
    <div v-if="loading" class="loading-state">
      <p>Loading dashboard...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>
    <div v-else>
      <div v-for="area in sortedAreas" :key="area.name" class="area-section">
        <h2 class="area-title">{{ area.area_name }}</h2>
        <div class="machine-grid">
          <MachineCard
            v-for="machine in getMachinesForArea(area.name)"
            :key="machine.name"
            :machine="machine"
            :job-metrics="machineJobMetrics[machine.name]"
            @card-clicked="handleMachineClick"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui"
import { computed, onMounted, onUnmounted, ref } from "vue"
import { initSocket, useSocket } from "../socket.js"
import MachineCard from "./MachineCard.vue"

const props = defineProps({
	areas: {
		type: Array,
		required: true,
	},
	machines: {
		type: Array,
		required: true,
	},
	selectedFactory: {
		type: String,
		default: "",
	},
})

const loading = ref(false)
const error = ref(null)
const machineJobMetrics = ref({})

const sortedAreas = computed(() => {
	return [...props.areas].sort((a, b) => a.sequence_number - b.sequence_number)
})

const getMachinesForArea = (areaName) => {
	return props.machines
		.filter((machine) => machine.area === areaName)
		.sort((a, b) => a.sequence_number - b.sequence_number)
}

const handleMachineClick = (machineId) => {
	console.log("Machine clicked:", machineId)
	// Handle machine click event, e.g., navigate to machine details page
}

// Function to handle job metrics update from socket
const handleJobMetricsUpdate = (data) => {
	// Handle different data structures that Frappe might send
	let actualData = data
	if (data && data.message) {
		actualData = data.message // Frappe sometimes wraps data in 'message'
	}

	if (actualData && actualData.machine && actualData.job_metrics) {
		const machineName = actualData.machine
		const jobMetrics = actualData.job_metrics

		console.log(
			`📊 Dashboard - Updating machine ${machineName} - run_rate: ${jobMetrics.run_rate_indicator}`,
		)

		// Update machine job metrics
		machineJobMetrics.value[machineName] = jobMetrics
	} else {
		console.warn(`❌ Invalid job metrics data received in dashboard`)
	}
}

// Setup socket listener
const setupSocketListener = () => {
	const socketInstance = useSocket() || initSocket()

	// Listen for any socket event that contains job metrics data
	socketInstance.onAny((...args) => {
		// Check if any event contains our job metrics data
		args.forEach((arg) => {
			if (arg && typeof arg === "object") {
				// Check for direct machine/job_metrics structure
				if (arg.machine && arg.job_metrics) {
					handleJobMetricsUpdate(arg)
				}
				// Check for nested message structure
				else if (
					arg.message &&
					arg.message.machine &&
					arg.message.job_metrics
				) {
					handleJobMetricsUpdate(arg.message)
				}
				// Check for event-specific structure
				else if (arg.event === "job_metrics_update" && arg.data) {
					handleJobMetricsUpdate(arg.data)
				}
			}
		})
	})

	// Primary listener for direct job_metrics_update events
	socketInstance.on("job_metrics_update", (data) => {
		handleJobMetricsUpdate(data)
	})

	// Listen for Frappe's default realtime event structure
	socketInstance.on("msgprint", (data) => {
		if (data && data.message && typeof data.message === "object") {
			if (data.message.machine && data.message.job_metrics) {
				handleJobMetricsUpdate(data.message)
			}
		}
	})

	// Verify socket connection
	if (socketInstance.connected) {
		console.log("✅ Dashboard socket connected for realtime updates")
	}
}

// Fetch initial job metrics for all machines
const fetchInitialJobMetrics = () => {
	const jobMetricsResource = createResource({
		url: "dppl_mes.api.get_all_machines_job_metrics",
		auto: false,
		onSuccess(data) {
			if (data.status === "success" && data.data) {
				// Populate initial job metrics
				machineJobMetrics.value = { ...data.data }
				console.log(
					`📊 Dashboard - Loaded initial job metrics for ${data.machines_count} machines`,
				)
			} else {
				console.warn("⚠️ Dashboard - No initial job metrics data received")
			}
		},
		onError(error) {
			console.error(
				"❌ Dashboard - Failed to fetch initial job metrics:",
				error,
			)
		},
	})

	jobMetricsResource.reload()
}

onMounted(() => {
	if (!props.areas || !props.machines) {
		loading.value = true
		// In a real app, you might want to fetch data here if it's not passed via props
	} else {
		loading.value = false
	}

	// Fetch initial job metrics first
	fetchInitialJobMetrics()

	// Then setup socket listeners for realtime updates
	setupSocketListener()
})

onUnmounted(() => {
	const socketInstance = useSocket()
	if (socketInstance) {
		socketInstance.off("job_metrics_update")
	}
})
</script>

<style scoped>
.dashboard-container {
  padding: 16px;
}

.area-section {
  margin-bottom: 32px;
}

.area-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
  padding-bottom: 8px;
  color: #333;
}

.machine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #888;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }
  
  .area-section {
    margin-bottom: 24px;
  }
  
  .area-title {
    font-size: 18px;
    margin-bottom: 12px;
    padding-bottom: 6px;
  }
  
  .machine-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .machine-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 18px;
  }
}

@media (min-width: 1025px) {
  .dashboard-container {
    padding: 24px;
  }
  
  .area-section {
    margin-bottom: 40px;
  }
  
  .area-title {
    font-size: 24px;
    margin-bottom: 20px;
    padding-bottom: 12px;
  }
  
  .machine-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 24px;
  }
}
</style>