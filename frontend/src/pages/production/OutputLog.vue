<template>
  <div class="output-log-page p-6">

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading output log details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Error Loading Output Log Details</h3>
      <p>{{ error }}</p>
      <button @click="goBack" class="back-button">Go Back</button>
    </div>

    <!-- Output Log Details -->
    <div v-else-if="outputLog" class="output-log-content">
      <!-- Output Log Page Header -->
      <div class="output-log-page-header">
        <button @click="goBack" class="back-icon-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="header-info">
          <h1 class="output-log-title">{{ outputLog.name || 'N/A' }}</h1>
        </div>
      </div>

      <!-- Output Log Details Grid -->
      <div class="output-log-details-grid">
        <!-- Basic Information Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Basic Information</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Job Card:</span>
              <span class="detail-value">{{ outputLog.job_card || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Machine:</span>
              <span class="detail-value">{{ outputLog.machine || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Timestamp:</span>
              <span class="detail-value">{{ formatDateTime(outputLog.timestamp) }}</span>
            </div>
          </div>
        </div>

        <!-- Production Details Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Production Details</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Output:</span>
              <span class="detail-value output-value">{{ outputLog.output || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Run Rate:</span>
              <span class="detail-value">{{ formatRunRate(outputLog.run_rate) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource } from "frappe-ui"
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

// Reactive data
const outputLog = ref(null)
const isLoading = ref(true)
const error = ref("")

// Get output log ID from route params
const outputLogId = route.params.name

// Create document resource for output log
// Note: outputLogResource is used implicitly by frappe-ui's auto-fetch mechanism
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const outputLogResource = createDocumentResource({
	doctype: "Output Log",
	name: outputLogId,
	auto: true,
	onSuccess(data) {
		outputLog.value = data
		isLoading.value = false
		error.value = ""
	},
	onError(err) {
		error.value = `Failed to load output log details: ${err.message}`
		isLoading.value = false
	},
})

// Utility functions
const goBack = () => {
	router.push('/production/output-logs')
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

const formatRunRate = (runRate) => {
	if (!runRate && runRate !== 0) return "N/A"
	return `${Number.parseFloat(runRate).toFixed(2)} per minute`
}
</script>

<style scoped>
.output-log-page {
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
.output-log-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Output Log Page Header */
.output-log-page-header {
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

.output-log-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.output-log-subtitle {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0;
}

/* Details Grid */
.output-log-details-grid {
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

.output-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #28a745;
}

/* Responsive Design */
@media (max-width: 768px) {
  .output-log-content {
    padding: 16px;
  }

  .output-log-page-header {
    padding: 16px;
  }

  .output-log-title {
    font-size: 1.3rem;
  }

  .output-log-details-grid {
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
}

@media (max-width: 480px) {
  .output-log-content {
    padding: 12px;
  }

  .output-log-page-header {
    padding: 14px;
  }

  .output-log-title {
    font-size: 1.2rem;
  }
}
</style>
