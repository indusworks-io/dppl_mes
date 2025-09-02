<template>
  <div v-if="isVisible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="modal-title-section">
          <h2 class="modal-title">Update Downtime Log</h2>
          <p class="modal-subtitle">{{ downtimeLogData?.name || 'N/A' }}</p>
        </div>
        <button @click="closeModal" class="close-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Alert for Information -->
      <div class="alert-section">
        <div class="alert alert-info">
          <div class="alert-icon">ℹ️</div>
          <div class="alert-content">
            <strong>Note:</strong> Updating the reason will automatically update the category based on the selected downtime reason.
          </div>
        </div>
      </div>

      <!-- Form Content -->
      <div class="modal-body">
        <form @submit.prevent="submitUpdate" class="update-form">
          <!-- Reason Section -->
          <div class="form-section">
            <h3 class="section-title">Downtime Reason</h3>
            <div class="form-row">
              <div class="form-field full-width">
                <label class="field-label">Current Reason</label>
                <div class="current-value-display">
                  <div class="current-value">
                    <span class="value-text">{{ downtimeLogData?.reason || 'No reason selected' }}</span>
                    <span v-if="downtimeLogData?.category" class="category-badge">{{ downtimeLogData.category }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-field full-width">
                <label class="field-label">Select New Reason</label>
                <select
                  v-model="formData.reason"
                  class="field-select"
                  :disabled="isSaving || isLoadingReasons"
                  required
                >
                  <option value="">-- Select a reason --</option>
                  <option 
                    v-for="reason in availableReasons" 
                    :key="reason.name" 
                    :value="reason.name"
                  >
                    {{ reason.name }} ({{ reason.category }})
                  </option>
                </select>
                <div v-if="isLoadingReasons" class="field-loading">
                  <div class="mini-spinner"></div>
                  <span>Loading reasons...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <button
              type="button"
              @click="closeModal"
              class="btn btn-secondary"
              :disabled="isSaving"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isSaving || isLoadingReasons || !formData.reason"
            >
              <div v-if="isSaving" class="btn-spinner"></div>
              {{ isSaving ? 'Saving...' : 'Update Reason' }}
            </button>
          </div>
        </form>

        <!-- Error Display -->
        <div v-if="errorMessage" class="error-section">
          <div class="alert alert-error">
            <div class="alert-icon">❌</div>
            <div class="alert-content">
              <strong>Update Failed:</strong>
              {{ errorMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createListResource } from "frappe-ui"
import { computed, ref, watch } from "vue"

const props = defineProps({
	isVisible: {
		type: Boolean,
		default: false,
	},
	downtimeLogData: {
		type: Object,
		default: null,
	},
})

const emit = defineEmits(["close", "updated"])

// Reactive state
const isSaving = ref(false)
const isLoadingReasons = ref(false)
const errorMessage = ref("")
const availableReasons = ref([])

// Form data
const formData = ref({
	reason: "",
})

// Create list resource for downtime reasons
const downtimeReasonsResource = createListResource({
	doctype: "Downtime Reason",
	fields: ["name", "category"],
	filters: {
		is_active: 1,
	},
	onSuccess(data) {
		availableReasons.value = data || []
		isLoadingReasons.value = false
		console.log("Downtime reasons loaded:", data)
	},
	onError(error) {
		console.error("Failed to fetch downtime reasons:", error)
		errorMessage.value = "Failed to load downtime reasons. Please try again."
		isLoadingReasons.value = false
	},
})

// Watch for modal visibility to initialize data and load reasons
watch(
	() => props.isVisible,
	(isVisible) => {
		if (isVisible) {
			// Reset form and errors
			formData.value.reason = ""
			errorMessage.value = ""

			// Load downtime reasons if not already loaded
			if (availableReasons.value.length === 0) {
				isLoadingReasons.value = true
				downtimeReasonsResource.reload()
			}
		}
	},
)

const submitUpdate = async () => {
	if (isSaving.value || !props.downtimeLogData?.name || !formData.value.reason)
		return

	isSaving.value = true
	errorMessage.value = ""

	try {
		console.log("Updating downtime log:", props.downtimeLogData.name, {
			reason: formData.value.reason,
		})

		// Create resource for updating
		const updateResource = createDocumentResource({
			doctype: "Downtime Log",
			name: props.downtimeLogData.name,
		})

		// Submit update
		await updateResource.setValue.submit({
			reason: formData.value.reason,
		})

		console.log("Downtime log updated successfully")

		// Success - emit updated event and close modal
		emit("updated")
		closeModal()
	} catch (error) {
		console.error("Failed to update downtime log:", error)
		errorMessage.value =
			error.message || "Failed to update downtime log. Please try again."
	} finally {
		isSaving.value = false
	}
}

const closeModal = () => {
	errorMessage.value = ""
	formData.value.reason = ""
	emit("close")
}

const handleOverlayClick = () => {
	if (!isSaving.value) {
		closeModal()
	}
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e9ecef;
}

.modal-title-section {
  flex: 1;
}

.modal-title {
  margin: 0 0 4px 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.modal-subtitle {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
}

.close-button {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-button:hover {
  background-color: #f8f9fa;
  color: #495057;
}

/* Alert Section */
.alert-section {
  padding: 0 32px 24px;
}

.alert {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-radius: 8px;
  gap: 12px;
}

.alert-info {
  background-color: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.alert-error {
  background-color: #f8d7da;
  border: 1px solid #f1aeb5;
  color: #721c24;
}

.alert-icon {
  flex-shrink: 0;
  font-size: 1.1rem;
}

.alert-content {
  flex: 1;
}

/* Modal Body */
.modal-body {
  padding: 0 32px 32px;
}

/* Form Sections */
.form-section {
  margin-bottom: 32px;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
}

.form-row {
  margin-bottom: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.form-field.full-width {
  width: 100%;
}

.field-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

/* Current Value Display */
.current-value-display {
  margin-bottom: 16px;
}

.current-value {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
}

.value-text {
  flex: 1;
  font-weight: 500;
  color: #2c3e50;
}

.category-badge {
  background-color: #3b82f6;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Form Fields */
.field-select {
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: white;
}

.field-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.field-select:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.field-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  color: #6c757d;
  font-size: 0.9rem;
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid #e9ecef;
  gap: 12px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #e9ecef;
  color: #495057;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #dee2e6;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-section {
  margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 12px;
  }
  
  .modal-container {
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 20px 24px;
  }
  
  .alert-section,
  .modal-body {
    padding-left: 24px;
    padding-right: 24px;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .btn {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .modal-title {
    font-size: 1.3rem;
  }
  
  .current-value {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>