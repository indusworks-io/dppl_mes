<template>
  <div class="machine-details-page p-6">
    
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
                    <div class="tile-label">Completion %</div>
                    <div class="tile-value">{{ jobMetrics.target_quantity ? Math.round((jobMetrics.completed_quantity || 0) / jobMetrics.target_quantity * 100) : 0 }}%</div>
                  </div>
                  <div class="job-detail-tile">
                    <div class="tile-label">Performance</div>
                    <div class="tile-value" :class="jobMetrics.run_rate_indicator === 1 ? 'performance-on-schedule' : 'performance-behind'">
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
          <div v-if="jobCardsResource.loading && allJobCards.length === 0" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading job cards...</p>
          </div>
          <div v-else-if="jobCardsResource.error" class="error-state">
            <p>Error loading job cards: {{ jobCardsResource.error }}</p>
            <button @click="retryLoadJobCards" class="retry-button">Retry</button>
          </div>
          <div v-else-if="allJobCards.length > 0" class="job-cards-container">
            <!-- Job Cards List Header (Desktop) -->
            <div class="job-cards-header">
              <div class="header-cell">Date</div>
              <div class="header-cell">Shift</div>
              <div class="header-cell">Job Name</div>
              <div class="header-cell">Target Qty</div>
              <div class="header-cell">Completed Qty</div>
              <div class="header-cell">Status</div>
            </div>
            
            <!-- Job Cards List Items -->
            <div class="job-cards-list">
              <div 
                v-for="jobCard in allJobCards" 
                :key="jobCard.name" 
                class="job-card-row"
                @click="navigateToJobCard(jobCard.name)"
              >
                <div class="job-card-cell date-cell">
                  <span class="mobile-label">Date:</span>
                  <span class="cell-value">{{ formatDate(jobCard.date) }}</span>
                </div>
                <div class="job-card-cell shift-cell">
                  <span class="mobile-label">Shift:</span>
                  <span class="cell-value">{{ jobCard.shift || 'N/A' }}</span>
                </div>
                <div class="job-card-cell job-name-cell">
                  <span class="mobile-label">Job Name:</span>
                  <span class="cell-value">{{ jobCard.job_name || 'Unnamed Job' }}</span>
                </div>
                <div class="job-card-cell target-cell">
                  <span class="mobile-label">Target Qty:</span>
                  <span class="cell-value">{{ jobCard.target_quantity || 0 }}</span>
                </div>
                <div class="job-card-cell completed-cell">
                  <span class="mobile-label">Completed Qty:</span>
                  <span class="cell-value">{{ jobCard.completed_quantity || 0 }}</span>
                </div>
                <div class="job-card-cell status-cell">
                  <span class="mobile-label">Status:</span>
                  <span class="status-badge" :class="getJobStatusClass(jobCard.status)">
                    {{ jobCard.status || 'Unknown' }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Load More Section -->
            <div class="load-more-container">
              <div v-if="jobCardsLoadingMore" class="loading-more">
                <div class="loading-spinner-small"></div>
                <span>Loading more job cards...</span>
              </div>
              <button 
                v-else-if="jobCardsHasMore" 
                @click="loadMoreJobCards" 
                class="load-more-button"
              >
                Load More Job Cards
              </button>
              <div v-else class="no-more-records">
                No More Records Found
              </div>
            </div>
          </div>
          <div v-else-if="!jobCardsResource.loading && allJobCards.length === 0" class="no-data">
            <p>No job cards found for this machine</p>
            <button @click="retryLoadJobCards" class="retry-button">Refresh</button>
          </div>
        </div>
        
        <!-- Downtime Logs Tab -->
        <div v-show="activeTab === 'downtime'" class="downtime-section">
          <div v-if="downtimeLogsResource.loading && allDowntimeLogs.length === 0" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading downtime logs...</p>
          </div>
          <div v-else-if="downtimeLogsResource.error" class="error-state">
            <p>Error loading downtime logs: {{ downtimeLogsResource.error }}</p>
            <button @click="retryLoadDowntimeLogs" class="retry-button">Retry</button>
          </div>
          <div v-else-if="allDowntimeLogs.length > 0" class="downtime-logs-container">
            <!-- Downtime Logs List Header (Desktop) -->
            <div class="downtime-logs-header">
              <div class="header-cell">Log Name</div>
              <div class="header-cell">Start DateTime</div>
              <div class="header-cell">End DateTime</div>
              <div class="header-cell">Duration</div>
              <div class="header-cell">Reason</div>
              <div class="header-cell">Status</div>
            </div>
            
            <!-- Downtime Logs List Items -->
            <div class="downtime-logs-list">
              <div 
                v-for="log in allDowntimeLogs" 
                :key="log.name" 
                class="downtime-log-row"
                @click="navigateToDowntimeLog(log.name)"
              >
                <div class="downtime-log-cell name-cell">
                  <span class="mobile-label">Log Name:</span>
                  <span class="cell-value">{{ log.name || 'N/A' }}</span>
                </div>
                <div class="downtime-log-cell start-cell">
                  <span class="mobile-label">Start:</span>
                  <span class="cell-value">{{ formatDateTime(log.start_date_time) }}</span>
                </div>
                <div class="downtime-log-cell end-cell">
                  <span class="mobile-label">End:</span>
                  <span class="cell-value">{{ log.end_date_time ? formatDateTime(log.end_date_time) : 'Ongoing' }}</span>
                </div>
                <div class="downtime-log-cell duration-cell">
                  <span class="mobile-label">Duration:</span>
                  <span class="cell-value">{{ formatDurationDetailed(log.duration) }}</span>
                </div>
                <div class="downtime-log-cell reason-cell">
                  <span class="mobile-label">Reason:</span>
                  <span class="cell-value">{{ log.reason || 'Unknown' }}</span>
                </div>
                <div class="downtime-log-cell status-cell">
                  <span class="mobile-label">Status:</span>
                  <span class="status-badge" :class="getDowntimeStatusClass(log.status)">
                    {{ log.status || 'Unknown' }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Load More Section -->
            <div class="load-more-container">
              <div v-if="downtimeLogsLoadingMore" class="loading-more">
                <div class="loading-spinner-small"></div>
                <span>Loading more downtime logs...</span>
              </div>
              <button 
                v-else-if="downtimeLogsHasMore" 
                @click="loadMoreDowntimeLogs" 
                class="load-more-button"
              >
                Load More Downtime Logs
              </button>
              <div v-else class="no-more-records">
                No More Records Found
              </div>
            </div>
          </div>
          <div v-else-if="!downtimeLogsResource.loading && allDowntimeLogs.length === 0" class="no-data">
            <p>No downtime logs found for this machine</p>
            <button @click="retryLoadDowntimeLogs" class="retry-button">Refresh</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createListResource, createResource } from "frappe-ui"
import { onMounted, onUnmounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { initSocket } from "../../socket.js"

const route = useRoute()
const router = useRouter()

// Reactive data
const machine = ref(null)
const jobMetrics = ref(null)
const isLoading = ref(true)
const error = ref("")
const socket = ref(null)
const activeTab = ref("overview")

// Pagination state for Job Cards
const jobCardsStart = ref(0)
const jobCardsHasMore = ref(true)
const jobCardsLoadingMore = ref(false)
const allJobCards = ref([])

// Pagination state for Downtime Logs
const downtimeLogsStart = ref(0)
const downtimeLogsHasMore = ref(true)
const downtimeLogsLoadingMore = ref(false)
const allDowntimeLogs = ref([])

// Tab definitions
const tabs = ref([
	{ id: "overview", name: "Overview" },
	{ id: "jobcards", name: "Job Cards" },
	{ id: "downtime", name: "Downtime Logs" },
])

// Get machine ID from route params
const machineId = route.params.id

// Create Job Cards resource with reactive start
const jobCardsResource = createListResource({
	doctype: "Job Card",
	fields: [
		"name",
		"machine",
		"date",
		"shift",
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
	start: 0, // Start with 0 initially
	pageLength: 50,
	auto: false,
	cache: false, // Disable cache to avoid stale data issues
	onSuccess(data) {
		console.log(
			"Job cards loaded:",
			data?.length || 0,
			"Start:",
			jobCardsStart.value,
		)

		if (jobCardsStart.value === 0) {
			// Initial load - replace data
			allJobCards.value = data || []
			// Reset hasMore flag for initial load
			jobCardsHasMore.value = data && data.length === 50
		} else {
			// Load more - append data
			allJobCards.value = [...allJobCards.value, ...(data || [])]
			// Check if there are more records
			if (!data || data.length < 50) {
				jobCardsHasMore.value = false
			}
		}

		jobCardsLoadingMore.value = false
	},
	onError(err) {
		console.error("Error fetching job cards:", err)
		jobCardsLoadingMore.value = false
		// Reset loading states on error
		if (jobCardsResource.loading) {
			jobCardsResource.loading = false
		}
	},
})

// Create Downtime Logs resource with reactive start
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
		"machine", // Add machine field to ensure proper filtering
	],
	filters: { machine: machineId },
	orderBy: "created_date desc",
	start: 0, // Start with 0 initially
	pageLength: 50,
	auto: false,
	cache: false, // Disable cache to avoid stale data issues
	onSuccess(data) {
		console.log(
			"Downtime logs loaded:",
			data?.length || 0,
			"Start:",
			downtimeLogsStart.value,
		)

		if (downtimeLogsStart.value === 0) {
			// Initial load - replace data
			allDowntimeLogs.value = data || []
			// Reset hasMore flag for initial load
			downtimeLogsHasMore.value = data && data.length === 50
		} else {
			// Load more - append data
			allDowntimeLogs.value = [...allDowntimeLogs.value, ...(data || [])]
			// Check if there are more records
			if (!data || data.length < 50) {
				downtimeLogsHasMore.value = false
			}
		}

		downtimeLogsLoadingMore.value = false
	},
	onError(err) {
		console.error("Error fetching downtime logs:", err)
		downtimeLogsLoadingMore.value = false
		// Reset loading states on error
		if (downtimeLogsResource.loading) {
			downtimeLogsResource.loading = false
		}
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
		// Don't auto-load job cards and downtime logs here
		// They will be loaded when their respective tabs are clicked
		console.log("Machine details loaded:", data.name)
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

const navigateToJobCard = (jobCardId) => {
	router.push(`/job-card/${jobCardId}`)
}

const navigateToDowntimeLog = (downtimeLogId) => {
	router.push(`/downtime-log/${downtimeLogId}`)
}

// Utility functions for formatting and status classes
const formatDate = (dateString) => {
	if (!dateString) return "N/A"
	try {
		return new Date(dateString).toLocaleDateString("en-GB")
	} catch {
		return "Invalid Date"
	}
}

const formatDateTime = (dateTimeString) => {
	if (!dateTimeString) return "N/A"
	try {
		return new Date(dateTimeString).toLocaleString("en-GB", {
			day: "2-digit",
			month: "2-digit",
			year: "numeric",
			hour: "2-digit",
			minute: "2-digit",
			hour12: true,
		})
	} catch {
		return "Invalid DateTime"
	}
}

const formatDurationDetailed = (seconds) => {
	if (!seconds || seconds === 0) return "N/A"

	const totalSeconds = Math.floor(seconds)
	const hours = Math.floor(totalSeconds / 3600)
	const minutes = Math.floor((totalSeconds % 3600) / 60)
	const remainingSeconds = totalSeconds % 60

	const parts = []
	if (hours > 0) parts.push(`${hours}h`)
	if (minutes > 0) parts.push(`${minutes}m`)
	if (remainingSeconds > 0 || parts.length === 0)
		parts.push(`${remainingSeconds}s`)

	return parts.join(" ")
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

// Retry functions for error states
const retryLoadJobCards = () => {
	console.log("Retrying job cards load")
	jobCardsStart.value = 0
	allJobCards.value = []
	jobCardsHasMore.value = true
	jobCardsResource.update({
		start: 0,
		filters: { machine: machineId },
	})
	jobCardsResource.reload()
}

const retryLoadDowntimeLogs = () => {
	console.log("Retrying downtime logs load")
	downtimeLogsStart.value = 0
	allDowntimeLogs.value = []
	downtimeLogsHasMore.value = true
	downtimeLogsResource.update({
		start: 0,
		filters: { machine: machineId },
	})
	downtimeLogsResource.reload()
}

// Load more functions for pagination
const loadMoreJobCards = () => {
	if (jobCardsLoadingMore.value || !jobCardsHasMore.value) return

	jobCardsLoadingMore.value = true
	jobCardsStart.value += 50

	// Update the resource with new start value and reload
	jobCardsResource.update({
		start: jobCardsStart.value,
	})
	jobCardsResource.reload()
}

const loadMoreDowntimeLogs = () => {
	if (downtimeLogsLoadingMore.value || !downtimeLogsHasMore.value) return

	downtimeLogsLoadingMore.value = true
	downtimeLogsStart.value += 50

	// Update the resource with new start value and reload
	downtimeLogsResource.update({
		start: downtimeLogsStart.value,
	})
	downtimeLogsResource.reload()
}

// Watch for tab changes to load data if needed
watch(
	activeTab,
	(newTab, oldTab) => {
		console.log("Tab changed from", oldTab, "to", newTab)

		if (newTab === "jobcards") {
			// Always try to load job cards when switching to this tab if not already loaded
			if (allJobCards.value.length === 0 && !jobCardsResource.loading) {
				console.log("Loading job cards for first time")
				// Reset pagination before loading
				jobCardsStart.value = 0
				jobCardsHasMore.value = true
				// Update resource and reload
				jobCardsResource.update({
					start: 0,
					filters: { machine: machineId },
				})
				jobCardsResource.reload()
			}
		} else if (newTab === "downtime") {
			// Always try to load downtime logs when switching to this tab if not already loaded
			if (allDowntimeLogs.value.length === 0 && !downtimeLogsResource.loading) {
				console.log("Loading downtime logs for first time")
				// Reset pagination before loading
				downtimeLogsStart.value = 0
				downtimeLogsHasMore.value = true
				// Update resource and reload
				downtimeLogsResource.update({
					start: 0,
					filters: { machine: machineId },
				})
				downtimeLogsResource.reload()
			}
		}
	},
	{ immediate: false },
)

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

.performance-on-schedule {
  color: #28a745;
}

.performance-behind {
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

.job-cards-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.job-cards-header {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr 1fr 1fr 1.2fr;
  background-color: #f8f9fa;
  border-bottom: 2px solid #e9ecef;
  padding: 0;
}

.header-cell {
  padding: 16px 12px;
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
  text-align: left;
  border-right: 1px solid #dee2e6;
}

.header-cell:last-child {
  border-right: none;
}

.job-cards-list {
  display: flex;
  flex-direction: column;
}

.job-card-row {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr 1fr 1fr 1.2fr;
  border-bottom: 1px solid #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

.job-card-row:hover {
  background-color: #f8f9fa;
}

.job-card-row:last-child {
  border-bottom: none;
}

.job-card-cell {
  padding: 16px 12px;
  display: flex;
  align-items: center;
  border-right: 1px solid #f8f9fa;
  font-size: 0.9rem;
}

.job-card-cell:last-child {
  border-right: none;
}

.mobile-label {
  display: none;
  font-weight: 600;
  color: #6c757d;
  margin-right: 8px;
  min-width: 100px;
}

.cell-value {
  color: #2c3e50;
  font-weight: 500;
}

.job-name-cell .cell-value {
  font-weight: 600;
}

.status-cell {
  justify-content: flex-start;
}

/* Downtime Logs Tab */
.downtime-section {
  padding: 20px 0;
}

.downtime-logs-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.downtime-logs-header {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1.5fr 1fr 1.2fr 1fr;
  background-color: #f8f9fa;
  border-bottom: 2px solid #e9ecef;
  padding: 0;
}

.downtime-logs-list {
  display: flex;
  flex-direction: column;
}

.downtime-log-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1.5fr 1fr 1.2fr 1fr;
  border-bottom: 1px solid #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

.downtime-log-row:hover {
  background-color: #f8f9fa;
}

.downtime-log-row:last-child {
  border-bottom: none;
}

.downtime-log-cell {
  padding: 16px 12px;
  display: flex;
  align-items: center;
  border-right: 1px solid #f8f9fa;
  font-size: 0.9rem;
}

.downtime-log-cell:last-child {
  border-right: none;
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
@media (max-width: 1024px) and (min-width: 769px) {
  .job-cards-header {
    grid-template-columns: 1fr 1fr 1.5fr 1fr 1fr 1fr;
    font-size: 0.8rem;
  }
  
  .job-card-row {
    grid-template-columns: 1fr 1fr 1.5fr 1fr 1fr 1fr;
  }
  
  .job-card-cell {
    padding: 12px 8px;
    font-size: 0.8rem;
  }
  
  .header-cell {
    padding: 12px 8px;
    font-size: 0.8rem;
  }
  
  .downtime-logs-header {
    grid-template-columns: 1.2fr 1.3fr 1.3fr 0.8fr 1fr 0.8fr;
    font-size: 0.8rem;
  }
  
  .downtime-log-row {
    grid-template-columns: 1.2fr 1.3fr 1.3fr 0.8fr 1fr 0.8fr;
  }
  
  .downtime-log-cell {
    padding: 12px 8px;
    font-size: 0.8rem;
  }
}

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
  
  .job-cards-header {
    display: none;
  }
  
  .job-card-row {
    display: block;
    padding: 16px;
    margin-bottom: 12px;
    background: white;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }
  
  .job-cards-container {
    background: transparent;
    box-shadow: none;
  }
  
  .job-cards-list {
    gap: 0;
  }
  
  .job-card-cell {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-right: none;
    border-bottom: 1px solid #f8f9fa;
  }
  
  .job-card-cell:last-child {
    border-bottom: none;
  }
  
  .mobile-label {
    display: block;
  }
  
  .cell-value {
    text-align: right;
  }
  
  .status-badge {
    margin-left: auto;
  }
  
  .downtime-logs-header {
    display: none;
  }
  
  .downtime-log-row {
    display: block;
    padding: 16px;
    margin-bottom: 12px;
    background: white;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }
  
  .downtime-logs-container {
    background: transparent;
    box-shadow: none;
  }
  
  .downtime-logs-list {
    gap: 0;
  }
  
  .downtime-log-cell {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-right: none;
    border-bottom: 1px solid #f8f9fa;
  }
  
  .downtime-log-cell:last-child {
    border-bottom: none;
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

/* Load More Styles */
.load-more-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 0;
  margin-top: 16px;
  border-top: 1px solid #e9ecef;
}

.load-more-button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-button:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.load-more-button:active {
  transform: translateY(0);
}

.loading-more {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #6c757d;
  font-size: 0.9rem;
}

.loading-spinner-small {
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.no-more-records {
  color: #6c757d;
  font-size: 0.9rem;
  font-style: italic;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .load-more-container {
    padding: 20px 16px;
  }
  
  .load-more-button {
    width: 100%;
    padding: 14px;
  }
}
</style>