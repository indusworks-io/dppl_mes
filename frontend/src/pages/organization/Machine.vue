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
          <ListView
            doctype="Job Card"
            title="Job Cards"
            :columns="jobCardColumns"
            :fields="['name', 'date', 'shift', 'job_name', 'target_quantity', 'completed_quantity', 'status', 'machine']"
            :filters="jobCardFilters"
            :hideHeader="true"
            :hideSubheader="true"
            orderBy="creation desc"
            :pageLength="50"
            :enableRouting="true"
            routePrefix="/production/job-cards"
          >
            <!-- Custom Date Cell -->
            <template #cell-date="{ value }">
              {{ formatDate(value) }}
            </template>

            <!-- Custom Status Cell -->
            <template #cell-status="{ value }">
              <span :class="getJobStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                {{ value || 'Unknown' }}
              </span>
            </template>
          </ListView>
        </div>
        
        <!-- Downtime Logs Tab -->
        <div v-show="activeTab === 'downtime'" class="downtime-section">
          <ListView
            doctype="Downtime Log"
            title="Downtime Logs"
            :columns="downtimeLogColumns"
            :fields="['name', 'status', 'start_date_time', 'end_date_time', 'duration', 'reason', 'category', 'machine']"
            :filters="downtimeLogFilters"
            :hideHeader="true"
            :hideSubheader="true"
            orderBy="start_date_time desc"
            :pageLength="50"
            :enableRouting="true"
            routePrefix="/production/downtime-logs"
          >
            <!-- Custom Status Cell -->
            <template #cell-status="{ value }">
              <span :class="getDowntimeStatusClass(value)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                {{ value || 'Unknown' }}
              </span>
            </template>

            <!-- Custom Start Date Time Cell -->
            <template #cell-start_date_time="{ value }">
              {{ formatDateTime(value) }}
            </template>

            <!-- Custom End Date Time Cell -->
            <template #cell-end_date_time="{ value }">
              {{ formatDateTime(value) }}
            </template>

            <!-- Custom Duration Cell -->
            <template #cell-duration="{ value }">
              {{ formatDuration(value) }}
            </template>

            <!-- Custom Actions Cell -->
            <template #cell-actions="{ row }">
              <button
                v-if="!row.reason"
                @click.stop="openUpdateReasonDialog(row.name)"
                class="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 transition-colors"
              >
                Update Reason
              </button>
              <span v-else class="text-xs text-gray-500">-</span>
            </template>
          </ListView>
        </div>
      </div>
    </div>

    <!-- Update Reason Dialog -->
    <UpdateReasonDialog
      :visible="isReasonDialogVisible"
      :downtimeId="selectedDowntimeId"
      @update="handleReasonUpdated"
      @cancel="closeReasonDialog"
    />
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui"
import { computed, onMounted, onUnmounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { initSocket } from "../../socket.js"
import ListView from "../../components/ListView.vue"
import UpdateReasonDialog from "../../components/UpdateReasonDialog.vue"

const route = useRoute()
const router = useRouter()

// Reactive data
const machine = ref(null)
const jobMetrics = ref(null)
const isLoading = ref(true)
const error = ref("")
const socket = ref(null)
const activeTab = ref("overview")
const isReasonDialogVisible = ref(false)
const selectedDowntimeId = ref(null)

// Tab definitions
const tabs = ref([
	{ id: "overview", name: "Overview" },
	{ id: "jobcards", name: "Job Cards" },
	{ id: "downtime", name: "Downtime Logs" },
])

// Get machine ID from route params
const machineId = route.params.id

// Column definitions for Job Cards ListView
const jobCardColumns = [
	{ fieldname: 'name', label: 'Job Card ID' },
	{ fieldname: 'date', label: 'Date' },
	{ fieldname: 'shift', label: 'Shift' },
	{ fieldname: 'job_name', label: 'Job Name' },
	{ fieldname: 'target_quantity', label: 'Target Qty' },
	{ fieldname: 'completed_quantity', label: 'Completed Qty' },
	{ fieldname: 'status', label: 'Status' }
]

// Filters for Job Cards tab
const jobCardFilters = computed(() => {
	return [['machine', '=', machineId]]
})

// Column definitions for Downtime Logs ListView
const downtimeLogColumns = [
	{ fieldname: 'name', label: 'ID' },
	{ fieldname: 'status', label: 'Status' },
	{ fieldname: 'start_date_time', label: 'Start' },
	{ fieldname: 'end_date_time', label: 'End' },
	{ fieldname: 'duration', label: 'Duration' },
	{ fieldname: 'reason', label: 'Reason' },
	{ fieldname: 'category', label: 'Category' },
	{ fieldname: 'actions', label: 'Actions' }
]

// Filters for Downtime Logs tab
const downtimeLogFilters = computed(() => {
	return [['machine', '=', machineId]]
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
		const date = new Date(dateTimeString)
		// Format date as DD/MM/YYYY
		const day = date.getDate().toString().padStart(2, "0")
		const month = (date.getMonth() + 1).toString().padStart(2, "0")
		const year = date.getFullYear()
		// Format time in 12-hour AM/PM format
		let hours = date.getHours()
		const minutes = date.getMinutes().toString().padStart(2, "0")
		const ampm = hours >= 12 ? "PM" : "AM"
		hours = hours % 12
		hours = hours ? hours : 12 // Convert 0 to 12
		const formattedHours = hours.toString().padStart(2, "0")
		return `${day}/${month}/${year} ${formattedHours}:${minutes} ${ampm}`
	} catch {
		return "Invalid DateTime"
	}
}

const formatDuration = (seconds) => {
	if (!seconds || seconds === 0) return "0h 0m 0s"
	const totalSeconds = Math.floor(seconds)
	const hours = Math.floor(totalSeconds / 3600)
	const minutes = Math.floor((totalSeconds % 3600) / 60)
	const secs = totalSeconds % 60
	const parts = []
	if (hours > 0) parts.push(`${hours}h`)
	if (minutes > 0) parts.push(`${minutes}m`)
	if (secs > 0 || parts.length === 0) parts.push(`${secs}s`)
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
	if (!status) return 'bg-gray-100 text-gray-800'
	const statusLower = status.toLowerCase()
	if (statusLower === 'open') {
		return 'bg-red-100 text-red-800'
	} else if (statusLower === 'closed') {
		return 'bg-green-100 text-green-800'
	}
	return 'bg-gray-100 text-gray-800'
}

// Dialog handlers for Update Reason
const openUpdateReasonDialog = (downtimeId) => {
	selectedDowntimeId.value = downtimeId
	isReasonDialogVisible.value = true
}

const closeReasonDialog = () => {
	isReasonDialogVisible.value = false
	selectedDowntimeId.value = null
}

const handleReasonUpdated = () => {
	// Close the dialog
	closeReasonDialog()
	// Reload the page to refresh the data
	window.location.reload()
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

/* Job Cards Tab */
.jobcards-section {
  padding: 0;
}

/* Downtime Logs Tab */
.downtime-section {
  padding: 0;
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