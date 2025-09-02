<template>
  <div v-if="isVisible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="modal-title-section">
          <h2 class="modal-title">Update Job Card</h2>
          <p class="modal-subtitle">{{ jobCardData?.name || 'N/A' }}</p>
        </div>
        <button @click="closeModal" class="close-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Form Content -->
      <div class="modal-body">
        <form @submit.prevent="submitUpdate" class="update-form">
          <!-- Production Metrics Section -->
          <div class="form-section">
            <h3 class="section-title">Production Metrics</h3>
            <div class="form-row">
              <div class="form-field">
                <label class="field-label">Target Quantity</label>
                <input
                  v-model="formData.target_quantity"
                  type="number"
                  class="field-input"
                  min="0"
                  :disabled="isSaving"
                />
              </div>
              <div class="form-field">
                <label class="field-label">
                  Completed Quantity
                </label>
                <input
                  v-model="formData.completed_quantity"
                  type="number"
                  class="field-input"
                  min="0"
                  :disabled="isSaving"
                />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field full-width">
                <label class="field-label">Status</label>
                <select
                  v-model="formData.status"
                  class="field-select"
                  :disabled="isSaving"
                >
                  <option value="Not Started">Not Started</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Wastage Section -->
          <div class="form-section">
            <h3 class="section-title">Wastage Information (kg)</h3>
            <div class="form-row">
              <div class="form-field">
                <label class="field-label">Machine Wastage</label>
                <input
                  v-model="formData.machine_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  class="field-input"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                />
              </div>
              <div class="form-field">
                <label class="field-label">Job Setting Wastage</label>
                <input
                  v-model="formData.job_setting_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  class="field-input"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label class="field-label">Roll Wastage</label>
                <input
                  v-model="formData.roll_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  class="field-input"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                />
              </div>
              <div class="form-field">
                <label class="field-label">Printing Wastage</label>
                <input
                  v-model="formData.printing_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  class="field-input"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label class="field-label">Barcode Wastage</label>
                <input
                  v-model="formData.barcode_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  class="field-input"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                />
              </div>
              <div class="form-field">
                <label class="field-label">Total Wastage</label>
                <input
                  v-model="calculatedTotalWastage"
                  type="number"
                  step="0.01"
                  class="field-input total-wastage-preview"
                  readonly
                  disabled
                />
                <small class="field-hint">Auto-calculated from above values</small>
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
              :disabled="isSaving"
            >
              <div v-if="isSaving" class="btn-spinner"></div>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
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
import { createDocumentResource } from "frappe-ui"
import { computed, ref, watch } from "vue"

const props = defineProps({
	isVisible: {
		type: Boolean,
		default: false,
	},
	jobCardData: {
		type: Object,
		default: null,
	},
})

const emit = defineEmits(["close", "updated"])

// Reactive state
const isSaving = ref(false)
const errorMessage = ref("")

// Form data - initialize with current job card data
const formData = ref({
	target_quantity: 0,
	completed_quantity: 0,
	status: "Not Started",
	machine_wastage: 0,
	job_setting_wastage: 0,
	roll_wastage: 0,
	printing_wastage: 0,
	barcode_wastage: 0,
})

// Computed total wastage
const calculatedTotalWastage = computed(() => {
	const total =
		(Number.parseFloat(formData.value.machine_wastage) || 0) +
		(Number.parseFloat(formData.value.job_setting_wastage) || 0) +
		(Number.parseFloat(formData.value.roll_wastage) || 0) +
		(Number.parseFloat(formData.value.printing_wastage) || 0) +
		(Number.parseFloat(formData.value.barcode_wastage) || 0)

	return total.toFixed(2)
})

// Watch for modal visibility and job card data to populate form
watch(
	[() => props.isVisible, () => props.jobCardData],
	([isVisible, jobCardData]) => {
		if (isVisible && jobCardData) {
			// Populate form with current data
			formData.value = {
				target_quantity: jobCardData.target_quantity || 0,
				completed_quantity: jobCardData.completed_quantity || 0,
				status: jobCardData.status || "Not Started",
				machine_wastage: jobCardData.machine_wastage || 0,
				job_setting_wastage: jobCardData.job_setting_wastage || 0,
				roll_wastage: jobCardData.roll_wastage || 0,
				printing_wastage: jobCardData.printing_wastage || 0,
				barcode_wastage: jobCardData.barcode_wastage || 0,
			}
			errorMessage.value = ""
		}
	},
)

const submitUpdate = async () => {
	if (isSaving.value || !props.jobCardData?.name) return

	isSaving.value = true
	errorMessage.value = ""

	try {
		// Prepare update data
		const updateData = {
			target_quantity: Number.parseInt(formData.value.target_quantity) || 0,
			completed_quantity:
				Number.parseInt(formData.value.completed_quantity) || 0,
			status: formData.value.status,
			machine_wastage: Number.parseFloat(formData.value.machine_wastage) || 0,
			job_setting_wastage:
				Number.parseFloat(formData.value.job_setting_wastage) || 0,
			roll_wastage: Number.parseFloat(formData.value.roll_wastage) || 0,
			printing_wastage: Number.parseFloat(formData.value.printing_wastage) || 0,
			barcode_wastage: Number.parseFloat(formData.value.barcode_wastage) || 0,
		}

		console.log("Updating job card:", props.jobCardData.name, updateData)

		// Create resource for updating
		const updateResource = createDocumentResource({
			doctype: "Job Card",
			name: props.jobCardData.name,
		})

		// Submit update
		await updateResource.setValue.submit(updateData)

		console.log("Job card updated successfully")

		// Success - emit updated event and close modal
		emit("updated")
		closeModal()
	} catch (error) {
		console.error("Failed to update job card:", error)
		errorMessage.value =
			error.message || "Failed to update job card. Please try again."
	} finally {
		isSaving.value = false
	}
}

const closeModal = () => {
	errorMessage.value = ""
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
  max-width: 700px;
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

.alert-warning {
  background-color: #fff3cd;
  border: 1px solid #ffecb5;
  color: #856404;
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-field.full-width {
  grid-column: 1 / -1;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.field-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-warning {
  font-size: 0.75rem;
  color: #856404;
  font-weight: 500;
}

.field-input,
.field-select {
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: white;
}

.field-input:focus,
.field-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.field-input:disabled,
.field-select:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.total-wastage-preview {
  background-color: #f8f9fa !important;
  font-weight: 600;
  color: #dc3545 !important;
}

.field-hint {
  margin-top: 4px;
  font-size: 0.75rem;
  color: #6c757d;
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
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .btn {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .modal-title {
    font-size: 1.3rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>