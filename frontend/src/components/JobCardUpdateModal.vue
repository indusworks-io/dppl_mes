<template>
  <div v-if="isVisible" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click="handleOverlayClick">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto" @click.stop>
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <div class="flex-1">
          <h2 class="text-xl font-semibold text-gray-900">Update Job Card</h2>
          <p class="text-sm text-gray-500 mt-1">{{ jobCardData?.name || 'N/A' }}</p>
        </div>
        <button @click="closeModal" class="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors duration-200">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Form Content -->
      <div class="px-6 py-4">
        <form @submit.prevent="submitUpdate">
          <!-- Production Metrics Section -->
          <div class="space-y-6 mb-8">
            <h3 class="text-lg font-semibold text-gray-900 border-b-2 border-gray-200 pb-2">Production Metrics</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Target Quantity</label>
                <input
                  v-model="formData.target_quantity"
                  type="number"
                  min="0"
                  :disabled="isSaving"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">
                  Completed Quantity
                </label>
                <input
                  v-model="formData.completed_quantity"
                  type="number"
                  min="0"
                  :disabled="isSaving"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
            </div>
            <div class="grid grid-cols-1 gap-4">
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  v-model="formData.status"
                  :disabled="isSaving"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
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
          <div class="space-y-6 mb-8">
            <h3 class="text-lg font-semibold text-gray-900 border-b-2 border-gray-200 pb-2">Wastage Information (kg)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Machine Wastage</label>
                <input
                  v-model="formData.machine_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Job Setting Wastage</label>
                <input
                  v-model="formData.job_setting_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Roll Wastage</label>
                <input
                  v-model="formData.roll_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Printing Wastage</label>
                <input
                  v-model="formData.printing_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Barcode Wastage</label>
                <input
                  v-model="formData.barcode_wastage"
                  type="number"
                  step="0.01"
                  min="0"
                  :disabled="isSaving"
                  @input="calculateTotalWastage"
                  class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
                />
              </div>
              <div class="flex flex-col">
                <label class="text-sm font-medium text-gray-700 mb-2">Total Wastage</label>
                <input
                  :value="calculatedTotalWastage"
                  type="text"
                  readonly
                  disabled
                  class="w-full px-3 py-3 bg-gray-100 border border-gray-300 rounded-md font-semibold text-red-600 cursor-not-allowed"
                />
                <div class="text-xs text-gray-500 mt-1">Calculated automatically</div>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mt-6">
            <div class="flex items-start p-4 bg-red-50 border border-red-200 rounded-lg">
              <span class="text-red-600 mr-2">⚠️</span>
              <div class="flex-1 text-sm text-red-800">{{ errorMessage }}</div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="flex items-center justify-end gap-3 pt-6 border-t border-gray-200 mt-8">
            <button 
              type="button" 
              @click="closeModal" 
              :disabled="isSaving"
              class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="isSaving"
              class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full shadow-sm hover:shadow-md transition-all duration-200 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              {{ isSaving ? 'Updating...' : 'Update Job Card' }}
            </button>
          </div>
        </form>
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

const calculateTotalWastage = () => {
	// Auto-calculates via computed property
}
</script>