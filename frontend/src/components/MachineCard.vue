<template>
  <div class="machine-card" @click="handleClick">
    <div class="machine-image-container">
      <img 
        v-if="machineImageUrl" 
        :src="machineImageUrl" 
        :alt="machine.machine_name || machine.name"
        class="machine-photo"
        @error="handleImageError"
      />
      <div v-else class="no-image-placeholder">
        <span>📷</span>
        <p>No image</p>
      </div>
    </div>
    <div class="machine-details">
      <p><strong>Machine: </strong>{{ machine.machine_name || machine.name }}</p>
      <p><strong>Area: </strong>{{ machine.area || 'N/A' }}</p>
      <p><strong>Status: </strong>
        <span class="status-badge" :class="getStatusClass()">
          {{ machine.is_active ? 'Active' : 'Inactive' }}
        </span>
      </p>
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

// Methods
const handleClick = () => {
	emit("card-clicked", props.machine.name)
	router.push(`/machine/${props.machine.name}`)
}

const handleImageError = (event) => {
	event.target.style.display = "none"
	event.target.nextElementSibling?.classList.remove("hidden")
}

const getStatusClass = () => {
	return props.machine.is_active ? "status-active" : "status-inactive"
}
</script>

<style scoped>
.machine-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  margin: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.machine-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.machine-image-container {
  width: 100%;
  height: 150px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.machine-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #6c757d;
  text-align: center;
}

.no-image-placeholder span {
  font-size: 2rem;
  margin-bottom: 4px;
}

.no-image-placeholder p {
  margin: 0;
  font-size: 0.9rem;
}

.machine-details p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  line-height: 1.4;
}

.machine-details strong {
  min-width: 80px;
  color: #495057;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}
</style>