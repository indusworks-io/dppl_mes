<template>
  <div v-if="isVisible" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click="handleOverlayClick">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto" @click.stop>
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <div class="flex-1">
          <h2 class="text-xl font-semibold text-gray-900">Update Downtime Log</h2>
          <p class="text-sm text-gray-500 mt-1">{{ downtimeLogData?.name || 'N/A' }}</p>
        </div>
        <button @click="closeModal" class="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors duration-200">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Alert for Information -->
      <div class="px-6 pt-4">
        <div class="flex items-start p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <span class="text-blue-600 mr-2">ℹ️</span>
          <div class="flex-1 text-sm text-blue-800">
            <strong>Note:</strong> Updating the reason will automatically update the category based on the selected downtime reason.
          </div>
        </div>
      </div>

      <!-- Form Content -->
      <div class="px-6 py-4">
        <form @submit.prevent="submitUpdate">
          <!-- Reason Section -->
          <div class="space-y-6">
            <h3 class="text-lg font-semibold text-gray-900 border-b-2 border-gray-200 pb-2">Downtime Reason</h3>
            
            <!-- Current Reason Display -->
            <div class="flex flex-col">
              <label class="text-sm font-medium text-gray-700 mb-2">Current Reason</label>
              <div class="p-3 bg-gray-50 border border-gray-200 rounded-md">
                <div class="flex items-center justify-between">
                  <span class="text-gray-900 font-medium">{{ downtimeLogData?.reason || 'No reason selected' }}</span>
                  <span v-if="downtimeLogData?.category" class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full">
                    {{ downtimeLogData.category }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- New Reason Select -->
            <div class="flex flex-col">
              <label class="text-sm font-medium text-gray-700 mb-2">Select New Reason</label>
              <select
                v-model="formData.reason"
                :disabled="isSaving || isLoadingReasons"
                required
                class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
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
              <div v-if="isLoadingReasons" class="flex items-center gap-2 mt-2 text-sm text-gray-600">
                <div class="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                <span>Loading reasons...</span>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mt-6">
            <div class="flex items-start p-4 bg-red-50 border border-red-200 rounded-lg">
              <span class="text-red-600 mr-2">❌</span>
              <div class="flex-1 text-sm text-red-800">
                <strong>Update Failed:</strong>
                {{ errorMessage }}
              </div>
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
              :disabled="isSaving || isLoadingReasons || !formData.reason"
              class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full shadow-sm hover:shadow-md transition-all duration-200 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              {{ isSaving ? 'Saving...' : 'Update Reason' }}
            </button>
          </div>
        </form>
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