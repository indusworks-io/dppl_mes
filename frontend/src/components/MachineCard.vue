<template>
  <div 
    @click="handleClick"
    class="bg-white rounded-xl shadow-sm hover:shadow-md border p-4 cursor-pointer transition-all duration-200 hover:-translate-y-1"
    :class="cardColorClass"
  >
    <div class="w-full h-40 mb-3 flex items-center justify-center bg-gray-50 border border-gray-200 rounded-lg overflow-hidden">
      <img 
        v-if="machineImageUrl" 
        :src="machineImageUrl" 
        :alt="machine.machine_name || machine.name"
        class="w-full h-full object-cover"
        @error="handleImageError"
      />
      <div v-else class="flex flex-col items-center text-gray-400">
        <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
        <p class="text-sm">No image</p>
      </div>
    </div>
    <div class="space-y-2">
      <h3 class="text-lg font-semibold text-gray-900" :class="titleColorClass">{{ machine.machine_name || machine.name }}</h3>
      
      <!-- Show Inactive Status for inactive machines -->
      <div v-if="machine.is_active === 0" class="text-center py-2">
        <span class="inline-flex px-3 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-600 uppercase">Inactive</span>
      </div>
      
      <!-- Job Progress Metrics for active machines -->
      <div v-else-if="jobMetrics" class="space-y-1.5">
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Job:</span>
          <span class="font-semibold text-gray-900 truncate ml-2">{{ jobMetrics.job_name || 'No Job Running' }}</span>
        </div>
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Job #:</span>
          <span class="font-semibold text-gray-900">{{ jobMetrics.job_number || 'N/A' }}</span>
        </div>
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Target:</span>
          <span class="font-semibold text-gray-900">{{ jobMetrics.target_quantity || 0 }}</span>
        </div>
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Completed:</span>
          <span class="font-semibold text-gray-900">{{ jobMetrics.completed_quantity || 0 }}</span>
        </div>
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Balance:</span>
          <span class="font-semibold text-gray-900">{{ (jobMetrics.target_quantity || 0) - (jobMetrics.completed_quantity || 0) }}</span>
        </div>
        <div class="flex justify-between items-center text-sm">
          <span class="font-medium text-gray-600">Completion:</span>
          <span class="font-semibold text-gray-900">{{ jobMetrics.target_quantity ? Math.round((jobMetrics.completed_quantity || 0) / jobMetrics.target_quantity * 100) : 0 }}%</span>
        </div>
      </div>
      <div v-else class="text-center py-3">
        <span class="text-sm text-gray-400 italic">No active job</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineEmits, defineProps } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const props = defineProps({
	machine: {
		type: Object,
		required: true,
		validator: (machine) => {
			return (
				typeof machine.name === "string" &&
				(machine.machine_name === undefined ||
					typeof machine.machine_name === "string") &&
				(machine.area === undefined || typeof machine.area === "string") &&
				typeof machine.is_active === "number"
			)
		},
	},
	jobMetrics: {
		type: Object,
		default: () => null,
	},
})

const emit = defineEmits(["card-clicked"])

// Computed properties
const machineImageUrl = computed(() => {
	if (!props.machine.machine_image) return null

	const imagePath = props.machine.machine_image
	return imagePath.startsWith("http")
		? imagePath
		: `${window.location.origin}${imagePath}`
})

const cardColorClass = computed(() => {
	// If machine is inactive (is_active = 0), show gray
	if (props.machine.is_active === 0) {
		return "bg-gray-50 border-2 border-gray-400"
	}

	// If machine is active, check if job is running
	if (!props.jobMetrics || props.jobMetrics.job_name === "No Job Running") {
		// Active with no job running
		return "bg-yellow-50 border-2 border-yellow-400"
	}

	// If machine is active with job running, check run_rate_indicator from jobMetrics
	if (props.jobMetrics.run_rate_indicator !== undefined) {
		return props.jobMetrics.run_rate_indicator === 1
			? "bg-green-50 border-2 border-green-500"
			: "bg-red-50 border-2 border-red-500"
	}

	// Default: if no job metrics available but machine is active
	return "border-gray-200"
})

const titleColorClass = computed(() => {
	// If machine is inactive (is_active = 0), show gray
	if (props.machine.is_active === 0) {
		return "text-gray-600"
	}

	// If machine is active, check if job is running
	if (!props.jobMetrics || props.jobMetrics.job_name === "No Job Running") {
		// Active with no job running
		return "text-yellow-700"
	}

	// If machine is active with job running, check run_rate_indicator from jobMetrics
	if (props.jobMetrics.run_rate_indicator !== undefined) {
		return props.jobMetrics.run_rate_indicator === 1
			? "text-green-700"
			: "text-red-700"
	}

	// Default: if no job metrics available but machine is active
	return "text-gray-900"
})

// Methods
const handleClick = () => {
	emit("card-clicked", props.machine.name)
	router.push(`organization/machines/${props.machine.name}`)
}

const handleImageError = (event) => {
	event.target.style.display = "none"
	event.target.nextElementSibling?.classList.remove("hidden")
}
</script>
