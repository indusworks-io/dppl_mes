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
      <!-- Machine Page Header -->
      <div class="machine-page-header">
        <button @click="goBack" class="back-icon-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <h1 class="machine-title">{{ machine.machine_name || machine.name }}</h1>
      </div>
      
      <!-- Machine Details Tabs Section -->
      <div class="machine-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab-button', { 'active': activeTab === tab.id }]"
        >
          {{ tab.name }}
        </button>
      </div>
      
      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Overview Tab -->
        <div v-show="activeTab === 'overview'" class="overview-section">
          <div class="overview-grid">
            <!-- Machine Card -->
            <div class="machine-card-section">
              <div class="machine-card">
                <div class="machine-image-container">
                  <img 
                    v-if="machine.machine_image" 
                    :src="getMachineImageUrl(machine.machine_image)" 
                    :alt="machine.machine_name"
                    class="machine-image"
                    @error="handleImageError"
                  />
                  <div v-else class="no-image-placeholder">
                    <p>No Image Available</p>
                  </div>
                </div>
                <div class="machine-info">
                  <div class="info-item">
                    <span class="info-label">Factory:</span>
                    <span class="info-value">{{ machine.factory || 'N/A' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Area:</span>
                    <span class="info-value">{{ machine.area || 'N/A' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="info-value status-badge" :class="getStatusClass()">
                      {{ machine.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Active Job Card -->
            <div class="active-job-section">
              <div class="active-job-card">
                <div class="active-job-header">
                  <h3>Active Job</h3>
                  <hr class="divider">
                </div>
                <div v-if="jobMetrics && jobMetrics.job_name" class="job-details">
                  <div class="job-detail-tile">
                    <div class="tile-label">Job Name</div>
                    <div class="tile-value">{{ jobMetrics.job_name }}</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Job Number</div>
                    <div class="tile-value">{{ jobMetrics.job_number || 'N/A' }}</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Target Quantity</div>
                    <div class="tile-value">{{ jobMetrics.target_quantity || 0 }}</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Completed Quantity</div>
                    <div class="tile-value">{{ jobMetrics.completed_quantity || 0 }}</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Balance Quantity</div>
                    <div class="tile-value">{{ jobMetrics.balance_quantity || 0 }}</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Performance</div>
                    <div class="tile-value" :class="jobMetrics.run_rate_indicator === 1 ? 'performance-good' : 'performance-poor'">
                      {{ jobMetrics.run_rate_indicator === 1 ? 'On Schedule' : 'Behind Schedule' }}
                    </div>
                  </div>
                </div>
                <div v-else class="no-job">
                  <p>No active job running</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Job Cards Tab -->
        <div v-show="activeTab === 'jobcards'" class="jobcards-section">
          <div v-if="jobCardsResource.loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading job cards...</p>
          </div>
          <div v-else-if="jobCardsResource.error" class="error-state">
            <p>Error loading job cards: {{ jobCardsResource.error }}</p>
            <button @click="jobCardsResource.reload()" class="retry-button">Retry</button>
          </div>
          <div v-else-if="jobCardsResource.data && jobCardsResource.data.length > 0" class="job-cards-list">
            <div v-for="jobCard in jobCardsResource.data" :key="jobCard.name" class="job-card-item">
              <div class="job-card-header">
                <h4>{{ jobCard.job_name || 'Unnamed Job' }}</h4>
                <span class="status-badge" :class="getJobStatusClass(jobCard.status)">
                  {{ jobCard.status || 'Unknown' }}
                </span>
              </div>
              <div class="job-card-details">
                <p><strong>Job #:</strong> {{ jobCard.job_number || 'N/A' }}</p>
                <p><strong>Target:</strong> {{ jobCard.target_quantity || 0 }}</p>
                <p><strong>Completed:</strong> {{ jobCard.completed_quantity || 0 }}</p>
                <p><strong>Created:</strong> {{ formatDate(jobCard.creation) }}</p>
              </div>
            </div>
          </div>
          <div v-else class="no-data">
            <p>No job cards found for this machine</p>
          </div>
        </div>
        
        <!-- Downtime Logs Tab -->
        <div v-show="activeTab === 'downtime'" class="downtime-section">
          <div v-if="downtimeLogsResource.loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading downtime logs...</p>
          </div>
          <div v-else-if="downtimeLogsResource.error" class="error-state">
            <p>Error loading downtime logs: {{ downtimeLogsResource.error }}</p>
            <button @click="downtimeLogsResource.reload()" class="retry-button">Retry</button>
          </div>
          <div v-else-if="downtimeLogsResource.data && downtimeLogsResource.data.length > 0" class="downtime-logs-list">
            <div v-for="log in downtimeLogsResource.data" :key="log.name" class="downtime-log-item">
              <div class="downtime-log-header">
                <h4>{{ log.reason || 'Unknown Reason' }}</h4>
                <span class="status-badge" :class="getDowntimeStatusClass(log.status)">
                  {{ log.status || 'Unknown' }}
                </span>
              </div>
              <div class="downtime-log-details">
                <p><strong>Start:</strong> {{ formatDateTime(log.start_date_time) || 'N/A' }}</p>
                <p><strong>End:</strong> {{ formatDateTime(log.end_date_time) || 'Ongoing' }}</p>
                <p><strong>Duration:</strong> {{ log.duration || 'Calculating...' }}</p>
                <p><strong>Created:</strong> {{ formatDate(log.created_date) }}</p>
                <p v-if="log.category"><strong>Category:</strong> {{ log.category }}</p>
                <p v-if="log.remarks" class="remarks"><strong>Remarks:</strong> {{ log.remarks }}</p>
              </div>
            </div>
          </div>
          <div v-else class="no-data">
            <p>No downtime logs found for this machine</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource, createResource } from "frappe-ui"
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
const activeTab = ref("overview")

// Tab definitions
const tabs = ref([
	{ id: "overview", name: "Overview" },
	{ id: "jobcards", name: "Job Cards" },
	{ id: "downtime", name: "Downtime Logs" },
])

// Get machine ID from route params
const machineId = route.params.id

// Create Job Cards resource
const jobCardsResource = createListResource({
	doctype: "Job Card",
	fields: [
		"name",
		"job_name",
		"job_number",
		"status",
		"target_quantity",
		"completed_quantity",
		"creation",
		"planned_start_date_time",
		"planned_end_date_time",
	],
	filters: { machine: machineId },
	orderBy: "creation desc",
	pageLength: 50,
	auto: false,
	cache: ["job_cards", machineId],
	onSuccess(data) {
		console.log("Job cards loaded:", data?.length || 0)
	},
	onError(err) {
		console.warn("Could not fetch job cards:", err)
	},
})

// Create Downtime Logs resource
const downtimeLogsResource = createListResource({
	doctype: "Downtime Log",
	fields: [
		"name",
		"reason",
		"start_date_time",
		"end_date_time",
		"duration",
		"created_date",
		"status",
		"category",
		"remarks",
	],
	filters: { machine: machineId },
	orderBy: "created_date desc",
	pageLength: 50,
	auto: false,
	cache: ["downtime_logs", machineId],
	onSuccess(data) {
		console.log("Downtime logs loaded:", data?.length || 0)
	},
	onError(err) {
		console.warn("Could not fetch downtime logs:", err)
	},
})

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
		// Reload the list resources
		jobCardsResource.reload()
		downtimeLogsResource.reload()
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

const goBack = () => {
	router.go(-1)
}

// Utility functions for formatting and status classes
const formatDate = (dateString) => {
	if (!dateString) return "N/A"
	try {
		return new Date(dateString).toLocaleDateString()
	} catch {
		return "Invalid Date"
	}
}

const formatDateTime = (dateTimeString) => {
	if (!dateTimeString) return "N/A"
	try {
		return new Date(dateTimeString).toLocaleString()
	} catch {
		return "Invalid DateTime"
	}
}

const getJobStatusClass = (status) => {
	if (!status) return "status-unknown"
	const statusLower = status.toLowerCase()
	if (statusLower.includes("progress") || statusLower.includes("active")) {
		return "status-active"
	} else if (statusLower.includes("complete") || statusLower.includes("done")) {
		return "status-complete"
	} else if (
		statusLower.includes("cancelled") ||
		statusLower.includes("failed")
	) {
		return "status-error"
	}
	return "status-pending"
}

const getDowntimeStatusClass = (status) => {
	if (!status) return "status-unknown"
	const statusLower = status.toLowerCase()
	if (statusLower.includes("active") || statusLower.includes("ongoing")) {
		return "status-error"
	} else if (
		statusLower.includes("resolved") ||
		statusLower.includes("complete")
	) {
		return "status-complete"
	}
	return "status-pending"
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

/* Machine Page Header */
.machine-page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
}

.back-icon-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #6c757d;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-icon-button:hover {
  background-color: #e9ecef;
  color: #495057;
}

.machine-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

/* Tab Navigation */
.machine-tabs {
  display: flex;
  border-bottom: 2px solid #e9ecef;
  margin-bottom: 24px;
  gap: 0;
}

.tab-button {
  background: none;
  border: none;
  padding: 12px 24px;
  cursor: pointer;
  font-weight: 500;
  color: #6c757d;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
  font-size: 1rem;
}

.tab-button:hover {
  color: #495057;
  background-color: #f8f9fa;
}

.tab-button.active {
  color: #007bff;
  border-bottom-color: #007bff;
  background-color: #fff;
}

/* Tab Content */
.tab-content {
  min-height: 400px;
}

/* Overview Section */
.overview-section {
  padding: 0;
}

.overview-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* Machine Card */
.machine-card-section {
  display: flex;
  flex-direction: column;
}

.machine-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.machine-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  margin-bottom: 16px;
}

.machine-image {
  max-width: 100%;
  max-height: 180px;
  border-radius: 8px;
  object-fit: cover;
}

.no-image-placeholder {
  color: #6c757d;
  font-size: 1rem;
  text-align: center;
}

.machine-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.info-value {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
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

/* Active Job Card */
.active-job-section {
  display: flex;
  flex-direction: column;
}

.active-job-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.active-job-header h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 600;
}

.divider {
  border: none;
  height: 2px;
  background-color: #e9ecef;
  margin-bottom: 20px;
}

.job-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-detail-tile {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tile-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.tile-value {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.performance-good {
  color: #28a745;
}

.performance-poor {
  color: #dc3545;
}

.no-job {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 40px 0;
}

/* Loading and Error States */
.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #6c757d;
  text-align: center;
}

.error-state {
  color: #dc3545;
}

.retry-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 12px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #0056b3;
}

/* Job Cards Tab */
.jobcards-section {
  padding: 20px 0;
}

.job-cards-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.job-card-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.job-card-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
}

.job-card-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  flex: 1;
}

.job-card-details p {
  margin: 8px 0;
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
}

.job-card-details strong {
  color: #495057;
  font-weight: 600;
}

/* Downtime Logs Tab */
.downtime-section {
  padding: 20px 0;
}

.downtime-logs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.downtime-log-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.downtime-log-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.downtime-log-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
}

.downtime-log-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  flex: 1;
}

.downtime-log-details p {
  margin: 8px 0;
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
}

.downtime-log-details strong {
  color: #495057;
  font-weight: 600;
}

.downtime-log-details .remarks {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f8f9fa;
  font-style: italic;
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  margin-left: 0;
  margin-right: 0;
}

/* Status Badge Variants */
.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.status-complete {
  background-color: #d4edda;
  color: #155724;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-error {
  background-color: #f8d7da;
  color: #721c24;
}

.status-unknown {
  background-color: #e2e3e5;
  color: #6c757d;
}

.no-data {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 60px 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .machine-content {
    padding: 16px;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .machine-page-header {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .machine-title {
    font-size: 1.5rem;
  }
  
  .machine-tabs {
    flex-wrap: wrap;
  }
  
  .tab-button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
  
  .job-cards-list,
  .downtime-logs-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .machine-content {
    padding: 12px;
  }
  
  .machine-title {
    font-size: 1.3rem;
  }
  
  .job-detail-tile {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .active-job-card,
  .machine-card {
    padding: 16px;
  }
}
</style>