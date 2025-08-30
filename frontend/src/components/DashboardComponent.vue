<template>
  <div class="dashboard-container">
    <div v-if="loading" class="loading-state">
      <p>Loading dashboard...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>
    <div v-else>
      <div v-for="area in sortedAreas" :key="area.name" class="area-section">
        <h2 class="area-title">{{ area.area_name }}</h2>
        <div class="machine-grid">
          <MachineCard
            v-for="machine in getMachinesForArea(area.name)"
            :key="machine.name"
            :machine="machine"
            @card-clicked="handleMachineClick"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import MachineCard from "./MachineCard.vue"

const props = defineProps({
	areas: {
		type: Array,
		required: true,
	},
	machines: {
		type: Array,
		required: true,
	},
	selectedFactory: {
		type: String,
		default: "",
	},
})

const loading = ref(false)
const error = ref(null)

const sortedAreas = computed(() => {
	return [...props.areas].sort((a, b) => a.sequence_number - b.sequence_number)
})

const getMachinesForArea = (areaName) => {
	return props.machines
		.filter((machine) => machine.area === areaName)
		.sort((a, b) => a.sequence_number - b.sequence_number)
}

const handleMachineClick = (machineId) => {
	console.log("Machine clicked:", machineId)
	// Handle machine click event, e.g., navigate to machine details page
}

onMounted(() => {
	if (!props.areas || !props.machines) {
		loading.value = true
		// In a real app, you might want to fetch data here if it's not passed via props
	} else {
		loading.value = false
	}
})
</script>

<style scoped>
.dashboard-container {
  padding: 16px;
}

.area-section {
  margin-bottom: 32px;
}

.area-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
  padding-bottom: 8px;
  color: #333;
}

.machine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #888;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }
  
  .area-section {
    margin-bottom: 24px;
  }
  
  .area-title {
    font-size: 18px;
    margin-bottom: 12px;
    padding-bottom: 6px;
  }
  
  .machine-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .machine-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 18px;
  }
}

@media (min-width: 1025px) {
  .dashboard-container {
    padding: 24px;
  }
  
  .area-section {
    margin-bottom: 40px;
  }
  
  .area-title {
    font-size: 24px;
    margin-bottom: 20px;
    padding-bottom: 12px;
  }
  
  .machine-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 24px;
  }
}
</style>