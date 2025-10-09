<template>
  <div v-if="visible" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <h3 class="text-xl font-semibold text-gray-900">Update Downtime Reason</h3>
        <button 
          @click="handleCancel" 
          :disabled="loading || fetchingReason"
          class="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- Modal Body -->
      <div class="px-6 py-4">
        <!-- Alert Message -->
        <div v-if="updateMessage" 
          class="mb-4 p-3 rounded-lg text-sm font-medium"
          :class="updateSuccess ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200'"
        >
          {{ updateMessage }}
        </div>
        
        <!-- Select Field -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Reason</label>
          <select 
            v-model="selectedReason" 
            :disabled="loading || fetchingReason"
            class="w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600 disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <option value="" disabled>Select a reason</option>
            <option v-for="reason in reasonOptions" :key="reason.name" :value="reason.name">
              {{ reason.name }}
            </option>
          </select>
        </div>
      </div>
      
      <!-- Modal Footer -->
      <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200">
        <button 
          @click="handleCancel" 
          :disabled="loading || fetchingReason"
          class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button 
          @click="handleUpdate" 
          :disabled="!selectedReason || loading || fetchingReason"
          class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full shadow-sm hover:shadow-md transition-all duration-200 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed"
        >
          Update
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createDocumentResource, createListResource } from "frappe-ui"
import { defineEmits, defineProps, ref, watch } from "vue"

const props = defineProps({
	visible: Boolean,
	downtimeId: String,
})

const emit = defineEmits(["update", "cancel"])

const selectedReason = ref("")
const reasonOptions = ref([])
const updateMessage = ref("")
const updateSuccess = ref(false)
const loading = ref(false)
const fetchingReason = ref(false)

// Fetch downtime reasons
const downtimereason = createListResource({
	doctype: "Downtime Reason",
	fields: ["name"], // Adjust if your doctype uses a different field (e.g., reason_name)
	auto: true,
	onSuccess: (data) => {
		reasonOptions.value = data // Assuming data is an array of { name: string }
		console.log("Downtime reasons fetched successfully:", reasonOptions.value)
	},
	onError: (error) => {
		console.error("Failed to fetch downtime reasons:", error)
		updateMessage.value = "Failed to load downtime reasons."
		updateSuccess.value = false
	},
})

// Fetch current reason and reset state when dialog opens
watch(
	() => props.visible,
	async (isVisible) => {
		if (isVisible && props.downtimeId) {
			fetchingReason.value = true
			selectedReason.value = ""
			updateMessage.value = ""
			updateSuccess.value = false
			try {
				const downtimeResource = createDocumentResource({
					doctype: "Downtime Log",
					name: props.downtimeId,
					fields: ["reason"],
					auto: false,
				})
				await downtimeResource.reload()
				if (downtimeResource.doc && downtimeResource.doc.reason) {
					selectedReason.value = downtimeResource.doc.reason
				} else {
					console.warn("No reason found for Downtime Log:", props.downtimeId)
				}
			} catch (error) {
				console.error("Failed to fetch current reason:", error)
				updateMessage.value = "Failed to load current reason."
				updateSuccess.value = false
			} finally {
				fetchingReason.value = false
			}
		}
	},
	{ immediate: true },
)

const handleUpdate = async () => {
	if (!selectedReason.value) {
		updateMessage.value = "Please select a reason."
		updateSuccess.value = false
		return
	}

	loading.value = true
	updateMessage.value = ""

	try {
		console.log("Updating reason to:", props.downtimeId)
		console.log("New reason:", selectedReason.value)

		const downtimeResource = createDocumentResource({
			doctype: "Downtime Log",
			name: props.downtimeId,
			auto: false, // Explicitly disable auto-fetch
		})

		await downtimeResource.reload()
		console.log("Document resource:", downtimeResource)

		await downtimeResource.setValue.submit({
			reason: selectedReason.value,
		})

		// Reload the document to get the auto-fetched category from reason
		await downtimeResource.reload()

		const updatedCategory = downtimeResource.doc.category

		updateMessage.value = "Reason updated successfully!"
		updateSuccess.value = true

		// Emit update event to parent with both reason and category
		emit("update", {
			downtimeId: props.downtimeId,
			reason: selectedReason.value,
			category: updatedCategory,
		})

		// Clear selectedReason to reset the dropdown
		selectedReason.value = ""

		// Clear message and close dialog after 3 seconds (increased for visibility)
		setTimeout(() => {
			updateMessage.value = ""
			updateSuccess.value = false
			emit("cancel")
		}, 3000)
	} catch (error) {
		console.error("Failed to update reason:", error)
		updateMessage.value = "Failed to update reason. Please try again."
		updateSuccess.value = false
	} finally {
		loading.value = false // Always reset loading
	}
}

const handleCancel = () => {
	updateMessage.value = ""
	updateSuccess.value = false
	selectedReason.value = ""
	emit("cancel")
}
</script>