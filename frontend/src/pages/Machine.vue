<template>
  <div class="machine-details-page">
    <NavBar title="Machine Details" />
    
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading machine details...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">�</div>
      <h3>Error Loading Machine Details</h3>
      <p>{{ error }}</p>
      <button @click="goBack" class="back-button">Go Back</button>
    </div>
    
    <!-- Machine Details -->
    <div v-else-if="machine" class="machine-content">
      <!-- Header Section -->
      <div class="machine-header">
        <button @click="goBack" class="back-button">� Back</button>
        <h1>{{ machine.machine_name || machine.name }}</h1>
        <div class="machine-status" :class="getStatusClass()">
          {{ getStatusText() }}
        </div>
      </div>
      
      <!-- Machine Information Grid -->
      <div class="machine-info-grid">
        <!-- Machine Image -->
        <div class="machine-image-section">
          <h3>Machine Image</h3>
          <div class="machine-image-container">
            <img 
              v-if="machine.machine_image" 
              :src="getMachineImageUrl(machine.machine_image)" 
              :alt="machine.machine_name"
              class="machine-image"
              @error="handleImageError"
            />
            <div v-else class="no-image-placeholder">
              <span>=�</span>
              <p>No image available</p>
            </div>
          </div>
        </div>
        
        <!-- Basic Info -->
        <div class="basic-info-section">
          <h3>Basic Information</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Machine ID:</label>
              <span>{{ machine.name }}</span>
            </div>
            <div class="info-item">
              <label>Machine Name:</label>
              <span>{{ machine.machine_name || 'N/A' }}</span>
            </div>
            <div class="info-item">
              <label>Area:</label>
              <span>{{ machine.area || 'N/A' }}</span>
            </div>
            <div class="info-item">
              <label>Status:</label>
              <span class="status-badge" :class="getStatusClass()">
                {{ machine.is_active ? 'Active' : 'Inactive' }}
              </span>
            </div>
            <div class="info-item">
              <label>Sequence Number:</label>
              <span>{{ machine.sequence_number || 'N/A' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Current Job Information -->
      <div v-if="jobMetrics" class="job-info-section">
        <h3>Current Job</h3>
        <div class="job-metrics-grid">
          <div class="metric-card">
            <div class="metric-label">Job Name</div>
            <div class="metric-value">{{ jobMetrics.job_name || 'No Job Running' }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Job Number</div>
            <div class="metric-value">{{ jobMetrics.job_number || 'N/A' }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Target Quantity</div>
            <div class="metric-value">{{ jobMetrics.target_quantity || 0 }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Completed Quantity</div>
            <div class="metric-value">{{ jobMetrics.completed_quantity || 0 }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Balance Quantity</div>
            <div class="metric-value">{{ jobMetrics.balance_quantity || 0 }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Performance</div>
            <div class="metric-value" :class="jobMetrics.run_rate_indicator === 1 ? 'performance-good' : 'performance-poor'">
              {{ jobMetrics.run_rate_indicator === 1 ? 'On Track' : 'Behind Schedule' }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui"
import { onMounted, onUnmounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import NavBar from "../components/NavBar.vue"
import { initSocket } from "../socket.js"

const route = useRoute()
const router = useRouter()

// Reactive data
const machine = ref(null)
const jobMetrics = ref(null)
const isLoading = ref(true)
const error = ref("")
const socket = ref(null)

// Get machine ID from route params
const machineId = route.params.id

// Fetch machine details
createResource({
	url: "frappe.client.get",
	params: {
		doctype: "Machine",
		name: machineId,
	},
	auto: true,
	onSuccess(data) {
		machine.value = data
		fetchJobMetrics()
	},
	onError(err) {
		error.value = `Failed to load machine details: ${err.message}`
		isLoading.value = false
	},
})

// Fetch job metrics
const fetchJobMetrics = () => {
	createResource({
		url: "dppl_mes.api.get_job_metrics_internal_function",
		params: { machine: machineId },
		auto: true,
		onSuccess(response) {
			if (response.status === "success" || response.data) {
				jobMetrics.value = response.data
			}
			isLoading.value = false
		},
		onError(err) {
			console.warn("Could not fetch job metrics:", err)
			isLoading.value = false
		},
	})
}

// Socket integration for real-time updates
const setupSocketListener = () => {
	if (!socket.value) {
		socket.value = initSocket()
	}

	socket.value.on("job_metrics_update", (data) => {
		if (data.machine === machineId) {
			jobMetrics.value = data.job_metrics
		}
	})
}

// Utility functions
const getMachineImageUrl = (imagePath) => {
	if (!imagePath) return ""
	return imagePath.startsWith("http")
		? imagePath
		: `${window.location.origin}${imagePath}`
}

const handleImageError = (event) => {
	event.target.style.display = "none"
}

const getStatusClass = () => {
	if (!machine.value) return ""
	return machine.value.is_active ? "status-active" : "status-inactive"
}

const getStatusText = () => {
	if (!machine.value) return "Unknown"
	return machine.value.is_active ? "Active" : "Inactive"
}

const goBack = () => {
	router.go(-1)
}

// Lifecycle hooks
onMounted(() => {
	setupSocketListener()
})

onUnmounted(() => {
	if (socket.value) {
		socket.value.off("job_metrics_update")
	}
})
</script>

<style scoped>
.machine-details-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Loading and Error States */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
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

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* Main Content */
.machine-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.machine-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.machine-header h1 {
  flex: 1;
  margin: 0;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
}

.machine-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}

/* Back Button */
.back-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #5a6268;
}

/* Machine Info Grid */
.machine-info-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
  margin-bottom: 40px;
}

@media (max-width: 768px) {
  .machine-info-grid {
    grid-template-columns: 1fr;
  }
}

.machine-image-section, .basic-info-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.machine-image-section h3, .basic-info-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

/* Machine Image */
.machine-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.machine-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #6c757d;
  font-size: 1.1rem;
}

.no-image-placeholder span {
  font-size: 3rem;
  margin-bottom: 10px;
}

/* Basic Info Grid */
.info-grid {
  display: grid;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #007bff;
}

.info-item label {
  font-weight: 600;
  color: #495057;
}

.info-item span {
  font-weight: 500;
  color: #212529;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

/* Job Info Section */
.job-info-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.job-info-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.job-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.metric-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #dee2e6;
  transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.metric-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.performance-good {
  color: #28a745;
}

.performance-poor {
  color: #dc3545;
}
</style>