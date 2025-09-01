<template>
  <div class="machine-card" :class="cardColorClass" @click="handleClick">
    <div class="machine-image-container">
      <img 
        v-if="machineImageUrl" 
        :src="machineImageUrl" 
        :alt="machine.machine_name || machine.name"
        class="machine-photo"
        @error="handleImageError"
      />
      <div v-else class="no-image-placeholder">
        <span>📷</span>
        <p>No image</p>
      </div>
    </div>
    <div class="machine-details">
      <h3 class="machine-name">{{ machine.machine_name || machine.name }}</h3>
      
      <!-- Job Progress Metrics -->
      <div v-if="jobMetrics" class="job-metrics">
        <div class="metric-item">
          <span class="metric-label">Job:</span>
          <span class="metric-value">{{ jobMetrics.job_name || 'No Job Running' }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Job #:</span>
          <span class="metric-value">{{ jobMetrics.job_number || 'N/A' }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Target:</span>
          <span class="metric-value">{{ jobMetrics.target_quantity || 0 }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Completed:</span>
          <span class="metric-value">{{ jobMetrics.completed_quantity || 0 }}</span>
        </div>
      </div>
      <div v-else class="no-job">
        <span class="no-job-text">No active job</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineEmits, defineProps } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const props = defineProps({
	machine: {
		type: Object,
		required: true,
		validator: (machine) => {
			return (
				typeof machine.name === "string" &&
				(machine.machine_name === undefined ||
					typeof machine.machine_name === "string") &&
				(machine.area === undefined || typeof machine.area === "string") &&
				typeof machine.is_active === "number"
			)
		},
	},
	jobMetrics: {
		type: Object,
		default: () => null,
	},
})

const emit = defineEmits(["card-clicked"])

// Computed properties
const machineImageUrl = computed(() => {
	if (!props.machine.machine_image) return null

	const imagePath = props.machine.machine_image
	return imagePath.startsWith("http")
		? imagePath
		: `${window.location.origin}${imagePath}`
})

const cardColorClass = computed(() => {
	// If machine is inactive (is_active = 0), show gray
	if (props.machine.is_active === 0) {
		return 'card-inactive'
	}
	
	// If machine is active, check run_rate_indicator from jobMetrics
	if (props.jobMetrics && props.jobMetrics.run_rate_indicator !== undefined) {
		return props.jobMetrics.run_rate_indicator === 1 ? 'card-good' : 'card-poor'
	}
	
	// Default: if no job metrics available but machine is active
	return 'card-default'
})

// Methods
const handleClick = () => {
	emit("card-clicked", props.machine.name)
	router.push(`/machine/${props.machine.name}`)
}

const handleImageError = (event) => {
	event.target.style.display = "none"
	event.target.nextElementSibling?.classList.remove("hidden")
}

const getStatusClass = () => {
	return props.machine.is_active ? "status-active" : "status-inactive"
}
</script>

<style scoped>
.machine-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  margin: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.machine-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.machine-image-container {
  width: 100%;
  height: 150px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.machine-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #6c757d;
  text-align: center;
}

.no-image-placeholder span {
  font-size: 2rem;
  margin-bottom: 4px;
}

.no-image-placeholder p {
  margin: 0;
  font-size: 0.9rem;
}

.machine-details p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  line-height: 1.4;
}

.machine-name {
  margin: 8px 0 12px 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: #495057;
  line-height: 1.2;
}

.job-metrics {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.metric-label {
  font-weight: 500;
  color: #6c757d;
}

.metric-value {
  font-weight: 600;
  color: #495057;
}

.no-job {
  padding: 8px 0;
  text-align: center;
}

.no-job-text {
  font-size: 0.85rem;
  color: #adb5bd;
  font-style: italic;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}

/* Card color classes based on machine status */
.card-inactive {
  background-color: #f8f9fa !important;
  border-color: #dee2e6 !important;
}

.card-good {
  background-color: #d4edda !important;
  border-color: #28a745 !important;
  border-width: 2px !important;
}

.card-poor {
  background-color: #f8d7da !important;
  border-color: #dc3545 !important;
  border-width: 2px !important;
}

.card-default {
  background-color: #fff !important;
  border-color: #ddd !important;
}

.card-inactive .machine-name {
  color: #6c757d !important;
}

.card-good .machine-name {
  color: #155724 !important;
}

.card-poor .machine-name {
  color: #721c24 !important;
}
</style>