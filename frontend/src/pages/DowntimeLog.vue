<template>
  <div class="downtime-log-page">
    <NavBar title="Downtime Log Details" />
    
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading downtime log details...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠</div>
      <h3>Error Loading Downtime Log Details</h3>
      <p>{{ error }}</p>
      <button @click="goBack" class="back-button">Go Back</button>
    </div>
    
    <!-- Downtime Log Details -->
    <div v-else-if="downtimeLog" class="downtime-log-content">
      <!-- Downtime Log Page Header -->
      <div class="downtime-log-page-header">
        <button @click="goBack" class="back-icon-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="header-info">
          <h1 class="downtime-log-title">{{ downtimeLog.name || 'N/A' }}</h1>
        </div>
        <div class="header-actions">
          <button @click="openUpdateModal" class="edit-button">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="m18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            Edit
          </button>
          <span class="status-badge" :class="getDowntimeStatusClass(downtimeLog.status)">
            {{ downtimeLog.status || 'Unknown' }}
          </span>
        </div>
      </div>
      
      <!-- Success Message -->
      <div v-if="successMessage" class="success-message">
        <div class="success-alert">
          <div class="success-icon">✅</div>
          <div class="success-content">{{ successMessage }}</div>
        </div>
      </div>
      
      <!-- Downtime Duration Progress -->
      <div class="duration-section">
        <h3>Downtime Duration</h3>
        <div class="duration-display">
          <div class="duration-value">
            {{ formatDurationDetailed(downtimeLog.duration) }}
          </div>
          <div class="duration-info">
            <div class="duration-item">
              <span class="duration-label">Started:</span>
              <span class="duration-text">{{ formatDateTime(downtimeLog.start_date_time) }}</span>
            </div>
            <div class="duration-item" v-if="downtimeLog.end_date_time">
              <span class="duration-label">Ended:</span>
              <span class="duration-text">{{ formatDateTime(downtimeLog.end_date_time) }}</span>
            </div>
            <div class="duration-item" v-else>
              <span class="duration-label">Status:</span>
              <span class="duration-text ongoing">Ongoing</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Downtime Log Details Grid -->
      <div class="downtime-log-details-grid">
        <!-- Basic Information Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Basic Information</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Machine:</span>
              <span class="detail-value">{{ downtimeLog.machine || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Created Date:</span>
              <span class="detail-value">{{ formatDate(downtimeLog.created_date) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Reason:</span>
              <span class="detail-value">{{ downtimeLog.reason || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Category:</span>
              <span class="detail-value">{{ downtimeLog.category || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Status:</span>
              <span class="detail-value">
                <span class="status-badge" :class="getDowntimeStatusClass(downtimeLog.status)">
                  {{ downtimeLog.status || 'Unknown' }}
                </span>
              </span>
            </div>
          </div>
        </div>

        <!-- Timing Details Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Timing Details</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Start Date & Time:</span>
              <span class="detail-value">{{ formatDateTime(downtimeLog.start_date_time) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">End Date & Time:</span>
              <span class="detail-value">
                {{ downtimeLog.end_date_time ? formatDateTime(downtimeLog.end_date_time) : 'Ongoing' }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Total Duration:</span>
              <span class="detail-value">{{ formatDurationDetailed(downtimeLog.duration) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Duration in Seconds:</span>
              <span class="detail-value">{{ downtimeLog.duration || 0 }}s</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Remarks Section -->
      <div v-if="downtimeLog.remarks" class="remarks-section">
        <div class="details-card">
          <div class="card-header">
            <h3>Remarks</h3>
          </div>
          <div class="card-content">
            <div class="remarks-content">
              {{ downtimeLog.remarks }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Update Modal -->
      <DowntimeLogUpdateModal
        :is-visible="isUpdateModalVisible"
        :downtime-log-data="downtimeLog"
        @close="closeUpdateModal"
        @updated="handleDowntimeLogUpdated"
      />
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource } from "frappe-ui"
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import DowntimeLogUpdateModal from "../components/DowntimeLogUpdateModal.vue"
import NavBar from "../components/NavBar.vue"

const route = useRoute()
const router = useRouter()

// Reactive data
const downtimeLog = ref(null)
const isLoading = ref(true)
const error = ref("")
const isUpdateModalVisible = ref(false)
const successMessage = ref("")

// Get downtime log ID from route params
const downtimeLogId = route.params.id

// Create document resource for downtime log
const downtimeLogResource = createDocumentResource({
	doctype: "Downtime Log",
	name: downtimeLogId,
	auto: true,
	onSuccess(data) {
		downtimeLog.value = data
		isLoading.value = false
		error.value = ""
	},
	onError(err) {
		error.value = `Failed to load downtime log details: ${err.message}`
		isLoading.value = false
	},
})

// Utility functions
const goBack = () => {
	router.go(-1)
}

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

const getDowntimeStatusClass = (status) => {
	if (!status) return "status-unknown"
	const statusLower = status.toLowerCase()
	if (
		statusLower.includes("open") ||
		statusLower.includes("active") ||
		statusLower.includes("ongoing")
	) {
		return "status-error"
	} else if (
		statusLower.includes("closed") ||
		statusLower.includes("resolved") ||
		statusLower.includes("complete")
	) {
		return "status-complete"
	}
	return "status-pending"
}

// Modal handling methods
const openUpdateModal = () => {
	isUpdateModalVisible.value = true
}

const closeUpdateModal = () => {
	isUpdateModalVisible.value = false
}

const handleDowntimeLogUpdated = () => {
	// Refresh the downtime log data after successful update
	downtimeLogResource.reload()
	successMessage.value = "Downtime log updated successfully!"

	// Clear success message after 3 seconds
	setTimeout(() => {
		successMessage.value = ""
	}, 3000)
}
</script>

<style scoped>
.downtime-log-page {
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

.back-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  margin-top: 16px;
}

.back-button:hover {
  background-color: #0056b3;
}

/* Main Content */
.downtime-log-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Downtime Log Page Header */
.downtime-log-page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  flex-shrink: 0;
}

.back-icon-button:hover {
  background-color: #e9ecef;
  color: #495057;
}

.header-info {
  flex: 1;
}

.downtime-log-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.edit-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: #2563eb;
}

.edit-button:active {
  transform: translateY(1px);
}

/* Duration Section */
.duration-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.duration-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.duration-display {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.duration-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #dc3545;
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border-radius: 12px;
  border: 2px solid #f5c6cb;
}

.duration-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.duration-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.duration-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.duration-text {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.duration-text.ongoing {
  color: #dc3545;
  font-weight: 600;
}

/* Details Grid */
.downtime-log-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.details-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  background-color: #f8f9fa;
  padding: 16px 24px;
  border-bottom: 1px solid #e9ecef;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.card-content {
  padding: 20px 24px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f8f9fa;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.detail-value {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
  text-align: right;
}

/* Status Badge */
.status-badge {
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  flex-shrink: 0;
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

/* Remarks Section */
.remarks-section {
  margin-bottom: 32px;
}

.remarks-content {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  font-style: italic;
  color: #495057;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* Success Message */
.success-message {
  margin: 0 20px 20px 20px;
}

.success-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 8px;
  color: #155724;
  font-weight: 500;
  animation: slideDown 0.3s ease-out;
}

.success-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.success-content {
  flex: 1;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .downtime-log-content {
    padding: 16px;
  }
  
  .downtime-log-page-header {
    padding: 16px;
  }
  
  .downtime-log-title {
    font-size: 1.3rem;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .edit-button {
    padding: 8px 12px;
    font-size: 0.8rem;
  }
  
  .downtime-log-details-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .details-card {
    margin-bottom: 0;
  }
  
  .card-content {
    padding: 16px 20px;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    padding: 10px 0;
  }
  
  .detail-value {
    text-align: left;
    font-weight: 600;
  }
  
  .duration-value {
    font-size: 2rem;
    padding: 16px;
  }
  
  .duration-info {
    grid-template-columns: 1fr;
  }
  
  .duration-section {
    padding: 20px 16px;
  }
}

@media (max-width: 480px) {
  .downtime-log-content {
    padding: 12px;
  }
  
  .downtime-log-page-header {
    padding: 14px;
  }
  
  .downtime-log-title {
    font-size: 1.2rem;
  }
  
  .duration-value {
    font-size: 1.8rem;
    padding: 12px;
  }
  
  .duration-section {
    padding: 16px 12px;
  }
}
</style>