<template>
  <div class="job-card-page">
    <NavBar title="Job Card Details" />
    
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading job card details...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠</div>
      <h3>Error Loading Job Card Details</h3>
      <p>{{ error }}</p>
      <button @click="goBack" class="back-button">Go Back</button>
    </div>
    
    <!-- Job Card Details -->
    <div v-else-if="jobCard" class="job-card-content">
      <!-- Job Card Page Header -->
      <div class="job-card-page-header">
        <button @click="goBack" class="back-icon-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="header-info">
          <h1 class="job-card-title">{{ jobCard.name || 'N/A' }}</h1>
        </div>
        <span class="status-badge" :class="getJobStatusClass(jobCard.status)">
          {{ jobCard.status || 'Unknown' }}
        </span>
      </div>
      
      <!-- Progress Bar -->
      <div v-if="jobCard.target_quantity" class="progress-section">
        <h3>Production Progress</h3>
        <div class="progress-bar-container">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: getProgressPercentage() + '%' }"
            ></div>
          </div>
          <div class="progress-text">
            {{ jobCard.completed_quantity || 0 }} / {{ jobCard.target_quantity }} completed
          </div>
        </div>
      </div>
      
      <!-- Job Card Details Grid -->
      <div class="job-card-details-grid">
        <!-- Basic Information Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Basic Information</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Machine:</span>
              <span class="detail-value">{{ jobCard.machine || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Date:</span>
              <span class="detail-value">{{ formatDate(jobCard.date) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Shift:</span>
              <span class="detail-value">{{ jobCard.shift || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Operator:</span>
              <span class="detail-value">{{ jobCard.operator || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Job Sequence:</span>
              <span class="detail-value">{{ jobCard.job_sequence_number || 'N/A' }}</span>
            </div>
          </div>
        </div>

        <!-- Production Metrics Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Production Metrics</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Target Quantity:</span>
              <span class="detail-value">{{ jobCard.target_quantity || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Completed Quantity:</span>
              <span class="detail-value">{{ jobCard.completed_quantity || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Balance Quantity:</span>
              <span class="detail-value">{{ (jobCard.target_quantity || 0) - (jobCard.completed_quantity || 0) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Progress:</span>
              <span class="detail-value">{{ getProgressPercentage() }}%</span>
            </div>
          </div>
        </div>

        <!-- Performance Metrics Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Performance Metrics</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Planned Run Rate:</span>
              <span class="detail-value">{{ jobCard.planned_run_rate || 'N/A' }} per minute</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Actual Run Rate:</span>
              <span class="detail-value">{{ jobCard.actual_run_rate || 'N/A' }} per minute</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Planned Duration:</span>
              <span class="detail-value">{{ formatDuration(jobCard.planned_duration) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Actual Duration:</span>
              <span class="detail-value">{{ formatDuration(jobCard.actual_duration) }}</span>
            </div>
          </div>
        </div>

        <!-- Timing Information Card -->
        <div class="details-card">
          <div class="card-header">
            <h3>Timing Information</h3>
          </div>
          <div class="card-content">
            <div class="detail-item">
              <span class="detail-label">Planned Start:</span>
              <span class="detail-value">{{ formatDateTime(jobCard.planned_start_date_time) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Planned End:</span>
              <span class="detail-value">{{ formatDateTime(jobCard.planned_end_date_time) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Actual Start:</span>
              <span class="detail-value">{{ formatDateTime(jobCard.actual_start_date_time) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Actual End:</span>
              <span class="detail-value">{{ formatDateTime(jobCard.actual_end_date_time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui"
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import NavBar from "../components/NavBar.vue"

const route = useRoute()
const router = useRouter()

// Reactive data
const jobCard = ref(null)
const isLoading = ref(true)
const error = ref("")

// Get job card ID from route params
const jobCardId = route.params.id

// Fetch job card details
createResource({
  url: "frappe.client.get",
  params: {
    doctype: "Job Card",
    name: jobCardId,
  },
  auto: true,
  onSuccess(data) {
    jobCard.value = data
    isLoading.value = false
  },
  onError(err) {
    error.value = `Failed to load job card details: ${err.message}`
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
    return new Date(dateString).toLocaleDateString('en-GB')
  } catch {
    return "Invalid Date"
  }
}

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return "N/A"
  try {
    return new Date(dateTimeString).toLocaleString('en-GB')
  } catch {
    return "Invalid DateTime"
  }
}

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return "N/A"
  
  const totalSeconds = Math.floor(seconds)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  
  if (hours > 0 && minutes > 0) {
    return `${hours}h ${minutes}m`
  } else if (hours > 0) {
    return `${hours}h`
  } else if (minutes > 0) {
    return `${minutes}m`
  } else {
    return "< 1m"
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

const getProgressPercentage = () => {
  if (!jobCard.value || !jobCard.value.target_quantity) return 0
  const completed = jobCard.value.completed_quantity || 0
  const target = jobCard.value.target_quantity
  return Math.round((completed / target) * 100)
}
</script>

<style scoped>
.job-card-page {
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
.job-card-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Job Card Page Header */
.job-card-page-header {
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

.job-card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 4px 0;
}


/* Details Grid */
.job-card-details-grid {
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
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  flex-shrink: 0;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
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

/* Progress Section */
.progress-section {
  background: white;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.progress-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 600;
}

.progress-bar-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-weight: 500;
  color: #495057;
}

/* Responsive Design */
@media (max-width: 768px) {
  .job-card-content {
    padding: 16px;
  }
  
  .job-card-page-header {
    flex-direction: row;
    align-items: center;
    gap: 12px;
    padding: 16px;
  }
  
  .job-card-title {
    font-size: 1.5rem;
  }
  
  .job-card-details-grid {
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
  .job-card-content {
    padding: 12px;
  }

  .job-card-page-header {
    padding: 16px;
  }
  
  .job-card-title {             
    font-size: 1.3rem;
  }
  
  .progress-section {
    padding: 20px 16px;
  }
}
</style>